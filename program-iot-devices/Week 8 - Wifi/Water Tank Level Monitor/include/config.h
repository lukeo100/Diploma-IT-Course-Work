// config.h
// Pins, thresholds and timings for the water-tank monitor.
// Change values here instead of hunting through main.cpp.
//
// Board: Waveshare ESP32-S3-Pico on the Waveshare Pico Sensor Kit B.
// The kit's ports are wired to Raspberry Pi Pico "GP" pins. Waveshare's own
// demo code gives the GP number, and the ESP32-S3-Pico pinout gives the GPIO
// that sits in that position:
//
//   Kit port   Module          Pico pin   ESP32-S3 GPIO
//   ADC1       potentiometer   GP27       GPIO8   (ADC1 channel 7, works with Wi-Fi on)
//   D1         LED             GP10       GPIO35
//   D2         passive buzzer  GP12       GPIO37
//   I2C1       1.5" OLED       GP6/GP7    GPIO17 (SDA) / GPIO18 (SCL)
//   D3         IR receiver     GP15       GPIO40

#pragma once
#include <stdint.h>

// ---------------- Pins ----------------
constexpr uint8_t potPin      = 8;    // tank-level sensor (potentiometer), kit port ADC1
constexpr uint8_t alertLedPin = 35;   // low-level alert LED, kit port D1
constexpr uint8_t buzzerPin   = 37;   // passive buzzer, kit port D2
constexpr uint8_t oledSdaPin  = 17;   // OLED screen data, kit port I2C1
constexpr uint8_t oledSclPin  = 18;   // OLED screen clock, kit port I2C1
constexpr uint8_t irPin       = 40;   // IR remote receiver, kit port D3

// ---------------- IR remote (changes the screen's page) ----------------
// To use other buttons: press one, read its code in the log
// ("Remote button 0x.."), and put that code here.
constexpr uint16_t IR_CMD_PREV    = 0x45;   // previous page (same remote as Week 7)
constexpr uint16_t IR_CMD_NEXT    = 0x46;   // next page
constexpr uint32_t IR_DEBOUNCE_MS = 250;    // ignore a second press within this time

// ---------------- OLED screen (SSD1327, 128 x 128, 16 grays) ----------------
constexpr uint16_t OLED_WIDTH    = 128;
constexpr uint16_t OLED_HEIGHT   = 128;
constexpr uint8_t  OLED_I2C_ADDR = 0x3D;     // from the kit wiki
constexpr uint32_t OLED_I2C_HZ   = 400000;   // I2C speed (400 kHz is the SSD1327 limit)
constexpr uint8_t  OLED_ROTATION = 0;        // 0 to 3, use 2 if the image is upside down
constexpr int      CHART_POINTS  = 60;       // 60 readings x 2 s = the last 2 minutes
constexpr int      LOG_ENTRIES   = 8;        // log lines kept for the Log page

// ---------------- Tank level ----------------
// The level is stored as a percentage: 0 = empty, 100 = full.
constexpr int LOW_LEVEL_THRESHOLD = 20;   // below this % the LED + buzzer alert fires
constexpr int AVG_WINDOW          = 5;    // rolling average of the last 5 readings

// ---------------- Timings (milliseconds) ----------------
constexpr unsigned long READ_INTERVAL_MS      = 2000;    // read the potentiometer
constexpr unsigned long SEND_INTERVAL_MS      = 15000;   // insert a row in Supabase
constexpr unsigned long RECONNECT_INTERVAL_MS = 10000;   // check Wi-Fi, call WiFi.begin() if down
constexpr unsigned long ALERT_TOGGLE_MS       = 250;     // alert beeps: 250 ms on, 250 ms off
constexpr unsigned int  ALERT_TONE_HZ         = 2000;    // alert pitch

// ---------------- Access point (the device's own network) ----------------
// Staff join this network and open http://192.168.4.1. Its password is
// AP_PASSWORD in secrets.h.
#define AP_SSID "TankMonitor"
constexpr int PAGE_REFRESH_S = 2;   // the web page reloads itself every 2 seconds

// ---------------- Wi-Fi start-up (setup() only) ----------------
constexpr int WIFI_CONNECT_TRIES = 20;    // 20 tries x 500 ms = give up after 10 seconds
constexpr int NTP_SYNC_TRIES     = 20;    // 20 tries x 500 ms = give up after 10 seconds

// ---------------- Time ----------------
// Melbourne time: AEST (UTC+10), daylight saving AEDT from the 1st Sunday of
// October to the 1st Sunday of April.
#define TIME_ZONE    "AEST-10AEDT,M10.1.0,M4.1.0/3"
#define NTP_SERVER_1 "pool.ntp.org"
#define NTP_SERVER_2 "time.nist.gov"
