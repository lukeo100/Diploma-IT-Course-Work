// pins.h
// Every GPIO used by the project, in one place.
// Board: Waveshare ESP32-S3-Pico on the Waveshare Pico Sensor Kit B.
// The kit wiki only gives port labels, so these numbers come from Luca's own
// pin mapping, not from Waveshare.

#pragma once
#include <stdint.h>

// OLED, kit port I2C1 (1.5 inch, 128x128, 16 grays, SSD1327 assumed)
constexpr uint8_t OLED_SDA_PIN = 17;
constexpr uint8_t OLED_SCL_PIN = 18;

// SHTC3 temperature and humidity sensor, kit port I2C0
// GPIO33 and 34 are only reserved on ESP32-S3 chips with OCTAL PSRAM (R8).
// The ESP32-S3R2 has quad PSRAM, so they are free to use here.
constexpr uint8_t SHTC3_SDA_PIN = 33;
constexpr uint8_t SHTC3_SCL_PIN = 34;

// LDR, kit port ADC0. GPIO7 is ADC1 channel 6, which keeps working with Wi-Fi on.
constexpr uint8_t LDR_PIN = 7;

// IR receiver, kit port D3. Confirmed working on GPIO40.
#define IR_RX_PIN 40

// Passive buzzer, kit port D2. Not confirmed which GPIO this is.
// You should hear a short two-note chirp at start-up. If you hear nothing,
// change this to 38 and upload again.
#define BUZZER_PIN 37
