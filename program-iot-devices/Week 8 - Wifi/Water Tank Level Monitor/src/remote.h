// remote.h
// The kit's IR receiver (port D3), used to change the screen's page.

#pragma once
#include <stdint.h>

// Starts listening for the remote. Call once from setup().
void remote_begin();

// Call on every pass of loop(). Returns the button's command code (e.g. 0x46)
// when a new button press has arrived, or -1 when there is nothing new.
int remote_poll();
