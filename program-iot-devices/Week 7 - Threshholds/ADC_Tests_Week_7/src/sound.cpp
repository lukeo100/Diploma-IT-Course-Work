// sound.cpp
//
// Passive vs active buzzer (same idea as the Week 7 notes):
// A passive buzzer has no oscillator of its own, so it needs a square wave.
// tone(pin, frequency, duration) makes one with the ESP32's LEDC PWM hardware.
// The pitch you hear is the frequency of that wave.
//
// Why tone() does not block here:
// In the ESP32 Arduino core, tone() only puts a message on a queue. A small
// background task (created by the core) starts the note, waits for the
// duration, and stops it. So loop() carries straight on, and several tone()
// calls in a row play one after the other.
//
// Volume:
// tone() always drives the buzzer at full strength (50 % duty cycle), so the
// two remote buttons are simply "sound off" and "sound on at max volume".
//
// Pitch for chart ticks:
// position 0..1 is mapped exponentially between SOUND_TICK_LOW_HZ and
// SOUND_TICK_HIGH_HZ. Exponential sounds even to the ear: each step up the
// chart raises the pitch by the same musical interval, like keys on a piano.

#include "sound.h"

#include <Arduino.h>
#include <math.h>

#include "config.h"
#include "pins.h"

static bool enabled = SOUND_START_ON;

static void play(uint16_t hz, uint16_t ms) {
  if (enabled) tone(BUZZER_PIN, hz, ms);
}

void sound_begin() {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR < 3
  // Core 2.x quirk: the first tone() reads LEDC channel 0 before it exists and
  // prints "ledc_get_duty: LEDC is not initialized". Setting the channel up
  // first stops that harmless error message.
  ledcSetup(0, 1000, 10);
#endif
  Serial.printf("Sound: buzzer on GPIO%d, %s\n", BUZZER_PIN, enabled ? "on" : "off");
  // Rising two-note chirp so you can tell the buzzer pin is right.
  play(1500, 60);
  play(2200, 80);
}

void sound_setEnabled(bool on) {
  enabled = on;
  Serial.printf("Sound: %s\n", on ? "on (max volume)" : "off");
  if (on) {
    play(1500, 60);
    play(2200, 80);
  }
}

bool sound_enabled() {
  return enabled;
}

void sound_click() {
  play(SOUND_CLICK_HZ, SOUND_CLICK_MS);
}

void sound_chartTick(float position) {
  if (position < 0.0f) position = 0.0f;
  if (position > 1.0f) position = 1.0f;
  const float ratio = (float)SOUND_TICK_HIGH_HZ / (float)SOUND_TICK_LOW_HZ;
  const float hz = SOUND_TICK_LOW_HZ * powf(ratio, position);
  play((uint16_t)hz, SOUND_TICK_MS);
}
