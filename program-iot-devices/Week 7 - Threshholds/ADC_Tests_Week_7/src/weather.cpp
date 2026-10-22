// weather.cpp
//
// Why a separate FreeRTOS task?
// An HTTPS request takes 1 to 3 seconds on an ESP32 (most of it is the TLS
// handshake), and much longer when the network is slow. Doing that inside
// loop() would freeze the screen and miss IR presses. A task is a second
// "loop" that FreeRTOS runs alongside the Arduino loop. It is pinned to
// core 0 (the Wi-Fi core); the Arduino loop runs on core 1.
//
// Sharing data safely:
// The task writes the result and loop() reads it. A mutex (lock) makes sure
// loop() never reads half-written data. Only plain numbers cross over; no
// LVGL calls happen in this task, because LVGL is not thread safe.
//
// Failure handling:
// - Wi-Fi down: the task waits and checks again, no request is made.
// - Request fails (timeout, HTTP error, bad JSON, odd value): the old value is
//   kept and marked Stale, and the task retries after WEATHER_RETRY_MS.

#include "weather.h"

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#include "config.h"

// Shared between the task and loop(). Only touched while holding `lock`.
struct WeatherShared {
  bool     haveValue;
  bool     lastAttemptOk;
  float    tempC;
  uint32_t fetchedAtMs;
};
static WeatherShared shared = {false, false, 0.0f, 0};
static SemaphoreHandle_t lock = nullptr;

// One HTTPS request. Returns true and sets tempC on success.
static bool fetchOnce(float &tempC) {
  WiFiClientSecure client;
  // Skips checking the server's certificate. The data is public and harmless,
  // and this avoids storing a root certificate that expires. Do not use this
  // shortcut for anything that sends passwords or controls hardware.
  client.setInsecure();
  client.setHandshakeTimeout(WEATHER_TIMEOUT_MS / 1000);

  HTTPClient http;
  http.setConnectTimeout(WEATHER_TIMEOUT_MS);
  http.setTimeout(WEATHER_TIMEOUT_MS);

  if (!http.begin(client, WEATHER_URL)) {
    Serial.println("Weather: could not start the request");
    return false;
  }

  const int code = http.GET();
  if (code != HTTP_CODE_OK) {
    Serial.printf("Weather: HTTP error %d (%s)\n", code,
                  HTTPClient::errorToString(code).c_str());
    http.end();
    return false;
  }

  const String body = http.getString();
  http.end();

  // The reply looks like:
  // {"latitude":-37.8,...,"current_units":{...},
  //  "current":{"time":"2026-10-21T12:15","interval":900,"temperature_2m":16.4}}
  // The filter tells ArduinoJson to keep only current.temperature_2m.
  JsonDocument filter;
  filter["current"]["temperature_2m"] = true;
  JsonDocument doc;
  const DeserializationError err =
      deserializeJson(doc, body, DeserializationOption::Filter(filter));
  if (err) {
    Serial.printf("Weather: JSON error: %s\n", err.c_str());
    return false;
  }

  JsonVariant t = doc["current"]["temperature_2m"];
  if (!t.is<float>()) {
    Serial.println("Weather: temperature_2m missing from reply");
    return false;
  }
  tempC = t.as<float>();
  if (tempC < -50.0f || tempC > 60.0f) {          // sanity check
    Serial.printf("Weather: ignoring odd value %.1f\n", tempC);
    return false;
  }
  return true;
}

static void weatherTask(void *) {
  vTaskDelay(pdMS_TO_TICKS(2000));   // let Wi-Fi start first

  for (;;) {
    uint32_t waitMs = 2000;          // default: Wi-Fi not up yet, check again soon

    if (WiFi.status() == WL_CONNECTED) {
      float t = 0;
      const bool ok = fetchOnce(t);

      xSemaphoreTake(lock, portMAX_DELAY);
      shared.lastAttemptOk = ok;
      if (ok) {
        shared.haveValue = true;
        shared.tempC = t;
        shared.fetchedAtMs = millis();
      }
      xSemaphoreGive(lock);

      if (ok) Serial.printf("Weather: Melbourne %.1f C\n", t);
      waitMs = ok ? WEATHER_REFRESH_MS : WEATHER_RETRY_MS;
    }

    vTaskDelay(pdMS_TO_TICKS(waitMs));   // sleep; costs no CPU while waiting
  }
}

void weather_begin() {
  lock = xSemaphoreCreateMutex();
  // 12 KB of stack: TLS needs a lot. Priority 1 (low). Core 0.
  xTaskCreatePinnedToCore(weatherTask, "weather", 12 * 1024, nullptr, 1,
                          nullptr, 0);
}

WeatherSnapshot weather_get() {
  WeatherSnapshot s = {WeatherStatus::None, 0.0f, 0};
  if (lock == nullptr) return s;

  xSemaphoreTake(lock, portMAX_DELAY);
  const WeatherShared copy = shared;
  xSemaphoreGive(lock);

  if (!copy.haveValue) return s;
  s.tempC = copy.tempC;
  s.ageMs = millis() - copy.fetchedAtMs;
  const bool tooOld = s.ageMs > 2 * WEATHER_REFRESH_MS;
  s.status = (copy.lastAttemptOk && !tooOld) ? WeatherStatus::Ok
                                             : WeatherStatus::Stale;
  return s;
}
