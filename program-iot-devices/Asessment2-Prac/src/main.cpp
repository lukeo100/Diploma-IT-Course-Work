/*
  Assessment Task 2
  Electronic Simon Says Memory Game

  Student name: Luca
  Student ID:   200069155
  Date:         14/10/26

  Board: ESP32-S2

  Required libraries:
  - Adafruit GFX Library
  - Adafruit SSD1306

  Instructions:
  1. Complete every numbered TODO.
  2. Keep all runtime timing non-blocking.
  3. Do not use delay() in loop() or its helper functions.
  4. Test all eleven functional requirements.
  5. Complete the Business Requirements & Test Documentation.
  6. Demonstrate the physical circuit to your trainer.

  Verify these pin assignments against your circuit.
  Buttons connect between their GPIO and GND.
  Use a 220 ohm resistor in series with each LED.
*/

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Prevent Arduino automatic prototype errors.
struct ColourMap;
struct GameResult;

ColourMap get_colour(String name);
void log_result(GameResult &result);

// ==================================================
// Pin assignments
// ==================================================

const int NUM_COLOURS = 4;
const int NUM_LEVELS = 3;

const int LED_PINS[NUM_COLOURS] = {};
const int BUTTON_PINS[NUM_COLOURS] = {};

const int POT_PIN = 1;
const int BUZZER_PIN = 21;

const int OLED_SDA_PIN = 8;
const int OLED_SCL_PIN = 9;

// ==================================================
// Constants
// ==================================================

const int MAX_ROUNDS = 20;
const int MAX_GAMES = 10;

const int MAX_TOTAL_PRESSES =
    MAX_ROUNDS * (MAX_ROUNDS + 1) / 2;

const int ADC_MAX = 4095;
const int TONE_LEVEL_STEP = 200;
const int MAX_SAFE_FREQ = 4000;
const int GAME_OVER_FREQ = 100;

const unsigned long DEBOUNCE_TIME = 40;
const unsigned long INPUT_TIMEOUT_MS = 3000;
const unsigned long GAME_OVER_MS = 600;
const unsigned long ALERT_FLASH_MS = 100;
const unsigned long BUTTON_SOUND_MS = 120;
const unsigned long DISPLAY_INTERVAL_MS = 2000;

// Easy, Medium, Hard.
const unsigned long LEVEL_ON_MS[NUM_LEVELS] = {
    400, 300, 200};

const unsigned long LEVEL_GAP_MS[NUM_LEVELS] = {
    200, 160, 140};

// ==================================================
// Structured data
// ==================================================

struct ColourMap
{
    String name;
    int ledPin;
    int toneFreq;
};

ColourMap colourMap[NUM_COLOURS] = {
    {"Red", LED_PINS[0], 262},
    {"Green", LED_PINS[1], 330},
    {"Blue", LED_PINS[2], 392},
    {"Yellow", LED_PINS[3], 494}};

struct GameResult
{
    int session;
    int score;
    float avgReactionMs;
    unsigned long timestamp;
};

GameResult leaderboard[MAX_GAMES];

int gameCount = 0;
int sessionCounter = 0;

int toneGrid[NUM_LEVELS][NUM_COLOURS];

// ==================================================
// Game state and variables
// ==================================================

enum GameState
{
    IDLE,
    PLAYING_SEQUENCE,
    WAITING_FOR_INPUT,
    GAME_OVER_STATE
};

GameState state = IDLE;

int sequence[MAX_ROUNDS];
int round_ = 0;
int completedRounds = 0;
int currentLevel = 0;
int potValue = 0;

unsigned long reactionTimes[MAX_TOTAL_PRESSES];
int totalCorrectPresses = 0;

// Sequence playback.
int playbackStep = 0;
bool ledIsOn = false;

unsigned long playbackTimer = 0;
unsigned long sequenceOnMs = LEVEL_ON_MS[0];
unsigned long sequenceGapMs = LEVEL_GAP_MS[0];

// Player input.
int inputStep = 0;
unsigned long inputWindowStart = 0;
unsigned long stepReadyTime = 0;

// Button debounce.
int buttonState[NUM_COLOURS];
int lastButtonReading[NUM_COLOURS];
unsigned long debounceStart[NUM_COLOURS];
bool buttonPressed[NUM_COLOURS];

// Player LED and sound feedback.
int feedbackColour = -1;
unsigned long feedbackStart = 0;
int activeToneFreq = 0;

// Game-over alert.
bool alertActive = false;
bool alertLedsOn = false;

unsigned long alertStart = 0;
unsigned long alertFlashTimer = 0;

// Latest completed game.
float lastGameAvgReaction = 0.0;
bool lastGameFinished = false;

// OLED.
Adafruit_SSD1306 display(128, 64, &Wire, -1);

bool displayReady = false;
bool displayDirty = true;
unsigned long lastDisplayUpdate = 0;

// ==================================================
// Student programming tasks
// ==================================================

// Finds a colour by name using a linear search.
ColourMap get_colour(String name)
{
    // TODO 1 — Requirement 4
    // Search colourMap one entry at a time.
    // Return the matching entry when its name matches.
    // Keep the sentinel below for an unknown name.
    // Search colourMap one entry at a time.
    for (int i = 0; i < NUM_COLOURS; i++)
    {
        if (colourMap[i].name.equalsIgnoreCase(name))
        {
            return colourMap[i];
        }
    }

    // Sentinel for an unknown name.
    ColourMap notFound = {"", -1, -1};
    return notFound;
}

// Builds the two-dimensional tone-frequency grid.
void build_tone_grid()
{
    // TODO 2a — Requirement 5
    // Use nested loops for difficulty level and colour.
    // Calculate each frequency from the colour's base frequency
    // plus the level-dependent TONE_LEVEL_STEP.
    // Access each cell with toneGrid[level][colour].
    for (int level = 0; level < NUM_LEVELS; level++)
    {
        for (int colour = 0; colour < NUM_COLOURS; colour++)
        {
            toneGrid[level][colour] =
                colourMap[colour].toneFreq + level * TONE_LEVEL_STEP;
        }
    }
}

// Calculates the sum of all tone-grid frequencies.
long sum_all_tones()
{
    long total = 0;

    // TODO 2b — Requirement 5
    // Use nested loops to add every grid cell to total.
    for (int level = 0; level < NUM_LEVELS; level++)
    {
        for (int colour = 0; colour < NUM_COLOURS; colour++)
        {
            total += toneGrid[level][colour];
        }
    }

    return total;
}

// Checks whether any grid frequency exceeds the limit.
bool any_tone_exceeds(int limit)
{
    // TODO 2c — Requirement 5
    // Use nested loops to check every grid cell.
    // Return true when a frequency exceeds limit.
    for (int level = 0; level < NUM_LEVELS; level++)
    {
        for (int colour = 0; colour < NUM_COLOURS; colour++)
        {
            if (toneGrid[level][colour] > limit)
            {
                return true;
            }
        }
    }

    return false;
}

// Adds a result and inserts it into descending score order.
void log_result(GameResult &result)
{
    // TODO 3 — Requirements 1 and 10
    // Guard gameCount so it cannot exceed MAX_GAMES.
    // Add the new record to leaderboard.
    // Use insertion sort to move ONLY the new record into place.
    // Highest score must appear at leaderboard[0].
    // Decide and document what happens when the array is full.
    if (gameCount < MAX_GAMES)
    {
        leaderboard[gameCount] = result;
        gameCount++;

        // Insertion sort to place the new record in the correct position.
        // Move the new result left while its score is higher than the result before it,
        // keeping the leaderboard in descending score order.
        for (int i = gameCount - 1; i > 0 && leaderboard[i].score > leaderboard[i - 1].score; i--)
        {
            GameResult temp = leaderboard[i];
            leaderboard[i] = leaderboard[i - 1];
            leaderboard[i - 1] = temp;
        }
    }
}

// Appends one random colour to the current sequence.
void add_round()
{
    // TODO 4 — Requirement 2
    // Check that round_ is below MAX_ROUNDS.
    // Store a random colour index from 0 to NUM_COLOURS - 1.
    // Increase round_ after storing the new colour.
    if (round_ < MAX_ROUNDS)
    {
        sequence[round_] = random(0, NUM_COLOURS);
        round_++;
    }
}

// Resets the game and begins playback at the selected level.
void start_game(int level)
{
    // TODO 5a — Requirements 2 and 3
    // Set currentLevel to a valid level.
    // Select sequenceOnMs and sequenceGapMs from the timing arrays.
    // Reset round_, completedRounds, inputStep and reaction count.
    // Reset playback and feedback variables.
    // Clear any previous alert.
    // Add the first round.
    // Set playbackTimer to millis().
    // Enter PLAYING_SEQUENCE and set displayDirty.
    // Keep the previous game's average visible until a new result exists.
    currentLevel = level;
    sequenceOnMs = LEVEL_ON_MS[level];
    sequenceGapMs = LEVEL_GAP_MS[level];
    round_ = 0;
    completedRounds = 0;
    inputStep = 0;
    totalCorrectPresses = 0;
    playbackTimer = millis();
    state = PLAYING_SEQUENCE;
    displayDirty = true;
}

// Starts an idle game using any fresh button press.
void check_start_trigger()
{
    // TODO 5b — Requirement 3
    // Return immediately unless state is IDLE.
    // Check all buttonPressed entries.
    // Map the current potValue to levels 0, 1 or 2.
    // Call start_game() once for a fresh press.
    // Set feedbackColour and feedbackStart for a short start beep.
    // Keep difficulty fixed for the rest of that game.
    if (state == IDLE)
    {
        for (int i = 0; i < NUM_COLOURS; i++)
        {
            if (buttonPressed[i])
            {
                int level = map(potValue, 0, ADC_MAX, 0, NUM_LEVELS);
                start_game(level);
                feedbackColour = i;
                feedbackStart = millis();
                break; // Start game on first detected button press
            }
        }
    }
}


// TODO 6 — Requirements 2, 5 and 9
// Use millis(), playbackTimer and ledIsOn.
//
// When a colour is on:
// - Keep it on for sequenceOnMs.
// - Then set ledIsOn false, advance playbackStep and reset the timer.
//
// When a colour is off:
// - Wait for sequenceGapMs without blocking.
// - If more colours remain, set ledIsOn true and reset the timer.
// - Otherwise enter WAITING_FOR_INPUT.
//
// Include the gap AFTER the final colour.
// Initialise inputStep, inputWindowStart and stepReadyTime.
// Clear button events sampled during playback at this transition.
// Mark the display dirty and print "Your turn" to Serial.
// Keep sequence indices within bounds.

// Plays the sequence one step at a time without blocking.
void update_playback()
{
    unsigned long now = millis();

    if (ledIsOn)
    {
        if (now - playbackTimer >= sequenceOnMs)
        {
            ledIsOn = false;
            playbackStep++;
            playbackTimer = now;
        }
        return;
    }

    if (now - playbackTimer >= sequenceGapMs)
    {
        if (playbackStep < round_)
        {
            ledIsOn = true;
            playbackTimer = now;
        }
        else
        {
            state = WAITING_FOR_INPUT;
            inputStep = 0;
            inputWindowStart = now;
            stepReadyTime = now;

            for (int i = 0; i < NUM_COLOURS; i++)
            {
                buttonPressed[i] = false;
            }

            displayDirty = true;
            Serial.println("Your turn");
        }
    }
}

// Calculates reaction-time statistics in one scan.
void compute_stats(
    unsigned long &minOut,
    unsigned long &maxOut,
    float &avgOut)
{
    // Safe placeholder outputs.
    minOut = 0;
    maxOut = 0;
    avgOut = 0.0;

    // TODO 7 — Requirements 7 and 10
    // Handle totalCorrectPresses == 0 first.
    // Otherwise initialise min and max from reactionTimes[0].
    // Find minimum, maximum and sum in ONE loop.
    // Calculate a floating-point average.
    // Write the results into the reference parameters.
}

// Logs the final result and starts a timed alert.
void finish_game()
{
    // TODO 8a — Requirements 1, 6 and 7
    // Call compute_stats().
    // Update lastGameAvgReaction and lastGameFinished.
    // Create a GameResult containing:
    // - A new session number
    // - completedRounds as the score
    // - The average reaction time
    // - millis() as the timestamp
    //
    // Call log_result().
    // Print the score and statistics to Serial.
    // Enter GAME_OVER_STATE.
    // Initialise alertActive, alertStart, alertFlashTimer and alertLedsOn.
    // Clear player feedback and playback LED state.
    // Mark the display dirty.
}

// Matches player presses against the sequence.
void update_input()
{
    // TODO 8b — Requirements 2, 7 and 9
    // End the game if INPUT_TIMEOUT_MS has elapsed without a new answer.
    // Check fresh button presses against sequence[inputStep].
    // A wrong answer calls finish_game() and returns immediately.
    // Decide and document how simultaneous presses are handled.
    //
    // For a correct answer:
    // - Guard the reactionTimes array.
    // - Record millis() - stepReadyTime.
    // - Increase totalCorrectPresses and inputStep.
    // - Reset both input timers.
    // - Set feedbackColour and feedbackStart for LED/tone feedback.
    //
    // After a full correct sequence:
    // - Set completedRounds to round_.
    // - If MAX_ROUNDS is complete, finish the game.
    // - Otherwise add_round() and reset playback for the longer sequence.
    //
    // Keep array indices within bounds.
    // Process one answer per loop iteration.
}

// Flashes the alert LEDs and returns to idle when time expires.
void update_alert()
{
    // TODO 9 — Requirements 6 and 9
    // Return if no alert is active.
    // Toggle alertLedsOn every ALERT_FLASH_MS using millis().
    // After GAME_OVER_MS:
    // - Clear alertActive, alertLedsOn and feedbackColour.
    // - Return to IDLE.
    // - Mark the display dirty.
    //
    // Do not use delay() or a waiting loop.
}

// Applies LED and buzzer output with clear priorities.
void update_outputs()
{
    // TODO 10 — Requirements 2, 5 and 6, plus button feedback
    // Expire feedbackColour after BUTTON_SOUND_MS.
    //
    // Select the required output in this priority order:
    // 1. Game-over alert: all LEDs follow alertLedsOn; use GAME_OVER_FREQ.
    // 2. Active sequence colour: matching LED and
    //    toneGrid[currentLevel][sequence[playbackStep]].
    // 3. Player feedback: matching LED and grid tone.
    // 4. Otherwise: LEDs off and buzzer silent.
    //
    // Change the buzzer only when its desired frequency changes.
    // Use activeToneFreq to remember the current frequency.
    // Use tone() or noTone(); do not block.
    // Keep output control here so button tones cannot overwrite alerts.
}

// ==================================================
// Provided supporting functions
// ==================================================

// Returns true once for a newly debounced button press.
bool read_button_pressed(int index)
{
    int reading = digitalRead(BUTTON_PINS[index]);
    unsigned long now = millis();

    if (reading != lastButtonReading[index])
    {
        debounceStart[index] = now;
    }

    bool pressed = false;

    if (now - debounceStart[index] >= DEBOUNCE_TIME)
    {
        if (reading != buttonState[index])
        {
            buttonState[index] = reading;
            pressed = (reading == LOW);
        }
    }

    lastButtonReading[index] = reading;
    return pressed;
}

// Samples every button and the potentiometer in all states.
void update_controls()
{
    for (int i = 0; i < NUM_COLOURS; i++)
    {
        buttonPressed[i] = read_button_pressed(i);
    }

    potValue = constrain(analogRead(POT_PIN), 0, ADC_MAX);
}

// Displays game information on changes or every two seconds.
void update_display()
{
    if (!displayReady)
    {
        return;
    }

    unsigned long now = millis();

    if (!displayDirty &&
        now - lastDisplayUpdate < DISPLAY_INTERVAL_MS)
    {
        return;
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);

    switch (state)
    {
    case IDLE:
        display.println("Press button to start");
        break;

    case PLAYING_SEQUENCE:
        display.println("Watch...");
        break;

    case WAITING_FOR_INPUT:
        display.println("Your turn!");
        break;

    case GAME_OVER_STATE:
        display.println("Game Over");
        break;
    }

    display.print("Round: ");
    display.println(round_);

    display.print("Level: ");
    display.println(currentLevel + 1);

    // TODO 11 — Requirement 8
    // Show the high score from the sorted leaderboard.
    // Safely handle gameCount == 0.
    // Show the latest completed game's average reaction time in ms
    // only when lastGameFinished is true.

    display.display();

    lastDisplayUpdate = now;
    displayDirty = false;
}

// Initialises pins, button data, tone grid and OLED.
void setup()
{
    Serial.begin(115200);

    for (int i = 0; i < NUM_COLOURS; i++)
    {
        pinMode(LED_PINS[i], OUTPUT);
        digitalWrite(LED_PINS[i], LOW);

        pinMode(BUTTON_PINS[i], INPUT_PULLUP);

        int reading = digitalRead(BUTTON_PINS[i]);

        buttonState[i] = reading;
        lastButtonReading[i] = reading;
        debounceStart[i] = millis();
        buttonPressed[i] = false;
    }

    pinMode(POT_PIN, INPUT);
    pinMode(BUZZER_PIN, OUTPUT);

    analogReadResolution(12);

    build_tone_grid();

    if (any_tone_exceeds(MAX_SAFE_FREQ))
    {
        Serial.println("Warning: tone-frequency limit exceeded.");
    }

    Serial.print("Tone grid sum: ");
    Serial.println(sum_all_tones());

    Wire.begin(OLED_SDA_PIN, OLED_SCL_PIN);

    displayReady = display.begin(
        SSD1306_SWITCHCAPVCC,
        0x3C);

    if (!displayReady)
    {
        Serial.println("OLED initialisation failed.");
    }

    randomSeed(analogRead(POT_PIN));

    Serial.println("Assessment starter loaded.");
    Serial.println("Complete all numbered TODO tasks.");
}

// Services controls, game state, outputs and OLED.
void loop()
{
    update_controls();
    check_start_trigger();

    switch (state)
    {
    case IDLE:
        break;

    case PLAYING_SEQUENCE:
        update_playback();
        break;

    case WAITING_FOR_INPUT:
        update_input();
        break;

    case GAME_OVER_STATE:
        update_alert();
        break;
    }

    update_outputs();
    update_display();

    // TODO 12 — Requirements 9, 10 and 11
    // Review your completed code:
    // - No delay() or blocking timing loops.
    // - Every function has a short purpose comment.
    // - Named constants replace unexplained values.
    // - Explain a reference-parameter function in your documentation.
    //
    // Complete the written deliverables:
    // - Business requirements analysis
    // - Tests and actual results for all eleven requirements
    // - Known limitations
    // - Real-hardware demonstration and trainer observation record
}