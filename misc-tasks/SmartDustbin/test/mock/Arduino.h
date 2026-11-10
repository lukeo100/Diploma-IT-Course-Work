// Minimal Arduino/ESP32 mock so the sketch's logic can be tested on a PC.
#pragma once
#include <cstdint>
#include <cstdio>
#include <cstdarg>
#include <functional>
#include <cstdlib>
#define constrain(x, a, b) ((x) < (a) ? (a) : ((x) > (b) ? (b) : (x)))

#define HIGH 1
#define LOW 0
#define OUTPUT 1
#define INPUT 0
#define ESP_ARDUINO_VERSION_MAJOR 3

extern uint32_t g_now_ms;
extern int g_pins[64];
extern std::function<float(uint32_t)> g_distance;   // cm at time t, <=0 means no echo
extern float g_lastServoAngle;
extern bool g_quiet;

inline uint32_t millis() { return g_now_ms; }
inline void delayMicroseconds(unsigned) {}
inline void pinMode(uint8_t, uint8_t) {}
inline void digitalWrite(uint8_t p, int v) { g_pins[p] = v; }
inline unsigned long pulseIn(uint8_t, int, unsigned long timeout) {
  float cm = g_distance(g_now_ms);
  if (cm <= 0) return 0;
  unsigned long us = (unsigned long)(cm * 2.0f / 0.0343f);
  return us > timeout ? 0 : us;
}
inline void ledcAttach(uint8_t, uint32_t, uint8_t) {}
inline void ledcWrite(uint8_t, uint32_t duty) {
  float us = duty * 20000.0f / 16383.0f;
  g_lastServoAngle = (us - 500.0f) / (1900.0f / 180.0f);
}

struct SerialMock {
  void begin(unsigned long) {}
  int available() { return 0; }
  int read() { return -1; }
  void println(const char *s) { if (!g_quiet) std::printf("[%6u] %s\n", g_now_ms, s); }
  void printf(const char *fmt, ...) {
    if (g_quiet) return;
    std::printf("[%6u] ", g_now_ms);
    va_list a; va_start(a, fmt); std::vprintf(fmt, a); va_end(a);
  }
};
extern SerialMock Serial;
