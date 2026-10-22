// main.cpp
// Week 7 extension: sensor dashboard on the Waveshare ESP32-S3-Pico with the
// Pico Sensor Kit B. LVGL 9.6 UI on the 128x128 grayscale OLED.
//
// What runs where:
//   setup()  starts Serial, both I2C buses, LVGL, the OLED, the UI, the
//            sensors, Wi-Fi, the weather task and the IR receiver.
//   loop()   never waits on anything. Each pass it:
//              1. advances the sensor state machines   (sensors_update)
//              2. checks the Wi-Fi state                (net_update)
//              3. checks for an IR button press         (ir_poll)
//              4. lets LVGL run its timers and redraw   (lv_timer_handler)
//   weather  runs in its own FreeRTOS task (see weather.cpp)
//
// The once-per-second label and chart refresh is an LVGL timer created in
// ui.cpp, so it runs inside lv_timer_handler().

#include <Arduino.h>
#include <Wire.h>
#include <lvgl.h>

#include "boot_info.h"
#include "config.h"
#include "display_driver.h"
#include "ir_input.h"
#include "net.h"
#include "pins.h"
#include "sensors.h"
#include "sound.h"
#include "ui.h"
#include "weather.h"

// LVGL needs to know how many milliseconds have passed. millis() returns
// unsigned long, LVGL wants uint32_t, so wrap it in a small function.
static uint32_t lvglTick() {
  return millis();
}

// LVGL warnings and errors are printed to the Serial Monitor.
static void lvglLog(lv_log_level_t level, const char *msg) {
  (void)level;
  Serial.print("LVGL: ");
  Serial.print(msg);
}

static void handleIr(uint32_t nowMs) {
  const IrAction action = ir_poll(nowMs);
  switch (action) {
    case IrAction::Next:      ui_nextPage(); break;
    case IrAction::Prev:      ui_prevPage(); break;
    case IrAction::Home:      ui_showPage(UiPage::Home); break;
    case IrAction::PageLdr:   ui_showPage(UiPage::Ldr); break;
    case IrAction::PageTemp:  ui_showPage(UiPage::Temp); break;
    case IrAction::PageHum:   ui_showPage(UiPage::Hum); break;
    case IrAction::VolumeOff: sound_setEnabled(false); break;
    case IrAction::VolumeMax: sound_setEnabled(true); break;
    case IrAction::None:      break;
  }
  // Every page change gets a click (volume buttons have their own sound).
  if (action != IrAction::None && action != IrAction::VolumeOff &&
      action != IrAction::VolumeMax) {
    sound_click();
  }
}

void setup() {
  Serial.begin(115200);
  // With native USB, the first prints are lost if the Serial Monitor is not
  // open yet. Wait up to 2 s for it, then carry on regardless.
  const uint32_t waitStart = millis();
  while (!Serial && millis() - waitStart < 2000) {
    delay(10);
  }

  boot_printChipInfo();

  // Two separate I2C buses, as wired on the kit:
  //   Wire  (I2C0): SHTC3 on GPIO33/34
  //   Wire1 (I2C1): OLED  on GPIO17/18
  Wire.begin(SHTC3_SDA_PIN, SHTC3_SCL_PIN, SHTC3_I2C_HZ);
  Wire1.begin(OLED_SDA_PIN, OLED_SCL_PIN, OLED_I2C_HZ);
  boot_scanI2C(Wire, "I2C0 (SHTC3, expect 0x70)");
  boot_scanI2C(Wire1, "I2C1 (OLED, expect 0x3D)");

  lv_init();
  lv_tick_set_cb(lvglTick);
  lv_log_register_print_cb(lvglLog);

  display_begin();
  ui_begin();
  sensors_begin();
  net_begin();
  weather_begin();
  ir_begin();
  sound_begin();

  Serial.println("Setup done. Press remote buttons to see their codes.");
}

void loop() {
  const uint32_t now = millis();

  sensors_update(now);
  net_update(now);
  handleIr(now);

  // lv_timer_handler() redraws anything that changed and returns how many ms
  // until LVGL next needs attention. A short delay hands the CPU back to
  // FreeRTOS (Wi-Fi, the weather task). It is capped at 5 ms so IR presses
  // and sensor timing stay responsive.
  const uint32_t idleMs = lv_timer_handler();
  delay(idleMs < 5 ? (idleMs == 0 ? 1 : idleMs) : 5);
}
