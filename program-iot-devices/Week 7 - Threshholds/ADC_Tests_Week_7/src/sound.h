// sound.h
// UI sounds on the kit's passive buzzer: page clicks, chart ticks and an
// on/off chirp. No Arduino includes, so the UI can be tested on a PC.

#pragma once

void sound_begin();               // plays a short chirp if sound starts on

void sound_setEnabled(bool on);   // remote "volume max" = true, "volume off" = false
bool sound_enabled();

void sound_click();               // short click when the page changes

// Short tick for a new chart point. position: 0.0 = bottom of the chart,
// 1.0 = top. Higher on the chart means higher pitch.
void sound_chartTick(float position);
