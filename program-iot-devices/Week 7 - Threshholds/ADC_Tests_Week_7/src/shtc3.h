// shtc3.h
// Non-blocking driver for the Sensirion SHTC3 temperature and humidity sensor.
//
// Why not the Adafruit_SHTC3 library? Its getEvent() call waits about 13 ms
// with delay() while the sensor measures. Here the same steps are split into a
// small state machine, so update() returns straight away and the UI and IR
// keep running while the sensor works.

#pragma once
#include <Arduino.h>
#include <Wire.h>

class Shtc3 {
public:
  // Starts talking to the sensor on an already started I2C bus.
  // Returns true if the chip answered and its ID looks like an SHTC3.
  bool begin(TwoWire &wire, uint8_t address, uint32_t intervalMs);

  // Call on every pass of loop(). Moves the state machine on when its
  // waiting time is over. Never calls delay().
  void update(uint32_t nowMs);

  bool     valid() const        { return _valid; }        // true once a good reading exists
  float    temperatureC() const { return _tempC; }
  float    humidity() const     { return _humidity; }     // relative humidity in %
  uint32_t errorCount() const   { return _errors; }

  // Why the most recent cycle failed, in words, for the Serial Monitor.
  const char *lastErrorText() const;

  // The 6 bytes from the most recent read, as hex text, for diagnosing
  // CRC failures. Format: "T_hi T_lo T_crc RH_hi RH_lo RH_crc".
  const char *lastRawText() const { return _rawText; }

private:
  enum class State : uint8_t { Idle, Waking, Measuring };
  enum class Error : uint8_t { None, NoAckWake, NoAckMeasure, NoData, BadCrc };

  bool writeCommand(uint16_t cmd);
  void finishCycle(Error err);

  TwoWire *_wire = nullptr;
  uint8_t  _addr = 0x70;
  uint32_t _intervalMs = 1000;

  State    _state = State::Idle;
  uint32_t _stateStartMs = 0;    // when the current state began
  uint32_t _cycleStartMs = 0;    // when the last measurement cycle began
  bool     _firstCycle = true;

  bool     _valid = false;
  float    _tempC = 0;
  float    _humidity = 0;
  uint8_t  _failsInARow = 0;
  uint32_t _errors = 0;
  Error    _lastError = Error::None;
  char     _rawText[24] = "none yet";
};
