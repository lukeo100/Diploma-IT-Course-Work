//
// Security System
// By Luca for IoT Class (Diploma of IT)
// This code is designed for an Arduino-based security system that uses an RGB LED, a buzzer, a button, and a PIR sensor.
//

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
// The parameter -1 indicates that the display does not have a shared reset pin
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

const uint8_t rLedPin = 26;             // red LED pin
const uint8_t buttonPin = 27;           // button pin (avoid GPIO12, a flash-voltage strapping pin)
const uint8_t buzzerPin = 23;           // buzzer pin
const uint8_t PIRPin = 13;              // PIR sensor pin
const unsigned long previousMillis = 0; // last time the LED was updated
const long interval = 500;              // interval at which to blink (milliseconds)
bool ledState = false;                  // on/off
bool buzzerActive = false;              // on/off
unsigned long buzzerStartTime = 0;      // time when the buzzer was activated
int buzzerDuration = 1000;              // duration for which the buzzer will be active (milliseconds)

const int sweepMinFreq = 500;               // Hz, start of alarm sweep
const int sweepMaxFreq = 2000;              // Hz, end of alarm sweep
const unsigned long sweepPeriod = 500;      // ms for one low->high sweep cycle
const unsigned long freqUpdateInterval = 1; // ms between frequency updates
unsigned long lastFreqUpdateTime = 0;

const int debounceDelay = 600; // milliseconds
bool lastRawButtonState = HIGH;    // INPUT_PULLUP means HIGH when not pressed
bool lastStableButtonState = HIGH;
unsigned long lastDebounceTime = 0;

bool systemArmed = true; // System is armed by default
int triggeredCount = 0;  // Count of how many times the alarm has been triggered
bool lastTriggeredState = false; // Last state of the motion detection

void startBuzzer(int duration)
{
  buzzerActive = true;
  buzzerStartTime = millis();
  buzzerDuration = duration;
  lastFreqUpdateTime = 0; // force an immediate frequency update
}

void updateBuzzer()
{
  if (!buzzerActive)
  {
    return;
  }

  unsigned long elapsed = millis() - buzzerStartTime;
  if (elapsed >= (unsigned long)buzzerDuration)
  {
    noTone(buzzerPin); // Stop the buzzer
    buzzerActive = false;
    return;
  }

  if (millis() - lastFreqUpdateTime >= freqUpdateInterval)
  {
    lastFreqUpdateTime = millis();
    unsigned long posInCycle = elapsed % sweepPeriod;
    int freq = sweepMinFreq + (long)(sweepMaxFreq - sweepMinFreq) * posInCycle / sweepPeriod;
    tone(buzzerPin, freq);
  }
}

void setLight(int r)
{
  analogWrite(rLedPin, r);
}

bool readPIR()
{
  return digitalRead(PIRPin) == HIGH;
}

bool readButton()
{
  return digitalRead(buttonPin) == LOW; // Button is pressed when LOW
}

void updateDisplay(bool lightOn, bool motionDetected, bool systemArmed)
{
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println(F("Luca Security System"));
  display.setCursor(0, 10);
  display.print(F("Light: "));
  display.println(lightOn ? F("ON") : F("OFF"));
  display.setCursor(0, 20);
  display.print(F("Motion: "));
  display.println(motionDetected ? F("DETECTED") : F("NONE"));
  display.setCursor(0, 30);
  display.print(F("Triggered: "));
  display.println(triggeredCount);
  display.setCursor(0, 40);
  display.print(F("System: "));
  display.println(systemArmed ? F("ARMED") : F("DISARMED"));
  display.display();
}

void setup()
{
  pinMode(rLedPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP); // button connected to GND when pressed
  pinMode(PIRPin, INPUT);           // PIR sensor pin
  Serial.begin(115200);

  // Initialize the OLED display. Address 0x3C is common for 128x64 displays.
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
  {
    Serial.println(F("SSD1306 allocation failed. Check connections!"));
  }
}

void loop()
{
  if (readButton())
  {
    if (millis() - lastDebounceTime > debounceDelay)
    {
      systemArmed = !systemArmed; // Toggle system armed state
      lastDebounceTime = millis();
    }
  }

  bool motionDetected = readPIR();
  if (systemArmed && motionDetected)
  {
    setLight(255); // Red light
    if (!buzzerActive)
    {
      startBuzzer(1000); // Buzzer for 1 second, auto-retriggers while motion persists
    }
    if (!lastTriggeredState) // Only increment count on the first detection
    {
      triggeredCount++;
      lastTriggeredState = true;
    }
  }
  else
  {
    setLight(0); // Turn off light
    lastTriggeredState = false; // Reset the triggered state when no motion is detected
  }
  updateDisplay(motionDetected, motionDetected, systemArmed);
  updateBuzzer();
}