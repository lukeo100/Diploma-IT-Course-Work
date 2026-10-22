// sensors.h
// LDR (analogue) and SHTC3 (I2C) readings, gathered without blocking.
// This header has no Arduino includes, so the UI can be tested on a PC.

#pragma once
#include <stdint.h>

struct SensorSnapshot {
  bool     ldrValid;      // false until the first LDR average is ready
  uint16_t ldrRaw;        // averaged ADC value, 0 to 4095
  float    ldrPercent;    // ldrRaw as 0 to 100 %

  bool     climateValid;  // false until the SHTC3 gives a good reading (or after repeated failures)
  float    tempC;
  float    humidity;      // relative humidity, %
};

// Starts the ADC for the LDR and the SHTC3 on Wire (I2C0, already started).
void sensors_begin();

// Call on every pass of loop().
void sensors_update(uint32_t nowMs);

// Latest values. Cheap to call.
SensorSnapshot sensors_get();
