// boot_info.cpp

#include "boot_info.h"

#include <Arduino.h>

void boot_printChipInfo() {
  Serial.println();
  Serial.println("=== Week 7 sensor dashboard ===");
  Serial.printf("Chip:   %s rev %d, %d cores, %lu MHz\n", ESP.getChipModel(),
                ESP.getChipRevision(), ESP.getChipCores(),
                (unsigned long)ESP.getCpuFreqMHz());
  Serial.printf("Flash:  %lu MB\n", (unsigned long)(ESP.getFlashChipSize() / (1024 * 1024)));
  Serial.printf("PSRAM:  %lu KB\n", (unsigned long)(ESP.getPsramSize() / 1024));
  Serial.printf("Heap:   %lu KB free\n", (unsigned long)(ESP.getFreeHeap() / 1024));
  // Expected for the ESP32-S3R2: Flash 16 MB, PSRAM about 2048 KB.
  if (ESP.getPsramSize() == 0) {
    Serial.println("Note:   no PSRAM found. Fine for this project; it does not need PSRAM.");
  }
}

// The I2C0 result is kept so the SHTC3 status line can repeat it later
// (boot messages are easy to miss with native USB).
static char i2c0Result[96] = "not scanned";

void boot_scanI2C(TwoWire &bus, const char *name) {
  char result[96] = "";
  size_t len = 0;
  int found = 0;
  for (uint8_t addr = 1; addr < 127; addr++) {
    bus.beginTransmission(addr);
    if (bus.endTransmission() == 0) {   // 0 = a device acknowledged
      len += snprintf(result + len, sizeof(result) - len, " 0x%02X", addr);
      if (len >= sizeof(result)) len = sizeof(result) - 1;
      found++;
    }
  }
  if (!found) snprintf(result, sizeof(result), " nothing found");
  Serial.printf("I2C scan on %s:%s\n", name, result);
  if (&bus == &Wire) {
    snprintf(i2c0Result, sizeof(i2c0Result), "%s", result + 1);   // +1 skips the leading space
  }
}

const char *boot_i2c0ScanResult() {
  return i2c0Result;
}
