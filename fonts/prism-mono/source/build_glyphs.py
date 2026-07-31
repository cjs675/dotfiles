"""build_glyphs.py - build Prism Mono letterforms into the base font.

Round 1: identity glyphs - o, zero, at.
Run from the project root:  .venv/bin/python source/build_glyphs.py
"""

import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import prism_geo as geo

import fontforge

BASE = os.path.join(os.path.dirname(__file__), "IBMPlexMono-Regular.ttf")
OUT_SFD = os.path.join(os.path.dirname(__file__), "..", "build", "PrismMono.sfd")
OUT_TTF = os.path.join(os.path.dirname(__file__), "..", "build", "PrismMono-Regular.ttf")
FEATURES = os.path.join(os.path.dirname(__file__), "features.fea")


def build_o(g, pen):
    cx, cy = 300, 258
    s_o, seg_o, s_i, seg_i = geo.ring(cx, cy, 220, 270, 120, 170)
    geo.emit(pen, s_o, seg_o)
    geo.emit(pen, s_i, seg_i)


def build_zero(g, pen):
    cx, cy = 300, 349
    s_o, seg_o, s_i, seg_i = geo.ring(cx, cy, 230, 361, 130, 261)
    geo.emit(pen, s_o, seg_o)
    geo.emit(pen, s_i, seg_i)

    # chamfered diagonal slash, contained inside the counter
    d = (math.cos(math.radians(45)), -math.sin(math.radians(45)))
    perp = (-d[1], d[0])
    half = 34.0
    for L in (150, 145, 140, 135, 130, 125, 120, 115, 110, 105, 100):
        a = (cx + d[0] * L + perp[0] * half, cy + d[1] * L + perp[1] * half)
        b = (cx + d[0] * L - perp[0] * half, cy + d[1] * L - perp[1] * half)
        c = (cx - d[0] * L - perp[0] * half, cy - d[1] * L - perp[1] * half)
        e = (cx - d[0] * L + perp[0] * half, cy - d[1] * L + perp[1] * half)
        blade = [a, b, c, e]
        rx_c, ry_c = 130, 261

        def inside(p):
            return ((p[0] - cx) / rx_c) ** 4 + ((p[1] - cy) / ry_c) ** 4 <= 0.9
        if all(inside(p) for p in blade):
            break
    blade = geo.chamfer_polygon(blade, 30)
    geo.emit_polygon(pen, blade)


def build_at(g, pen):
    # octagonal ring (machined nut), chamfered vertices
    cx, cy = 280, 258
    R_o = 292.3
    # outer octagon vertices at 22.5 + 45k
    verts = []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        verts.append((cx + R_o * math.cos(a), cy + R_o * math.sin(a)))
    outer = geo.chamfer_polygon(verts, 38)
    geo.emit_polygon(pen, outer)

    # counter: inset octagon (offset inward by stroke T * weight)
    R_c = R_o - geo.T * geo.WEIGHT / math.cos(math.radians(22.5))
    iver = []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        iver.append((cx + R_c * math.cos(a), cy + R_c * math.sin(a)))
    iver.reverse()
    geo.emit_polygon(pen, iver)

    # inner coin: solid octagon, off-center lower-left
    coin_c = (205, 238)
    coin = []
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        coin.append((coin_c[0] + 62 * math.cos(a), coin_c[1] + 62 * math.sin(a)))
    geo.emit_polygon(pen, coin)

    # chamfered tail exiting the ring lower right
    t1 = (551, 150)
    t2 = (566, 300)
    dx, dy = t2[0] - t1[0], t2[1] - t1[1]
    ln = math.hypot(dx, dy)
    nd, pd = (dx / ln, dy / ln), (-dy / ln, dx / ln)
    hw = 24.0
    corners = [
        (t1[0] + pd[0] * hw, t1[1] + pd[1] * hw),
        (t1[0] - pd[0] * hw, t1[1] - pd[1] * hw),
        (t2[0] - pd[0] * hw, t2[1] - pd[1] * hw),
        (t2[0] + pd[0] * hw, t2[1] + pd[1] * hw),
    ]
    tail = geo.chamfer_polygon(corners, 26)
    geo.emit_polygon(pen, tail)


def _crect(pen, x0, y0, x1, y1, d=30):
    """Chamfered axis-aligned rectangle (machined bar / stem).

    The stroke is thinned by the global weight factor: stems narrow
    horizontally, bars narrow vertically."""
    w = abs(x1 - x0)
    h = abs(y1 - y0)
    inset = (1.0 - geo.WEIGHT) / 2.0
    if h >= w:
        x0, x1 = x0 + w * inset, x1 - w * inset
    else:
        y0, y1 = y0 + h * inset, y1 - h * inset
    pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    geo.emit_polygon(pen, geo.chamfer_polygon(pts, d))


def _ring(pen, cx, cy, rx_o, ry_o, rx_i, ry_i):
    """Chamfered squircle ring, inner grown outward by the global weight."""
    s, segs = geo.squircle_segments(cx, cy, rx_o, ry_o, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    rx_i = rx_o - (rx_o - rx_i) * geo.WEIGHT
    ry_i = ry_o - (ry_o - ry_i) * geo.WEIGHT
    s, segs = geo.squircle_segments(cx, cy, rx_i, ry_i, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)


def build_a(g, pen):
    # single-story a: squircle bowl (slightly low) + right stem + chamfered flag
    _ring(pen, 280, 240, 180, 220, 80, 120)
    _crect(pen, 405, 0, 505, 528)
    _bar(pen, (405, 528), (240, 470), 50)
    g.removeOverlap()


def build_g(g, pen):
    # single-story g: upper bowl + descending stem + flat lower ring
    cx, cy, rx_o, ry_o = 230, 258, 175, 270
    rx_c, ry_c = 95, 190
    lcx, lcy, lrx, lry = 330, -106, 175, 110
    lrx_c, lry_c = 95, 30
    d = 30
    pen.moveTo((485, -215))
    pen.lineTo((485, 528))
    pen.lineTo((405 + d, 528))
    pen.lineTo((405, 528 - d))
    pen.lineTo((405, 258))
    _, seg = geo.squircle_segments(cx, cy, rx_o, ry_o, u0=0.0, u1=2 * math.pi)
    geo.continue_segments(pen, seg, (405, 258))
    # stem-left edge down to the lower ring, then around its left/bottom
    cross = ((405 - lcx) / lrx) ** 2
    u_top = math.acos(min(1.0, max(-1.0, cross)))
    u_bot = 2 * math.pi - u_top
    _, seg = geo.squircle_segments(lcx, lcy, lrx, lry, u0=u_top, u1=u_bot)
    start = geo.superellipse_point(lcx, lcy, lrx, lry, geo.N, u_top)
    pen.lineTo(start)
    geo.continue_segments(pen, seg, start)
    pen.lineTo((485, -215))
    pen.closePath()
    _, seg = geo.squircle_segments(cx, cy, rx_c, ry_c, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, (325, 258), seg)
    _, seg = geo.squircle_segments(lcx, lcy, lrx_c, lry_c, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, (425, -106), seg)


def build_e(g, pen):
    # geometric e: closed squircle bowl + crossbar to the right edge
    _ring(pen, 300, 258, 220, 270, 120, 170)
    pen.moveTo((400, 215))
    pen.lineTo((520, 215))
    pen.lineTo((520, 301))
    pen.lineTo((400, 301))
    pen.closePath()
    g.removeOverlap()


def build_Q(g, pen):
    # capital Q: squircle ring at cap height + chamfered tail
    _ring(pen, 300, 349, 230, 361, 130, 261)
    t1, t2 = (500, 60), (548, 10)
    dx, dy = t2[0] - t1[0], t2[1] - t1[1]
    ln = math.hypot(dx, dy)
    pd = (-dy / ln, dx / ln)
    hw = 30.0
    corners = [
        (t1[0] + pd[0] * hw, t1[1] + pd[1] * hw),
        (t1[0] - pd[0] * hw, t1[1] - pd[1] * hw),
        (t2[0] - pd[0] * hw, t2[1] - pd[1] * hw),
        (t2[0] + pd[0] * hw, t2[1] + pd[1] * hw),
    ]
    tail = geo.chamfer_polygon(corners, 28)
    geo.emit_polygon(pen, tail)
    g.removeOverlap()


def build_percent(g, pen):
    # machined percent: two solid squircles + chamfered diagonal bar
    s, segs = geo.squircle_segments(215, 555, 88, 88, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(385, 145, 88, 88, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    t1, t2 = (280, 475), (320, 225)
    dx, dy = t2[0] - t1[0], t2[1] - t1[1]
    ln = math.hypot(dx, dy)
    pd = (-dy / ln, dx / ln)
    hw = 28.0
    corners = [
        (t1[0] + pd[0] * hw, t1[1] + pd[1] * hw),
        (t1[0] - pd[0] * hw, t1[1] - pd[1] * hw),
        (t2[0] - pd[0] * hw, t2[1] - pd[1] * hw),
        (t2[0] + pd[0] * hw, t2[1] + pd[1] * hw),
    ]
    tail = geo.chamfer_polygon(corners, 26)
    geo.emit_polygon(pen, tail)


def _bar(pen, t1, t2, hw, d=26):
    dx, dy = t2[0] - t1[0], t2[1] - t1[1]
    ln = math.hypot(dx, dy)
    pd = (-dy / ln, dx / ln)
    hw = hw * geo.WEIGHT
    corners = [
        (t1[0] + pd[0] * hw, t1[1] + pd[1] * hw),
        (t1[0] - pd[0] * hw, t1[1] - pd[1] * hw),
        (t2[0] - pd[0] * hw, t2[1] - pd[1] * hw),
        (t2[0] + pd[0] * hw, t2[1] + pd[1] * hw),
    ]
    geo.emit_polygon(pen, geo.chamfer_polygon(corners, d))


def build_dollar(g, pen):
    # machined dollar: two offset loops + chamfered vertical stroke
    cx, cy = 290, 520
    s, segs = geo.squircle_segments(cx, cy, 145, 135, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(cx, cy, 55, 45, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    cx, cy = 310, 180
    s, segs = geo.squircle_segments(cx, cy, 145, 140, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(cx, cy, 55, 50, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    pen.moveTo((277, 40))
    pen.lineTo((322, 40))
    pen.lineTo((322, 660))
    pen.lineTo((277, 660))
    pen.closePath()
    g.removeOverlap()


def build_ampersand(g, pen):
    # geometric ampersand: upper loop + body diagonal + lower loop + arm
    cx, cy = 300, 500
    s, segs = geo.squircle_segments(cx, cy, 140, 110, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(cx, cy, 68, 54, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    cx, cy = 290, 140
    s, segs = geo.squircle_segments(cx, cy, 150, 130, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(cx, cy, 78, 62, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    _bar(pen, (350, 470), (300, 230), 42)
    _bar(pen, (200, 640), (330, 510), 26)
    g.removeOverlap()


def build_one(g, pen):
    _crect(pen, 295, 0, 355, 700)
    _bar(pen, (355, 700), (205, 600), 55)
    g.removeOverlap()


def build_two(g, pen):
    _ring(pen, 300, 570, 220, 130, 120, 70)
    _bar(pen, (470, 470), (110, 0), 50)
    _crect(pen, 110, 0, 520, 100)
    g.removeOverlap()


def _ring_arc(pen, cx, cy, rx_o, ry_o, rx_i, ry_i, u0, u1):
    """Closed C-band: outer squircle arc (u0..u1) + weighted inner arc back."""
    s, segs = geo.squircle_segments(cx, cy, rx_o, ry_o, u0=u0, u1=u1)
    geo.emit(pen, s, segs)
    rx_i = rx_o - (rx_o - rx_i) * geo.WEIGHT
    ry_i = ry_o - (ry_o - ry_i) * geo.WEIGHT
    s, segs = geo.squircle_segments(cx, cy, rx_i, ry_i, u0=u1, u1=u0)
    geo.emit(pen, s, segs)


def build_three(g, pen):
    # geometric 3: two C-bands (open right) joined by a left spine
    u0, u1 = math.radians(50), math.radians(310)
    _ring_arc(pen, 300, 570, 215, 135, 130, 75, u0, u1)
    _ring_arc(pen, 300, 90, 215, 135, 130, 75, u0, u1)
    _crect(pen, 90, 230, 170, 430)
    g.removeOverlap()


def build_four(g, pen):
    _bar(pen, (170, 0), (430, 700), 50)
    _crect(pen, 370, 0, 440, 700)
    _crect(pen, 140, 330, 480, 430)
    g.removeOverlap()


def build_five(g, pen):
    _crect(pen, 120, 480, 480, 580)
    _crect(pen, 120, 0, 220, 580)
    _ring(pen, 320, 130, 190, 140, 90, 60)
    g.removeOverlap()


def build_six(g, pen):
    _ring(pen, 290, 185, 205, 165, 105, 65)
    _bar(pen, (340, 350), (490, 700), 50)
    g.removeOverlap()


def build_seven(g, pen):
    _crect(pen, 90, 598, 510, 698)
    _bar(pen, (510, 598), (150, 0), 50)
    g.removeOverlap()


def build_eight(g, pen):
    _ring(pen, 300, 545, 190, 155, 90, 55)
    _ring(pen, 300, 240, 190, 155, 90, 55)
    g.removeOverlap()


def build_nine(g, pen):
    _ring(pen, 290, 545, 205, 155, 105, 55)
    _bar(pen, (350, 395), (490, 0), 50)
    g.removeOverlap()


def build_b(g, pen):
    _crect(pen, 95, 0, 195, 528)
    _ring(pen, 370, 258, 175, 270, 75, 170)
    g.removeOverlap()


def build_c(g, pen):
    pen.moveTo((445, 510))
    _, segs = geo.squircle_segments(300, 258, 220, 270, u0=math.radians(75),
                                    u1=math.radians(285))
    geo.continue_segments(pen, segs, (445, 510))
    pen.lineTo((361, 91))
    _, segs = geo.squircle_segments(300, 258, 140, 190, u0=math.radians(285),
                                    u1=math.radians(75))
    geo.continue_segments(pen, segs, (361, 91))
    pen.closePath()
    g.removeOverlap()


def build_d(g, pen):
    _ring(pen, 330, 258, 175, 270, 75, 170)
    _crect(pen, 405, 0, 505, 528)
    g.removeOverlap()


def build_f(g, pen):
    _crect(pen, 285, 0, 335, 700)
    _crect(pen, 245, 480, 405, 580)
    g.removeOverlap()


def build_h(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 195, 428, 405, 528)
    _crect(pen, 405, 0, 505, 528)
    g.removeOverlap()


def build_i(g, pen):
    _crect(pen, 275, 0, 325, 528)
    _crect(pen, 270, 628, 330, 688, 26)
    g.removeOverlap()


def build_j(g, pen):
    _crect(pen, 275, -220, 325, 528)
    _crect(pen, 270, 628, 330, 688, 26)
    g.removeOverlap()


def build_k(g, pen):
    _crect(pen, 95, 0, 195, 528)
    _bar(pen, (195, 420), (505, 528), 50)
    _bar(pen, (195, 420), (505, 0), 50)
    g.removeOverlap()


def build_l(g, pen):
    _crect(pen, 275, 0, 325, 528)


def build_m(g, pen):
    for x0, x1 in ((95, 195), (295, 395), (495, 595)):
        _crect(pen, x0, 0, x1, 528)
    _crect(pen, 195, 428, 295, 528)
    _crect(pen, 395, 428, 495, 528)
    g.removeOverlap()


def build_n(g, pen):
    _crect(pen, 95, 0, 195, 528)
    _crect(pen, 405, 0, 505, 528)
    _crect(pen, 195, 428, 405, 528)
    g.removeOverlap()


def build_p(g, pen):
    _crect(pen, 95, -220, 195, 528)
    s, segs = geo.squircle_segments(370, 258, 175, 270, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(370, 258, 75, 170, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    g.removeOverlap()


def build_q(g, pen):
    _ring(pen, 230, 258, 175, 270, 75, 170)
    _crect(pen, 405, -220, 505, 528)
    g.removeOverlap()


def build_r(g, pen):
    _crect(pen, 95, 0, 195, 528)
    _crect(pen, 195, 428, 355, 528)
    _bar(pen, (355, 428), (505, 0), 50)
    g.removeOverlap()


def build_s(g, pen):
    s, segs = geo.squircle_segments(250, 375, 150, 125, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(350, 135, 150, 125, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    g.removeOverlap()


def build_t(g, pen):
    _crect(pen, 285, 0, 335, 528)
    _crect(pen, 225, 400, 415, 500)
    g.removeOverlap()


def build_u(g, pen):
    _crect(pen, 95, 0, 195, 528)
    _crect(pen, 405, 0, 505, 528)
    _crect(pen, 195, 0, 405, 100)
    g.removeOverlap()


def build_v(g, pen):
    _bar(pen, (90, 528), (300, 60), 50)
    _bar(pen, (510, 528), (300, 60), 50)
    g.removeOverlap()


def build_w(g, pen):
    _bar(pen, (90, 528), (240, 20), 50)
    _bar(pen, (240, 20), (300, 528), 50)
    _bar(pen, (300, 528), (360, 20), 50)
    _bar(pen, (360, 20), (510, 528), 50)
    g.removeOverlap()


def build_x(g, pen):
    _bar(pen, (90, 528), (510, 0), 50)
    _bar(pen, (90, 0), (510, 528), 50)
    g.removeOverlap()


def build_y(g, pen):
    _bar(pen, (90, 528), (300, 258), 50)
    _bar(pen, (510, 528), (300, 258), 50)
    _crect(pen, 275, -220, 325, 258)
    g.removeOverlap()


def build_z(g, pen):
    _crect(pen, 90, 428, 510, 528)
    _crect(pen, 90, 0, 510, 100)
    _bar(pen, (510, 428), (90, 100), 50)
    g.removeOverlap()


def build_A(g, pen):
    _bar(pen, (300, 700), (100, 0), 50)
    _bar(pen, (300, 700), (500, 0), 50)
    _crect(pen, 150, 340, 450, 440)
    g.removeOverlap()


def build_B(g, pen):
    _crect(pen, 95, 0, 195, 700)
    s, segs = geo.squircle_segments(330, 490, 175, 170, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(330, 490, 75, 70, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(330, 205, 175, 170, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(330, 205, 75, 70, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    g.removeOverlap()


def build_C(g, pen):
    pen.moveTo((451, 685))
    _, segs = geo.squircle_segments(300, 349, 230, 361, u0=math.radians(75),
                                    u1=math.radians(285))
    geo.continue_segments(pen, segs, (451, 685))
    pen.lineTo((366, 92))
    _, segs = geo.squircle_segments(300, 349, 130, 261, u0=math.radians(285),
                                    u1=math.radians(75))
    geo.continue_segments(pen, segs, (366, 92))
    pen.closePath()
    g.removeOverlap()


def build_D(g, pen):
    _crect(pen, 95, 0, 195, 700)
    s, segs = geo.squircle_segments(330, 349, 195, 361, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(330, 349, 95, 261, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    g.removeOverlap()


def build_E(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 95, 600, 520, 700)
    _crect(pen, 95, 258, 400, 358)
    _crect(pen, 95, 0, 520, 100)
    g.removeOverlap()


def build_F(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 95, 600, 520, 700)
    _crect(pen, 95, 258, 400, 358)
    g.removeOverlap()


def build_G(g, pen):
    pen.moveTo((451, 685))
    _, segs = geo.squircle_segments(300, 349, 230, 361, u0=math.radians(75),
                                    u1=math.radians(285))
    geo.continue_segments(pen, segs, (451, 685))
    pen.lineTo((366, 92))
    _, segs = geo.squircle_segments(300, 349, 130, 261, u0=math.radians(285),
                                    u1=math.radians(75))
    geo.continue_segments(pen, segs, (366, 92))
    pen.closePath()
    _crect(pen, 300, 0, 545, 100)
    g.removeOverlap()


def build_H(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 405, 0, 505, 700)
    _crect(pen, 95, 258, 505, 358)
    g.removeOverlap()


def build_I(g, pen):
    _crect(pen, 275, 0, 325, 700)
    _crect(pen, 245, 600, 355, 700)
    _crect(pen, 245, 0, 355, 100)
    g.removeOverlap()


def build_J(g, pen):
    _crect(pen, 90, 600, 505, 700)
    _crect(pen, 405, -220, 505, 700)
    _crect(pen, 285, -220, 445, -120)
    g.removeOverlap()


def build_K(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _bar(pen, (195, 570), (490, 680), 40)
    _bar(pen, (195, 570), (505, 0), 50)
    g.removeOverlap()


def build_L(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 95, 0, 520, 100)
    g.removeOverlap()


def build_M(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 405, 0, 505, 700)
    _bar(pen, (195, 700), (300, 420), 50)
    _bar(pen, (405, 700), (300, 420), 50)
    g.removeOverlap()


def build_N(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 405, 0, 505, 700)
    _bar(pen, (195, 700), (405, 0), 50)
    g.removeOverlap()


def build_O(g, pen):
    _ring(pen, 300, 349, 230, 361, 130, 261)


def build_P(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _ring(pen, 330, 490, 175, 170, 75, 70)
    g.removeOverlap()


def build_R(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _ring(pen, 330, 490, 175, 170, 75, 70)
    _bar(pen, (400, 320), (505, 0), 50)
    g.removeOverlap()


def build_S(g, pen):
    s, segs = geo.squircle_segments(250, 520, 150, 165, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(350, 190, 150, 165, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    g.removeOverlap()


def build_T(g, pen):
    _crect(pen, 90, 600, 510, 700)
    _crect(pen, 275, 0, 325, 700)
    g.removeOverlap()


def build_U(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 405, 0, 505, 700)
    pen.moveTo((505, -12))
    _, segs = geo.squircle_segments(300, -12, 205, 150, u0=2 * math.pi, u1=math.pi)
    geo.continue_segments(pen, segs, (505, -12))
    _, segs = geo.squircle_segments(300, -12, 125, 70, u0=math.pi, u1=2 * math.pi)
    geo.continue_segments(pen, segs, (95, -12))
    pen.closePath()
    g.removeOverlap()


def build_V(g, pen):
    _bar(pen, (90, 700), (300, 60), 50)
    _bar(pen, (510, 700), (300, 60), 50)
    g.removeOverlap()


def build_W(g, pen):
    _bar(pen, (90, 700), (240, 60), 50)
    _bar(pen, (240, 60), (300, 700), 50)
    _bar(pen, (300, 700), (360, 60), 50)
    _bar(pen, (360, 60), (510, 700), 50)
    g.removeOverlap()


def build_X(g, pen):
    _bar(pen, (90, 700), (510, 0), 50)
    _bar(pen, (90, 0), (510, 700), 50)
    g.removeOverlap()


def build_Y(g, pen):
    _bar(pen, (90, 700), (300, 380), 50)
    _bar(pen, (510, 700), (300, 380), 50)
    _crect(pen, 275, 0, 325, 380)
    g.removeOverlap()


def build_Z(g, pen):
    _crect(pen, 90, 598, 510, 698)
    _crect(pen, 90, 0, 510, 100)
    _bar(pen, (510, 598), (90, 100), 50)
    g.removeOverlap()


def build_parenleft(g, pen):
    cx, cy = 300, 258
    pen.moveTo((300, 538))
    _, segs = geo.squircle_segments(cx, cy, 120, 280, u0=math.radians(90),
                                    u1=math.radians(270))
    geo.continue_segments(pen, segs, (300, 538))
    pen.lineTo((300, 78))
    _, segs = geo.squircle_segments(cx, cy, 40, 200, u0=math.radians(270),
                                    u1=math.radians(90))
    geo.continue_segments(pen, segs, (300, 78))
    pen.closePath()
    g.removeOverlap()


def build_parenright(g, pen):
    cx, cy = 300, 258
    pen.moveTo((300, 538))
    _, segs = geo.squircle_segments(cx, cy, 120, 280, u0=math.radians(90),
                                    u1=math.radians(-90))
    geo.continue_segments(pen, segs, (300, 538))
    pen.lineTo((300, 78))
    _, segs = geo.squircle_segments(cx, cy, 40, 200, u0=math.radians(-90),
                                    u1=math.radians(90))
    geo.continue_segments(pen, segs, (300, 78))
    pen.closePath()
    g.removeOverlap()


def build_bracketleft(g, pen):
    _crect(pen, 95, 0, 195, 700)
    _crect(pen, 95, 600, 505, 700)
    _crect(pen, 95, 0, 505, 100)
    g.removeOverlap()


def build_bracketright(g, pen):
    _crect(pen, 405, 0, 505, 700)
    _crect(pen, 95, 600, 505, 700)
    _crect(pen, 95, 0, 505, 100)
    g.removeOverlap()


def build_braceleft(g, pen):
    _crect(pen, 150, 0, 250, 700)
    _bar(pen, (250, 560), (360, 700), 45)
    _bar(pen, (250, 258), (390, 358), 45)
    _bar(pen, (250, 0), (360, 140), 45)
    g.removeOverlap()


def build_braceright(g, pen):
    _crect(pen, 350, 0, 450, 700)
    _bar(pen, (350, 560), (240, 700), 45)
    _bar(pen, (350, 258), (210, 358), 45)
    _bar(pen, (350, 0), (240, 140), 45)
    g.removeOverlap()


def build_plus(g, pen):
    _crect(pen, 200, 299, 400, 399)
    _crect(pen, 250, 199, 350, 399)
    g.removeOverlap()


def build_hyphen(g, pen):
    _crect(pen, 150, 299, 450, 399)


def build_equal(g, pen):
    _crect(pen, 150, 249, 450, 349)
    _crect(pen, 150, 399, 450, 499)


def build_asterisk(g, pen):
    _crect(pen, 180, 299, 420, 399, 26)
    _bar(pen, (240, 245), (360, 453), 40)
    _bar(pen, (240, 453), (360, 245), 40)
    g.removeOverlap()


def build_slash(g, pen):
    _bar(pen, (100, 0), (500, 700), 50)


def build_backslash(g, pen):
    _bar(pen, (500, 0), (100, 700), 50)


def build_less(g, pen):
    _bar(pen, (415, 528), (185, 258), 45)
    _bar(pen, (185, 258), (415, -12), 45)
    g.removeOverlap()


def build_greater(g, pen):
    _bar(pen, (185, 528), (415, 258), 45)
    _bar(pen, (415, 258), (185, -12), 45)
    g.removeOverlap()


def build_bar(g, pen):
    _crect(pen, 280, 0, 320, 700)


def build_underscore(g, pen):
    _crect(pen, 75, 0, 525, 100)


def build_asciicircum(g, pen):
    _bar(pen, (140, 258), (300, 458), 45)
    _bar(pen, (300, 458), (460, 258), 45)
    g.removeOverlap()


def build_asciitilde(g, pen):
    _bar(pen, (140, 350), (300, 208), 40)
    _bar(pen, (300, 208), (460, 350), 40)
    g.removeOverlap()


def build_grave(g, pen):
    _bar(pen, (260, 428), (170, 528), 32)


def build_quotesingle(g, pen):
    _bar(pen, (170, 428), (260, 528), 32)


def build_quotedbl(g, pen):
    _bar(pen, (140, 428), (230, 528), 30)
    _bar(pen, (300, 428), (390, 528), 30)
    g.removeOverlap()


def build_exclam(g, pen):
    _crect(pen, 285, 158, 315, 528, 22)
    _crect(pen, 270, 0, 330, 60, 22)
    g.removeOverlap()


def build_question(g, pen):
    s, segs = geo.squircle_segments(300, 540, 190, 130, u0=0.0, u1=2 * math.pi)
    geo.emit(pen, s, segs)
    s, segs = geo.squircle_segments(300, 540, 90, 70, u0=2 * math.pi, u1=0.0)
    geo.emit(pen, s, segs)
    _bar(pen, (445, 480), (300, 100), 45)
    _crect(pen, 270, 0, 330, 60, 22)
    g.removeOverlap()


def build_comma(g, pen):
    _crect(pen, 272, 0, 328, 56, 20)
    _bar(pen, (300, 0), (240, -90), 26)
    g.removeOverlap()


def build_period(g, pen):
    _crect(pen, 272, 0, 328, 56, 20)


def build_semicolon(g, pen):
    _crect(pen, 272, 208, 328, 264, 20)
    _crect(pen, 272, 0, 328, 56, 20)
    _bar(pen, (300, 0), (240, -90), 26)
    g.removeOverlap()


def build_colon(g, pen):
    _crect(pen, 272, 208, 328, 264, 20)
    _crect(pen, 272, 0, 328, 56, 20)


def build_numbersign(g, pen):
    _crect(pen, 200, 0, 240, 700)
    _crect(pen, 360, 0, 400, 700)
    _bar(pen, (140, 450), (320, 150), 45)
    _bar(pen, (280, 450), (460, 150), 45)
    g.removeOverlap()


def _arrowhead(pen, base_x, apex_x, cy, hw=45, d=45):
    """Filled chamfered arrowhead. base_x = vertical edge, apex_x = tip."""
    tri = [(base_x, cy + 270), (base_x, cy - 270), (apex_x, cy)]
    geo.emit_polygon(pen, geo.chamfer_polygon(tri, d))


def build_arrow_right(g, pen):
    _crect(pen, 100, 299, 800, 399, 26)
    _arrowhead(pen, 780, 1050, 258)
    g.removeOverlap()


def build_arrow_left(g, pen):
    _crect(pen, 400, 299, 1100, 399, 26)
    _arrowhead(pen, 420, 150, 258)
    g.removeOverlap()


def build_arrow_double(g, pen):
    _crect(pen, 100, 249, 780, 349, 26)
    _crect(pen, 100, 399, 780, 499, 26)
    _arrowhead(pen, 760, 1060, 250)
    g.removeOverlap()


def build_arrow_double_right(g, pen):
    _crect(pen, 100, 249, 1380, 349, 26)
    _crect(pen, 100, 399, 1380, 499, 26)
    _arrowhead(pen, 1360, 1660, 250)
    g.removeOverlap()


def build_less_equal(g, pen):
    _bar(pen, (580, 528), (260, 258), 45)
    _bar(pen, (260, 258), (580, -12), 45)
    _crect(pen, 580, 249, 1150, 349, 26)
    _crect(pen, 580, 399, 1150, 499, 26)
    g.removeOverlap()


def build_greater_equal(g, pen):
    _bar(pen, (620, 528), (940, 258), 45)
    _bar(pen, (940, 258), (620, -12), 45)
    _crect(pen, 50, 249, 620, 349, 26)
    _crect(pen, 50, 399, 620, 499, 26)
    g.removeOverlap()


def build_equal_equal(g, pen):
    _crect(pen, 150, 249, 1050, 349, 26)
    _crect(pen, 150, 399, 1050, 499, 26)


def build_equal_equal_equal(g, pen):
    for y in (249, 349, 449):
        _crect(pen, 150, y, 1650, y + 100, 26)


def build_not_equal(g, pen):
    _crect(pen, 150, 249, 1050, 349, 26)
    _crect(pen, 150, 399, 1050, 499, 26)
    _bar(pen, (950, 650), (250, 50), 40)
    g.removeOverlap()


def build_not_equal_equal(g, pen):
    for y in (199, 349, 499):
        _crect(pen, 150, y, 1650, y + 100, 26)
    _bar(pen, (1550, 650), (250, 50), 40)
    g.removeOverlap()


def build_spaceship(g, pen):
    _bar(pen, (600, 528), (300, 258), 45)
    _bar(pen, (300, 258), (600, -12), 45)
    _bar(pen, (1200, 528), (1500, 258), 45)
    _bar(pen, (1500, 258), (1200, -12), 45)
    _crect(pen, 700, 249, 1100, 349, 26)
    _crect(pen, 700, 399, 1100, 499, 26)
    g.removeOverlap()


LIGATURES = {
    "arrowRight": build_arrow_right,
    "arrowLeft": build_arrow_left,
    "arrowDouble": build_arrow_double,
    "arrowDoubleRight": build_arrow_double_right,
    "lessEqual": build_less_equal,
    "greaterEqual": build_greater_equal,
    "equalEqual": build_equal_equal,
    "equalEqualEqual": build_equal_equal_equal,
    "notEqual": build_not_equal,
    "notEqualEqual": build_not_equal_equal,
    "spaceship": build_spaceship,
}

LIG_WIDTHS = {
    "arrowRight": 1200,
    "arrowLeft": 1200,
    "arrowDouble": 1200,
    "arrowDoubleRight": 1800,
    "lessEqual": 1200,
    "greaterEqual": 1200,
    "equalEqual": 1200,
    "equalEqualEqual": 1800,
    "notEqual": 1200,
    "notEqualEqual": 1800,
    "spaceship": 1800,
}


BUILDERS = {
    "A": build_A,
    "B": build_B,
    "C": build_C,
    "D": build_D,
    "E": build_E,
    "F": build_F,
    "G": build_G,
    "H": build_H,
    "I": build_I,
    "J": build_J,
    "K": build_K,
    "L": build_L,
    "M": build_M,
    "N": build_N,
    "O": build_O,
    "P": build_P,
    "Q": build_Q,
    "R": build_R,
    "S": build_S,
    "T": build_T,
    "U": build_U,
    "V": build_V,
    "W": build_W,
    "X": build_X,
    "Y": build_Y,
    "Z": build_Z,
    "o": build_o,
    "zero": build_zero,
    "one": build_one,
    "two": build_two,
    "three": build_three,
    "four": build_four,
    "five": build_five,
    "six": build_six,
    "seven": build_seven,
    "eight": build_eight,
    "nine": build_nine,
    "at": build_at,
    "a": build_a,
    "b": build_b,
    "c": build_c,
    "d": build_d,
    "e": build_e,
    "f": build_f,
    "g": build_g,
    "h": build_h,
    "i": build_i,
    "j": build_j,
    "k": build_k,
    "l": build_l,
    "m": build_m,
    "n": build_n,
    "o": build_o,
    "p": build_p,
    "q": build_q,
    "r": build_r,
    "s": build_s,
    "t": build_t,
    "u": build_u,
    "v": build_v,
    "w": build_w,
    "x": build_x,
    "y": build_y,
    "z": build_z,
    "Q": build_Q,
    "percent": build_percent,
    "dollar": build_dollar,
    "ampersand": build_ampersand,
    "parenleft": build_parenleft,
    "parenright": build_parenright,
    "bracketleft": build_bracketleft,
    "bracketright": build_bracketright,
    "braceleft": build_braceleft,
    "braceright": build_braceright,
    "plus": build_plus,
    "hyphen": build_hyphen,
    "asterisk": build_asterisk,
    "slash": build_slash,
    "backslash": build_backslash,
    "equal": build_equal,
    "less": build_less,
    "greater": build_greater,
    "bar": build_bar,
    "underscore": build_underscore,
    "asciicircum": build_asciicircum,
    "asciitilde": build_asciitilde,
    "grave": build_grave,
    "quotesingle": build_quotesingle,
    "quotedbl": build_quotedbl,
    "exclam": build_exclam,
    "question": build_question,
    "comma": build_comma,
    "period": build_period,
    "semicolon": build_semicolon,
    "colon": build_colon,
    "numbersign": build_numbersign,
}


def main():
    font = fontforge.open(BASE)
    font.fontname = "PrismMono-Regular"
    font.familyname = "Prism Mono"
    font.fullname = "Prism Mono Regular"
    font.weight = "Regular"
    font.encoding = "UnicodeFull"

    for name, fn in BUILDERS.items():
        g = font[name]
        g.clear()
        fn(g, g.glyphPen())
        g.correctDirection()
        g.round(1)
        g.width = geo.WIDTH
        print(f"{name:5s} built  bbox={tuple(round(v,1) for v in g.boundingBox())}")

    for name, fn in LIGATURES.items():
        g = font.createChar(-1, name)
        fn(g, g.glyphPen())
        g.correctDirection()
        g.round(1)
        g.width = LIG_WIDTHS[name]
        print(f"lig   {name:5s} built  bbox={tuple(round(v,1) for v in g.boundingBox())}")

    if os.path.exists(FEATURES):
        font.mergeFeature(FEATURES)
        print("merged features:", FEATURES)

    font.os2_typoascent = 1025
    font.os2_typodescent = -275
    font.os2_typolinegap = 0
    font.os2_winascent = 1119
    font.os2_windescent = 350
    print("vertical metrics: sTypo(1025/-275/0) win(1119/350)")

    os.makedirs(os.path.dirname(OUT_SFD), exist_ok=True)
    font.save(OUT_SFD)
    font.generate(OUT_TTF)
    print("wrote", OUT_SFD)
    print("wrote", OUT_TTF)


if __name__ == "__main__":
    main()
