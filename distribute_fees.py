import csv
from xml.etree import ElementTree as ET
import sys
from collections import defaultdict

assert len(sys.argv) >= 2

ET.register_namespace("", "http://www.orienteering.org/datastandard/3.0")
NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}
tree = ET.parse(sys.argv[1])
ET.indent(tree)

payments = defaultdict(float)
if len(sys.argv) >= 3:
    with open(sys.argv[2], newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            club = row["Názov klubu"]
            amount = float(row["Suma"].rstrip("€"))
            payments[club] += amount

entries = sorted(
    tree.getroot().findall("iof:PersonEntry", NS),
    key=lambda e: e.get("entryTime", ""),
)
for person_entry in entries:
    club_name = person_entry.find("./iof:Organisation/iof:Name", NS).text
    fee = person_entry.find("./iof:AssignedFee/iof:Fee/iof:Amount", NS).text
    assert fee is not None
    fee = float(fee)

    club_total = payments.get(club_name, 0.0)
    available = min(club_total, fee)
    payments[club_name] -= available

    fee_entry = person_entry.find("./iof:AssignedFee", NS)
    assert fee_entry is not None
    paid = ET.SubElement(fee_entry, "PaidAmount", {"currency": "EUR"})
    paid.text = str(available)


ET.indent(tree)
tree.write(sys.stdout.buffer, encoding="UTF-8", xml_declaration=True)
