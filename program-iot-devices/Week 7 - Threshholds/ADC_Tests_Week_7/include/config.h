// config.h
// Tunable settings: timings, addresses, the weather location and the time zone.
// Change values here instead of hunting through the .cpp files.

#pragma once
#include <stdint.h>

// ---------------- OLED ----------------
constexpr uint16_t OLED_WIDTH    = 128;
constexpr uint16_t OLED_HEIGHT   = 128;
constexpr uint8_t  OLED_I2C_ADDR = 0x3D;     // from the kit wiki
// 400 kHz is the SSD1327 datasheet limit. Many modules also work at 800000 or
// 1000000, which makes screen updates faster. Try it once everything works.
constexpr uint32_t OLED_I2C_HZ   = 400000;
constexpr uint8_t  OLED_CONTRAST = 0x7F;     // 0x00 (dim) to 0xFF (bright)
constexpr uint8_t  OLED_ROTATION = 0;        // 0 to 3, use 2 if the image is upside down

// ---------------- Sensors ----------------
constexpr uint8_t  SHTC3_I2C_ADDR        = 0x70;
// 100 kHz is the standard I2C speed. Slower than the OLED bus, but more
// tolerant of the kit's longer wiring and the other devices on I2C0.
constexpr uint32_t SHTC3_I2C_HZ          = 100000;
constexpr uint32_t SHTC3_INTERVAL_MS     = 1000;  // one temperature/humidity reading per second
constexpr uint32_t LDR_INTERVAL_MS       = 500;   // publish a new LDR average twice per second
constexpr uint32_t LDR_SAMPLE_PERIOD_MS  = 50;    // LDR sampled every 50 ms, so 10 samples per average

// ---------------- Wi-Fi and time ----------------
constexpr uint32_t WIFI_RETRY_MS = 15000;          // restart a connection attempt after this long
#define TZ_MELBOURNE "AEST-10AEDT,M10.1.0,M4.1.0/3"
#define NTP_SERVER_1 "pool.ntp.org"
#define NTP_SERVER_2 "time.google.com"
#define NTP_SERVER_3 "time.cloudflare.com"

// ---------------- Weather (Open-Meteo, no API key) ----------------
// Melbourne CBD coordinates
#define WEATHER_URL "https://api.open-meteo.com/v1/forecast" \
                    "?latitude=-37.8136&longitude=144.9631"   \
                    "&current=temperature_2m&timezone=Australia%2FMelbourne"
constexpr uint32_t WEATHER_REFRESH_MS    = 5UL * 60UL * 1000UL;  // every 5 minutes after a success
constexpr uint32_t WEATHER_RETRY_MS      = 30UL * 1000UL;        // retry after 30 s on failure
constexpr uint32_t WEATHER_TIMEOUT_MS    = 8000;                 // give up on one request after this

// ---------------- UI ----------------
constexpr uint32_t UI_REFRESH_MS     = 1000;  // clock, temp, humidity, weather: once per second
constexpr uint32_t UI_LDR_REFRESH_MS = 500;   // LDR label and chart: twice per second
constexpr uint16_t CHART_POINTS      = 120;   // temp/humidity: 120 points x 1 s   = last 2 minutes
constexpr uint16_t LDR_CHART_POINTS  = 240;   // LDR:           240 points x 0.5 s = last 2 minutes

// ---------------- Sound (passive buzzer) ----------------
constexpr bool     SOUND_START_ON    = true;  // sound on at power-up (remote can turn it off)
constexpr uint16_t SOUND_CLICK_HZ    = 1800;  // page change click
constexpr uint16_t SOUND_CLICK_MS    = 12;
constexpr uint16_t SOUND_TICK_MS     = 20;    // chart tick length
constexpr uint16_t SOUND_TICK_LOW_HZ = 400;   // pitch when the newest point is at the bottom of the chart
constexpr uint16_t SOUND_TICK_HIGH_HZ = 2400; // pitch when it is at the top

// ---------------- IR remote ----------------
constexpr uint32_t IR_DEBOUNCE_MS = 250;   // ignore a second press within this time
