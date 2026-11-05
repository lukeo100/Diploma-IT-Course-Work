// main.cpp
// Rooftop water-tank monitor.
//
// - Reads the tank level (potentiometer) every 2 seconds.
// - Inserts a row in the Supabase table tank_levels every 15 seconds.
// - Beeps the buzzer and flashes the LED while the level is below
//   LOW_LEVEL_THRESHOLD, even when Wi-Fi is down.
// - Reconnects to Wi-Fi by itself if the connection drops.
// - Runs its own Wi-Fi network "TankMonitor" with a web page at
//   http://192.168.4.1, so on-site staff can see the level with no router.
// - Shows four pages on the kit's OLED (see display.cpp): the level and a
//   2-minute chart, two QR codes for the web page, and the log. The IR
//   remote changes the page (see remote.cpp).
//
// loop() never waits. Each job has its own "last time I ran" variable and
// only runs when enough time has passed (the millis() pattern):
//
//   if (millis() - lastRunMs >= INTERVAL_MS) { lastRunMs = millis(); doTheJob(); }

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include <time.h>

#include "config.h"
#include "display.h"
#include "remote.h"

#if __has_include("secrets.h")
#include "secrets.h"
#else
#error "Missing include/secrets.h. Copy include/secrets.example.h to include/secrets.h and fill it in."
#endif

// ---------------- State ----------------
int   tankLevel = 0;          // latest reading, 0-100 %
float avgLevel  = 0;          // rolling average of the last AVG_WINDOW readings

int readings[AVG_WINDOW];     // the last few readings, for the average
int readingIndex = 0;         // where the next reading goes in the array
int readingCount = 0;         // how many slots are filled (up to AVG_WINDOW)

bool alertActive = false;     // true while the level is below the threshold
bool alertOn     = false;     // true during the "beep" half of the on/off pattern

bool wasConnected = false;    // Wi-Fi state on the previous pass of loop()

String lastCloudStatus = "not sent yet";   // shown on the web page

WebServer server(80);         // the on-site web page (port 80 = normal http://)

unsigned long lastReadMs      = 0;
unsigned long lastSendMs      = 0;
unsigned long lastReconnectMs = 0;
unsigned long lastAlertMs     = 0;

// ---------------- Time and logging ----------------

// Real date and time from the internet (NTP), e.g. "2026-10-28 14:05:31".
String getTimestamp() {
  time_t now = time(nullptr);
  if (now < 1700000000) {        // clock still near 1970: NTP has not synced
    return "time not synced";
  }
  struct tm local;
  localtime_r(&now, &local);     // convert to Melbourne time (TIME_ZONE)
  char text[20];
  strftime(text, sizeof(text), "%Y-%m-%d %H:%M:%S", &local);
  return String(text);
}

// Every Serial line goes through here, so every line gets a timestamp.
// The same line also goes to the screen's Log page, with the time only
// (there is no room for the date on a 128-pixel screen).
void logLine(const String& message) {
  String stamp = getTimestamp();
  Serial.println("[" + stamp + "] " + message);

  String timeOnly = (stamp.length() == 19) ? stamp.substring(11) : "--:--:--";   // "14:05:31"
  display_addLog((timeOnly + " " + message).c_str());
}

// ---------------- Wi-Fi ----------------

// Called once from setup(). Blocks for at most WIFI_CONNECT_TRIES x 500 ms.
bool connectWiFi() {
  WiFi.mode(WIFI_AP_STA);           // Station (join the building's router) + Access Point (own network)
  WiFi.setAutoReconnect(false);    // maybe_reconnect() handles drop-outs, so they show in the log
  WiFi.begin(SSID, PASSWORD);
  logLine("Connecting to Wi-Fi \"" + String(SSID) + "\"...");

  for (int i = 0; i < WIFI_CONNECT_TRIES && WiFi.status() != WL_CONNECTED; i++) {
    delay(500);                     // OK here: setup() runs once, before loop() starts
  }

  if (WiFi.status() == WL_CONNECTED) {
    logLine("Wi-Fi connected, IP " + WiFi.localIP().toString());
    return true;
  }
  logLine("Wi-Fi connection failed, carrying on offline (maybe_reconnect() will keep trying)");
  return false;
}

// Called once from setup(), only if Wi-Fi connected.
void syncTime() {
  configTzTime(TIME_ZONE, NTP_SERVER_1, NTP_SERVER_2);   // start NTP in the background

  // Wait (at most 10 s) until the clock has really been set.
  for (int i = 0; i < NTP_SYNC_TRIES && time(nullptr) < 1700000000; i++) {
    delay(500);
  }
  logLine(time(nullptr) >= 1700000000 ? "Time synced from NTP" : "NTP sync timed out");
}

// Runs every pass of loop(), but only does anything every RECONNECT_INTERVAL_MS.
// It calls WiFi.begin() once and returns straight away. It never waits for the
// result: the next check, 10 seconds later, sees whether it worked.
void maybe_reconnect() {
  if (millis() - lastReconnectMs < RECONNECT_INTERVAL_MS) return;
  lastReconnectMs = millis();

  if (WiFi.status() == WL_CONNECTED) return;

  logLine("Wi-Fi down, reconnect attempt...");
  WiFi.disconnect();                // cancel any half-finished attempt
  WiFi.begin(SSID, PASSWORD);
}

// Compares this pass's Wi-Fi state with the last pass, so each change is
// logged once instead of on every pass.
void checkWiFiState() {
  bool connected = (WiFi.status() == WL_CONNECTED);

  if (connected && !wasConnected) {
    logLine("[RECOVERED] Wi-Fi reconnected, IP " + WiFi.localIP().toString());
  } else if (!connected && wasConnected) {
    logLine("[OFFLINE] Wi-Fi connection lost");
  }
  if (connected != wasConnected) display_setWiFi(connected);
  wasConnected = connected;
}

// ---------------- Supabase ----------------

// Inserts one row in tank_levels. Returns true only on HTTP 201 (Created).
bool sendToSupabase(int level, float average) {
  // Check again right now: Wi-Fi may have dropped since the last check.
  if (WiFi.status() != WL_CONNECTED) {
    logLine("Cloud send skipped: Wi-Fi offline");
    lastCloudStatus = "skipped, Wi-Fi offline (" + getTimestamp() + ")";
    return false;
  }

  WiFiClientSecure client;
  client.setInsecure();             // HTTPS without checking the certificate (fine for this course)

  HTTPClient http;
  http.begin(client, String(SUPABASE_URL) + "/rest/v1/tank_levels");
  http.addHeader("Content-Type", "application/json");
  http.addHeader("apikey", SUPABASE_KEY);
  http.addHeader("Authorization", String("Bearer ") + SUPABASE_KEY);

  String body = "{\"level\":" + String(level) + ",\"avg_level\":" + String(average, 1) + "}";
  int code = http.POST(body);
  // A negative code means the request never got a reply (no internet, timeout).
  // A positive code is Supabase's answer, and its reply text explains any error.
  String reply = (code > 0) ? http.getString() : HTTPClient::errorToString(code);
  http.end();                       // always free the connection, success or not

  if (code == 201) {
    logLine("Cloud send OK: " + body);
    lastCloudStatus = "OK (" + getTimestamp() + ")";
    return true;
  }
  logLine("Cloud send FAILED, code " + String(code) + ": " + reply);
  lastCloudStatus = "FAILED, code " + String(code) + " (" + getTimestamp() + ")";
  return false;
}

// ---------------- On-site web page (Access Point) ----------------

// Builds the page each time a browser asks for "/". The <meta refresh> tag
// makes the browser ask again every PAGE_REFRESH_S seconds, so the numbers
// stay current without any JavaScript.
void handleRoot() {
  String colour = alertActive ? "#c62828" : "#2e7d32";   // red when low, green when OK
  String status = alertActive ? "LOW LEVEL ALERT" : "Level OK";
  String wifi   = (WiFi.status() == WL_CONNECTED) ? "connected" : "offline";

  String html = "<!DOCTYPE html><html><head><meta charset='utf-8'>";
  html += "<meta name='viewport' content='width=device-width, initial-scale=1'>";
  html += "<meta http-equiv='refresh' content='" + String(PAGE_REFRESH_S) + "'>";
  html += "<title>Tank Monitor</title>";
  html += "<style>body{font-family:sans-serif;text-align:center;margin:24px}";
  html += ".level{font-size:72px;font-weight:bold;color:" + colour + "}</style></head><body>";
  html += "<h1>Rooftop Water Tank</h1>";
  html += "<div class='level'>" + String(tankLevel) + "%</div>";
  html += "<h2 style='color:" + colour + "'>" + status + "</h2>";
  html += "<p>Average of last " + String(AVG_WINDOW) + " readings: " + String(avgLevel, 1) + "%</p>";
  html += "<p>Alert below: " + String(LOW_LEVEL_THRESHOLD) + "%</p>";
  html += "<p>Building Wi-Fi: " + wifi + "</p>";
  html += "<p>Last cloud send: " + lastCloudStatus + "</p>";
  html += "<p>Updated: " + getTimestamp() + "</p>";
  html += "</body></html>";

  server.send(200, "text/html", html);
}

// Called once from setup(), after connectWiFi() has put the radio in
// WIFI_AP_STA mode.
void startAccessPoint() {
  if (WiFi.softAP(AP_SSID, AP_PASSWORD)) {
    logLine("Access point \"" + String(AP_SSID) + "\" started, page at http://" + WiFi.softAPIP().toString());
    display_setAccessPoint(AP_SSID, AP_PASSWORD, WiFi.softAPIP().toString().c_str());   // the QR codes
  } else {
    logLine("Access point FAILED to start (is AP_PASSWORD 8+ characters?)");
  }
  server.on("/", handleRoot);       // when a browser asks for "/", run handleRoot()
  server.begin();
}

// ---------------- Low-level alert (LED + buzzer) ----------------

void start_alert() {
  alertActive = true;
  alertOn = false;
  lastAlertMs = millis() - ALERT_TOGGLE_MS;   // so update_alert() beeps on its very next pass
  display_showPage(PAGE_TANK);                // whatever page is showing, jump to the level
  logLine("ALERT: tank level LOW (" + String(tankLevel) + "% < " + String(LOW_LEVEL_THRESHOLD) + "%)");
}

void stop_alert() {
  alertActive = false;
  alertOn = false;
  digitalWrite(alertLedPin, LOW);
  noTone(buzzerPin);
  logLine("Alert cleared: tank level back to " + String(tankLevel) + "%");
}

// Runs every pass of loop(). Every ALERT_TOGGLE_MS it flips the LED and the
// buzzer together: on (LED lit + tone) / off (LED dark + silence).
void update_alert() {
  if (!alertActive) return;
  if (millis() - lastAlertMs < ALERT_TOGGLE_MS) return;
  lastAlertMs = millis();

  alertOn = !alertOn;
  digitalWrite(alertLedPin, alertOn ? HIGH : LOW);
  if (alertOn) {
    tone(buzzerPin, ALERT_TONE_HZ);
  } else {
    noTone(buzzerPin);
  }
}

// ---------------- Tank level ----------------

void readTankLevel() {
  int raw = analogRead(potPin);              // 0 (0 V) to 4095 (3.3 V)
  tankLevel = map(raw, 0, 4095, 0, 100);     // convert to 0-100 %

  // Rolling average: overwrite the oldest of the last AVG_WINDOW readings.
  readings[readingIndex] = tankLevel;
  readingIndex = (readingIndex + 1) % AVG_WINDOW;
  if (readingCount < AVG_WINDOW) readingCount++;

  int total = 0;
  for (int i = 0; i < readingCount; i++) total += readings[i];
  avgLevel = (float)total / readingCount;

  logLine("Tank level " + String(tankLevel) + "% (avg " + String(avgLevel, 1) + "%)");

  // Start or stop the alert straight away, without waiting for the cloud send.
  bool low = tankLevel < LOW_LEVEL_THRESHOLD;
  if (low && !alertActive) start_alert();
  if (!low && alertActive) stop_alert();

  display_showReading(tankLevel, avgLevel, alertActive);   // labels + new chart point
}

// ---------------- setup() and loop() ----------------

void setup() {
  Serial.begin(115200);
  delay(1500);                     // give the USB Serial Monitor time to connect

  pinMode(alertLedPin, OUTPUT);
  digitalWrite(alertLedPin, LOW);
  analogReadResolution(12);        // 0-4095

#if defined(ESP_ARDUINO_VERSION_MAJOR) && ESP_ARDUINO_VERSION_MAJOR < 3
  // Core 2.x quirk: the first tone() prints "LEDC is not initialized" unless
  // the PWM channel it uses (0) has been set up first.
  ledcSetup(0, 1000, 10);
#endif

  if (display_begin()) {
    logLine("OLED screen started");
  } else {
    logLine("OLED screen not found (check it is in kit port I2C1), carrying on without it");
  }
  remote_begin();

  bool online = connectWiFi();
  if (online) syncTime();          // NTP only works with a connection
  wasConnected = online;
  display_setWiFi(online);
  startAccessPoint();              // after connectWiFi(), so the AP shares the router's channel

  readTankLevel();                 // first reading now, so there is a value to send
  lastReadMs = millis();
  lastSendMs = millis();
  lastReconnectMs = millis();
}

void loop() {
  // 1. Read the tank level every READ_INTERVAL_MS (this also starts/stops the alert).
  if (millis() - lastReadMs >= READ_INTERVAL_MS) {
    lastReadMs = millis();
    readTankLevel();
  }

  // 2. Keep the alert beeping on its own timer. Works with or without Wi-Fi.
  update_alert();

  // 3. Send to Supabase every SEND_INTERVAL_MS.
  if (millis() - lastSendMs >= SEND_INTERVAL_MS) {
    lastSendMs = millis();
    sendToSupabase(tankLevel, avgLevel);
  }

  // 4. Watch the Wi-Fi connection and reconnect if it drops.
  checkWiFiState();
  maybe_reconnect();

  // 5. Answer any browser asking for the web page. Must run every pass.
  server.handleClient();

  // 6. Change the screen's page when a remote button is pressed.
  int button = remote_poll();
  if (button == IR_CMD_NEXT) {
    display_nextPage();
  } else if (button == IR_CMD_PREV) {
    display_prevPage();
  } else if (button >= 0) {
    logLine("Remote button 0x" + String(button, HEX) + " (not used, see IR_CMD_ in config.h)");
  }

  // 7. Redraw anything that changed on the OLED screen.
  display_update();
}
