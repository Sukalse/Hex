import math

def hex_to_pixel(q, r, HEX_SIZE):
    x = HEX_SIZE * math.sqrt(3) * (q + r / 2)
    y = HEX_SIZE * 1.5 * r
    return x, y

def pixel_to_hex(x, y, HEX_SIZE):
    q = (math.sqrt(3) / 3 * x - 1 / 3 * y) / HEX_SIZE
    r = (2 / 3 * y) / HEX_SIZE
    return q, r

def hex_points(cx, cy, size):

    pts = []

    for i in range(6):
        angle = math.radians(60 * i - 30)

        x = cx + size * math.cos(angle)
        y = cy + size * math.sin(angle)

        pts.append((x, y))

    return pts

def hex_round(q, r):
    x = q
    z = r
    y = -x - z

    rx = round(x)
    ry = round(y)
    rz = round(z)

    dx = abs(rx - x)
    dy = abs(ry - y)
    dz = abs(rz - z)

    if dx > dy and dx > dz:
        rx = -ry - rz
    elif dy > dz:
        ry = -rx - rz
    else:
        rz = -rx - ry

    return rx, rz
