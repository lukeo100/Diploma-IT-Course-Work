// weather.h
// Current Melbourne temperature from Open-Meteo, fetched in a background task.
// No Arduino includes, so the UI can be tested on a PC.

#pragma once
#include <stdint.h>

enum class WeatherStatus : uint8_t {
  None,    // no successful fetch yet
  Ok,      // recent value
  Stale,   // have a value, but the latest fetch failed or it is old
};

struct WeatherSnapshot {
  WeatherStatus status;
  float    tempC;
  uint32_t ageMs;   // how long ago the value was fetched
};

// Starts the background fetch task. Call once in setup().
void weather_begin();

// Latest value. Safe to call from loop() at any time.
WeatherSnapshot weather_get();
