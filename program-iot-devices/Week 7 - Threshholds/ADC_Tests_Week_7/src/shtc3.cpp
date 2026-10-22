// shtc3.cpp
//
// One measurement cycle, as a state machine:
//
//   Idle --(interval passed)--> send WAKEUP --> Waking
//   Waking --(1 ms)--> send MEASURE --> Measuring
//   Measuring --(15 ms)--> read 6 bytes, check CRC, convert, send SLEEP --> Idle
//
// The sensor sleeps between cycles, which also stops it heating itself up.
// Command codes are from the SHTC3 datasheet (and match Adafruit_SHTC3.h).

#include "shtc3.h"
#include "shtc3_math.h"

namespace {
constexpr uint16_t CMD_WAKEUP     = 0x3517;
constexpr uint16_t CMD_SLEEP      = 0xB098;
constexpr uint16_t CMD_READ_ID    = 0xEFC8;
// Normal mode, temperature first, clock stretching OFF. With stretching off
// the sensor simply does not answer (NACK) until the result is ready.
constexpr uint16_t CMD_MEASURE    = 0x7866;

constexpr uint32_t WAKE_TIME_MS      = 1;   // datasheet max 0.24 ms
constexpr uint32_t MEASURE_TIME_MS   = 15;  // datasheet max 12.1 ms, plus margin
constexpr uint32_t MEASURE_TIMEOUT_MS = 60; // give up on this cycle after this
constexpr uint8_t  FAILS_BEFORE_INVALID = 5;
}

bool Shtc3::writeCommand(uint16_t cmd) {
  _wire->beginTransmission(_addr);
  _wire->write((uint8_t)(cmd >> 8));    // high byte first
  _wire->write((uint8_t)(cmd & 0xFF));
  return _wire->endTransmission() == 0; // 0 means the sensor acknowledged
}

bool Shtc3::begin(TwoWire &wire, uint8_t address, uint32_t intervalMs) {
  _wire = &wire;
  _addr = address;
  _intervalMs = intervalMs;

  // A short blocking check is fine here because it only runs once in setup().
  if (!writeCommand(CMD_WAKEUP)) {
    Serial.printf("SHTC3: no answer at 0x%02X\n", _addr);
    return false;
  }
  delay(1);

  bool idOk = false;
  if (writeCommand(CMD_READ_ID) &&
      _wire->requestFrom((uint16_t)_addr, (uint8_t)3) == 3) {
    uint8_t b[3];
    for (uint8_t &v : b) v = _wire->read();
    const uint16_t id = (uint16_t)(b[0] << 8) | b[1];
    // The datasheet says bits 11 and 5..0 of the ID identify an SHTC3.
    idOk = (shtc3_crc8(b, 2) == b[2]) && ((id & 0x083F) == 0x0807);
    Serial.printf("SHTC3: ID 0x%04X %s\n", id, idOk ? "(OK)" : "(unexpected)");
  }
  writeCommand(CMD_SLEEP);
  return idOk;
}

const char *Shtc3::lastErrorText() const {
  switch (_lastError) {
    case Error::None:         return "none";
    case Error::NoAckWake:    return "no reply to WAKEUP (wrong pins or address, or no sensor)";
    case Error::NoAckMeasure: return "no reply to MEASURE (sensor woke but stopped answering)";
    case Error::NoData:       return "no data after 60 ms";
    case Error::BadCrc:       return "CRC mismatch (corrupted bytes: bus noise or another device answering)";
  }
  return "?";
}

void Shtc3::finishCycle(Error err) {
  writeCommand(CMD_SLEEP);
  _state = State::Idle;
  _lastError = err;
  if (err == Error::None) {
    _failsInARow = 0;
    _valid = true;
  } else {
    _errors++;
    if (_failsInARow < 255) _failsInARow++;
    // One bad read keeps the last good value; several in a row mean the
    // sensor is gone, so stop showing an old number as if it were live.
    if (_failsInARow >= FAILS_BEFORE_INVALID) _valid = false;
  }
}

void Shtc3::update(uint32_t nowMs) {
  if (_wire == nullptr) return;

  switch (_state) {
    case State::Idle:
      if (_firstCycle || nowMs - _cycleStartMs >= _intervalMs) {
        _firstCycle = false;
        _cycleStartMs = nowMs;
        if (writeCommand(CMD_WAKEUP)) {
          _state = State::Waking;
          _stateStartMs = nowMs;
        } else {
          finishCycle(Error::NoAckWake);
        }
      }
      break;

    case State::Waking:
      if (nowMs - _stateStartMs >= WAKE_TIME_MS) {
        if (writeCommand(CMD_MEASURE)) {
          _state = State::Measuring;
          _stateStartMs = nowMs;
        } else {
          finishCycle(Error::NoAckMeasure);
        }
      }
      break;

    case State::Measuring: {
      const uint32_t elapsed = nowMs - _stateStartMs;
      if (elapsed < MEASURE_TIME_MS) break;   // not ready yet, come back next pass

      if (_wire->requestFrom((uint16_t)_addr, (uint8_t)6) == 6) {
        uint8_t b[6];
        for (uint8_t &v : b) v = _wire->read();
        snprintf(_rawText, sizeof(_rawText), "%02X %02X %02X %02X %02X %02X",
                 b[0], b[1], b[2], b[3], b[4], b[5]);
        // Bytes: T high, T low, T CRC, RH high, RH low, RH CRC
        const bool crcOk = shtc3_crc8(&b[0], 2) == b[2] &&
                           shtc3_crc8(&b[3], 2) == b[5];
        if (crcOk) {
          _tempC    = shtc3_rawToTempC((uint16_t)(b[0] << 8) | b[1]);
          _humidity = shtc3_rawToHumidity((uint16_t)(b[3] << 8) | b[4]);
        }
        finishCycle(crcOk ? Error::None : Error::BadCrc);
      } else if (elapsed > MEASURE_TIMEOUT_MS) {
        finishCycle(Error::NoData);      // never answered
      }
      // Otherwise the sensor NACKed because it is still busy: try next pass.
      break;
    }
  }
}
