#!/usr/bin/env python3
"""Small z-buffer renderer for preview images (no OpenGL needed)."""
import numpy as np
from PIL import Image, ImageDraw
import smart_bin as sb


def mesh_arrays(m, colour):
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3].astype(float)
    f = np.asarray(mesh.tri_verts)
    return v, f, np.array(colour, float)


def render(objs, az, el, size=(900, 900), scale=2.2, centre=(0, 20, 150)):
    a, e = np.radians(az), np.radians(el)
    # camera basis
    fwd = np.array([np.cos(e) * np.sin(a), -np.cos(e) * np.cos(a), np.sin(e)])  # towards the camera
    right = np.array([np.cos(a), np.sin(a), 0.0])
    up = np.cross(fwd, right)
    light = 0.6 * fwd + 0.5 * up - 0.3 * right
    light /= np.linalg.norm(light)
    W, H = size
    zbuf = np.full((H, W), -np.inf)
    img = np.ones((H, W, 3)) * 0.97
    c = np.array(centre, float)
    for v, f, col in objs:
        p = v - c
        sx = p @ right * scale + W / 2
        sy = -(p @ up) * scale + H / 2
        sz = p @ fwd
        tri = v[f]
        n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        lam = 0.28 + 0.72 * np.abs(n @ light)
        for t in range(len(f)):
            i0, i1, i2 = f[t]
            x = np.array([sx[i0], sx[i1], sx[i2]]); y = np.array([sy[i0], sy[i1], sy[i2]])
            z = np.array([sz[i0], sz[i1], sz[i2]])
            x0, x1 = int(max(np.floor(x.min()), 0)), int(min(np.ceil(x.max()), W - 1))
            y0, y1 = int(max(np.floor(y.min()), 0)), int(min(np.ceil(y.max()), H - 1))
            if x1 < x0 or y1 < y0:
                continue
            den = (y[1] - y[2]) * (x[0] - x[2]) + (x[2] - x[1]) * (y[0] - y[2])
            if abs(den) < 1e-9:
                continue
            gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            w0 = ((y[1] - y[2]) * (gx - x[2]) + (x[2] - x[1]) * (gy - y[2])) / den
            w1 = ((y[2] - y[0]) * (gx - x[2]) + (x[0] - x[2]) * (gy - y[2])) / den
            w2 = 1 - w0 - w1
            inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
            if not inside.any():
                continue
            depth = w0 * z[0] + w1 * z[1] + w2 * z[2]
            sub = zbuf[y0:y1 + 1, x0:x1 + 1]
            upd = inside & (depth > sub)
            sub[upd] = depth[upd]
            img[y0:y1 + 1, x0:x1 + 1][upd] = np.clip(col * lam[t], 0, 1)
    return Image.fromarray((img * 255).astype(np.uint8))


def main():
    body, lid, cover = sb.make_body(), sb.make_lid(), sb.make_cover()
    servo = sb.make_servo_dummy(with_horn=True)
    grey, dgrey, lgrey, blue = (0.30, 0.33, 0.38), (0.42, 0.45, 0.50), (0.55, 0.58, 0.63), (0.17, 0.36, 0.84)
    green, red = (0.2, 0.8, 0.3), (0.9, 0.2, 0.2)
    import manifold3d as mf
    leds = [mf.Manifold.sphere(2.6).translate([sb.LED_GREEN_X, -sb.D / 2 - 1, sb.SENSOR_Z]),
            mf.Manifold.sphere(2.6).translate([sb.LED_RED_X, -sb.D / 2 - 1, sb.SENSOR_Z])]
    sensor = sb.union([sb.cyl_y(-sb.D / 2 - 9.6, -sb.D / 2 + 2.4, sb.SENSOR_X + dx, sb.SENSOR_Z, 8)
                       - sb.cyl_y(-sb.D / 2 - 10, -sb.D / 2 - 6, sb.SENSOR_X + dx, sb.SENSOR_Z, 6.5)
                       for dx in (-13, 13)])
    shots = []
    for title, deg, az, el, led in [("Closed - front", 0, -30, 22, red), ("Open - front", 90, -30, 22, green),
                                    ("Open - back right", 90, 145, 22, green), ("Closed - back right", 0, 145, 15, red)]:
        objs = [mesh_arrays(body, grey), mesh_arrays(cover, dgrey),
                mesh_arrays(sb.rotate_lid(lid, deg), lgrey),
                mesh_arrays(servo if deg == 0 else sb.make_servo_dummy(False), blue),
                mesh_arrays(sensor, (0.75, 0.77, 0.8)),
                mesh_arrays(leds[0], green if led == green else (0.15, 0.3, 0.18)),
                mesh_arrays(leds[1], red if led == red else (0.35, 0.12, 0.12))]
        im = render(objs, az, el)
        ImageDraw.Draw(im).text((20, 20), title, fill=(30, 30, 30))
        shots.append(im)
    sheet = Image.new("RGB", (1800, 1800), "white")
    for i, im in enumerate(shots):
        sheet.paste(im, ((i % 2) * 900, (i // 2) * 900))
    sheet.save("preview.png")
    print("wrote preview.png")


if __name__ == "__main__":
    main()
