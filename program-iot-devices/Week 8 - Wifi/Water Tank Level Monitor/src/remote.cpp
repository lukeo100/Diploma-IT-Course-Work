// remote.cpp
//
// How IR remotes work, briefly:
// The remote flashes an IR LED in a pattern of short bursts. The receiver
// module turns that into a clean on/off signal. The IRremote library times the
// pulses in the background (with a hardware timer interrupt) and decodes them
// into a command number, one per button.
//
// remote_poll() never waits: if no complete button press has arrived yet,
// decode() is false and it returns -1 straight away.
//
// Holding a button: remotes send the code once, then short "repeat" signals.
// Repeats are ignored so holding a button does not race through the pages.

#include "remote.h"

#include <Arduino.h>

// No feedback LED is used. This must come before the include. IRremote.hpp
// contains the library's code, so it is included in this one .cpp file only.
#define NO_LED_FEEDBACK_CODE
#include <IRremote.hpp>

#include "config.h"

static unsigned long lastPressMs = 0;

void remote_begin() {
  IrReceiver.begin(irPin, false);   // false = no feedback LED
}

int remote_poll() {
  if (!IrReceiver.decode()) return -1;   // nothing complete yet

  IRData data = IrReceiver.decodedIRData;
  IrReceiver.resume();                   // ready for the next button press

  if (data.protocol == UNKNOWN) return -1;                   // noise or sunlight
  if (data.flags & IRDATA_FLAGS_IS_REPEAT) return -1;        // button held down
  if (millis() - lastPressMs < IR_DEBOUNCE_MS) return -1;    // too soon after the last one

  lastPressMs = millis();
  return data.command;
}
