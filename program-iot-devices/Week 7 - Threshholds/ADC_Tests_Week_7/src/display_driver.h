// display_driver.h
// Connects LVGL to the SSD1327 OLED through the Adafruit_SSD1327 library.

#pragma once

// Starts the OLED on the I2C1 bus (Wire1 must already be started) and creates
// the LVGL display. Call after lv_init().
// Returns false if the OLED did not answer. LVGL is still set up in that case,
// so the rest of the firmware (Serial output, IR, sensors) keeps running.
bool display_begin();
