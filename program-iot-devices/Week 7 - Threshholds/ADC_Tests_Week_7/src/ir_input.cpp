// ir_input.cpp
//
// How IR remotes work, briefly:
// The remote flashes an IR LED at 38 kHz in a pattern of on/off bursts. The
// receiver module (probably a 38 kHz type on this kit) removes the 38 kHz
// carrier and outputs a clean digital signal: LOW during a burst, HIGH between.
// The IRremote library times those pulses with a hardware timer interrupt and
// decodes them into a protocol (NEC is the most common on cheap remotes), an
// address (which remote) and a command (which button).
//
// Holding a button: NEC remotes send the full code once, then short "repeat"
// frames. Repeats are printed but ignored for page changes, so holding a
// button does not race through the pages.

#include "ir_input.h"

#include <Arduino.h>

// Leave out the feedback LED code (no LED is used). Must come before the
// include. IRremote.hpp contains the library's code, so include it in this
// one .cpp file only.
#define NO_LED_FEEDBACK_CODE
#include <IRremote.hpp>

#include "config.h"
#include "ir_codes.h"
#include "pins.h"

static uint32_t lastActionMs = 0;

// True if at least one button has been mapped in ir_codes.h.
static constexpr bool mappingConfigured =
    IR_CMD_NEXT != IR_UNMAPPED || IR_CMD_PREV != IR_UNMAPPED ||
    IR_CMD_VOL_OFF != IR_UNMAPPED || IR_CMD_VOL_MAX != IR_UNMAPPED ||
    IR_CMD_HOME != IR_UNMAPPED || IR_CMD_PAGE_LDR != IR_UNMAPPED ||
    IR_CMD_PAGE_TEMP != IR_UNMAPPED || IR_CMD_PAGE_HUM != IR_UNMAPPED;

void ir_begin() {
  IrReceiver.begin(IR_RX_PIN, false);   // false = no feedback LED
  Serial.printf("IR: listening on GPIO%d\n", IR_RX_PIN);
  if (!mappingConfigured) {
    Serial.println("IR: no buttons mapped in ir_codes.h yet, any button = next page");
  }
}

static IrAction mapCommand(const IRData &d) {
  if (IR_REQUIRED_ADDRESS >= 0 && d.address != (uint16_t)IR_REQUIRED_ADDRESS) {
    return IrAction::None;   // a different remote
  }
  if (!mappingConfigured) return IrAction::Next;

  if (d.command == IR_CMD_NEXT)      return IrAction::Next;
  if (d.command == IR_CMD_PREV)      return IrAction::Prev;
  if (d.command == IR_CMD_VOL_OFF)   return IrAction::VolumeOff;
  if (d.command == IR_CMD_VOL_MAX)   return IrAction::VolumeMax;
  if (d.command == IR_CMD_HOME)      return IrAction::Home;
  if (d.command == IR_CMD_PAGE_LDR)  return IrAction::PageLdr;
  if (d.command == IR_CMD_PAGE_TEMP) return IrAction::PageTemp;
  if (d.command == IR_CMD_PAGE_HUM)  return IrAction::PageHum;
  return IrAction::None;
}

IrAction ir_poll(uint32_t nowMs) {
  // decode() is true when the interrupt has captured a complete frame.
  if (!IrReceiver.decode()) return IrAction::None;

  // Copy the result, then let the receiver capture the next frame right away.
  const IRData d = IrReceiver.decodedIRData;
  IrReceiver.resume();

  if (d.protocol == UNKNOWN) {
    // Noise, sunlight, or a protocol the library does not know.
    Serial.printf("IR  unknown signal (%u pulses)\n", (unsigned)d.rawlen);
    return IrAction::None;
  }

  const bool isRepeat = d.flags & IRDATA_FLAGS_IS_REPEAT;
  Serial.printf("IR  protocol=%s  address=0x%04X  command=0x%02X  raw=0x%08llX%s\n",
                getProtocolString(d.protocol), d.address, d.command,
                (unsigned long long)d.decodedRawData, isRepeat ? "  (repeat)" : "");

  if (isRepeat) return IrAction::None;
  if (nowMs - lastActionMs < IR_DEBOUNCE_MS) return IrAction::None;

  const IrAction a = mapCommand(d);
  if (a != IrAction::None) lastActionMs = nowMs;
  return a;
}
