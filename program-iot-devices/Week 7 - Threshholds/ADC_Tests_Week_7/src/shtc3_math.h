// shtc3_math.h
// Pure maths for the SHTC3, kept separate from the I2C code so it can be
// tested on a PC. Formulas and the CRC come from the Sensirion SHTC3 datasheet.

#pragma once
#include <stdint.h>

// CRC-8 check used by Sensirion sensors.
// Polynomial 0x31 (x^8 + x^5 + x^4 + 1), start value 0xFF, no final XOR.
// Datasheet test vector: bytes 0xBE 0xEF give 0x92.
inline uint8_t shtc3_crc8(const uint8_t *data, int len) {
  uint8_t crc = 0xFF;
  for (int i = 0; i < len; i++) {
    crc ^= data[i];
    for (int bit = 0; bit < 8; bit++) {
      crc = (crc & 0x80) ? (uint8_t)((crc << 1) ^ 0x31) : (uint8_t)(crc << 1);
    }
  }
  return crc;
}

// Raw 16-bit readings to real units.
inline float shtc3_rawToTempC(uint16_t raw) {
  return -45.0f + 175.0f * (float)raw / 65536.0f;
}

inline float shtc3_rawToHumidity(uint16_t raw) {
  return 100.0f * (float)raw / 65536.0f;
}
