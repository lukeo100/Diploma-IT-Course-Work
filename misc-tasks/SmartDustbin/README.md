# Smart Automatic Dustbin – build pack

Touch-free bin: ESP32-C3 + HC-SR04 + SG90 + two LEDs, built to the robotics-lab brief.

```
SmartDustbin/
├── README.md                     this file
├── firmware/SmartDustbin/        Arduino sketch (open SmartDustbin.ino)
├── cad/
│   ├── stl/01_body.stl           print upright, opening up
│   ├── stl/02_lid.stl            already flipped: top face on the bed
│   ├── stl/03_bay_cover.stl      print flat
│   ├── stl/04_servo_shims_1-1-2-2mm.stl   spacers to line the horn up with the lid
│   ├── stl/assembly_*.stl        previews only, don't print
│   ├── smart_bin.py              parametric model (edit sizes, re-run)
│   ├── check_model.py            fit and lid-swing checks
│   ├── render.py                 makes preview.png
│   └── preview.png
└── test/                         PC simulation of the sketch (12 test cases)
```

## Team roles (two people)

| | **Person A – Hardware & enclosure** | **Person B – Firmware & testing** |
|---|---|---|
| Owns | 3D prints, mechanics, wiring, power | Arduino code, Serial Monitor, test cases, lab write-up of results |
| Step 1 | Start the body print first (longest job), then lid and cover | Install Arduino IDE + ESP32 core; flash the sketch to the bare board; check Serial prints at 115200 |
| Step 2 | Build the ECHO voltage divider (1 kΩ + 2 kΩ) and LED resistors on a small perfboard | Bench test on a breadboard before the bin is ready: sensor + LEDs + servo on the desk |
| Step 3 | Fit sensor, LEDs, DC jack, board in the bay; mount the servo (with shims) and hang the lid | Calibrate the servo with `SERVO_TEST_MODE` **before** the lid goes on: check 0° and 90° really are 90° apart; set `SERVO_MIN_US` / `SERVO_MAX_US` / `SERVO_REVERSED` |
| Step 4 | Route and tie the servo cable through the side clips; tidy wiring | Run the lab test-case table on the finished bin and record results |
| Checks the other's work | Reviews that the code's pins match the wiring | Reviews the wiring against the pin table before first power-on |

**Do together:** first power-on (one person watches the Serial Monitor, the other the lid), the final demo, and the safety check (shared ground, divider fitted, servo on external 5 V).

## Parts

| Qty | Part | Notes |
|---|---|---|
| 1 | ESP32-C3 board | C3 Zero or SuperMini (~18 × 23 mm) |
| 1 | HC-SR04 | |
| 1 | SG90 micro servo | the one in your datasheet; use the single-arm horn and its screws |
| 1 + 1 | 5 mm LED green, 5 mm LED red | + 2 × 220–330 Ω resistors |
| 1 + 1 | 1 kΩ and 2 kΩ resistor | ECHO divider (5 V → 3.3 V) |
| 1 | 5 V 2 A plug pack + 5.5 × 2.1 mm panel jack (DC-022B, 11 mm hole) | powers servo, sensor and ESP32 |
| 1 | 470 µF 10 V capacitor | across servo 5 V / GND, stops brown-outs |
| 2 | M3 × 25 bolt + M3 nyloc nut | hinge pins |
| 2 | M3 × 8 screw (self-tapping or machine screw) | bay cover |
| | Small perfboard, hook-up wire, cable ties, double-sided foam tape | |

## Wiring

| From | To | Notes |
|---|---|---|
| HC-SR04 VCC | 5 V | |
| HC-SR04 TRIG | GPIO 3 | 3.3 V trigger works |
| HC-SR04 ECHO | 1 kΩ → **GPIO 1**, and GPIO 1 → 2 kΩ → GND | **Required**: ECHO is 5 V |
| SG90 brown | GND | |
| SG90 red | 5 V (external supply) | 470 µF across 5 V/GND near the servo |
| SG90 orange | GPIO 5 | |
| Green LED | GPIO 8 → 220 Ω → LED → GND | lid open |
| Red LED | GPIO 6 → 220 Ω → LED → GND | lid closed |
| ESP32 5V pin | 5 V supply | |
| All GNDs | common | |

Notes:
- Don't plug the USB cable in while the 5 V supply is connected unless your board has a diode between USB and its 5 V pin (check the schematic). Otherwise unplug the DC jack to program.
- GPIO 8 is a boot strapping pin on the C3. An LED to GND is fine for normal boot; if the board ever refuses to enter download mode, unplug the LED.

## Printing

Fits a 220 × 220 × 250 mm bed (body is 201 × 168 × 218 mm).

| Part | Orientation | Settings |
|---|---|---|
| Body | upright | PLA/PETG, 0.2 mm layers, 3 walls, 15 % infill, **no supports** (bay floor, hinges and servo shelf all have 45° undersides) |
| Lid | as exported (top on bed) | 2 walls, 3 top/bottom layers, 10–15 % infill, no supports (keep it light) |
| Servo shims | flat | any; print one set |
| Bay cover | flat | 100 % or 4 walls |

Roughly 600 g of filament in total.

## Assembly

1. **Front wall:** push the HC-SR04 transducers through the two holes from inside; the board rests on the two small ledges below (header pins point down between them). A dab of hot glue holds it. Push the LEDs through: green on the left, red on the right.
2. **Right wall (inside the bay):** fit the DC jack in the 11 mm hole. The rounded slot lines up with the ESP32's USB-C port; stick the board to the bay floor with foam tape so the port faces the slot.
3. **Servo:** calibrate it first (see *Servo setup* below), then leave it at 0°. Push the servo through the window in the back-right bracket, shaft towards the bin, and screw its tabs to the bracket with the two SG90 screws. Fit the single-arm horn pointing **forwards** (towards the front of the bin) and fix it with the horn screw. Hold the lid's lug against the horn: if there's a gap, unscrew the servo and put shims between its tabs and the bracket until the horn just touches the lug (the bracket is sized for the tallest servo in the datasheet, so you'll usually need 1–3 mm).
4. **Lid:** slide the lid's hinge knuckles over the two body knuckles and push the M3 × 25 bolts through as pins (nyloc nuts, finger-tight so the lid swings freely). The horn sits in the recess on the lid's right lug; fix it with two small screws through the horn holes or a drop of CA glue. The hole in the middle of the lug gives screwdriver access to the horn screw.
5. **Cable:** run the servo lead from the servo, along the top of the shelf, through the two clips on the right wall and in through the small round port into the bay.
6. **Cover:** screw the bay cover down with the two M3 screws.

## Servo setup (from your SG90 datasheet)

Your datasheet (friendlywire `SG90-datasheet.pdf`) is a compilation of several SG90 listings, and they don't fully agree. What the design and code take from it:

| Datasheet value | Used for |
|---|---|
| Body 22.2 × 11.8 × 31 mm (generic) and 23.1 × 12.2 × 29.0 mm (TowerPro) | Bracket window fits the larger body (23.9 × 13.0 mm). The lid lug is placed for the tallest servo (31 mm + 1 mm margin); shims make up the difference |
| 1.8 kgf·cm stall torque at 4.8 V | Lid made lighter (2.4 mm top, 6 mm skirt). It needs about 0.5–0.7 kgf·cm to lift, roughly 30–37 % of stall, depending on infill |
| 0.1 s per 60° | Opening takes 0.4 s, well within what it can do; closing is slowed to 1.5 s on purpose |
| 4.8 V operating | Run it from the 5 V supply, never the ESP32's 3.3 V pin |
| 20 ms period (50 Hz) | Code uses 50 Hz |
| Pulse 500–2400 µs (TowerPro section) vs ~1–2 ms (generic section) | Code defaults to 500–2400 µs; test it as below |
| Red = +, brown = −, orange = signal | Wiring table |

**Calibrate before fitting the lid**
1. Set `SERVO_TEST_MODE = true` at the top of the sketch and upload.
2. Fit a horn, open Serial Monitor (115200, newline on), type `0`, Enter, then `90`, Enter.
3. The horn should move a quarter turn (90°). If it only moves about 45°, or buzzes at 0°, change to `SERVO_MIN_US = 1000` and `SERVO_MAX_US = 2000`. Fine-tune `SERVO_MIN_US` until `0` is clean and `90` is a true right angle.
4. If it turns the wrong way for opening (see the lid's hinge), set `SERVO_REVERSED = true`.
5. Type `0` to park it closed, set `SERVO_TEST_MODE = false`, upload again.

Print the lid with 2 walls, 3 top/bottom layers and 10–15 % infill to keep it light for the servo.

## Firmware

Open `firmware/SmartDustbin/SmartDustbin.ino` in Arduino IDE.

- Board: *ESP32C3 Dev Module* (or your board's entry), **Tools → USB CDC On Boot → Enabled** so Serial works over USB.
- No extra libraries: the servo uses the ESP32's built-in LEDC PWM (works with ESP32 core 2.x and 3.x).
- Serial Monitor at 115200 baud prints every reading, e.g. `Distance:   18.3 cm   Lid: CLOSED`.

### What it does

| Situation | Response |
|---|---|
| Power on | lid to 0°, red on, green off |
| Every second | measures and prints the distance |
| Hand ≤ 20 cm | lid opens to 90°, green on, red off |
| 20–30 cm while open | stays open (hysteresis) |
| ≥ 30 cm | after 3 consecutive valid readings spanning 3 s, the lid closes slowly; red on |
| No echo (999 cm) | printed as 999; ignored, so one missed echo can't close the lid |
| Only 999 readings for 15 s | lid closes anyway (bin facing an empty room) |
| Anything within 30 cm while closing | reopens immediately (sensor is read every 100 ms during the close) |

The first three rows are the original brief. The rest is the "more robust version" the brief asks for: consecutive clear readings, a closing delay, and reopening on an obstruction. All timings and thresholds are constants at the top of the sketch.

### Lab test cases (verified in the PC simulation)

| Test | Expected | Simulation |
|---|---|---|
| No object | closed, red on | ✅ |
| Hand at 18 cm | opens, green on | ✅ |
| Hand to 25 cm | stays open | ✅ |
| Hand to ≥ 30 cm | closes after 3 s, red on | ✅ |
| Object stays within 20 cm | stays open (60 s tested) | ✅ |
| No echo | prints 999; **does not** close the lid on its own | ✅ (improved) |
| Hand back while closing | reopens | ✅ |

Run it yourself: `cd test && g++ -std=c++17 -I mock test_sketch.cpp -o test_sketch && ./test_sketch`

## Limits worth knowing

- The ultrasonic sensor only sees what's in front of the bin. It won't detect something jammed in the lid's path from above; for that, add a microswitch under the lid or a current sensor on the servo.
- The datasheet doesn't give the shaft position or tab height. The model assumes the usual SG90 values (shaft 6 mm from the end, tabs 15.9 mm up). If your servo differs, measure it and change `SG_SHAFT_FROM_END` / `SG_TAB_S0` / `HORN_FACE_S` in `smart_bin.py`, then re-run it.
