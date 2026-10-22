// ui.h
// The LVGL user interface: a readings page and three chart pages, shown as
// tabs along the bottom of the 128x128 OLED.
// No Arduino includes, so the UI can be built and previewed on a PC.

#pragma once
#include <stdint.h>

enum class UiPage : uint8_t {
  Home = 0,   // all readings, clock, Melbourne temperature
  Ldr,        // LDR chart
  Temp,       // temperature chart
  Hum,        // humidity chart
  Count,
};

// Builds every screen object and starts a 1 second LVGL timer that refreshes
// the labels and adds a point to each chart. Call after display_begin().
void ui_begin();

void ui_showPage(UiPage page);
void ui_nextPage();
void ui_prevPage();
