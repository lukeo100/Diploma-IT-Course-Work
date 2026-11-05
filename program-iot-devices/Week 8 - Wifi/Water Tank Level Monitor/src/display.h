// display.h
// The kit's 1.5 inch OLED screen, drawn with LVGL. Four pages, chosen with
// the tabs along the bottom (the IR remote moves between them):
//
//   Tank  current level, average, LOW! badge and a 2-minute chart
//   WiFi  QR code: scan to join the device's own network "TankMonitor"
//   Web   QR code: scan to open the web page http://192.168.4.1
//   Log   the most recent log lines
//
//   +----------------------------+
//   | Water Tank            WiFi |
//   |            63%             |
//   | avg 61.4%            LOW!  |
//   |  ____/\______    chart     |
//   | last 2 min       alert<20% |
//   |  Tank | WiFi | Web | Log   |   <- tab bar, current page highlighted
//   +----------------------------+

#pragma once

// The pages, in tab order.
enum Page { PAGE_TANK, PAGE_WIFI_QR, PAGE_WEB_QR, PAGE_LOG, PAGE_COUNT };

// Starts the OLED and LVGL and builds the pages. Call once from setup().
// Returns false if the OLED did not answer (the program still runs without it).
bool display_begin();

// Shows a new reading: updates the labels and adds a point to the chart.
void display_showReading(int level, float average, bool alert);

// Shows "WiFi" or "offline" in the top-right corner of the Tank page.
void display_setWiFi(bool online);

// Makes the two QR codes from the access point's name, password and address.
void display_setAccessPoint(const char* ssid, const char* password, const char* ip);

// Adds a line to the Log page (the newest line goes at the bottom).
void display_addLog(const char* line);

// Page changes.
void display_showPage(Page page);
void display_nextPage();
void display_prevPage();

// Lets LVGL redraw whatever changed. Call on every pass of loop().
void display_update();
