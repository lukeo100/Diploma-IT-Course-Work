# Week 8 task: rooftop water-tank monitor

The ESP32 reads a tank level from a potentiometer, saves it to Supabase every 15 seconds, and flashes an LED and beeps a buzzer when the tank is low. When Wi-Fi drops it keeps working offline and reconnects by itself. It also runs its own Wi-Fi network, `TankMonitor`, with a web page at http://192.168.4.1, so staff on the roof can check the level without the building's Wi-Fi. As my own extra, the kit's OLED screen has four pages, drawn with LVGL and changed with the IR remote: the current level with a 2-minute chart, two QR codes to reach the web page, and the log.

## First run

1. Copy `include/secrets.example.h` to `include/secrets.h` (a placeholder copy already exists). Fill in your 2.4 GHz Wi-Fi name and password, your Supabase Project URL and your **publishable** key. Never use the `service_role` key. Also set `AP_PASSWORD`, the password for the `TankMonitor` network (8 characters or more). Keeping it to 13 characters or fewer makes the WiFi QR code bigger and easier to scan (see below).
2. Plug the potentiometer into kit port **ADC1**, the LED into **D1**, the buzzer into **D2**, the OLED screen into **I2C1** and the IR receiver into **D3**.
3. Build, upload and open the Serial Monitor (115200).
4. Check **Table Editor → tank_levels** in Supabase for new rows.

`secrets.h` is in `.gitignore`, so your real password and key are never committed. Submit `secrets.example.h`, which already has the required `"YOUR_WIFI_PASSWORD"`, `"YOUR_PROJECT_ID"` and `"YOUR_SUPABASE_PUBLISHABLE_KEY"` placeholders.

## Pins

The board is a **Waveshare ESP32-S3-Pico** on the **Pico Sensor Kit B**. Each kit port is wired to a Raspberry Pi Pico "GP" pin, which I took from Waveshare's own demo code. The ESP32-S3-Pico puts a different GPIO in each Pico position:

| Connection | Kit port | Pico pin | ESP32-S3 GPIO | Constant in `config.h` |
|---|---|---|---|---|
| Potentiometer wiper | ADC1 | GP27 | **GPIO8** (ADC1 channel 7) | `potPin` |
| Alert LED | D1 | GP10 | **GPIO35** | `alertLedPin` |
| Passive buzzer | D2 | GP12 | **GPIO37** | `buzzerPin` |
| OLED screen (my extra) | I2C1 | GP6 / GP7 | **GPIO17** (SDA) / **GPIO18** (SCL) | `oledSdaPin`, `oledSclPin` |
| IR receiver (my extra) | D3 | GP15 | **GPIO40** | `irPin` |

Check: the same mapping gives GPIO40 for the IR receiver and GPIO7 for the LDR, and both of those worked in Week 7.

### About the task's pin rules

The task's pin rules are written for the original ESP32 chip, for example GPIO 32-39 for ADC1 and GPIO 34-39 as input-only. Your board has an **ESP32-S3**, which uses different numbers. The reasons behind each rule still apply, though:

| Rule | Original ESP32 | ESP32-S3 (this board) | This project |
|---|---|---|---|
| Analog input must be on ADC1, because ADC2 stops working with Wi-Fi on | ADC1 = GPIO 32-36, 39 | ADC1 = **GPIO 1-10**, ADC2 = GPIO 11-20 | GPIO8 is ADC1 ✔ |
| Outputs can't use input-only pins | GPIO 34-39 are input-only | No input-only pins | 35 and 37 can drive outputs ✔ |
| Avoid flash/PSRAM pins | GPIO 6-11, 16, 17 | GPIO 26-32 (and 33-37 only on chips with *octal* PSRAM) | Your chip has quad PSRAM, so 35 and 37 are free ✔ |
| Avoid boot-mode (strapping) pins | GPIO 0, 2, 5, 12, 15 | GPIO 0, 3, 45, 46 | Not used ✔ |

## How the program works

### The big idea: never wait

`delay()` freezes the whole program. If `loop()` called `delay(15000)` for the cloud send, the low-level alert couldn't fire for 15 seconds.

Instead, every job remembers when it last ran, and `loop()` checks the clock on every pass:

```cpp
if (millis() - lastSendMs >= SEND_INTERVAL_MS) {
  lastSendMs = millis();
  sendToSupabase(tankLevel, avgLevel);
}
```

`millis()` is the number of milliseconds since power-on. Most passes do nothing and `loop()` runs again straight away, thousands of times a second. When a job's time is up, it runs once and resets its own timer. Each job has its **own** timer, so they never hold each other up:

| Job | Timer | Function |
|---|---|---|
| Read the potentiometer | every 2 s | `readTankLevel()` |
| Flip the LED and buzzer on/off | every 250 ms (only while alerting) | `update_alert()` |
| Insert a row in Supabase | every 15 s | `sendToSupabase()` |
| Check Wi-Fi and retry if down | every 10 s | `maybe_reconnect()` |
| Log Wi-Fi changes | every pass | `checkWiFiState()` |
| Answer web page requests | every pass | `server.handleClient()` |
| Check for an IR remote button | every pass | `remote_poll()` |
| Redraw the OLED screen | every pass (LVGL redraws at most every 50 ms) | `display_update()` |

`millis() - last >= interval` keeps working when `millis()` wraps back to 0 after about 49 days, because unsigned subtraction still gives the right gap.

### setup(): runs once

1. **`connectWiFi()`** sets AP + Station mode (`WIFI_AP_STA`, see below) and calls `WiFi.begin()` to join the building's router. It then checks up to 20 times, 500 ms apart. This is the "bounded blocking retry": it waits, but for 10 seconds at most, and only in `setup()`. It returns `true` or `false`.
2. **`syncTime()`** runs only if Wi-Fi connected. `configTzTime()` asks an internet time server (NTP) for the time and sets Melbourne's time zone. The sync happens in the background, so we wait (up to 10 s) until the clock reads a date after 2023. Before that it still says 1970.
3. **`startAccessPoint()`** starts the `TankMonitor` network and the web server. This runs whether or not the router connected.
4. Takes the first reading and starts all the timers.

`delay()` is fine in `setup()` because nothing else needs to run yet.

### Timestamps: `getTimestamp()` and `logLine()`

Once NTP has set it, the ESP32 keeps its own clock running, even with Wi-Fi off. `getTimestamp()` turns it into text like `2026-10-28 14:05:31`. Every message goes through `logLine()`, which adds that timestamp in front, so no line can be printed without it.

If the board starts with no Wi-Fi, NTP never runs (the task only allows syncing in `setup()`), and lines show `[time not synced]` until the next reset.

### Reading the level: `readTankLevel()`

- `analogRead()` gives 0-4095 (0 V to 3.3 V). `map()` turns that into 0-100 %.
- **Rolling average (extension):** the last 5 readings are kept in an array. Each new reading overwrites the oldest one (`readingIndex` wraps 0,1,2,3,4,0...), and the average is their total ÷ count.
- It then compares the level with `LOW_LEVEL_THRESHOLD` and calls `start_alert()` or `stop_alert()` straight away. So the alert begins at most 2 s after the level drops, not at the next cloud send.

### The alert: `start_alert()`, `update_alert()`, `stop_alert()`

- `start_alert()` sets `alertActive = true` and logs it.
- `update_alert()` runs every pass. While active, it flips `alertOn` every 250 ms: on = LED HIGH + `tone(buzzerPin, 2000)`, off = LED LOW + `noTone(buzzerPin)`.
- `stop_alert()` turns both off when the level recovers.

A passive buzzer has no built-in beeper, so it needs a square wave to make a sound. `tone()` produces one using the ESP32's PWM hardware, which is why we never use `digitalWrite()` on the buzzer.

None of the alert code uses Wi-Fi, so it works exactly the same when the network is down.

### Sending to Supabase: `sendToSupabase()`

1. Checks `WiFi.status() == WL_CONNECTED` **at that moment**. Wi-Fi might have dropped since `setup()`, so the old result can't be trusted. If offline, it logs "skipped" and returns.
2. Opens an HTTPS connection (`WiFiClientSecure`; `setInsecure()` skips certificate checking to keep things simple).
3. POSTs JSON such as `{"level":42,"avg_level":40.6}` to `SUPABASE_URL/rest/v1/tank_levels`, with two headers:
   - `apikey`: your publishable key, which tells Supabase which project and role (`anon`) this is.
   - `Authorization: Bearer <key>`: the same key, as Supabase expects.

   The table's RLS policy lets `anon` **insert** only, so a leaked key can't read or delete your data.
4. Calls **`http.end()` every time**, success or fail, so the connection's memory is freed. Without it the ESP32 eventually runs out of memory.
5. Success only on **201 Created**. Anything else is logged with Supabase's reply, for example `401` for a wrong key. Negative codes mean no reply at all (no internet, timeout).

### Wi-Fi recovery: `maybe_reconnect()` and `checkWiFiState()`

- `maybe_reconnect()` runs every 10 s. If disconnected, it calls `WiFi.begin()` **once** and returns immediately. It never sits in a `while` loop waiting, so the readings and the alert keep running. The next check, 10 s later, tries again if needed.
- Auto-reconnect is turned off (`WiFi.setAutoReconnect(false)`), so every reconnect comes from `maybe_reconnect()` and shows up in the log.
- `checkWiFiState()` (extension) remembers last pass's state in `wasConnected`. It logs only on a **change**: `[OFFLINE]` when the link drops, `[RECOVERED]` when it comes back.

### On-site web page: AP + Station mode (extension)

The ESP32's Wi-Fi radio can do two jobs at the same time:

| Mode | What it does | Here |
|---|---|---|
| **Station** (`STA`) | Joins a router, like a phone does. Gives internet access. | Sends rows to Supabase |
| **Access Point** (`AP`) | *Is* a router: phones join the ESP32's own network. No internet. | Staff open the web page |
| **AP + Station** (`WIFI_AP_STA`) | Both at once | This project |

AP mode on its own wouldn't meet the brief, because with no connection to the building's router there's no internet, so no Supabase and no NTP time. Station mode on its own needs the router to work. With both, the office gets the cloud history, and staff on the roof can still see the level when the router or internet is down.

How the page works:

1. `startAccessPoint()` calls `WiFi.softAP("TankMonitor", AP_PASSWORD)`. The ESP32 gives itself the address **192.168.4.1** on that network and hands out addresses to phones that join.
2. `server.on("/", handleRoot)` says: "when a browser asks for the main page `/`, run `handleRoot()`". `server.begin()` starts listening on port 80 (normal `http://`).
3. `server.handleClient()` runs **every pass of `loop()`**. It checks whether a browser has sent a request. If not, it returns straight away. If so, it calls `handleRoot()`. If it didn't run every pass, the page would load slowly or time out.
4. `handleRoot()` builds the HTML text with the current values (level, average, alert, Wi-Fi state, last cloud send, time) and sends it with code 200 (OK). The level turns red during an alert.
5. The `<meta http-equiv='refresh' content='2'>` tag tells the browser to reload the page every 2 seconds, so it stays up to date without any JavaScript.

To try it: on your phone, join `TankMonitor` and open **http://192.168.4.1** (type the `http://`). Your phone may warn "no internet" on this network; choose to stay connected.

`startAccessPoint()` runs after `connectWiFi()` for a reason. The radio can only be on one channel at a time, so the AP has to use the same channel as the router. Starting it after the router connects puts it on the right channel from the start.

### OLED screen with LVGL (my own extra)

The kit's 1.5" OLED is 128 × 128 pixels with 16 shades of gray (SSD1327 chip). It connects over I2C, a 2-wire bus (data SDA + clock SCL), on the kit's I2C1 port.

The screen has four pages, with a tab bar along the bottom that highlights the current one:

| Page | Shows |
|---|---|
| **Tank** | Current level (big), average, a `LOW!` badge during an alert, Wi-Fi state, 2-minute chart |
| **WiFi** | QR code: scan it to join the `TankMonitor` network |
| **Web** | QR code: scan it to open http://192.168.4.1 |
| **Log** | The newest log lines, with the time |

```
Tank page
+----------------------------+
| Water Tank            WiFi |   title, Wi-Fi state ("offline" when down)
|            63%             |   current level, big
| avg 61.4%            LOW!  |   average; LOW! badge only during an alert
|  ____/\______              |   chart of the last 60 readings (2 minutes)
|  - - - - - - - - - - - -   |   gray line = alert threshold (20 %)
| last 2 min      alert < 20%|
| Tank | WiFi | Web | Log    |   tab bar
+----------------------------+
```

**LVGL** is a graphics library. You create widgets (labels, charts, QR codes) once. After that you only change their values, and LVGL works out what needs redrawing. All the screen code is in `src/display.cpp`. `main.cpp` only calls these functions:

| Function | Called from | What it does |
|---|---|---|
| `display_begin()` | `setup()` | Starts the I2C bus and the OLED, starts LVGL, builds all four pages |
| `display_showReading(level, avg, alert)` | `readTankLevel()`, every 2 s | Sets the label text, shows or hides `LOW!`, adds a chart point |
| `display_setWiFi(online)` | `setup()` and `checkWiFiState()` when Wi-Fi changes | Shows `WiFi` or `offline` |
| `display_setAccessPoint(ssid, password, ip)` | `startAccessPoint()` | Makes the two QR codes |
| `display_addLog(line)` | `logLine()`, for every log line | Adds the line to the Log page |
| `display_nextPage()` / `display_prevPage()` | `loop()`, on a remote button | Changes page |
| `display_showPage(PAGE_TANK)` | `start_alert()` | Jumps to the Tank page when an alert starts, whatever page was showing |
| `display_update()` | every pass of `loop()` | Calls `lv_timer_handler()`, which does the actual drawing |

#### Pages and the IR remote

The pages live in an LVGL **tabview**. It holds the pages side by side and slides the active one onto the screen. The kit's screen isn't a touch screen, so swiping is turned off and the IR remote changes pages instead, just like in Week 7:

- `remote_poll()` (in `src/remote.cpp`) runs every pass of `loop()`. The IRremote library catches the remote's signal in the background. If a full button press has arrived, `remote_poll()` returns its code (e.g. `0x46`), otherwise `-1` straight away. It never waits.
- Held-down buttons (which send "repeat" signals) and presses within 250 ms of the last one are ignored, so one press moves one page.
- `loop()` checks the code against `IR_CMD_NEXT` (`0x46`) and `IR_CMD_PREV` (`0x45`) from `config.h`. Those are the codes your Week 7 remote sent. Any other button is logged as `Remote button 0x..`, so you can copy its code into `config.h` to use it.
- `display_nextPage()` adds 1 to the page number and wraps from the last page (Log) back to the first (Tank), using `% PAGE_COUNT`. `display_prevPage()` goes the other way.

#### The QR codes

A phone has to **join the `TankMonitor` network first**, before `http://192.168.4.1` can load. So there are two QR codes, step 1 and step 2:

1. **WiFi page:** the QR holds `WIFI:T:WPA;S:TankMonitor;P:<password>;;`. Phone cameras recognise this format and offer to join the network, so nobody has to type the password. If the name or password contains `\ ; , : "`, `escapeForWifiQr()` puts a backslash in front of it, because those characters have a special meaning in the format.
2. **Web page:** the QR holds `http://192.168.4.1`. Scanning it opens the page in the browser.

The text for both is built in `display_setAccessPoint()`. It runs after `WiFi.softAP()` succeeds, so the QR codes use the real password and address. LVGL's `lv_qrcode` widget turns the text into black and white squares. The **quiet zone** is a white border around the code that cameras need to find its edges.

Why the password length matters: more text needs a QR code with more squares. The code has to fit in 100 × 100 pixels, and every square must be a whole number of pixels wide. With a password of 13 characters or fewer, each square is 3 pixels wide. With a longer one, the squares drop to 2 pixels and the code is harder to scan. Hold the phone close and keep it steady.

#### The Log page

Every log line already goes through `logLine()`. It now also calls `display_addLog()` with the time only (`14:05:31 Tank level 63% ...`), because the date doesn't fit on the screen.

`display.cpp` keeps the last `LOG_ENTRIES` (8) lines in a **ring buffer**. `nextLog` points at the slot for the next line, and once all 8 slots are full it wraps round and overwrites the oldest. Then `refreshLogLabel()` joins the lines oldest to newest into one label. That label is pinned to the **bottom** of the page, so the newest line is always visible. Long lines wrap, and when there's too much text, the oldest lines go off the top of the page and are cut off.

How a new reading gets onto the screen:

1. `display_showReading()` changes the labels and calls `lv_chart_set_next_value()`. Nothing is drawn yet. LVGL only marks those areas as "dirty" (needing a redraw).
2. On the next `display_update()`, `lv_timer_handler()` sees the dirty areas. It draws them into a small buffer in memory (`drawBuf`, 1 byte of gray per pixel) and calls `flushCb()`.
3. `flushCb()` copies each pixel into the OLED library, turning LVGL's 256 grays into the OLED's 16 (`>> 4` keeps the top 4 bits). Then `oled.display()` sends **only the changed rectangle** over I2C.

The chart:
- **`LV_CHART_UPDATE_MODE_SHIFT`**: each new value goes on the right and the oldest one drops off the left, so it scrolls like a heart-rate monitor.
- It holds `CHART_POINTS` = 60 values. With one reading every 2 s, that's the last 2 minutes.
- The Y axis is fixed at 0-100 %.
- It has two **series** (lines). The gray one is set once to `LOW_LEVEL_THRESHOLD` at every point, so it's a flat line showing where the alert starts. The white one is the tank level. When the white line drops below the gray line, the alarm goes off.

`include/lv_conf.h` holds the LVGL settings: 8-bit grayscale, the fonts (10, 12 and 28 pt), the tabview and QR code widgets, and no theme. The built-in themes are made for colour screens, so every widget is styled white-on-black in `display.cpp`. LVGL's own logging is off, because its messages wouldn't carry a `getTimestamp()` timestamp.

If the OLED isn't plugged in, `display_begin()` returns `false` and the program logs it and carries on. Everything else still works.

`platformio.ini` sets `workspace_dir = C:/pio/tankw8`. LVGL has very deep folders, and inside this repo the build paths would go past Windows' 260-character limit. Builds now go to `C:\pio\tankw8` instead of the project's `.pio` folder.

### What happens when the hotspot goes off

1. `checkWiFiState()` notices the change and logs `[OFFLINE]`.
2. Readings keep logging every 2 s, and the alert still fires if the level is low.
3. Every 15 s, `sendToSupabase()` logs `Cloud send skipped: Wi-Fi offline`, and no rows are added.
4. Every 10 s, `maybe_reconnect()` logs `Wi-Fi down, reconnect attempt...`.
5. The `TankMonitor` web page keeps working and shows "Building Wi-Fi: offline". The OLED shows `offline` and the chart keeps scrolling.
6. The hotspot comes back. The next `WiFi.begin()` connects, `[RECOVERED]` is logged, and the next 15 s send inserts a row again. There is no reset, and timestamps stay correct because the clock kept running.

If the router stays on but the internet drops, Wi-Fi still says "connected", so sends try and fail with a negative code instead of being skipped.

### Limitations to know about

- The HTTPS POST itself blocks for about 1 second (longer if the internet is slow). For that moment the LED/buzzer pattern pauses and the web page waits to load. A beep can last a little longer, but it never stops alerting. Fixing that would mean running the send in a separate FreeRTOS task, which is beyond this task.
- While the building's Wi-Fi is down, each reconnect attempt makes the radio search for the router on other channels. A phone on `TankMonitor` may briefly drop off or load the page slowly every 10 seconds. Raising `RECONNECT_INTERVAL_MS` makes this happen less often, but recovery then takes longer.
- Sending the changed part of the screen over I2C takes time: about 0.1 s every 2 s when the chart moves. The alert beeps are 250 ms long, so you won't notice it. Changing page redraws the whole screen (about 0.2 s).

## Example Serial output

```
[2026-10-28 14:05:29] Access point "TankMonitor" started, page at http://192.168.4.1
[2026-10-28 14:05:31] Tank level 63% (avg 63.0%)
[2026-10-28 14:05:39] Cloud send OK: {"level":63,"avg_level":63.0}
[2026-10-28 14:05:41] Tank level 12% (avg 41.0%)
[2026-10-28 14:05:41] ALERT: tank level LOW (12% < 20%)
[2026-10-28 14:05:44] [OFFLINE] Wi-Fi connection lost
[2026-10-28 14:05:49] Wi-Fi down, reconnect attempt...
[2026-10-28 14:05:54] Cloud send skipped: Wi-Fi offline
[2026-10-28 14:06:11] [RECOVERED] Wi-Fi reconnected, IP 192.168.1.42
```

## Files

| File | Job |
|---|---|
| `include/config.h` | Pins, threshold, intervals, time zone, AP name, remote button codes |
| `include/secrets.example.h` | Template for Wi-Fi, Supabase and AP password (committed) |
| `include/secrets.h` | Your real details (not committed) |
| `include/lv_conf.h` | LVGL settings (grayscale, fonts, no theme) |
| `src/main.cpp` | The main program: Wi-Fi, readings, alert, Supabase, web page |
| `src/display.h` / `src/display.cpp` | The OLED screen: LVGL setup and the four pages (chart, QR codes, log) |
| `src/remote.h` / `src/remote.cpp` | The IR remote: returns the code of each new button press |
