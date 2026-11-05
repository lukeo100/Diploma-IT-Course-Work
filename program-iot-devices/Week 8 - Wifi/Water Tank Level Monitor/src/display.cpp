// display.cpp
//
// How LVGL and the OLED fit together:
//
//   1. We create widgets (labels, a chart, QR codes) once, in display_begin().
//   2. When something changes we only update them: new label text, a new
//      chart point. Nothing is drawn yet; LVGL just marks those areas "dirty".
//   3. display_update() calls lv_timer_handler() every pass of loop(). Every
//      LV_DEF_REFR_PERIOD (50 ms) it redraws the dirty areas into drawBuf
//      (8-bit gray, 1 byte per pixel) and calls flushCb().
//   4. flushCb() copies those pixels into the Adafruit SSD1327 library,
//      which sends only the changed rectangle to the OLED over I2C.
//
// Pages: an LVGL "tabview" holds the four pages side by side, with a tab bar
// along the bottom. Only the active page is on screen.

#include "display.h"

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SSD1327.h>
#include <lvgl.h>
#include <stdio.h>

#include "config.h"

// ---------------- OLED driver ----------------

// The OLED is on the kit's second I2C bus (Wire1). -1 = no reset pin.
static Adafruit_SSD1327 oled(OLED_WIDTH, OLED_HEIGHT, &Wire1, -1, OLED_I2C_HZ);
static bool oledOk = false;

// LVGL draws the screen in strips of up to 32 rows into this buffer
// (128 x 32 pixels x 1 byte = 4 KB), then hands each strip to flushCb().
static constexpr uint32_t DRAW_BUF_ROWS = 32;
alignas(4) static uint8_t drawBuf[OLED_WIDTH * DRAW_BUF_ROWS];

static void flushCb(lv_display_t* disp, const lv_area_t* area, uint8_t* pixels) {
  if (oledOk) {
    int32_t w = lv_area_get_width(area);
    int32_t h = lv_area_get_height(area);
    uint32_t stride = lv_draw_buf_width_to_stride(w, LV_COLOR_FORMAT_L8);   // bytes per row

    for (int32_t y = 0; y < h; y++) {
      for (int32_t x = 0; x < w; x++) {
        // LVGL gray is 0-255, the OLED has 16 levels (0-15): keep the top 4 bits.
        oled.drawPixel(area->x1 + x, area->y1 + y, pixels[y * stride + x] >> 4);
      }
    }
    // After the last strip, send everything that changed to the screen at once.
    if (lv_display_flush_is_last(disp)) oled.display();
  }
  lv_display_flush_ready(disp);   // always tell LVGL we are done, or it waits forever
}

// LVGL needs to know how much time has passed.
static uint32_t tickCb() {
  return millis();
}

// ---------------- Widgets and colours ----------------

static constexpr int32_t TAB_BAR_H = 14;                          // tab bar along the bottom
static constexpr int32_t PAGE_H    = OLED_HEIGHT - TAB_BAR_H;     // 114 px left for each page
static constexpr int32_t QR_SIZE   = 100;                         // QR code width and height

static lv_obj_t* tabview;
static lv_obj_t* wifiLabel;
static lv_obj_t* levelLabel;
static lv_obj_t* avgLabel;
static lv_obj_t* alertLabel;
static lv_obj_t* chart;
static lv_chart_series_t* levelSeries;
static lv_obj_t* wifiQr;
static lv_obj_t* webQr;
static lv_obj_t* webTitle;
static lv_obj_t* logLabel = nullptr;   // nullptr until the Log page exists

static const lv_color_t COL_WHITE  = lv_color_hex(0xFFFFFF);
static const lv_color_t COL_DIM    = lv_color_hex(0x909090);   // secondary text, threshold line
static const lv_color_t COL_GRID   = lv_color_hex(0x383838);   // chart frame and grid
static const lv_color_t COL_TAB_BG = lv_color_hex(0x484848);   // the active tab

// With no theme, labels start black on black, so every label gets a colour.
static lv_obj_t* makeLabel(lv_obj_t* parent, const lv_font_t* font, lv_color_t colour, const char* text) {
  lv_obj_t* label = lv_label_create(parent);
  lv_obj_set_style_text_font(label, font, 0);
  lv_obj_set_style_text_color(label, colour, 0);
  lv_label_set_text(label, text);
  return label;
}

// A QR code: black squares on white, with a white border (the "quiet zone")
// that phone cameras need to find the edges of the code.
static lv_obj_t* makeQr(lv_obj_t* parent) {
  lv_obj_t* qr = lv_qrcode_create(parent);
  lv_qrcode_set_size(qr, QR_SIZE);
  lv_qrcode_set_dark_color(qr, lv_color_black());
  lv_qrcode_set_light_color(qr, COL_WHITE);
  lv_qrcode_set_quiet_zone(qr, true);
  lv_obj_align(qr, LV_ALIGN_TOP_MID, 0, 13);
  return qr;
}

// ---------------- Building the pages ----------------

static void buildTankPage(lv_obj_t* page) {
  // ---- Top row: title and Wi-Fi state ----
  lv_obj_t* title = makeLabel(page, &lv_font_montserrat_12, COL_WHITE, "Water Tank");
  lv_obj_align(title, LV_ALIGN_TOP_LEFT, 2, 0);
  wifiLabel = makeLabel(page, &lv_font_montserrat_10, COL_DIM, "...");
  lv_obj_align(wifiLabel, LV_ALIGN_TOP_RIGHT, -2, 1);

  // ---- Big level number ----
  levelLabel = makeLabel(page, &lv_font_montserrat_28, COL_WHITE, "--%");
  lv_obj_align(levelLabel, LV_ALIGN_TOP_MID, 0, 11);

  // ---- Average, and the alert badge (hidden until the level is low) ----
  avgLabel = makeLabel(page, &lv_font_montserrat_10, COL_DIM, "avg --%");
  lv_obj_align(avgLabel, LV_ALIGN_TOP_LEFT, 2, 42);

  alertLabel = makeLabel(page, &lv_font_montserrat_10, lv_color_black(), "LOW!");
  lv_obj_set_style_bg_color(alertLabel, COL_WHITE, 0);        // black text on white
  lv_obj_set_style_bg_opa(alertLabel, LV_OPA_COVER, 0);
  lv_obj_set_style_pad_hor(alertLabel, 3, 0);
  lv_obj_align(alertLabel, LV_ALIGN_TOP_RIGHT, -2, 42);
  lv_obj_set_hidden(alertLabel, true);

  // ---- Chart: the last CHART_POINTS readings ----
  chart = lv_chart_create(page);
  lv_obj_set_pos(chart, 0, 56);
  lv_obj_set_size(chart, OLED_WIDTH, 44);
  lv_obj_set_style_bg_opa(chart, LV_OPA_TRANSP, 0);
  lv_obj_set_style_border_width(chart, 1, 0);
  lv_obj_set_style_border_color(chart, COL_GRID, 0);
  lv_obj_set_style_pad_all(chart, 1, 0);

  lv_chart_set_type(chart, LV_CHART_TYPE_LINE);
  lv_chart_set_point_count(chart, CHART_POINTS);
  // SHIFT: each new value goes on the right and the oldest drops off the left.
  lv_chart_set_update_mode(chart, LV_CHART_UPDATE_MODE_SHIFT);
  lv_chart_set_axis_range(chart, LV_CHART_AXIS_PRIMARY_Y, 0, 100);   // 0-100 %

  // Grid: 3 horizontal lines (25, 50, 75 %), no vertical lines.
  lv_chart_set_div_line_count(chart, 3, 0);
  lv_obj_set_style_line_color(chart, COL_GRID, LV_PART_MAIN);
  lv_obj_set_style_line_width(chart, 1, LV_PART_MAIN);

  // Data lines: 2 px wide, no dot on each point.
  lv_obj_set_style_line_width(chart, 2, LV_PART_ITEMS);
  lv_obj_set_style_size(chart, 0, 0, LV_PART_INDICATOR);

  // Series 1: the alert threshold, a flat gray line. Added first so the
  // level line is drawn on top of it.
  lv_chart_series_t* thresholdSeries = lv_chart_add_series(chart, COL_DIM, LV_CHART_AXIS_PRIMARY_Y);
  lv_chart_set_all_values(chart, thresholdSeries, LOW_LEVEL_THRESHOLD);

  // Series 2: the tank level. Starts empty (POINT_NONE = nothing drawn there).
  levelSeries = lv_chart_add_series(chart, COL_WHITE, LV_CHART_AXIS_PRIMARY_Y);
  lv_chart_set_all_values(chart, levelSeries, LV_CHART_POINT_NONE);

  // ---- Footer ----
  char text[24];
  snprintf(text, sizeof(text), "last %lu min",
           (unsigned long)(CHART_POINTS * READ_INTERVAL_MS / 60000));
  lv_obj_t* spanLabel = makeLabel(page, &lv_font_montserrat_10, COL_DIM, text);
  lv_obj_align(spanLabel, LV_ALIGN_BOTTOM_LEFT, 2, 0);

  snprintf(text, sizeof(text), "alert < %d%%", LOW_LEVEL_THRESHOLD);
  lv_obj_t* thresholdLabel = makeLabel(page, &lv_font_montserrat_10, COL_DIM, text);
  lv_obj_align(thresholdLabel, LV_ALIGN_BOTTOM_RIGHT, -2, 0);
}

static void buildWifiQrPage(lv_obj_t* page) {
  lv_obj_t* title = makeLabel(page, &lv_font_montserrat_10, COL_WHITE, "1. Scan to join WiFi");
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 0);
  wifiQr = makeQr(page);   // filled in by display_setAccessPoint()
}

static void buildWebQrPage(lv_obj_t* page) {
  webTitle = makeLabel(page, &lv_font_montserrat_10, COL_WHITE, "2. Scan to open page");
  lv_obj_align(webTitle, LV_ALIGN_TOP_MID, 0, 0);
  webQr = makeQr(page);    // filled in by display_setAccessPoint()
}

static void buildLogPage(lv_obj_t* page) {
  // One label holding all the lines, pinned to the bottom of the page. As it
  // grows it pushes upwards, and the oldest lines disappear off the top
  // (the page clips anything outside it).
  logLabel = makeLabel(page, &lv_font_montserrat_10, COL_WHITE, "");
  lv_obj_set_width(logLabel, OLED_WIDTH - 4);
  lv_label_set_long_mode(logLabel, LV_LABEL_LONG_MODE_WRAP);   // long lines wrap onto the next row
  lv_obj_align(logLabel, LV_ALIGN_BOTTOM_LEFT, 2, 0);
}

// Tab bar: dim text on black, the active tab white on gray.
static void styleTabBar() {
  lv_obj_t* bar = lv_tabview_get_tab_bar(tabview);
  lv_obj_set_style_bg_color(bar, lv_color_black(), 0);
  lv_obj_set_style_bg_opa(bar, LV_OPA_COVER, 0);
  lv_obj_set_style_pad_all(bar, 0, 0);
  lv_obj_set_style_border_side(bar, LV_BORDER_SIDE_TOP, 0);
  lv_obj_set_style_border_width(bar, 1, 0);
  lv_obj_set_style_border_color(bar, COL_GRID, 0);

  for (uint32_t i = 0; i < lv_tabview_get_tab_count(tabview); i++) {
    lv_obj_t* button = lv_tabview_get_tab_button(tabview, (int32_t)i);
    lv_obj_set_style_radius(button, 0, 0);
    lv_obj_set_style_pad_all(button, 0, 0);
    lv_obj_set_style_border_width(button, 0, 0);
    lv_obj_set_style_text_font(button, &lv_font_montserrat_10, 0);
    lv_obj_set_style_text_color(button, COL_DIM, 0);
    lv_obj_set_style_bg_opa(button, LV_OPA_TRANSP, 0);
    // LVGL gives the active tab the CHECKED state.
    lv_obj_set_style_text_color(button, COL_WHITE, LV_STATE_CHECKED);
    lv_obj_set_style_bg_color(button, COL_TAB_BG, LV_STATE_CHECKED);
    lv_obj_set_style_bg_opa(button, LV_OPA_COVER, LV_STATE_CHECKED);
  }
}

// A page with no padding, border or scrolling.
static void makePlain(lv_obj_t* page) {
  lv_obj_set_style_pad_all(page, 0, 0);
  lv_obj_set_style_border_width(page, 0, 0);
  lv_obj_set_scrollable(page, false);
}

// ---------------- Log lines ----------------

// A ring of the last LOG_ENTRIES lines. nextLog is where the next one goes,
// overwriting the oldest once the ring is full.
static String logLines[LOG_ENTRIES];
static int nextLog = 0;

static void refreshLogLabel() {
  if (logLabel == nullptr) return;
  String text;
  // Oldest first, so the newest line ends up at the bottom.
  for (int i = 0; i < LOG_ENTRIES; i++) {
    const String& line = logLines[(nextLog + i) % LOG_ENTRIES];
    if (line.length() == 0) continue;
    if (text.length() > 0) text += "\n";
    text += line;
  }
  lv_label_set_text(logLabel, text.c_str());
}

// ---------------- Public functions ----------------

bool display_begin() {
  Wire1.begin(oledSdaPin, oledSclPin, OLED_I2C_HZ);

  // begin() checks something answers at the address and sets up the SSD1327.
  oledOk = oled.begin(OLED_I2C_ADDR, true);
  if (oledOk) {
    oled.setRotation(OLED_ROTATION);
    oled.clearDisplay();
    oled.display();
  }

  lv_init();
  lv_tick_set_cb(tickCb);

  lv_display_t* disp = lv_display_create(OLED_WIDTH, OLED_HEIGHT);
  lv_display_set_color_format(disp, LV_COLOR_FORMAT_L8);
  lv_display_set_flush_cb(disp, flushCb);
  lv_display_set_buffers(disp, drawBuf, nullptr, sizeof(drawBuf), LV_DISPLAY_RENDER_MODE_PARTIAL);

  lv_obj_t* screen = lv_screen_active();
  lv_obj_set_style_bg_color(screen, lv_color_black(), 0);
  lv_obj_set_style_bg_opa(screen, LV_OPA_COVER, 0);
  lv_obj_set_scrollable(screen, false);

  // The tabview: pages above, tab bar along the bottom.
  tabview = lv_tabview_create(screen);
  lv_obj_set_size(tabview, OLED_WIDTH, OLED_HEIGHT);
  lv_tabview_set_tab_bar_position(tabview, LV_DIR_BOTTOM);
  lv_tabview_set_tab_bar_size(tabview, TAB_BAR_H);
  // No touch screen, so no swiping between pages; the remote changes them.
  lv_obj_set_scrollable(lv_tabview_get_content(tabview), false);

  // Same order as the Page enum in display.h.
  lv_obj_t* tank = lv_tabview_add_tab(tabview, "Tank");
  lv_obj_t* wifi = lv_tabview_add_tab(tabview, "WiFi");
  lv_obj_t* web  = lv_tabview_add_tab(tabview, "Web");
  lv_obj_t* log  = lv_tabview_add_tab(tabview, "Log");
  for (lv_obj_t* page : {tank, wifi, web, log}) makePlain(page);

  buildTankPage(tank);
  buildWifiQrPage(wifi);
  buildWebQrPage(web);
  buildLogPage(log);
  styleTabBar();
  refreshLogLabel();   // show any lines logged before the page existed

  return oledOk;
}

void display_showReading(int level, float average, bool alert) {
  char text[16];

  snprintf(text, sizeof(text), "%d%%", level);
  lv_label_set_text(levelLabel, text);

  snprintf(text, sizeof(text), "avg %.1f%%", average);
  lv_label_set_text(avgLabel, text);

  lv_obj_set_hidden(alertLabel, !alert);   // show the LOW! badge only during an alert

  lv_chart_set_next_value(chart, levelSeries, level);
}

void display_setWiFi(bool online) {
  lv_label_set_text(wifiLabel, online ? "WiFi" : "offline");
}

// Wi-Fi QR codes use this format, which phone cameras understand:
//   WIFI:T:WPA;S:<network name>;P:<password>;;
// The characters \ ; , : " have a meaning in that format, so a backslash is
// put in front of any that appear in the name or password.
static String escapeForWifiQr(const char* text) {
  String out;
  for (const char* c = text; *c != '\0'; c++) {
    if (strchr("\\;,:\"", *c)) out += '\\';
    out += *c;
  }
  return out;
}

void display_setAccessPoint(const char* ssid, const char* password, const char* ip) {
  String wifiText = "WIFI:T:WPA;S:" + escapeForWifiQr(ssid) + ";P:" + escapeForWifiQr(password) + ";;";
  lv_qrcode_set_data(wifiQr, wifiText.c_str());

  String url = "http://" + String(ip);
  lv_qrcode_set_data(webQr, url.c_str());
  lv_label_set_text(webTitle, ("2. Open " + String(ip)).c_str());
}

void display_addLog(const char* line) {
  logLines[nextLog] = line;
  nextLog = (nextLog + 1) % LOG_ENTRIES;
  refreshLogLabel();
}

void display_showPage(Page page) {
  lv_tabview_set_active(tabview, page, LV_ANIM_OFF);
}

void display_nextPage() {
  int page = lv_tabview_get_tab_active(tabview);
  display_showPage((Page)((page + 1) % PAGE_COUNT));               // after Log, back to Tank
}

void display_prevPage() {
  int page = lv_tabview_get_tab_active(tabview);
  display_showPage((Page)((page + PAGE_COUNT - 1) % PAGE_COUNT));  // before Tank, round to Log
}

void display_update() {
  lv_timer_handler();   // redraws anything that changed since the last call
}
