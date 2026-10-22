/**
 * lv_conf.h for LVGL 9.6.0
 *
 * Only the settings this project changes are listed here. LVGL fills in a
 * default for everything else (see lvgl/include/lvgl/config/lv_conf_internal.h),
 * and lvgl/lv_conf_template.h documents every option if you need more.
 *
 * platformio.ini passes -D LV_CONF_INCLUDE_SIMPLE and -I include/ so LVGL
 * finds this file.
 */

/* clang-format off */
#ifndef LV_CONF_H
#define LV_CONF_H

/*====================
 * COLOUR AND RENDERING
 *====================*/

/* The OLED shows 16 gray levels. L8 means LVGL renders 8-bit grayscale
 * (1 byte per pixel, 0 = black, 255 = white). The display driver then keeps
 * the top 4 bits of each pixel for the SSD1327. In LVGL 9.6 this replaces
 * the old LV_COLOR_DEPTH setting. */
#define LV_COLOR_FORMAT_DEFAULT LV_COLOR_FORMAT_L8

/* Screen refresh check period in ms. Nothing on screen animates, and readings
 * change once per second, so a slower refresh saves CPU time. */
#define LV_DEF_REFR_PERIOD 50

/* Sizes widgets use by default. The screen is small, so lower than default. */
#define LV_DPI_DEF 100

/*====================
 * MEMORY
 *====================*/

/* LVGL's own memory pool for widgets, styles and chart data. */
#define LV_USE_STDLIB_MALLOC LV_STDLIB_BUILTIN
#define LV_MEM_SIZE (48U * 1024U)

/* No RTOS integration: every LVGL call happens from loop() on one core. */
#define LV_USE_OS LV_OS_NONE

/*====================
 * LOGGING
 *====================*/

/* Warnings and errors are passed to a callback in main.cpp, which prints them
 * to Serial. */
#define LV_USE_LOG 1
#define LV_LOG_LEVEL LV_LOG_LEVEL_WARN
#define LV_LOG_PRINTF 0

/*====================
 * THEME
 *====================*/

/* No theme at all. The built-in themes are designed for colour screens (and
 * the "simple" theme LVGL falls back to gives every object a white
 * background), so ui.cpp styles every widget explicitly instead. */
#define LV_USE_THEME_DEFAULT 0
#define LV_USE_THEME_SIMPLE  0
#define LV_USE_THEME_MONO    0

/*====================
 * FONTS
 *====================*/

/* Built-in Montserrat fonts. They include the degree sign. */
#define LV_FONT_MONTSERRAT_10 1
#define LV_FONT_MONTSERRAT_12 1
#define LV_FONT_MONTSERRAT_14 1
#define LV_FONT_MONTSERRAT_16 1
#define LV_FONT_DEFAULT LV_FONT_DEFAULT_MONTSERRAT_12

/*====================
 * WIDGETS
 *====================*/

/* Widgets this project uses (all on by default, listed for clarity). */
#define LV_USE_LABEL   1
#define LV_USE_CHART   1
#define LV_USE_TABVIEW 1

/* Not needed: do not compile the demos or examples. */
#define LV_BUILD_EXAMPLES 0

#endif /* LV_CONF_H */
