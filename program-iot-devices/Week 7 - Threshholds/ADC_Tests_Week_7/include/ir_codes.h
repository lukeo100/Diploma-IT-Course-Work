// ir_codes.h
// Maps your remote's buttons to UI actions.
//
// How to add more buttons:
// 1. Open the Serial Monitor (115200 baud).
// 2. Press the button. You will see a line like:
//      IR  protocol=NEC  address=0x0000  command=0x45  raw=0xBA45FF00
// 3. Copy the "command" value into the matching line below.
//
// If every command below is IR_UNMAPPED, ANY button press moves to the next
// page, so a new remote is usable before you map it.

#pragma once
#include <stdint.h>

constexpr uint16_t IR_UNMAPPED = 0xFFFF;

// Only accept codes from this remote address. -1 means accept any address.
// Your remote sends address 0x0000. Set this to 0x0000 if another remote in
// the room (TV, aircon) starts changing pages.
constexpr int32_t IR_REQUIRED_ADDRESS = -1;

// ---- Mapped on Luca's remote (NEC, address 0x0000) ----
constexpr uint16_t IR_CMD_PREV      = 0x45;         // back a page
constexpr uint16_t IR_CMD_NEXT      = 0x46;         // next page
constexpr uint16_t IR_CMD_VOL_OFF   = 0x07;         // sound off
constexpr uint16_t IR_CMD_VOL_MAX   = 0x15;         // sound on, full volume

// ---- Spare actions, not mapped yet ----
constexpr uint16_t IR_CMD_HOME      = IR_UNMAPPED;  // jump to the readings page
constexpr uint16_t IR_CMD_PAGE_LDR  = IR_UNMAPPED;  // jump to the LDR chart
constexpr uint16_t IR_CMD_PAGE_TEMP = IR_UNMAPPED;  // jump to the temperature chart
constexpr uint16_t IR_CMD_PAGE_HUM  = IR_UNMAPPED;  // jump to the humidity chart
