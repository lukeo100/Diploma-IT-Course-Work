/*
  Smart Automatic Dustbin  –  ESP32-C3 + HC-SR04 + SG90
  ------------------------------------------------------------------
  Follows the robotics-lab brief:
    * Power on  -> lid closed at 0°, red LED on, green LED off.
    * Every second: 10 µs TRIG pulse on GPIO 3, echo on GPIO 1,
      distance printed to Serial at 115200 baud.
    * Hand within 20 cm  -> lid opens to 90°, green on, red off.
    * Lid stays open while the hand is between 20 and 30 cm (hysteresis).
    * Hand at 30 cm or more -> lid closes to 0°, green off, red on.
    * No echo within 30 ms -> reported as 999 cm.

  "More robust version" from the brief, as implemented here:
    * An open lid only closes after CLEAR_READINGS_REQUIRED consecutive
      VALID readings of 30 cm or more, spanning at least CLOSE_DELAY_MS
      (3 s, as on the infographic).
    * A 999 cm (no echo) reading neither counts as clear nor resets the
      count, so a single missed echo can no longer close the lid.
      Failsafe: if nothing has been seen within 30 cm for
      NO_NEAR_FAILSAFE_MS (e.g. the bin faces an empty room and every
      reading is 999), the lid closes anyway.
    * The lid closes slowly. While it closes the sensor is read every
      100 ms, and anything within 30 cm reopens the lid at once.

  Board: any ESP32-C3 (C3 Zero, C3 SuperMini, DevKitM).
  Arduino IDE: install "esp32 by Espressif" (2.x or 3.x). No extra
  libraries needed – the servo is driven with the built-in LEDC PWM.
  For Serial Monitor output over the C3's own USB port, set
  Tools -> "USB CDC On Boot" -> Enabled.

  WIRING (see README for the full diagram)
    HC-SR04 ECHO is 5 V. Use a divider: ECHO -> 1 kΩ -> GPIO 1,
    and GPIO 1 -> 2 kΩ -> GND.  All grounds common.
*/

#include <Arduino.h>

// ------------------------------------------------------------------
// Pins (from the brief)
// ------------------------------------------------------------------
constexpr uint8_t PIN_SERVO     = 5;
constexpr uint8_t PIN_TRIG      = 3;
constexpr uint8_t PIN_ECHO      = 1;
constexpr uint8_t PIN_LED_GREEN = 8;   // lid open
constexpr uint8_t PIN_LED_RED   = 6;   // lid closed

// ------------------------------------------------------------------
// Behaviour
// ------------------------------------------------------------------
constexpr float    OPEN_DISTANCE_CM        = 20.0f;   // open at or below
constexpr float    CLOSE_DISTANCE_CM       = 30.0f;   // clear at or above
constexpr uint32_t MEASURE_INTERVAL_MS     = 1000;    // brief: every second
constexpr uint32_t CLOSING_MEASURE_MS      = 100;     // while lid is moving down
constexpr uint8_t  CLEAR_READINGS_REQUIRED = 3;       // consecutive valid clear readings
constexpr uint32_t CLOSE_DELAY_MS          = 3000;    // hand clear -> wait 3 s -> close
constexpr uint32_t NO_NEAR_FAILSAFE_MS     = 15000;   // close if nothing near for 15 s
constexpr uint32_t ECHO_TIMEOUT_US         = 30000;   // 30 ms
constexpr float    NO_ECHO_CM              = 999.0f;
constexpr float    MIN_VALID_CM            = 2.0f;    // HC-SR04 blind zone
constexpr float    MAX_VALID_CM            = 400.0f;

// ------------------------------------------------------------------
// Servo (SG90) – values from the team's datasheet (SG90-datasheet.pdf):
//   20 ms PWM period (50 Hz), 4.8 V, 1.8 kgf·cm stall, 0.1 s per 60°,
//   about 180° of travel. The TowerPro SG90 section gives a 500–2400 µs
//   pulse range (used below). The generic SG90 section gives ~1 ms to
//   ~2 ms with 1.5 ms at the centre; if your servo only moves about half
//   as far as expected, or buzzes at 0°, use 1000 / 2000 instead.
//   Check with SERVO_TEST_MODE before fitting the lid.
// ------------------------------------------------------------------
constexpr int      CLOSED_ANGLE   = 0;
constexpr int      OPEN_ANGLE     = 90;
constexpr bool     SERVO_REVERSED = false;  // set true if the lid moves the wrong way
constexpr uint16_t SERVO_MIN_US   = 500;    // pulse at 0°   (datasheet: TowerPro SG90)
constexpr uint16_t SERVO_MAX_US   = 2400;   // pulse at 180°
constexpr bool     SERVO_TEST_MODE = false; // true: type an angle (0–180) in Serial Monitor
constexpr uint32_t OPEN_SWEEP_MS  = 400;    // 0° -> 90°; servo can do it in 0.15 s
constexpr uint32_t CLOSE_SWEEP_MS = 1500;   // slow close, so a hand can stop it
constexpr uint32_t SERVO_FREQ_HZ  = 50;
constexpr uint8_t  SERVO_RES_BITS = 14;
#if !(defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3)
constexpr uint8_t  SERVO_LEDC_CH  = 0;      // Arduino-ESP32 2.x only
#endif

// ------------------------------------------------------------------
// State
// ------------------------------------------------------------------
enum class LidState : uint8_t { Closed, Opening, Open, Closing };

LidState lidState      = LidState::Closed;
float    servoAngle    = CLOSED_ANGLE;   // where the servo is now
float    servoTarget   = CLOSED_ANGLE;
float    servoDegPerMs = 0.0f;
uint32_t lastServoMs   = 0;
uint32_t lastMeasureMs = 0;
uint32_t lastNearMs    = 0;              // last valid reading under 30 cm
uint32_t clearSinceMs  = 0;
uint8_t  clearCount    = 0;

// ------------------------------------------------------------------
// Helpers
// ------------------------------------------------------------------
const char *stateName(LidState s) {
  switch (s) {
    case LidState::Closed:  return "CLOSED";
    case LidState::Opening: return "OPENING";
    case LidState::Open:    return "OPEN";
    case LidState::Closing: return "CLOSING";
  }
  return "?";
}

bool isValid(float cm) { return cm >= MIN_VALID_CM && cm <= MAX_VALID_CM; }

void setLeds(bool lidOpen) {
  digitalWrite(PIN_LED_GREEN, lidOpen ? HIGH : LOW);
  digitalWrite(PIN_LED_RED,   lidOpen ? LOW  : HIGH);
}

void servoWriteAngle(float angle) {
  if (angle < 0)   angle = 0;
  if (angle > 180) angle = 180;
  if (SERVO_REVERSED) angle = 180.0f - angle;
  const float us = SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0f);
  const uint32_t period_us = 1000000UL / SERVO_FREQ_HZ;
  const uint32_t duty = (uint32_t)(us * ((1UL << SERVO_RES_BITS) - 1) / period_us);
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcWrite(PIN_SERVO, duty);
#else
  ledcWrite(SERVO_LEDC_CH, duty);
#endif
}

void servoBegin() {
#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttach(PIN_SERVO, SERVO_FREQ_HZ, SERVO_RES_BITS);
#else
  ledcSetup(SERVO_LEDC_CH, SERVO_FREQ_HZ, SERVO_RES_BITS);
  ledcAttachPin(PIN_SERVO, SERVO_LEDC_CH);
#endif
}

void moveServo(float target, uint32_t sweepMs) {
  servoTarget   = target;
  servoDegPerMs = (float)(OPEN_ANGLE - CLOSED_ANGLE) / (float)sweepMs;
}

// Returns true when the servo has reached its target.
bool updateServo(uint32_t now) {
  const uint32_t dt = now - lastServoMs;
  lastServoMs = now;
  if (servoAngle == servoTarget) return true;
  const float step = servoDegPerMs * dt;
  if (servoAngle < servoTarget) {
    servoAngle += step;
    if (servoAngle > servoTarget) servoAngle = servoTarget;
  } else {
    servoAngle -= step;
    if (servoAngle < servoTarget) servoAngle = servoTarget;
  }
  servoWriteAngle(servoAngle);
  return servoAngle == servoTarget;
}

// HC-SR04 reading in cm, or NO_ECHO_CM (999) if nothing returns in 30 ms.
float measureDistanceCm() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  const unsigned long echoUs = pulseIn(PIN_ECHO, HIGH, ECHO_TIMEOUT_US);
  if (echoUs == 0) return NO_ECHO_CM;
  return echoUs * 0.0343f / 2.0f;   // speed of sound ≈ 343 m/s
}

// ------------------------------------------------------------------
// Lid actions
// ------------------------------------------------------------------
void startOpening(uint32_t now, const char *why) {
  lidState   = LidState::Opening;
  lastNearMs = now;
  clearCount = 0;
  setLeds(true);
  moveServo(OPEN_ANGLE, OPEN_SWEEP_MS);
  Serial.printf(">> Opening lid (%s)\n", why);
}

void startClosing(const char *why) {
  lidState = LidState::Closing;
  setLeds(false);
  moveServo(CLOSED_ANGLE, CLOSE_SWEEP_MS);
  Serial.printf(">> Closing lid (%s)\n", why);
}

// ------------------------------------------------------------------
// Decision logic for one distance reading
// ------------------------------------------------------------------
void handleReading(float cm, uint32_t now) {
  const bool valid = isValid(cm);

  switch (lidState) {
    case LidState::Closed:
      if (valid && cm <= OPEN_DISTANCE_CM) startOpening(now, "hand within 20 cm");
      break;

    case LidState::Opening:
    case LidState::Open:
      if (valid && cm < CLOSE_DISTANCE_CM) {          // still near: stay open
        lastNearMs = now;
        clearCount = 0;
      } else if (valid) {                             // valid clear reading
        if (clearCount == 0) clearSinceMs = now;
        if (clearCount < 255) clearCount++;
      }
      // cm == 999 (no echo): ignored – neither clear nor near.

      if (lidState == LidState::Open) {
        if (clearCount >= CLEAR_READINGS_REQUIRED &&
            now - clearSinceMs >= CLOSE_DELAY_MS) {
          startClosing("hand clear for 3 s");
        } else if (now - lastNearMs >= NO_NEAR_FAILSAFE_MS) {
          startClosing("nothing near for 15 s (failsafe)");
        }
      }
      break;

    case LidState::Closing:
      if (valid && cm < CLOSE_DISTANCE_CM) startOpening(now, "obstruction while closing");
      break;
  }
}

// ------------------------------------------------------------------
// Arduino entry points
// ------------------------------------------------------------------
void setup() {
  Serial.begin(115200);

  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  digitalWrite(PIN_TRIG, LOW);

  servoBegin();
  servoAngle = servoTarget = CLOSED_ANGLE;
  servoWriteAngle(CLOSED_ANGLE);      // lid closed at 0°
  setLeds(false);                     // red on, green off

  const uint32_t now = millis();
  lastServoMs = now;
  lastMeasureMs = now - MEASURE_INTERVAL_MS;   // measure straight away
  lastNearMs = now;

  if (SERVO_TEST_MODE) {
    Serial.println("SERVO TEST MODE: type an angle 0-180 and press Enter");
  } else {
    Serial.println("Smart dustbin ready: lid CLOSED");
  }
}

// Servo calibration: type an angle and press Enter; the servo moves there.
void servoTestLoop() {
  static char buf[8];
  static uint8_t len = 0;
  while (Serial.available()) {
    const char c = Serial.read();
    if (c == '\n' || c == '\r') {
      if (len) {
        buf[len] = '\0';
        const int angle = constrain(atoi(buf), 0, 180);
        servoWriteAngle(angle);
        const float us = SERVO_MIN_US + (SERVO_MAX_US - SERVO_MIN_US) * (angle / 180.0f);
        Serial.printf("Servo -> %d° (%.0f µs)\n", angle, us);
        len = 0;
      }
    } else if (len < sizeof(buf) - 1) {
      buf[len++] = c;
    }
  }
}

void loop() {
  if (SERVO_TEST_MODE) {
    servoTestLoop();
    return;
  }

  const uint32_t now = millis();

  if (updateServo(now)) {
    if (lidState == LidState::Opening) {
      lidState = LidState::Open;
      Serial.println("   Lid OPEN");
    } else if (lidState == LidState::Closing) {
      lidState = LidState::Closed;
      Serial.println("   Lid CLOSED");
    }
  }

  const uint32_t interval =
      (lidState == LidState::Closing) ? CLOSING_MEASURE_MS : MEASURE_INTERVAL_MS;

  if (now - lastMeasureMs >= interval) {
    lastMeasureMs = now;
    const float cm = measureDistanceCm();
    Serial.printf("Distance: %6.1f cm   Lid: %s\n", cm, stateName(lidState));
    handleReading(cm, now);
  }
}
