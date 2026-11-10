#!/usr/bin/env python3
"""
Smart Automatic Dustbin – parametric 3D model (body, lid, electronics-bay cover).

Hardware it is sized for:
  ESP32-C3 (Zero / SuperMini / DevKitM), HC-SR04, SG90 micro servo,
  2 x 5 mm LEDs, 5.5 x 2.1 mm DC jack (DC-022B, 11 mm thread).

Layout (X = width, Y = depth with the front at -Y, Z = up, origin at the
centre of the base):
  * Front wall: HC-SR04 holes on the left, green + red LED holes on the right.
  * Electronics bay behind the front wall, under a screw-down cover that
    sits flush with the rim. 45° sloped floor so it prints without supports.
  * Lid hinges at the back on two M3 pin hinges. The SG90 sits outside the
    back-right corner with its shaft on the hinge axis and drives the lid
    directly through its single-arm horn (no linkage to adjust).

Run:  pip install manifold3d trimesh numpy
      python3 smart_bin.py            -> writes STL files to ./stl
"""
import os
import numpy as np
import manifold3d as mf
from manifold3d import Manifold, CrossSection, JoinType

mf.set_circular_segments(64)

# ------------------------------------------------------------------ params
W, D, H = 85.0, 75.0, 105.0      # body outside
R = 10.0                           # outside corner radius
T = 2.4                            # wall
FLOOR = 3.0

AX_Y = D / 2 + 8.0                 # hinge / servo axis
AX_Z = H - 6.0
KR = 5.5                           # knuckle radius
PIN_D = 3.4                        # M3 bolt as hinge pin
HINGES_X = (-W / 2 + 22.0, W / 2 - 30.0)
BODY_KN_W = 10.0
LID_KN_W = 6.0
KN_GAP = 0.4

LID_T = 2.4                        # kept thin: lid weight is the SG90's load
SKIRT_IN = 0.8                     # gap between skirt and body
SKIRT_T = 2.0
SKIRT_H = 6.0

BAY_DEPTH = 34.0                   # clear depth behind the front wall
BAY_FLOOR_Z = H - 52.0
BAY_WALL_Y0 = -D / 2 + T + BAY_DEPTH
BAY_WALL_Y1 = BAY_WALL_Y0 + T
COVER_T = 3.0

SENSOR_X, SENSOR_Z = -30.0, H - 26.0
SENSOR_PITCH, SENSOR_HOLE_D = 26.0, 16.4
LED_GREEN_X, LED_RED_X, LED_D = 24.0, 38.0, 5.2

# SG90 – sized from the team's datasheet (friendlywire SG90-datasheet.pdf):
#   body 22.2 x 11.8 x 31 mm (generic SG90) and 23.1 x 12.2 x 29.0 mm (TowerPro SG90).
#   The bracket window takes the larger body; the lug is placed for the tallest
#   stack (31 mm + 1 mm margin), and printed shims under the tabs close any gap.
SG_LEN, SG_WID, SG_HGT = 23.1, 12.2, 22.7
SG_SHAFT_FROM_END = 6.0
SG_TAB_S0, SG_TAB_S1 = 15.9, 18.4    # tab faces, measured from the servo bottom
SG_TAB_LEN, SG_HOLE_PITCH = 32.2, 27.8
HORN_FACE_S = 32.0                    # outer face of horn, from the servo bottom (worst case)
HORN_T = 1.6
LUG_X0 = W / 2 + SKIRT_IN + 0.4
LUG_X1 = W / 2 + 5.2                  # lug face that the horn sits against
SERVO_BOTTOM_X = LUG_X1 + (HORN_FACE_S - HORN_T)
SG_ZC = AX_Z - (SG_LEN / 2 - SG_SHAFT_FROM_END)
PLATE_X0 = SERVO_BOTTOM_X - SG_TAB_S0
PLATE_X1 = PLATE_X0 + 4.0
SHELF_Z0, SHELF_Z1 = H - 46.0, H - 30.0


# ------------------------------------------------------------------ helpers
def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])


def cyl_x(x0, x1, y, z, r):
    return Manifold.cylinder(x1 - x0, r).rotate([0, 90, 0]).translate([x0, y, z])


def cyl_y(y0, y1, x, z, r):
    return Manifold.cylinder(y1 - y0, r).rotate([-90, 0, 0]).translate([x, y0, z])


def rrect_cs(w, d, r, cy=0.0):
    return (CrossSection.square([w - 2 * r, d - 2 * r], center=True)
            .offset(r, JoinType.Round).translate([0, cy]))


def prism(cs, z0, z1):
    return Manifold.extrude(cs, z1 - z0).translate([0, 0, z0])


def yz_profile(x0, x1, cs):
    """Extrude a 2D shape drawn in (y, z) along X from x0 to x1."""
    m = Manifold.extrude(cs, x1 - x0)          # shape in XY, extruded along +Z
    # map (x, y, z) -> (z + x0, x, y): shape-x becomes Y, shape-y becomes Z
    return m.transform([[0, 0, 1, x0], [1, 0, 0, 0], [0, 1, 0, 0]])


def circle_at(y, z, r):
    return CrossSection.circle(r).translate([y, z])


def union(parts):
    return Manifold.batch_boolean(parts, mf.OpType.Add)


# ------------------------------------------------------------------ body
def make_body():
    outer = prism(rrect_cs(W, D, R), 0, H)
    cavity = prism(rrect_cs(W - 2 * T, D - 2 * T, R - T), FLOOR, H + 1)

    ext = [outer]

    # body hinge knuckles (with 45° support underneath)
    for xh in HINGES_X:
        x0, x1 = xh - BODY_KN_W / 2, xh + BODY_KN_W / 2
        ext.append(Manifold.batch_hull([
            cyl_x(x0, x1, AX_Y, AX_Z, KR),
            box(x0, x1, D / 2 - T, D / 2, AX_Z - KR - 15, H - 0.5)]))

    # servo shelf with sloped underside
    sx0, sx1 = W / 2 - 15, PLATE_X1 + 7
    ext.append(Manifold.batch_hull([
        box(sx0, sx1, D / 2 - T, AX_Y + 10, SHELF_Z0, SHELF_Z1),
        box(sx0, W / 2, D / 2 - T, D / 2, SHELF_Z0 - 22, SHELF_Z0),
        box(W / 2 - T, W / 2, D / 2 - 30, D / 2, SHELF_Z0 - 28, SHELF_Z0)]))

    # servo mounting plate (tabs screw to its -X face)
    plate_top = SG_ZC + SG_TAB_LEN / 2 + 3
    plate = box(PLATE_X0, PLATE_X1, AX_Y - 10, AX_Y + 10, SHELF_Z0, plate_top)
    ext.append(plate)
    for s in (-1, 1):                       # gussets behind the plate
        y0, y1 = sorted((AX_Y + s * 6.8, AX_Y + s * 10))
        ext.append(Manifold.batch_hull([
            box(PLATE_X1 - 0.5, sx1 - 0.5, y0, y1, SHELF_Z1 - 2, SHELF_Z1 + 0.5),
            box(PLATE_X1 - 0.5, PLATE_X1 + 0.4, y0, y1, SHELF_Z1 - 2, H - 2)]))

    # cable clips on the outside of the right wall
    clips = []
    for cy in (-15.0, 25.0):
        clips.append(Manifold.batch_hull([
            box(W / 2 - 1, W / 2 + 6.5, cy - 3, cy + 3, H - 34, H - 24),
            box(W / 2 - 1, W / 2, cy - 3, cy + 3, H - 42, H - 34)]))
    ext += clips

    body = union(ext) - cavity

    # ---- inside the electronics bay (clipped to the body footprint)
    inner = []
    inner.append(box(-W / 2, W / 2, BAY_WALL_Y0, BAY_WALL_Y1, BAY_FLOOR_Z - 2.4, H - COVER_T))
    inner.append(Manifold.batch_hull([                       # 45° floor
        box(-W / 2, W / 2, -D / 2 + 1, -D / 2 + T + 0.1, BAY_FLOOR_Z - BAY_DEPTH - 4, BAY_FLOOR_Z),
        box(-W / 2, W / 2, BAY_WALL_Y1 - 0.1, BAY_WALL_Y1, BAY_FLOOR_Z - 2.4, BAY_FLOOR_Z)]))
    for s in (-1, 1):                                        # cover ledges
        xa, xb = sorted((s * W / 2, s * (W / 2 - T - 3)))
        xc, xd = sorted((s * W / 2, s * (W / 2 - T - 0.1)))
        inner.append(Manifold.batch_hull([
            box(xa, xb, -D / 2 + 12, BAY_WALL_Y0, H - 6, H - COVER_T),
            box(xc, xd, -D / 2 + 12, BAY_WALL_Y0, H - 10, H - COVER_T)]))
    boss_xy = [(-65.0, -D / 2 + T + 4), (65.0, -D / 2 + T + 4)]
    for bx, _ in boss_xy:                                    # cover screw bosses
        inner.append(Manifold.batch_hull([
            box(bx - 4, bx + 4, -D / 2 + 1, -D / 2 + T + 8, H - 14, H - COVER_T),
            box(bx - 4, bx + 4, -D / 2 + 1, -D / 2 + T + 0.1, H - 24, H - 14)]))
    for xa, xb in ((SENSOR_X - 22, SENSOR_X - 12), (SENSOR_X + 12, SENSOR_X + 22)):
        inner.append(Manifold.batch_hull([                   # HC-SR04 rests on these
            box(xa, xb, -D / 2 + 1, -D / 2 + T + 4, SENSOR_Z - 12, SENSOR_Z - 10),
            box(xa, xb, -D / 2 + 1, -D / 2 + T + 0.1, SENSOR_Z - 16, SENSOR_Z - 10)]))
    body = body + (union(inner) ^ outer)

    # ---- holes
    holes = []
    for dx in (-SENSOR_PITCH / 2, SENSOR_PITCH / 2):
        holes.append(cyl_y(-D / 2 - 1, -D / 2 + T + 1, SENSOR_X + dx, SENSOR_Z, SENSOR_HOLE_D / 2))
    for lx in (LED_GREEN_X, LED_RED_X):
        holes.append(cyl_y(-D / 2 - 1, -D / 2 + T + 1, lx, SENSOR_Z, LED_D / 2))
    # right wall: USB-C slot, DC jack, cable port
    usb = CrossSection.square([14 - 6, 12 - 6], center=True).offset(3, JoinType.Round)
    holes.append(yz_profile(W / 2 - T - 1, W / 2 + 1, usb.translate([-D / 2 + 16, H - 44])))
    holes.append(cyl_x(W / 2 - T - 1, W / 2 + 1, -D / 2 + 28, H - 26, 11.2 / 2))
    holes.append(cyl_x(W / 2 - T - 1, W / 2 + 1, -D / 2 + 16, H - 26, 3.5))
    # cable clip tunnels
    for cy in (-15.0, 25.0):
        holes.append(box(W / 2 - 0.01, W / 2 + 4.5, cy - 4, cy + 4, H - 31, H - 26))
    # hinge pins
    for xh in HINGES_X:
        holes.append(cyl_x(xh - 15, xh + 15, AX_Y, AX_Z, PIN_D / 2))
    # cover screw pilots (M3 self-tapping, 2.6 mm)
    for bx, by in boss_xy:
        holes.append(Manifold.cylinder(10.5, 1.3).translate([bx, by, H - COVER_T - 10]))
    # servo window and tab screw pilots (SG90 screws, 1.8 mm)
    holes.append(box(PLATE_X0 - 1, PLATE_X1 + 1, AX_Y - SG_WID / 2 - 0.4, AX_Y + SG_WID / 2 + 0.4,
                     SG_ZC - SG_LEN / 2 - 0.4, SG_ZC + SG_LEN / 2 + 0.4))
    for dz in (-SG_HOLE_PITCH / 2, SG_HOLE_PITCH / 2):
        holes.append(cyl_x(PLATE_X0 - 1, PLATE_X1 + 1, AX_Y, SG_ZC + dz, 0.9))
    return body - union(holes)


# ------------------------------------------------------------------ lid
def make_lid():
    y_back = D / 2 + 0.5
    skirt_out = rrect_cs(W + 2 * (SKIRT_IN + SKIRT_T), D + 2 * (SKIRT_IN + SKIRT_T), R + SKIRT_IN + SKIRT_T)
    skirt_in = rrect_cs(W + 2 * SKIRT_IN, D + 2 * SKIRT_IN, R + SKIRT_IN)
    plate_cs = skirt_out ^ CrossSection.square([2 * W, D + 50]).translate([-W, y_back - D - 50])
    plate = prism(plate_cs, H, H + LID_T)
    skirt = prism(skirt_out - skirt_in, H - SKIRT_H, H + 1.0) ^ box(-W, W, -D, D / 2 - 10, 0, 2 * H)

    parts = [plate, skirt]
    for xh in HINGES_X:
        for s in (-1, 1):
            xa = xh + s * (BODY_KN_W / 2 + KN_GAP)
            x0, x1 = sorted((xa, xa + s * LID_KN_W))
            parts.append(Manifold.batch_hull([
                cyl_x(x0, x1, AX_Y, AX_Z, KR),
                box(x0, x1, D / 2 + 0.6, D / 2 + 3, H, H + LID_T)]))
            parts.append(box(x0, x1, D / 2 - 6, D / 2 + 3, H, H + LID_T))

    # drive lug: takes the SG90 single-arm horn (arm points forward when closed)
    lug_cs = CrossSection.batch_hull([circle_at(AX_Y, AX_Z, 8.0), circle_at(D / 2 - 10, AX_Z, 6.0)])
    parts.append(yz_profile(LUG_X0, LUG_X1, lug_cs))

    lid = union(parts)

    holes = []
    for xh in HINGES_X:
        holes.append(cyl_x(xh - 15, xh + 15, AX_Y, AX_Z, PIN_D / 2 + 0.1))
    horn = CrossSection.batch_hull([circle_at(AX_Y, AX_Z, 4.1), circle_at(AX_Y - 15.5, AX_Z, 2.6)])
    holes.append(yz_profile(LUG_X1 - HORN_T, LUG_X1 + 0.1, horn))
    holes.append(cyl_x(LUG_X0 - 1, LUG_X1 + 1, AX_Y, AX_Z, 2.75))   # screwdriver access
    return lid - union(holes)


# ------------------------------------------------------------------ cover
def make_cover():
    inner = rrect_cs(W - 2 * T, D - 2 * T, R - T).offset(-0.3, JoinType.Round)
    keep = CrossSection.square([W, BAY_WALL_Y1 - 0.3 - (-D / 2)]).translate([-W / 2, -D / 2])
    cover = prism(inner ^ keep, H - COVER_T, H)
    for bx in (-65.0, 65.0):
        cover -= Manifold.cylinder(10, 1.7).translate([bx, -D / 2 + T + 4, H - 5])
        cover -= Manifold.cylinder(1.5, 1.7, 3.2).translate([bx, -D / 2 + T + 4, H - 1.5])  # countersink
    # finger notch
    cover -= Manifold.cylinder(10, 8).translate([0, BAY_WALL_Y1 - 0.3, H - 5])
    return cover


# ------------------------------------------------------------------ servo shims
def make_shim(thickness):
    """Goes between the servo tabs and the bracket to move the horn onto the lid lug."""
    w, l = SG_WID + 2.0, SG_TAB_LEN + 2.0
    shim = CrossSection.square([w, l], center=True) - CrossSection.square(
        [SG_WID + 0.8, SG_LEN + 0.8], center=True)
    for dz in (-SG_HOLE_PITCH / 2, SG_HOLE_PITCH / 2):
        shim -= CrossSection.circle(1.2).translate([0, dz])
    return Manifold.extrude(shim, thickness)


# ------------------------------------------------------------------ servo stand-in (checks/preview)
def make_servo_dummy(with_horn=True):
    xb = SERVO_BOTTOM_X
    parts = [
        box(xb - SG_HGT, xb, AX_Y - SG_WID / 2, AX_Y + SG_WID / 2, SG_ZC - SG_LEN / 2, SG_ZC + SG_LEN / 2),
        box(xb - SG_TAB_S1, xb - SG_TAB_S0, AX_Y - SG_WID / 2, AX_Y + SG_WID / 2,
            SG_ZC - SG_TAB_LEN / 2, SG_ZC + SG_TAB_LEN / 2),
        cyl_x(LUG_X1 + 0.2, xb - SG_HGT, AX_Y, AX_Z, 2.4),
    ]
    if with_horn:
        horn = CrossSection.batch_hull([circle_at(AX_Y, AX_Z, 3.9), circle_at(AX_Y - 15.5, AX_Z, 2.4)])
        parts.append(yz_profile(LUG_X1 - HORN_T, LUG_X1, horn))
    return union(parts)


def rotate_lid(m, deg):
    """Open the lid by `deg` degrees about the hinge axis."""
    return m.translate([0, -AX_Y, -AX_Z]).rotate([-deg, 0, 0]).translate([0, AX_Y, AX_Z])


def to_trimesh(m):
    import trimesh
    mesh = m.to_mesh()
    return trimesh.Trimesh(vertices=np.asarray(mesh.vert_properties)[:, :3],
                           faces=np.asarray(mesh.tri_verts), process=False)


def export(m, path):
    to_trimesh(m).export(path)


def to_bed(m):
    bb = m.bounding_box()
    return m.translate([-(bb[0] + bb[3]) / 2, -(bb[1] + bb[4]) / 2, -bb[2]])


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stl")
    os.makedirs(out, exist_ok=True)
    body, lid, cover = make_body(), make_lid(), make_cover()

    export(to_bed(body), f"{out}/01_body.stl")
    export(to_bed(lid.rotate([180, 0, 0])), f"{out}/02_lid.stl")          # print top-down
    export(to_bed(cover), f"{out}/03_bay_cover.stl")
    shims = union([make_shim(t).translate([i * 18.0, 0, 0]) for i, t in enumerate((1.0, 1.0, 2.0, 2.0))])
    export(to_bed(shims), f"{out}/04_servo_shims_1-1-2-2mm.stl")
    export(union([body, lid, cover]), f"{out}/assembly_closed_preview.stl")
    export(union([body, rotate_lid(lid, 90), cover]), f"{out}/assembly_open_preview.stl")
    for name, m in (("body", body), ("lid", lid), ("cover", cover)):
        bb = m.bounding_box()
        print(f"{name:6s} {m.status()}  size {bb[3]-bb[0]:.1f} x {bb[4]-bb[1]:.1f} x {bb[5]-bb[2]:.1f} mm  "
              f"vol {m.volume()/1000:.0f} cm3  genus {m.genus()}")
    return body, lid, cover


if __name__ == "__main__":
    main()
