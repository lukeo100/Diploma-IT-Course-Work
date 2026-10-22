// ir_input.h
// Reads the IR receiver, prints every code to Serial, and turns mapped
// buttons into UI actions.

#pragma once
#include <stdint.h>

enum class IrAction : uint8_t {
  None,
  Next,
  Prev,
  Home,
  PageLdr,
  PageTemp,
  PageHum,
  VolumeOff,
  VolumeMax,
};

void ir_begin();

// Call on every pass of loop(). Returns IrAction::None most of the time.
IrAction ir_poll(uint32_t nowMs);
