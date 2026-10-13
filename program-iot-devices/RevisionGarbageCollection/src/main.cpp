#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_VL53L0X.h>

// put function declarations here:
bool read_button();
bool check_motion();
int get_capacity(int bin);
bool collect_rubbish();
void alarm();


  //////////////////////////
 //       variables      //
//////////////////////////
// button
constexpr u_int8_t buttonPin = 2;
bool buttonReading = false; // updated every tick
bool lastButtonReading = false; // reading from previous tick
bool buttonState = false; // truthful debounced button state

// laser distance sensor
Adafruit_VL53L0X lox = Adafruit_VL53L0X(); // Create an instance of the sensor object
VL53L0X_RangingMeasurementData_t measure; // measure object for laser sensor


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Starting rubbish collection monitoring system..");

  // Initialize the laser distance sensor over I2C
  // Configure the I2C0 pins for Waveshare Kit
  Wire.begin(33, 34); 


  
  // Initialize the sensor passing the Wire reference
  // Parameters: (i2c_address, debug_override, *i2c_bus)
  if (!lox.begin()) {
    Serial.println(F("Failed to boot VL53L0X"));
    while(1);
  }

  // Set pin modes
  pinMode(buttonPin, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  check_motion();
}

// put function definitions here:
bool read_button() {
  buttonReading = digitalRead(buttonPin);
  
  return digitalRead(buttonPin);
}

bool check_motion() {
  Serial.print("Reading distance sensor... ");
  lox.rangingTest(&measure, false); // Pass 'true' to get debug data

  if (measure.RangeMilliMeter < 200) {
    return true; // activated
  } else {
    return false; // no activation
  }
}