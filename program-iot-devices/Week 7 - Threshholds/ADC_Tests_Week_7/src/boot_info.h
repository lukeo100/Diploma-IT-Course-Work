// boot_info.h
// Start-up diagnostics printed to Serial: chip, flash and PSRAM sizes, and
// which I2C addresses answer on each bus. Useful for checking assumptions
// about the board (is it really the ESP32-S3R2?) and the kit wiring.

#pragma once
#include <Wire.h>

void boot_printChipInfo();
void boot_scanI2C(TwoWire &bus, const char *name);

// Addresses found on I2C0 (Wire) by the boot scan, as text, e.g. "0x40 0x70".
const char *boot_i2c0ScanResult();
