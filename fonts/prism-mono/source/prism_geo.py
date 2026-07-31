"""prism_geo.py - geometry toolkit for Prism Mono.

Prism Mono is a chamfered-geometric monospace. Every letterform is
constructed from exact geometry:
  - concentric squircles (superellipses, n=4) for bowls and counters
  - straight stems and bars with 45-degree chamfered joins
  - machined details (octagonal bores, chamfered slashes)

Coordinates are FontForge style: y-up, UPM 1000, baseline y=0.
"""

import math

# ---- design tokens -------------------------------------------------------
T = 100      # stem / bar / ring stroke weight
WEIGHT = 0.80  # global stroke weight factor vs the original 100-unit design
OV = 12      # optical overshoot
XHEIGHT = 516
CAP = 698
ASCENT = 780
DESCENT = -220
WIDTH = 600  # fixed advance width (the mono contract)
N = 4.0      # superellipse exponent (4 = squircle)


def spow(x, e):
    """Signed power: sign(x) * |x|^e (smooth across zero)."""
    return math.copysign(abs(x) ** e, x)


def superellipse_point(cx, cy, rx, ry, n, u):
    """Point on a superellipse at parameter u (radians)."""
    return (cx + rx * spow(math.cos(u), 2.0 / n),
            cy + ry * spow(math.sin(u), 2.0 / n))


def squircle_segments(cx, cy, rx, ry, n=N, u0=0.0, u1=2 * math.pi, per_quad=6):
    """Cubic-bezier segments for a closed superellipse arc.

    Returns (start_point, [segments]) where each segment is
    ((c1x,c1y),(c2x,c2y),(p1x,p1y)).  Fitted with a Hermite cubic using
    numeric tangents.  Runs CCW for increasing u in y-up space.
    """
    m = max(4, int(round((u1 - u0) / (math.pi / 2))) * per_quad)
    us = [u0 + (u1 - u0) * i / m for i in range(m + 1)]
    pts = [superellipse_point(cx, cy, rx, ry, n, u) for u in us]
    h = (u1 - u0) / m

    def deriv(j):
        j0 = max(0, j - 1)
        j1 = min(m, j + 1)
        return ((pts[j1][0] - pts[j0][0]) / (us[j1] - us[j0]),
                (pts[j1][1] - pts[j0][1]) / (us[j1] - us[j0]))

    segs = []
    for i in range(m):
        p0, p1 = pts[i], pts[i + 1]
        d0, d1 = deriv(i), deriv(i + 1)
        c1 = (p0[0] + d0[0] * h / 3.0, p0[1] + d0[1] * h / 3.0)
        c2 = (p1[0] - d1[0] * h / 3.0, p1[1] - d1[1] * h / 3.0)
        segs.append((c1, c2, p1))
    return pts[0], segs


def arc_segments(cx, cy, r, a0, a1, max_delta=math.pi / 2):
    """Cubic-bezier segments for a circular arc (CCW if a1>a0)."""
    segs = []
    a = a0
    while a < a1 - 1e-9:
        step = min(a1 - a, max_delta)
        b = a + step
        k = (4.0 / 3.0) * math.tan(step / 4.0)
        t0 = (-math.sin(a), math.cos(a))
        t1 = (-math.sin(b), math.cos(b))
        p0 = (cx + r * math.cos(a), cy + r * math.sin(a))
        p3 = (cx + r * math.cos(b), cy + r * math.sin(b))
        c1 = (p0[0] + k * r * t0[0], p0[1] + k * r * t0[1])
        c2 = (p3[0] - k * r * t1[0], p3[1] - k * r * t1[1])
        segs.append((c1, c2, p3))
        a = b
    return segs


def chamfer_corner(prev, cur, nxt, d):
    """Cut a corner with a flat chamfer.

    Returns the two replacement points (a, b) that replace `cur`, or None
    when the corner is too shallow to chamfer.  Works for both convex
    (cuts the tip) and concave (fills the notch) corners.
    """
    v1 = (prev[0] - cur[0], prev[1] - cur[1])
    v2 = (nxt[0] - cur[0], nxt[1] - cur[1])
    l1 = math.hypot(*v1)
    l2 = math.hypot(*v2)
    if l1 == 0 or l2 == 0:
        return None
    v1 = (v1[0] / l1, v1[1] / l1)
    v2 = (v2[0] / l2, v2[1] / l2)
    dot = max(-1.0, min(1.0, v1[0] * v2[0] + v1[1] * v2[1]))
    ang = math.acos(dot)
    if ang > math.radians(150):  # nearly straight: leave it alone
        return None
    d1 = min(d, l1)
    d2 = min(d, l2)
    a = (cur[0] + v1[0] * d1, cur[1] + v1[1] * d1)
    b = (cur[0] + v2[0] * d2, cur[1] + v2[1] * d2)
    return (a, b)


def chamfer_polygon(points, d):
    """Return a closed polygon with sharp corners chamfered by distance d.

    Only chamfers corners sharper than 150 degrees.  Points is a list of
    (x, y) in order (unclosed)."""
    n = len(points)
    out = []
    for i in range(n):
        prev = points[i - 1]
        cur = points[i]
        nxt = points[(i + 1) % n]
        cut = chamfer_corner(prev, cur, nxt, d)
        if cut is None:
            out.append(cur)
        else:
            out.append(cut[0])
            out.append(cut[1])
    return out


def ring(cx, cy, rx_o, ry_o, rx_c, ry_c, n=N):
    """Contours for a squircle ring: outer + counter.

    The counter is grown outward by the global weight factor so rings thin
    proportionally.  Returns (outer_start, outer_segs, inner_start,
    inner_segs).  Outer is CCW, counter is CW (y-up)."""
    rx_c = rx_o - (rx_o - rx_c) * WEIGHT
    ry_c = ry_o - (ry_o - ry_c) * WEIGHT
    s_outer, seg_outer = squircle_segments(cx, cy, rx_o, ry_o, n, 0.0, 2 * math.pi)
    s_inner, seg_inner = squircle_segments(cx, cy, rx_c, ry_c, n, 2 * math.pi, 0.0)
    return s_outer, seg_outer, s_inner, seg_inner


def cubic_to_quadratics(p0, c1, c2, p3):
    """Approximate one cubic bezier with two quadratics."""
    qa = ((3 * c1[0] - p0[0]) / 2.0, (3 * c1[1] - p0[1]) / 2.0)
    qb = ((3 * c2[0] - p3[0]) / 2.0, (3 * c2[1] - p3[1]) / 2.0)
    m = ((p0[0] + 3 * c1[0] + 3 * c2[0] + p3[0]) / 8.0,
         (p0[1] + 3 * c1[1] + 3 * c2[1] + p3[1]) / 8.0)
    return ((qa, m), (qb, p3))


def continue_segments(pen, segs, p0):
    """Emit bezier segments continuing from current position p0."""
    for (c1, c2, p1) in segs:
        (qa, m), (qb, e) = cubic_to_quadratics(p0, c1, c2, p1)
        pen.qCurveTo(qa, m)
        pen.qCurveTo(qb, e)
        p0 = p1
    return p0


def emit(pen, start, segs, close=True):
    pen.moveTo(start)
    continue_segments(pen, segs, start)
    if close:
        pen.closePath()


def emit_polygon(pen, points, close=True):
    pen.moveTo(points[0])
    for p in points[1:]:
        pen.lineTo(p)
    if close:
        pen.closePath()
