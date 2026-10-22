# Week 7 extension: sensor dashboard

LVGL 9.6 dashboard for the Waveshare ESP32-S3-Pico with the Pico Sensor Kit B.

- Home page: clock (NTP, Melbourne time), LDR, SHTC3 temperature and humidity, Melbourne temperature (Open-Meteo)
- Three chart pages (LDR, temperature, humidity), last 2 minutes, updated every second
- IR remote switches pages, and every received code is printed to Serial

## First run

1. Copy `include/secrets.example.h` to `include/secrets.h` (a placeholder copy already exists) and enter your 2.4 GHz Wi-Fi name and password.
2. Build and upload. If the upload will not start, hold BOOT, tap RESET, release BOOT, and upload again.
3. Open the Serial Monitor (115200). Check:
   - `Flash: 16 MB` and `PSRAM: 2048 KB` confirm the ESP32-S3R2 assumption.
   - `I2C scan on I2C0` should list `0x70` (SHTC3) and `I2C1` should list `0x3D` (OLED).
   - `OLED: SSD1327 init OK`.
4. Press remote buttons. If no `IR ...` lines appear, change `IR_RX_PIN` in `include/pins.h` from 39 to 40.
5. Copy the `command=` values into `include/ir_codes.h`. Until then, any button moves to the next page.

## Files

| File | Job |
|---|---|
| `include/pins.h` | Every GPIO number |
| `include/config.h` | Timings, addresses, time zone, weather URL |
| `include/lv_conf.h` | LVGL settings (8-bit gray, fonts, no theme) |
| `include/ir_codes.h` | Remote button mapping |
| `src/main.cpp` | setup() and the non-blocking loop() |
| `src/display_driver.*` | LVGL to SSD1327 flush, sends only the changed area |
| `src/shtc3*.{h,cpp}` | Non-blocking SHTC3 driver and its maths |
| `src/sensors.*` | LDR averaging and SHTC3 readings |
| `src/net.*` | Wi-Fi connection and NTP time |
| `src/weather.*` | Open-Meteo fetch in a background FreeRTOS task |
| `src/ir_input.*` | IR decoding, code printing, button mapping |
| `src/ui.*` | LVGL pages, charts and the 1 second refresh |
| `src/boot_info.*` | Chip info and I2C scan at start-up |
