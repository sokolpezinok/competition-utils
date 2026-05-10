#!/usr/bin/env python3
# Ráta body za Pohár Oslobodenia Mesta Pezinok
# 3, 2, 1 body sú za 1. až 3. miesto v každej kategórii
# Dáta idú z IOF XML formátu výsledkov
# $ ./pomp.py results.xml

import xml.etree.ElementTree as ET
import csv
import sys

assert len(sys.argv) >= 2

tree = ET.parse(sys.argv[1])
ET.indent(tree)
NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}

POSITION_POINTS = {1: 3, 2: 2, 3: 1}

club_points = {}
classes = set()
for class_result in tree.getroot().findall("iof:ClassResult", NS):
    clas = class_result.find("./iof:Class/iof:Name", NS).text
    if clas == "MWR":
        continue
    classes.add(clas)
    for person_result in class_result.findall("./iof:PersonResult", NS):
        status = person_result.find("./iof:Result/iof:Status", NS)
        if status is None or status.text != "OK":
            continue
        position = int(person_result.find("./iof:Result/iof:Position", NS).text)
        club = person_result.find("./iof:Organisation", NS)
        if club is None:
            continue
        club = person_result.find("./iof:Organisation/iof:Name", NS)
        assert club is not None
        club = club.text
        if club not in club_points:
            club_points[club] = {}

        points = POSITION_POINTS.get(position, 0)
        club_points[club][clas] = club_points[club].setdefault(clas, 0) + points

csv_writer = csv.writer(sys.stdout)
club_table = list(club_points.items())
club_table.sort()

classes = list(classes)
classes.sort()

clubs, point_maps = list(zip(*club_table))
csv_writer.writerow(["Kategória/Kluby"] + list(clubs))
for clas in classes:
    points = [class_points.get(clas, 0) for class_points in point_maps]
    csv_writer.writerow([clas] + points)

total_points = [str(sum(class_points.values())) for class_points in point_maps]
csv_writer.writerow(["Spolu"] + total_points)
