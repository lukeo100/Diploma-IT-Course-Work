// sensors.cpp
//
// LDR: read every LDR_SAMPLE_PERIOD_MS (50 ms) and added to a running total.
// Every LDR_INTERVAL_MS (0.5 s) the total is turned into an average and
// published. Averaging 10 samples smooths out ADC noise and mains flicker
// from room lights, and spreading the reads out means no single loop pass
// spends long on the ADC.
//
// SHTC3: handled by the non-blocking Shtc3 class.
//
// Address clash fix (found from the Serial log: CRC mismatch on every read):
// The kit's motor driver is a PCA9685 at 0x40. As well as its own address, a
// PCA9685 answers an "All Call" address (used to update many chips at once),
// which is 0x70 by default and enabled at power-up. 0x70 is also the SHTC3's
// address, so both chips replied to every read and the bytes got mixed.
// fixPca9685AllCall() clears the ALLCALL bit in the PCA9685's MODE1 register
// before the SHTC3 is used.

#include "sensors.h"

#include <Arduino.h>
#include <Wire.h>

#include "boot_info.h"
#include "config.h"
#include "pins.h"
#include "shtc3.h"

static Shtc3 sht;
static SensorSnapshot snap = {};

static uint32_t ldrSum = 0;
static uint16_t ldrCount = 0;
static uint32_t lastSampleMs = 0;
static uint32_t lastPublishMs = 0;
static uint32_t lastShtReportMs = 0;
static bool     wasClimateValid = false;

// Read one 8-bit register from a device on I2C0.
static bool readReg(uint8_t dev, uint8_t reg, uint8_t &value) {
  Wire.beginTransmission(dev);
  Wire.write(reg);
  if (Wire.endTransmission() != 0) return false;
  if (Wire.requestFrom((uint16_t)dev, (uint8_t)1) != 1) return false;
  value = Wire.read();
  return true;
}

static bool writeReg(uint8_t dev, uint8_t reg, uint8_t value) {
  Wire.beginTransmission(dev);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission() == 0;
}

// The kit's motor driver (PCA9685) on I2C0. Kept here rather than in
// config.h because only this file uses it.
static constexpr uint8_t PCA9685_I2C_ADDR = 0x40;

// Result of fixPca9685AllCall(), repeated in the SHTC3 status line.
static char pcaStatus[72] = "not checked";

static void fixPca9685AllCall() {
  constexpr uint8_t REG_MODE1      = 0x00;
  constexpr uint8_t REG_ALLCALLADR = 0x05;
  constexpr uint8_t MODE1_ALLCALL  = 0x01;   // bit 0: answer the All Call address
  constexpr uint8_t MODE1_RESTART  = 0x80;   // bit 7: never write a 1 here by accident

  uint8_t mode1 = 0, allCall = 0;
  if (!readReg(PCA9685_I2C_ADDR, REG_MODE1, mode1) ||
      !readReg(PCA9685_I2C_ADDR, REG_ALLCALLADR, allCall)) {
    snprintf(pcaStatus, sizeof(pcaStatus), "no reply from 0x40");
    Serial.printf("PCA9685: %s\n", pcaStatus);
    return;
  }
  // ALLCALLADR holds the 8-bit form of the address: 0xE0 means 7-bit 0x70.
  // Only touch the chip if it really looks like a PCA9685 using 0x70.
  if ((allCall >> 1) != SHTC3_I2C_ADDR) {
    snprintf(pcaStatus, sizeof(pcaStatus), "MODE1 0x%02X, ALLCALLADR 0x%02X, not 0x70 so left alone",
             mode1, allCall);
    Serial.printf("PCA9685: %s\n", pcaStatus);
    return;
  }
  if (!(mode1 & MODE1_ALLCALL)) {
    snprintf(pcaStatus, sizeof(pcaStatus), "All Call already off (MODE1 0x%02X)", mode1);
    Serial.printf("PCA9685: %s\n", pcaStatus);
    return;
  }
  const uint8_t newMode1 = mode1 & (uint8_t)~(MODE1_ALLCALL | MODE1_RESTART);
  uint8_t check = 0;
  if (writeReg(PCA9685_I2C_ADDR, REG_MODE1, newMode1) &&
      readReg(PCA9685_I2C_ADDR, REG_MODE1, check) && !(check & MODE1_ALLCALL)) {
    snprintf(pcaStatus, sizeof(pcaStatus), "All Call switched off, MODE1 0x%02X -> 0x%02X",
             mode1, check);
  } else {
    snprintf(pcaStatus, sizeof(pcaStatus), "FAILED to switch off All Call (MODE1 0x%02X, read back 0x%02X)",
             mode1, check);
  }
  Serial.printf("PCA9685: %s\n", pcaStatus);
}

void sensors_begin() {
  // 12-bit results (0 to 4095). 11 dB attenuation lets the pin measure up to
  // about 3.1 V instead of about 1 V.
  analogReadResolution(12);
  analogSetPinAttenuation(LDR_PIN, ADC_11db);

  fixPca9685AllCall();   // must run before the first SHTC3 command
  if (!sht.begin(Wire, SHTC3_I2C_ADDR, SHTC3_INTERVAL_MS)) {
    Serial.println("SHTC3: not found. Temperature and humidity will show --");
  }
}

void sensors_update(uint32_t nowMs) {
  // ---- LDR: take one sample every 50 ms ----
  if (nowMs - lastSampleMs >= LDR_SAMPLE_PERIOD_MS) {
    lastSampleMs = nowMs;
    ldrSum += analogRead(LDR_PIN);
    ldrCount++;
  }

  // ---- LDR: publish the average twice per second ----
  if (nowMs - lastPublishMs >= LDR_INTERVAL_MS && ldrCount > 0) {
    lastPublishMs = nowMs;
    snap.ldrRaw = (uint16_t)(ldrSum / ldrCount);
    snap.ldrPercent = snap.ldrRaw * 100.0f / 4095.0f;  // 4095.0f: float maths, not integer
    snap.ldrValid = true;
    ldrSum = 0;
    ldrCount = 0;
  }

  // ---- SHTC3: advance its state machine ----
  sht.update(nowMs);
  snap.climateValid = sht.valid();
  if (snap.climateValid) {
    snap.tempC = sht.temperatureC();
    snap.humidity = sht.humidity();
  }

  // ---- SHTC3 diagnostics on the Serial Monitor ----
  if (snap.climateValid && !wasClimateValid) {
    Serial.printf("SHTC3: reading OK, %.1f C, %.1f %%\n", snap.tempC, snap.humidity);
  }
  if (!snap.climateValid && nowMs - lastShtReportMs >= 5000) {
    lastShtReportMs = nowMs;
    Serial.printf("SHTC3: no valid reading yet. Errors: %lu. Last error: %s\n",
                  (unsigned long)sht.errorCount(), sht.lastErrorText());
    Serial.printf("       raw bytes: %s | PCA9685: %s | I2C0 (GPIO%d/%d) boot scan: %s\n",
                  sht.lastRawText(), pcaStatus, SHTC3_SDA_PIN, SHTC3_SCL_PIN,
                  boot_i2c0ScanResult());
  }
  wasClimateValid = snap.climateValid;
}

SensorSnapshot sensors_get() {
  return snap;
}
