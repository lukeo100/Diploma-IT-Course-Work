// ui.cpp
//
// Screen layout (128 x 128 pixels):
//
//   +--------------------------+  y = 0
//   |                          |
//   |   page content, 112 px   |   Home, LDR, Temp or Hum
//   |                          |
//   +--------------------------+  y = 112
//   | Home | LDR | Temp | Hum  |   tab bar, 16 px, active tab highlighted
//   +--------------------------+  y = 128
//
// LVGL objects are created once in ui_begin(). After that, two LVGL timers
// keep the screen up to date:
//   refreshCb     every UI_REFRESH_MS (1 s):    clock, temperature, humidity,
//                                               weather, and their charts
//   refreshLdrCb  every UI_LDR_REFRESH_MS (0.5 s): the LDR label and chart
// Both read the latest data from the sensors, net and weather modules. All
// LVGL calls happen from loop() through lv_timer_handler(), never from the
// weather task.
//
// Charts store whole numbers, so temperature and humidity are stored in
// tenths (24.1 C is stored as 241). Each chart keeps a fixed number of points
// and shifts left as new ones arrive.
//
// Sound: when a chart page is on screen, every new point plays a short tick.
// Its pitch follows where the point sits on the chart: low at the bottom,
// high at the top.

#include "ui.h"

#include <lvgl.h>
#include <initializer_list>
#include <math.h>
#include <stdio.h>
#include <string.h>

#include "config.h"
#include "net.h"
#include "sensors.h"
#include "sound.h"
#include "weather.h"

namespace {

// ---------------- Layout ----------------
constexpr int32_t SCREEN_W  = 128;
constexpr int32_t TAB_BAR_H = 16;

// Home page rows
constexpr int32_t ROW_Y0   = 42;
constexpr int32_t ROW_STEP = 17;

// Chart pages
constexpr int32_t CHART_Y = 15;
constexpr int32_t CHART_H = 82;

// UTF-8 degree sign. The built-in Montserrat fonts include it.
#define DEG "\xC2\xB0"

// ---------------- Gray levels ----------------
// The OLED has 16 levels, so only big steps are visible.
lv_color_t colWhite()  { return lv_color_hex(0xFFFFFF); }
lv_color_t colDim()    { return lv_color_hex(0x909090); }  // labels, secondary text
lv_color_t colGrid()   { return lv_color_hex(0x383838); }  // chart grid, dividers
lv_color_t colTabBg()  { return lv_color_hex(0x484848); }  // active tab
lv_color_t colBlack()  { return lv_color_hex(0x000000); }

// ---------------- Chart page description ----------------
struct ChartPage {
  // Settings
  UiPage   page;        // which tab this chart is on
  uint16_t points;      // how many values the chart holds
  uint32_t periodMs;    // time between values (for the "2m" label)
  const char *title;
  int32_t scale;        // 1 = whole numbers, 10 = values stored in tenths
  bool    fixedRange;   // true: Y axis always hardMin..hardMax
  int32_t hardMin;      // Y axis never goes below this
  int32_t hardMax;      // Y axis never goes above this
  int32_t minSpan;      // smallest Y range when auto scaling (stops noise looking huge)
  int32_t pad;          // space added above and below the data when auto scaling
  // Objects
  lv_obj_t *chart;
  lv_chart_series_t *series;
  lv_obj_t *valueLabel;
  lv_obj_t *axisTopLabel;
  lv_obj_t *axisBottomLabel;
  lv_obj_t *footerLabel;
};

ChartPage ldrPage  = {UiPage::Ldr,  LDR_CHART_POINTS, UI_LDR_REFRESH_MS, "LDR",  1,  true,     0, 4095,   0,  0,
                      nullptr, nullptr, nullptr, nullptr, nullptr, nullptr};
ChartPage tempPage = {UiPage::Temp, CHART_POINTS,     UI_REFRESH_MS,     "Temp", 10, false, -400,  850,  20,  5,
                      nullptr, nullptr, nullptr, nullptr, nullptr, nullptr};
ChartPage humPage  = {UiPage::Hum,  CHART_POINTS,     UI_REFRESH_MS,     "Hum",  10, false,    0, 1000, 100, 10,
                      nullptr, nullptr, nullptr, nullptr, nullptr, nullptr};

// ---------------- Home page objects ----------------
lv_obj_t *tabview      = nullptr;
lv_obj_t *timeLabel    = nullptr;
lv_obj_t *dateLabel    = nullptr;
lv_obj_t *ldrValue     = nullptr;
lv_obj_t *tempValue    = nullptr;
lv_obj_t *humValue     = nullptr;
lv_obj_t *melbValue    = nullptr;
bool      melbDimmed   = false;

// ---------------- Small helpers ----------------

// Only touch a label when its text really changes. Setting the same text
// would still make LVGL redraw it and send pixels over I2C for nothing.
void setText(lv_obj_t *label, const char *text) {
  if (strcmp(lv_label_get_text(label), text) != 0) {
    lv_label_set_text(label, text);
  }
}

lv_obj_t *makeLabel(lv_obj_t *parent, const lv_font_t *font, lv_color_t color,
                    const char *text) {
  lv_obj_t *l = lv_label_create(parent);
  lv_obj_set_style_text_font(l, font, 0);
  lv_obj_set_style_text_color(l, color, 0);
  lv_label_set_text(l, text);
  return l;
}

// A plain object with no scrolling, padding or border, used as a page.
void makePlain(lv_obj_t *obj) {
  lv_obj_set_scrollable(obj, false);
  lv_obj_set_style_pad_all(obj, 0, 0);
  lv_obj_set_style_border_width(obj, 0, 0);
  lv_obj_set_style_radius(obj, 0, 0);
}

// One "Name ......... value" row on the home page. Returns the value label.
lv_obj_t *makeRow(lv_obj_t *page, int32_t y, const char *name) {
  lv_obj_t *n = makeLabel(page, &lv_font_montserrat_12, colDim(), name);
  lv_obj_align(n, LV_ALIGN_TOP_LEFT, 2, y);
  lv_obj_t *v = makeLabel(page, &lv_font_montserrat_12, colWhite(), "--");
  lv_obj_align(v, LV_ALIGN_TOP_RIGHT, -2, y);
  return v;
}

// Integer division that rounds towards minus infinity (needed for negative
// temperatures when rounding the axis to whole degrees).
int32_t floorDiv(int32_t a, int32_t b) {
  int32_t q = a / b;
  if ((a % b != 0) && ((a < 0) != (b < 0))) q--;
  return q;
}

// Writes a chart value as text: 2047, or 24.1 when stored in tenths.
void formatValue(char *buf, size_t len, int32_t v, int32_t scale) {
  if (scale == 10) {
    snprintf(buf, len, "%.1f", v / 10.0f);
  } else {
    snprintf(buf, len, "%ld", (long)v);
  }
}

// ---------------- Building the pages ----------------

void buildHomePage(lv_obj_t *page) {
  timeLabel = makeLabel(page, &lv_font_montserrat_16, colWhite(), "--:--:--");
  lv_obj_align(timeLabel, LV_ALIGN_TOP_MID, 0, 2);

  dateLabel = makeLabel(page, &lv_font_montserrat_10, colDim(), "Starting...");
  lv_obj_align(dateLabel, LV_ALIGN_TOP_MID, 0, 22);

  // Thin divider under the date
  lv_obj_t *line = lv_obj_create(page);
  makePlain(line);
  lv_obj_set_size(line, SCREEN_W - 8, 1);
  lv_obj_align(line, LV_ALIGN_TOP_MID, 0, 37);
  lv_obj_set_style_bg_color(line, colGrid(), 0);
  lv_obj_set_style_bg_opa(line, LV_OPA_COVER, 0);

  ldrValue  = makeRow(page, ROW_Y0 + 0 * ROW_STEP, "Light");
  tempValue = makeRow(page, ROW_Y0 + 1 * ROW_STEP, "Temp");
  humValue  = makeRow(page, ROW_Y0 + 2 * ROW_STEP, "Humidity");
  melbValue = makeRow(page, ROW_Y0 + 3 * ROW_STEP, "Melb");
}

void buildChartPage(lv_obj_t *page, ChartPage &cp) {
  lv_obj_t *title = makeLabel(page, &lv_font_montserrat_12, colWhite(), cp.title);
  lv_obj_align(title, LV_ALIGN_TOP_LEFT, 2, 0);

  cp.valueLabel = makeLabel(page, &lv_font_montserrat_12, colWhite(), "--");
  lv_obj_align(cp.valueLabel, LV_ALIGN_TOP_RIGHT, -2, 0);

  // ---- The chart ----
  lv_obj_t *c = lv_chart_create(page);
  cp.chart = c;
  makePlain(c);
  lv_obj_set_pos(c, 0, CHART_Y);
  lv_obj_set_size(c, SCREEN_W, CHART_H);
  lv_obj_set_style_bg_opa(c, LV_OPA_TRANSP, 0);

  lv_chart_set_type(c, LV_CHART_TYPE_LINE);
  lv_chart_set_point_count(c, cp.points);
  // SHIFT: each new value goes on the right and the oldest drops off the left.
  lv_chart_set_update_mode(c, LV_CHART_UPDATE_MODE_SHIFT);

  // Grid: 3 horizontal lines, no vertical lines. Drawn with the MAIN part's line style.
  lv_chart_set_div_line_count(c, 3, 0);
  lv_obj_set_style_line_color(c, colGrid(), LV_PART_MAIN);
  lv_obj_set_style_line_width(c, 1, LV_PART_MAIN);

  // Data line: 2 px wide so it is easy to see. No dots on each point.
  lv_obj_set_style_line_width(c, 2, LV_PART_ITEMS);
  lv_obj_set_style_size(c, 0, 0, LV_PART_INDICATOR);

  cp.series = lv_chart_add_series(c, colWhite(), LV_CHART_AXIS_PRIMARY_Y);
  // Start empty: LV_CHART_POINT_NONE means "no value here", so nothing is drawn.
  lv_chart_set_all_values(c, cp.series, LV_CHART_POINT_NONE);
  lv_chart_set_axis_range(c, LV_CHART_AXIS_PRIMARY_Y, cp.hardMin, cp.hardMax);

  // ---- Axis labels over the left edge of the chart (top and bottom value) ----
  // Black background so the data line does not run through the numbers.
  cp.axisTopLabel = makeLabel(page, &lv_font_montserrat_10, colDim(), "");
  lv_obj_set_pos(cp.axisTopLabel, 0, CHART_Y);
  cp.axisBottomLabel = makeLabel(page, &lv_font_montserrat_10, colDim(), "");
  lv_obj_set_pos(cp.axisBottomLabel, 0, CHART_Y + CHART_H - 12);
  for (lv_obj_t *l : {cp.axisTopLabel, cp.axisBottomLabel}) {
    lv_obj_set_style_bg_color(l, colBlack(), 0);
    lv_obj_set_style_bg_opa(l, LV_OPA_COVER, 0);
    lv_obj_set_style_pad_hor(l, 1, 0);
  }

  // ---- Footer: lowest and highest value on the chart, and the time span (2m) ----
  cp.footerLabel = makeLabel(page, &lv_font_montserrat_10, colDim(), "waiting for data");
  lv_obj_align(cp.footerLabel, LV_ALIGN_BOTTOM_LEFT, 2, -1);

  char span[16];
  snprintf(span, sizeof(span), "%um", (unsigned)((uint32_t)cp.points * cp.periodMs / 60000));
  lv_obj_t *spanLabel = makeLabel(page, &lv_font_montserrat_10, colDim(), span);
  lv_obj_align(spanLabel, LV_ALIGN_BOTTOM_RIGHT, -2, -1);
}

void styleTabBar() {
  lv_obj_t *bar = lv_tabview_get_tab_bar(tabview);
  lv_obj_set_style_bg_color(bar, colBlack(), 0);
  lv_obj_set_style_bg_opa(bar, LV_OPA_COVER, 0);
  lv_obj_set_style_pad_all(bar, 0, 0);
  lv_obj_set_style_border_side(bar, LV_BORDER_SIDE_TOP, 0);
  lv_obj_set_style_border_width(bar, 1, 0);
  lv_obj_set_style_border_color(bar, colGrid(), 0);

  for (uint32_t i = 0; i < lv_tabview_get_tab_count(tabview); i++) {
    lv_obj_t *btn = lv_tabview_get_tab_button(tabview, (int32_t)i);
    lv_obj_set_style_radius(btn, 0, 0);
    lv_obj_set_style_pad_all(btn, 0, 0);
    lv_obj_set_style_border_width(btn, 0, 0);
    lv_obj_set_style_shadow_width(btn, 0, 0);
    lv_obj_set_style_text_font(btn, &lv_font_montserrat_10, 0);
    // Normal tab: dim text, no background
    lv_obj_set_style_text_color(btn, colDim(), 0);
    lv_obj_set_style_bg_opa(btn, LV_OPA_TRANSP, 0);
    // Active tab (LVGL gives it the CHECKED state): white text on gray
    lv_obj_set_style_text_color(btn, colWhite(), LV_STATE_CHECKED);
    lv_obj_set_style_bg_color(btn, colTabBg(), LV_STATE_CHECKED);
    lv_obj_set_style_bg_opa(btn, LV_OPA_COVER, LV_STATE_CHECKED);
  }
}

// ---------------- Refreshing ----------------

// Adds a value to a chart page, rescales its Y axis and updates its labels.
void updateChart(ChartPage &cp, bool valid, int32_t value, const char *valueText) {
  lv_chart_set_next_value(cp.chart, cp.series, valid ? value : LV_CHART_POINT_NONE);
  setText(cp.valueLabel, valid ? valueText : "--");

  // Find the lowest and highest value currently on the chart.
  const int32_t *ys = lv_chart_get_series_y_array(cp.chart, cp.series);
  int32_t lo = INT32_MAX, hi = INT32_MIN;
  for (uint32_t i = 0; i < cp.points; i++) {
    if (ys[i] == LV_CHART_POINT_NONE) continue;
    if (ys[i] < lo) lo = ys[i];
    if (ys[i] > hi) hi = ys[i];
  }
  if (lo > hi) return;   // no data yet

  int32_t axisLo = cp.hardMin, axisHi = cp.hardMax;
  if (!cp.fixedRange) {
    axisLo = lo - cp.pad;
    axisHi = hi + cp.pad;
    if (axisHi - axisLo < cp.minSpan) {          // too flat: widen around the middle
      const int32_t mid = (lo + hi) / 2;
      axisLo = mid - cp.minSpan / 2;
      axisHi = axisLo + cp.minSpan;
    }
    // Round outwards to whole units so the axis labels read 22.0 and 26.0.
    axisLo = floorDiv(axisLo, cp.scale) * cp.scale;
    axisHi = -floorDiv(-axisHi, cp.scale) * cp.scale;
    if (axisLo < cp.hardMin) axisLo = cp.hardMin;
    if (axisHi > cp.hardMax) axisHi = cp.hardMax;
  }
  lv_chart_set_axis_range(cp.chart, LV_CHART_AXIS_PRIMARY_Y, axisLo, axisHi);

  char a[16], b[16], line[48];
  formatValue(a, sizeof(a), axisHi, cp.scale);
  setText(cp.axisTopLabel, a);
  formatValue(a, sizeof(a), axisLo, cp.scale);
  setText(cp.axisBottomLabel, a);

  formatValue(a, sizeof(a), lo, cp.scale);
  formatValue(b, sizeof(b), hi, cp.scale);
  snprintf(line, sizeof(line), "Lo %s  Hi %s", a, b);
  setText(cp.footerLabel, line);

  // Tick only for the chart you are looking at, and only for a real value.
  // position: 0.0 = bottom of the chart, 1.0 = top.
  const bool onScreen = lv_tabview_get_tab_active(tabview) == (uint32_t)cp.page;
  if (onScreen && valid && axisHi > axisLo) {
    float position = (float)(value - axisLo) / (float)(axisHi - axisLo);
    if (position < 0.0f) position = 0.0f;
    if (position > 1.0f) position = 1.0f;
    sound_chartTick(position);
  }
}

void refreshClock() {
  static const char *DAYS[]   = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
  static const char *MONTHS[] = {"Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"};
  char buf[32];
  struct tm t;
  if (net_localTime(t)) {
    // 12-hour clock: hour 0 is 12 AM, 13 is 1 PM.
    int h12 = t.tm_hour % 12;
    if (h12 == 0) h12 = 12;
    snprintf(buf, sizeof(buf), "%d:%02d:%02d %s", h12, t.tm_min, t.tm_sec,
             t.tm_hour < 12 ? "AM" : "PM");
    setText(timeLabel, buf);
    snprintf(buf, sizeof(buf), "%s %d %s %d", DAYS[t.tm_wday], t.tm_mday,
             MONTHS[t.tm_mon], t.tm_year + 1900);
    setText(dateLabel, buf);
  } else {
    setText(timeLabel, "--:--:--");
    switch (net_state()) {
      case NetState::NoCredentials: setText(dateLabel, "Wi-Fi not set up"); break;
      case NetState::Connecting:    setText(dateLabel, "Connecting Wi-Fi..."); break;
      case NetState::Connected:     setText(dateLabel, "Syncing time..."); break;
    }
  }
}

// Twice per second: LDR label on the home page and the LDR chart.
void refreshLdrCb(lv_timer_t *) {
  const SensorSnapshot s = sensors_get();
  char buf[32];
  snprintf(buf, sizeof(buf), "%u (%.0f%%)", (unsigned)s.ldrRaw, s.ldrPercent);
  setText(ldrValue, s.ldrValid ? buf : "--");
  snprintf(buf, sizeof(buf), "%u / %.0f%%", (unsigned)s.ldrRaw, s.ldrPercent);
  updateChart(ldrPage, s.ldrValid, s.ldrRaw, buf);
}

// Once per second: everything else.
void refreshCb(lv_timer_t *) {
  const SensorSnapshot s = sensors_get();
  const WeatherSnapshot w = weather_get();
  char buf[32];

  refreshClock();

  // ---- Temperature ----
  snprintf(buf, sizeof(buf), "%.1f" DEG "C", s.tempC);
  setText(tempValue, s.climateValid ? buf : "--");
  updateChart(tempPage, s.climateValid, (int32_t)lroundf(s.tempC * 10.0f), buf);

  // ---- Humidity ----
  snprintf(buf, sizeof(buf), "%.1f%%", s.humidity);
  setText(humValue, s.climateValid ? buf : "--");
  updateChart(humPage, s.climateValid, (int32_t)lroundf(s.humidity * 10.0f), buf);

  // ---- Melbourne (Open-Meteo) ----
  // Stale values stay on screen, dimmed, with "old" so you know they are not fresh.
  const bool stale = (w.status == WeatherStatus::Stale);
  if (w.status == WeatherStatus::None) {
    setText(melbValue, "--");
  } else {
    snprintf(buf, sizeof(buf), stale ? "%.1f" DEG "C old" : "%.1f" DEG "C", w.tempC);
    setText(melbValue, buf);
  }
  if (stale != melbDimmed) {
    melbDimmed = stale;
    lv_obj_set_style_text_color(melbValue, stale ? colDim() : colWhite(), 0);
  }
}

}  // namespace

// ---------------- Public functions ----------------

void ui_begin() {
  lv_obj_t *scr = lv_screen_active();
  lv_obj_set_style_bg_color(scr, colBlack(), 0);
  lv_obj_set_style_bg_opa(scr, LV_OPA_COVER, 0);
  lv_obj_set_style_text_color(scr, colWhite(), 0);   // children inherit this
  lv_obj_set_scrollable(scr, false);

  tabview = lv_tabview_create(scr);
  lv_obj_set_size(tabview, SCREEN_W, SCREEN_W);
  lv_tabview_set_tab_bar_position(tabview, LV_DIR_BOTTOM);
  lv_tabview_set_tab_bar_size(tabview, TAB_BAR_H);
  // No touch screen, so no swiping between tabs; the remote changes pages.
  lv_obj_set_scrollable(lv_tabview_get_content(tabview), false);

  lv_obj_t *home = lv_tabview_add_tab(tabview, "Home");
  lv_obj_t *ldr  = lv_tabview_add_tab(tabview, "LDR");
  lv_obj_t *temp = lv_tabview_add_tab(tabview, "Temp");
  lv_obj_t *hum  = lv_tabview_add_tab(tabview, "Hum");
  for (lv_obj_t *p : {home, ldr, temp, hum}) makePlain(p);

  buildHomePage(home);
  buildChartPage(ldr, ldrPage);
  buildChartPage(temp, tempPage);
  buildChartPage(hum, humPage);
  styleTabBar();

  lv_timer_t *t = lv_timer_create(refreshCb, UI_REFRESH_MS, nullptr);
  lv_timer_ready(t);   // run once straight away instead of waiting 1 s
  lv_timer_t *tl = lv_timer_create(refreshLdrCb, UI_LDR_REFRESH_MS, nullptr);
  lv_timer_ready(tl);
}

void ui_showPage(UiPage page) {
  if (page >= UiPage::Count) return;
  lv_tabview_set_active(tabview, (uint32_t)page, LV_ANIM_OFF);
}

void ui_nextPage() {
  const uint32_t n = (uint32_t)UiPage::Count;
  ui_showPage((UiPage)((lv_tabview_get_tab_active(tabview) + 1) % n));
}

void ui_prevPage() {
  const uint32_t n = (uint32_t)UiPage::Count;
  ui_showPage((UiPage)((lv_tabview_get_tab_active(tabview) + n - 1) % n));
}
