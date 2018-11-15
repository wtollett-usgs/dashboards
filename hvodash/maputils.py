# -*- coding: utf-8 -*-
from folium import CircleMarker

from .utils import date_to_j2k

FMT = '%Y-%m-%d %H:%M:%S'
TM_COLORS = [(0, 0, 159), (0, 0, 132), (0, 0, 137), (0, 0, 142), (0, 0, 147),
             (0, 0, 153), (0, 0, 158), (0, 0, 163), (0, 0, 168), (0, 0, 173),
             (0, 0, 178), (0, 0, 183), (0, 0, 188), (0, 0, 193), (0, 0, 198),
             (0, 0, 203), (0, 0, 209), (0, 0, 214), (0, 0, 219), (0, 0, 224),
             (0, 0, 229), (0, 0, 234), (0, 0, 239), (0, 0, 244), (0, 0, 249),
             (0, 0, 255), (0, 5, 255), (0, 10, 255), (0, 15, 255),
             (0, 20, 255), (0, 25, 255), (0, 30, 255), (0, 35, 255),
             (0, 40, 255), (0, 45, 255), (0, 50, 255), (0, 56, 255),
             (0, 61, 255), (0, 66, 255), (0, 71, 255), (0, 76, 255),
             (0, 81, 255), (0, 86, 255), (0, 91, 255), (0, 96, 255),
             (0, 102, 255), (0, 107, 255), (0, 112, 255), (0, 117, 255),
             (0, 122, 255), (0, 127, 255), (0, 132, 255), (0, 137, 255),
             (0, 142, 255), (0, 147, 255), (0, 153, 255), (0, 158, 255),
             (0, 163, 255), (0, 168, 255), (0, 173, 255), (0, 178, 255),
             (0, 183, 255), (0, 188, 255), (0, 193, 255), (0, 198, 255),
             (0, 204, 255), (0, 209, 255), (0, 214, 255), (0, 219, 255),
             (0, 224, 255), (0, 229, 255), (0, 234, 255), (0, 239, 255),
             (0, 244, 255), (0, 249, 255), (0, 255, 255), (5, 255, 249),
             (10, 255, 244), (15, 255, 239), (20, 255, 234), (25, 255, 229),
             (30, 255, 224), (35, 255, 219), (40, 255, 214), (45, 255, 209),
             (50, 255, 204), (56, 255, 198), (61, 255, 193), (66, 255, 188),
             (71, 255, 183), (76, 255, 178), (81, 255, 173), (86, 255, 168),
             (91, 255, 163), (96, 255, 158), (101, 255, 153), (107, 255, 147),
             (112, 255, 142), (117, 255, 137), (122, 255, 132),
             (127, 255, 127), (132, 255, 122), (137, 255, 117),
             (142, 255, 112), (147, 255, 107), (153, 255, 101), (158, 255, 96),
             (163, 255, 91), (168, 255, 86), (173, 255, 81), (178, 255, 76),
             (183, 255, 71), (188, 255, 66), (193, 255, 61), (198, 255, 56),
             (203, 255, 51), (209, 255, 45), (214, 255, 40), (219, 255, 35),
             (224, 255, 30), (229, 255, 25), (234, 255, 20), (239, 255, 15),
             (244, 255, 10), (249, 255, 5), (255, 255, 0), (255, 249, 0),
             (255, 244, 0), (255, 239, 0), (255, 234, 0), (255, 229, 0),
             (255, 224, 0), (255, 219, 0), (255, 214, 0), (255, 209, 0),
             (255, 203, 0), (255, 198, 0), (255, 193, 0), (255, 188, 0),
             (255, 183, 0), (255, 178, 0), (255, 173, 0), (255, 168, 0),
             (255, 163, 0), (255, 158, 0), (255, 153, 0), (255, 147, 0),
             (255, 142, 0), (255, 137, 0), (255, 132, 0), (255, 127, 0),
             (255, 122, 0), (255, 117, 0), (255, 112, 0), (255, 107, 0),
             (255, 101, 0), (255, 96, 0), (255, 91, 0), (255, 86, 0),
             (255, 81, 0), (255, 76, 0), (255, 71, 0), (255, 66, 0),
             (255, 61, 0), (255, 56, 0), (255, 51, 0), (255, 45, 0),
             (255, 40, 0), (255, 35, 0), (255, 30, 0), (255, 25, 0),
             (255, 20, 0), (255, 15, 0), (255, 10, 0), (255, 5, 0),
             (255, 0, 0), (249, 0, 0), (244, 0, 0), (239, 0, 0), (234, 0, 0),
             (229, 0, 0), (224, 0, 0), (219, 0, 0), (214, 0, 0), (209, 0, 0),
             (203, 0, 0), (198, 0, 0), (193, 0, 0), (188, 0, 0), (183, 0, 0),
             (178, 0, 0), (173, 0, 0), (168, 0, 0), (163, 0, 0), (158, 0, 0),
             (153, 0, 0), (147, 0, 0), (142, 0, 0), (137, 0, 0), (132, 0, 0),
             (159, 0, 0)]


def create_popup(d, de, m):
    return f"<b>{d.strftime(FMT)}</b><br>Depth: {de}, Mag: {m}"


def create_dcircle_marker(row, mm):
    return CircleMarker(location=[row.lat, row.lon],
                        radius=3*row.prefMag,
                        popup=create_popup(row.date, row.depth, row.prefMag),
                        color='black', fill=True, weight=2, fill_opacity=1.0,
                        fill_color=get_dcolor(row.depth)).add_to(mm)


def create_tcircle_marker(row, mm, mid, mad):
    return CircleMarker(location=[row.lat, row.lon],
                        radius=3*row.prefMag,
                        popup=create_popup(row.date, row.depth, row.prefMag),
                        color='black', fill=True, weight=2, fill_opacity=1.0,
                        fill_color=get_tcolor(row.date, mid, mad)).add_to(mm)


def get_dcolor(d):
    depth = int(d)
    if depth < 0:
        return 'red'
    elif depth < 5:
        return 'orange'
    elif depth < 13:
        return 'yellow'
    elif depth < 20:
        return 'green'
    elif depth < 40:
        return 'blue'
    else:
        return 'purple'


def get_tcolor(tm, min_date, max_date):
    dt = date_to_j2k(max_date) - date_to_j2k(min_date)
    if dt == 0:
        return to_hex(1)
    else:
        calc = ((date_to_j2k(tm) - date_to_j2k(min_date)) / dt) \
            * (float(len(TM_COLORS) - 1))
        return to_hex(int(calc))


def to_hex(id):
    tup = TM_COLORS[id]
    return '#{:02X}{:02X}{:02X}'.format(tup[0], tup[1], tup[2])