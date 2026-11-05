/**
 * lv_conf.h for LVGL 9.6
 *
 * Only the settings this project changes are listed here. LVGL fills in a
 * default for everything else (lvgl/lv_conf_template.h documents them all).
 *
 * platformio.ini passes -D LV_CONF_INCLUDE_SIMPLE and -I include/ so LVGL
 * finds this file.
 */

/* clang-format off */
#ifndef LV_CONF_H
#define LV_CONF_H

/* The OLED shows 16 shades of gray. L8 means LVGL draws in 8-bit grayscale
 * (1 byte per pixel, 0 = black, 255 = white). display.cpp then keeps the top
 * 4 bits of each pixel for the OLED. */
#define LV_COLOR_FORMAT_DEFAULT LV_COLOR_FORMAT_L8

/* How often (ms) LVGL checks whether anything needs redrawing. */
#define LV_DEF_REFR_PERIOD 50

/* LVGL's own memory for widgets, styles and chart data. */
#define LV_USE_STDLIB_MALLOC LV_STDLIB_BUILTIN
#define LV_MEM_SIZE (48U * 1024U)

/* Every LVGL call happens from loop(), so no RTOS support is needed. */
#define LV_USE_OS LV_OS_NONE

/* Off: LVGL's log lines would not carry the getTimestamp() timestamp. */
#define LV_USE_LOG 0

/* No theme. The built-in themes are made for colour screens, so display.cpp
 * styles every widget itself (white on black). */
#define LV_USE_THEME_DEFAULT 0
#define LV_USE_THEME_SIMPLE  0
#define LV_USE_THEME_MONO    0

/* Fonts: 10 and 12 for small text, 28 for the big level number. */
#define LV_FONT_MONTSERRAT_10 1
#define LV_FONT_MONTSERRAT_12 1
#define LV_FONT_MONTSERRAT_28 1
#define LV_FONT_DEFAULT &lv_font_montserrat_12

/* Widgets: tabview for the pages, QR code for the WiFi and Web pages. */
#define LV_USE_TABVIEW 1
#define LV_USE_QRCODE  1

/* Do not compile LVGL's demos or examples. */
#define LV_BUILD_EXAMPLES 0

#endif /* LV_CONF_H */
