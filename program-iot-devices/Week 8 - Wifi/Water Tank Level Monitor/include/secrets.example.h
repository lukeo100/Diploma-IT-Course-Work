// secrets.example.h
// Template for your Wi-Fi and Supabase details. This file IS committed to git.
//
// 1. Copy this file to include/secrets.h
// 2. Put your real values in secrets.h
// 3. secrets.h is listed in .gitignore, so it never gets committed
//
// The ESP32 only works with 2.4 GHz Wi-Fi networks.
// Use the PUBLISHABLE (anon) key, never the service_role key.

#pragma once

const char* SSID     = "YOUR_WIFI_NAME";
const char* PASSWORD = "YOUR_WIFI_PASSWORD";

const char* SUPABASE_URL = "https://YOUR_PROJECT_ID.supabase.co";
const char* SUPABASE_KEY = "YOUR_SUPABASE_PUBLISHABLE_KEY";

// Password for the device's own network "TankMonitor" (8 characters or more).
const char* AP_PASSWORD = "YOUR_AP_PASSWORD";
