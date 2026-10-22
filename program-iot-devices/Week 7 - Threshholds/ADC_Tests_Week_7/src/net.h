// net.h
// Wi-Fi connection and internet time (NTP) for Melbourne.
// No Arduino includes, so the UI can be tested on a PC.

#pragma once
#include <stdint.h>
#include <time.h>

enum class NetState : uint8_t {
  NoCredentials,   // secrets.h still has the placeholder values
  Connecting,
  Connected,
};

void     net_begin();
void     net_update(uint32_t nowMs);   // call on every pass of loop()
NetState net_state();

// True once NTP has set the clock (it starts at 1 January 1970).
bool net_timeSynced();

// Fills `out` with Melbourne local time (AEST or AEDT). Returns false if the
// time has not been synced yet.
bool net_localTime(struct tm &out);
