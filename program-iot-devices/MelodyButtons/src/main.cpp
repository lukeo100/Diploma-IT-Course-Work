#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1327.h>
#include "songs.h"

// Define pins
const uint8_t LEDS[3] = {13, 14, 16};
const uint8_t button = 4;
const uint8_t button2 = 1;
const uint8_t button3 = 34;
const uint8_t buzzer1 = 37;
const uint8_t buzzer2 = 2; //

// Display setup
#define OLED_SDA 17       // OLED I2C data pin
#define OLED_SCL 18       // OLED I2C clock pin
#define SCREEN_WIDTH 128  // OLED display width, in pixels
#define SCREEN_HEIGHT 128 // OLED display height, in pixels
#define OLED_RESET -1
#define OLED_ADDRESS 0x3D                                                     // I2C address of the OLED display                                             // No reset pin is used
TwoWire I2C_OLED = TwoWire(1);                                                // Use the second ESP32 I2C controller
Adafruit_SSD1327 display(SCREEN_WIDTH, SCREEN_HEIGHT, &I2C_OLED, OLED_RESET); // Create OLED display object
bool displayReady = false;

// Songs setup
struct Song
{
  const char *name;
  const int (*notes)[3];
  size_t length;
};

const Song songs[] = {
    {"Game of Thrones Theme", midi_gameofthrones, ARRAY_LEN(midi_gameofthrones)},
    {"Take  me to the Moon", midi_takeMeToTheMoon, ARRAY_LEN(midi_takeMeToTheMoon)},
    {"Man I need", midi_manINeedSynth, ARRAY_LEN(midi_manINeedSynth)},
    {"Freebird Theme", midi_freebirdMain, ARRAY_LEN(midi_freebirdMain)},
    {"Freebird Secondary", midi_freebirdSecondary, ARRAY_LEN(midi_freebirdSecondary)},
    {"Fein", midi_fein, ARRAY_LEN(midi_fein)},
};

constexpr size_t SONG_COUNT = sizeof(songs) / sizeof(songs[0]);

enum LEDColour
{
  RED = 0,
  GREEN = 1,
  BLUE = 2
};

bool set_light(LEDColour colour, float value)
{
  analogWrite(LEDS[colour], value);
  return true;
}

void random_light()
{
  int randomLight = random(0, (sizeof(LEDS) / sizeof(LEDS[0])));
  set_light(RED, random(0, 30));
  set_light(GREEN, random(0, 30));
  set_light(BLUE, random(0, 30));
  set_light((LEDColour)randomLight, random(100, 255));
}

bool read_button(uint8_t buttonPin)
{
  return !digitalRead(buttonPin);
}

struct MidiPlayer
{
  uint8_t toneChannel;
  const int (*activeNotes)[3] = nullptr;
  size_t activeNotesLength = 0;
  size_t activeNote = 0;
  unsigned long nextMidiEvent = 0;
  bool midiNoteOn = false;

  MidiPlayer(uint8_t channel) : toneChannel(channel) {}
};

MidiPlayer synthPlayer(0);
MidiPlayer drumPlayer(1);

void playMidi(uint8_t buzzerPin, const int notes[][3], size_t len, MidiPlayer &player)
{
  if (!player.midiNoteOn && player.activeNotes == nullptr)
  {
    player.activeNotes = notes;
    player.activeNotesLength = len;
    player.activeNote = 0;
    player.nextMidiEvent = 0;
  }

  if (player.activeNotes == nullptr || player.activeNote >= player.activeNotesLength)
  {
    return;
  }

  unsigned long now = millis();
  if ((long)(now - player.nextMidiEvent) < 0)
  {
    return;
  }

  if (!player.midiNoteOn)
  {
    setToneChannel(player.toneChannel);
    tone(buzzerPin, player.activeNotes[player.activeNote][0]);
    random_light();
    player.nextMidiEvent = now + player.activeNotes[player.activeNote][1];
    player.midiNoteOn = true;
  }
  else
  {
    setToneChannel(player.toneChannel);
    noTone(buzzerPin);
    player.nextMidiEvent = now + player.activeNotes[player.activeNote][2];
    player.activeNote++;
    player.midiNoteOn = false;

    if (player.activeNote >= player.activeNotesLength)
    {
      player.activeNotes = nullptr;
    }
  }
}

void stopMidi(uint8_t buzzerPin, MidiPlayer &player)
{
  setToneChannel(player.toneChannel);
  noTone(buzzerPin);
  player.activeNotes = nullptr;
  player.activeNotesLength = 0;
  player.activeNote = 0;
  player.midiNoteOn = false;
}

void displayMenu(size_t selectedSong)
{
  display.clearDisplay();
  display.setTextColor(SSD1327_WHITE);
  display.setTextSize(1.3);
  display.setCursor(0, 0);
  display.println("Songs:");
  for (size_t i = 0; i < SONG_COUNT; i++)
  {
    display.print(i == selectedSong ? ">" : " ");
    display.print(i + 1);
    display.print(". ");
    display.println(songs[i].name);
  }
  display.display();
}

void setup()
{
  Serial.begin(115200);

  Serial.println("Started");

  pinMode(OLED_SDA, INPUT_PULLUP);
  pinMode(OLED_SCL, INPUT_PULLUP);
  I2C_OLED.begin(OLED_SDA, OLED_SCL, 100000); // Start I2C on custom OLED pins

  if (!display.begin(OLED_ADDRESS))
  {
    Serial.println("SSD1327 not found at 0x3D");
  }
  else
  {
    displayReady = true;
    Serial.println("SSD1327 initialized at 0x3D");
  }

  // Divide total bytes by size of one element to get the actual item count
  for (int i = 0; i < (sizeof(LEDS) / sizeof(LEDS[0])); i++)
  {
    pinMode(LEDS[i], OUTPUT);
  }
  pinMode(button, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);
  pinMode(button3, INPUT);
  pinMode(buzzer1, OUTPUT); // techically the tone() function does this but good practice to put here
  pinMode(buzzer2, OUTPUT);

  displayMenu(0);
}

void loop()
{
  static size_t selectedSong = 0;
  static bool isPlaying = false;
  static bool wasButtonPressed = false;
  static bool wasButton2Pressed = false;
  static bool wasButton3Pressed = false;

  bool buttonPressed = read_button(button);
  bool button2Pressed = read_button(button2);
  bool button3Pressed = read_button(button3);

  if (button2Pressed && !wasButton2Pressed)
  {
    selectedSong = selectedSong == 0 ? SONG_COUNT - 1 : selectedSong - 1;
    displayMenu(selectedSong);
    Serial.print("Selected: ");
    Serial.println(songs[selectedSong].name);
  }

  if (button3Pressed && !wasButton3Pressed)
  {
    selectedSong = (selectedSong + 1) % SONG_COUNT;
    displayMenu(selectedSong);
    Serial.print("Selected: ");
    Serial.println(songs[selectedSong].name);
  }

  if (buttonPressed && !wasButtonPressed)
  {
    isPlaying = !isPlaying;
    if (isPlaying)
    {
      Serial.print("Playing: ");
      Serial.println(songs[selectedSong].name);
    }
    else
    {
      stopMidi(buzzer1, synthPlayer);
      set_light(RED, 0);
      set_light(GREEN, 0);
      set_light(BLUE, 0);
      Serial.println("Stopped");
    }
  }

  if (isPlaying)
  {
    const Song &song = songs[selectedSong];
    playMidi(buzzer1, song.notes, song.length, synthPlayer);
  }

  wasButtonPressed = buttonPressed;
  wasButton2Pressed = button2Pressed;
  wasButton3Pressed = button3Pressed;
}
