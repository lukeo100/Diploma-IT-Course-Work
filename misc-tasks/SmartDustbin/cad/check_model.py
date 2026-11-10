#!/usr/bin/env python3
"""Fit and motion checks for smart_bin.py, plus preview renders."""
import sys
import numpy as np
import smart_bin as sb
from manifold3d import Manifold

body, lid, cover = sb.make_body(), sb.make_lid(), sb.make_cover()
servo = sb.make_servo_dummy(with_horn=False)
servo_horn = sb.make_servo_dummy(with_horn=True)
fails = 0


def check(ok, msg):
    global fails
    print(("PASS " if ok else "FAIL ") + msg)
    fails += 0 if ok else 1


# 1. lid swing 0..95° never hits the body, cover or servo
worst = 0.0
for deg in np.arange(0, 96, 2.5):
    l = sb.rotate_lid(lid, deg)
    v = max((l ^ body).volume(), (l ^ cover).volume(), (l ^ servo).volume())
    worst = max(worst, v)
    if v > 0.5:
        print(f"   overlap {v:.2f} mm3 at {deg}°")
check(worst <= 0.5, f"lid swings 0–95° clear of body, cover and servo (worst overlap {worst:.3f} mm3)")

# 2. servo (with horn) fits the body bracket and the horn sits in the lid recess
check((servo_horn ^ body).volume() < 0.01, "servo + horn clear of the body")
check((servo_horn ^ lid).volume() < 0.01, "horn seats in the lid recess without overlap")
check((cover ^ body).volume() < 0.01, "bay cover fits the opening")

# 3. clearances
gap = lid.min_gap(body, 3.0)
check(gap >= 0.3 or gap == 0, f"closed lid to body min gap {gap:.2f} mm (0 = resting on rim)")
check(servo.min_gap(sb.rotate_lid(lid, 0), 5) >= 0.5, f"servo to lid min gap {servo.min_gap(lid, 5):.2f} mm")

# 4. print size (220 x 220 x 250 bed)
for name, m in (("body", body), ("lid", lid), ("cover", cover)):
    bb = m.bounding_box()
    s = sorted([bb[3] - bb[0], bb[4] - bb[1]]) + [bb[5] - bb[2]]
    check(s[0] <= 220 and s[1] <= 220 and s[2] <= 250, f"{name} fits a 220 x 220 x 250 bed ({s[0]:.0f} x {s[1]:.0f} x {s[2]:.0f})")

# 5. sensor/LED holes actually go through the front wall
for x in (sb.SENSOR_X - 13, sb.SENSOR_X + 13, sb.LED_GREEN_X, sb.LED_RED_X):
    probe = Manifold.cube([1, 6, 1]).translate([x - 0.5, -sb.D / 2 - 1, sb.SENSOR_Z - 0.5])
    check((probe ^ body).volume() < 1e-6, f"front hole open at x={x:.0f}")

# 6. open angle reaches past vertical without the lid hitting anything
lid_open = sb.rotate_lid(lid, 90)
bb = lid_open.bounding_box()
check(bb[4] < sb.AX_Y + 15, f"open lid stays within {bb[4]-sb.D/2:.0f} mm behind the bin")

print(f"\nbody genus {body.genus()}, lid genus {lid.genus()}")

# ---- renders
if "--render" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    def draw(ax, m, colour, alpha=1.0):
        mesh = m.to_mesh()
        v = np.asarray(mesh.vert_properties)[:, :3]
        f = np.asarray(mesh.tri_verts)
        tris = v[f]
        n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
        light = np.array([-0.4, -0.7, 0.6]); light /= np.linalg.norm(light)
        shade = 0.35 + 0.65 * np.clip(n @ light, 0, 1)
        base = np.array(matplotlib.colors.to_rgb(colour))
        cols = np.clip(base[None, :] * shade[:, None], 0, 1)
        pc = Poly3DCollection(tris, facecolors=cols, edgecolors="none", alpha=alpha)
        ax.add_collection3d(pc)

    views = [("closed – front", 0, -60, 25), ("open – front", 90, -60, 25),
             ("open – back right", 90, 35, 25), ("closed – back right", 0, 35, 15)]
    fig = plt.figure(figsize=(16, 12))
    for i, (title, deg, az, el) in enumerate(views):
        ax = fig.add_subplot(2, 2, i + 1, projection="3d")
        draw(ax, body, "#2b2f36")
        draw(ax, cover, "#3a404a")
        draw(ax, sb.rotate_lid(lid, deg), "#4a5260")
        draw(ax, servo_horn if deg == 0 else servo, "#2a5bd7")
        ax.set_xlim(-110, 110); ax.set_ylim(-110, 110); ax.set_zlim(0, 300)
        ax.set_box_aspect((1, 1, 300 / 220))
        ax.view_init(elev=el, azim=az)
        ax.set_axis_off(); ax.set_title(title, fontsize=14)
    plt.tight_layout()
    plt.savefig("preview.png", dpi=110)
    print("wrote preview.png")

sys.exit(1 if fails else 0)
