// display_driver.cpp
//
// How LVGL and the OLED fit together:
//
//   LVGL draws into drawBuf (8-bit gray, 1 byte per pixel)
//        |
//        v  flushCb() is called with the area that changed
//   Each pixel is reduced to 4 bits (0 to 15) and written into the Adafruit
//   library's own framebuffer with drawPixel(). drawPixel() also remembers the
//   smallest rectangle that changed (the "dirty window").
//        |
//        v  on the last flush of a refresh, oled.display()
//   Only the dirty window is sent over I2C to the SSD1327.
//
// Sending only the changed rectangle matters: a full 128x128 frame is 8 KB and
// takes about 0.2 s at 400 kHz, but the clock digits alone take a few ms.

#include "display_driver.h"

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_SSD1327.h>
#include <lvgl.h>

#include "config.h"
#include "pins.h"

// The OLED is on its own bus (Wire1 = I2C1). The 4th argument -1 means the
// module's reset pin is not connected. The 5th is the I2C speed used while
// sending pixels.
static Adafruit_SSD1327 oled(OLED_WIDTH, OLED_HEIGHT, &Wire1, -1, OLED_I2C_HZ);
static bool oledOk = false;

// LVGL render buffer: 32 rows of 128 pixels at 1 byte each = 4 KB.
// "Partial" render mode means LVGL draws the screen in strips of up to
// 32 rows and calls flushCb() once per strip.
static constexpr uint32_t DRAW_BUF_ROWS = 32;
alignas(4) static uint8_t drawBuf[OLED_WIDTH * DRAW_BUF_ROWS];

static void flushCb(lv_display_t *disp, const lv_area_t *area, uint8_t *pxMap) {
  if (oledOk) {
    const int32_t w = lv_area_get_width(area);
    const int32_t h = lv_area_get_height(area);
    // Bytes per row in pxMap (equals w for L8 with LVGL's default alignment).
    const uint32_t stride = lv_draw_buf_width_to_stride(w, LV_COLOR_FORMAT_L8);

    for (int32_t y = 0; y < h; y++) {
      const uint8_t *row = pxMap + y * stride;
      for (int32_t x = 0; x < w; x++) {
        // 0..255 from LVGL becomes 0..15 for the OLED (keep the top 4 bits).
        oled.drawPixel(area->x1 + x, area->y1 + y, row[x] >> 4);
      }
    }

    // LVGL may flush several strips per refresh. Send to the screen once,
    // after the last strip, so the I2C transfer covers them all.
    if (lv_display_flush_is_last(disp)) {
      oled.display();
    }
  }

  // Always tell LVGL we are done, otherwise it waits forever.
  lv_display_flush_ready(disp);
}

bool display_begin() {
  // begin() checks that something answers at the address, runs the SSD1327
  // init sequence and allocates the 8 KB framebuffer.
  oledOk = oled.begin(OLED_I2C_ADDR, true);
  if (oledOk) {
    oled.setRotation(OLED_ROTATION);
    oled.setContrast(OLED_CONTRAST);
    oled.clearDisplay();
    oled.display();
    Serial.printf("OLED: SSD1327 init OK at 0x%02X\n", OLED_I2C_ADDR);
  } else {
    Serial.printf("OLED: no answer at 0x%02X on I2C1 (SDA %d, SCL %d). "
                  "Check the I2C scan above for the real address.\n",
                  OLED_I2C_ADDR, OLED_SDA_PIN, OLED_SCL_PIN);
  }

  lv_display_t *disp = lv_display_create(OLED_WIDTH, OLED_HEIGHT);
  lv_display_set_color_format(disp, LV_COLOR_FORMAT_L8);
  lv_display_set_flush_cb(disp, flushCb);
  lv_display_set_buffers(disp, drawBuf, nullptr, sizeof(drawBuf),
                         LV_DISPLAY_RENDER_MODE_PARTIAL);
  return oledOk;
}
