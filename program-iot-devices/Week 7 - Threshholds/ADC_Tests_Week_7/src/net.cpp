// net.cpp
//
// Wi-Fi: WiFi.begin() starts connecting in the background and returns at once.
// net_update() only checks WiFi.status(), so it never blocks. If the first
// attempt fails (wrong password, router off), it tries again every
// WIFI_RETRY_MS. Once connected, the ESP32's auto-reconnect handles drop-outs.
//
// Time: configTzTime() sets the Melbourne time zone rule and starts SNTP, which
// runs in the background and syncs the clock from the NTP servers. The TZ rule
// "AEST-10AEDT,M10.1.0,M4.1.0/3" means:
//   AEST-10   standard time is UTC+10 (POSIX writes the sign backwards)
//   AEDT      the daylight saving name (1 hour ahead by default)
//   M10.1.0   daylight saving starts on the 1st Sunday of October (at 2 am)
//   M4.1.0/3  and ends on the 1st Sunday of April at 3 am

#include "net.h"

#include <Arduino.h>
#include <WiFi.h>
#include <string.h>

#include "config.h"

#if __has_include("secrets.h")
#include "secrets.h"
#else
#error "Missing include/secrets.h. Copy include/secrets.example.h to include/secrets.h and fill it in."
#endif

static NetState state = NetState::NoCredentials;
static uint32_t attemptStartMs = 0;
static bool     ntpStarted = false;
static bool     wasConnected = false;

static void startAttempt(uint32_t nowMs) {
  WiFi.disconnect();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  attemptStartMs = nowMs;
  Serial.printf("Wi-Fi: connecting to \"%s\"...\n", WIFI_SSID);
}

void net_begin() {
  if (strcmp(WIFI_SSID, "YOUR_WIFI_NAME") == 0) {
    Serial.println("Wi-Fi: placeholder SSID in secrets.h, Wi-Fi disabled");
    state = NetState::NoCredentials;
    return;
  }
  WiFi.mode(WIFI_STA);          // station (client) only, no access point
  WiFi.persistent(false);       // do not write the credentials to flash every boot
  WiFi.setAutoReconnect(true);  // reconnect by itself if the link drops later
  state = NetState::Connecting;
  startAttempt(millis());
}

void net_update(uint32_t nowMs) {
  if (state == NetState::NoCredentials) return;

  const bool connected = (WiFi.status() == WL_CONNECTED);

  if (connected && !wasConnected) {
    Serial.printf("Wi-Fi: connected, IP %s, signal %d dBm\n",
                  WiFi.localIP().toString().c_str(), WiFi.RSSI());
    if (!ntpStarted) {
      configTzTime(TZ_MELBOURNE, NTP_SERVER_1, NTP_SERVER_2, NTP_SERVER_3);
      ntpStarted = true;
      Serial.println("Time: NTP started (Melbourne time zone)");
    }
  } else if (!connected && wasConnected) {
    Serial.println("Wi-Fi: connection lost, reconnecting...");
    attemptStartMs = nowMs;
  }
  wasConnected = connected;
  state = connected ? NetState::Connected : NetState::Connecting;

  // Still not connected after WIFI_RETRY_MS: start a fresh attempt.
  if (!connected && nowMs - attemptStartMs >= WIFI_RETRY_MS) {
    startAttempt(nowMs);
  }
}

NetState net_state() {
  return state;
}

bool net_timeSynced() {
  // Any time after 14 Nov 2023 means NTP has set the clock.
  return time(nullptr) > 1700000000;
}

bool net_localTime(struct tm &out) {
  if (!net_timeSynced()) return false;
  const time_t now = time(nullptr);
  localtime_r(&now, &out);   // applies the TZ rule set by configTzTime()
  return true;
}
