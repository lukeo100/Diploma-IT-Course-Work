// PC simulation of SmartDustbin.ino against the lab test cases.
// Build: g++ -std=c++17 -I mock test_sketch.cpp -o test_sketch && ./test_sketch
#include "Arduino.h"

uint32_t g_now_ms = 0;
int g_pins[64] = {0};
std::function<float(uint32_t)> g_distance = [](uint32_t) { return 0.0f; };
float g_lastServoAngle = -1;
bool g_quiet = true;
SerialMock Serial;

#include "../firmware/SmartDustbin/SmartDustbin.ino"

#include <string>
static int failures = 0, passes = 0;

static void check(bool ok, const std::string &what) {
  std::printf("  %s  %s\n", ok ? "PASS" : "FAIL", what.c_str());
  ok ? passes++ : failures++;
}

static void reset() {
  g_now_ms = 0;
  for (int &p : g_pins) p = 0;
  lidState = LidState::Closed;
  servoAngle = servoTarget = CLOSED_ANGLE;
  clearCount = 0;
  setup();
}

static void runUntil(uint32_t t) {
  while (g_now_ms < t) { g_now_ms += 5; loop(); }
}

static bool redOn()   { return g_pins[PIN_LED_RED] == HIGH && g_pins[PIN_LED_GREEN] == LOW; }
static bool greenOn() { return g_pins[PIN_LED_GREEN] == HIGH && g_pins[PIN_LED_RED] == LOW; }

int main(int argc, char **) {
  g_quiet = argc < 2;

  std::puts("1. Power on");
  reset();
  check(redOn(), "red LED on, green off");
  check(servoAngle == 0, "servo at 0°");

  std::puts("2. No object near the sensor");
  reset();
  g_distance = [](uint32_t) { return 150.0f; };
  runUntil(10000);
  check(lidState == LidState::Closed && redOn(), "lid stays closed, red on");

  std::puts("3. Hand detected at 18 cm");
  reset();
  g_distance = [](uint32_t t) { return t >= 2000 ? 18.0f : 150.0f; };
  runUntil(3100);
  check(lidState == LidState::Open && greenOn(), "lid open, green on");
  check(servoAngle == 90, "servo at 90°");

  std::puts("4. Hand moves to 25 cm (between thresholds)");
  g_distance = [](uint32_t) { return 25.0f; };
  runUntil(20000);
  check(lidState == LidState::Open && greenOn(), "lid stays open");

  std::puts("5. Hand at 25 cm while lid closed does not open it");
  reset();
  g_distance = [](uint32_t) { return 25.0f; };
  runUntil(5000);
  check(lidState == LidState::Closed, "stays closed (hysteresis)");

  std::puts("6. Hand moves to 30 cm or farther");
  reset();
  g_distance = [](uint32_t t) { return t < 3000 ? 15.0f : 35.0f; };
  runUntil(4500);
  check(lidState == LidState::Open, "still open 1.5 s after hand leaves (3 s delay)");
  runUntil(9000);
  check(lidState == LidState::Closed && redOn(), "closed, red on");
  check(servoAngle == 0, "servo back at 0°");

  std::puts("7. Object remains within 20 cm");
  reset();
  g_distance = [](uint32_t) { return 12.0f; };
  runUntil(60000);
  check(lidState == LidState::Open && greenOn(), "lid open for 60 s");

  std::puts("8. Single missed echo (999 cm) while open");
  reset();
  g_distance = [](uint32_t t) {
    if (t >= 5000 && t < 6000) return 0.0f;  // one no-echo reading
    return 15.0f;
  };
  runUntil(12000);
  check(lidState == LidState::Open, "one 999 reading does not close the lid");

  std::puts("9. Mixed clear / no-echo readings do not close early");
  reset();
  g_distance = [](uint32_t t) {
    if (t < 3000) return 15.0f;
    return ((t / 1000) % 2) ? 0.0f : 40.0f;  // alternate 999 and 40 cm
  };
  runUntil(6500);
  check(lidState == LidState::Open, "still open with only 2 valid clear readings");

  std::puts("10. Bin facing empty room (all 999) closes by failsafe");
  reset();
  g_distance = [](uint32_t t) { return t < 3000 ? 15.0f : 0.0f; };
  runUntil(12000);
  check(lidState == LidState::Open, "open 9 s after hand left");
  runUntil(22000);
  check(lidState == LidState::Closed, "closed by 15 s failsafe");

  std::puts("11. Hand returns while lid is closing -> reopens");
  reset();
  uint32_t closingSeen = 0;
  g_distance = [&](uint32_t t) {
    if (t < 3000) return 15.0f;
    if (lidState == LidState::Closing && !closingSeen) closingSeen = t;
    if (closingSeen && t > closingSeen + 300) return 10.0f;
    return 50.0f;
  };
  runUntil(12000);
  check(closingSeen != 0, "lid started closing");
  check(lidState == LidState::Open && greenOn(), "lid reopened, green on");

  std::puts("12. Hand moves 19 -> 29 -> 31 cm (no chatter)");
  reset();
  int toggles = 0; LidState last = LidState::Closed;
  g_distance = [](uint32_t t) {
    if (t < 3000) return 19.0f;
    if (t < 15000) return (t / 500) % 2 ? 29.0f : 21.0f;
    return 31.0f;
  };
  while (g_now_ms < 25000) {
    g_now_ms += 5; loop();
    if (lidState != last) { toggles++; last = lidState; }
  }
  check(toggles == 4, "exactly one open and one close cycle");

  std::printf("\n%d passed, %d failed\n", passes, failures);
  return failures ? 1 : 0;
}
