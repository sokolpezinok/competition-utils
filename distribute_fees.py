from xml.etree import ElementTree as ET
import sys
from collections import defaultdict

assert len(sys.argv) >= 2

ET.register_namespace("", "http://www.orienteering.org/datastandard/3.0")
NS = {"iof": "http://www.orienteering.org/datastandard/3.0"}
tree = ET.parse(sys.argv[1])
ET.indent(tree)

# TODO: parse some known format, e.g. export from IS SZOŠ
payments = defaultdict(
    float,
    {
        "TJ Rapid Bratislava": 183.0,
        "HSP orienteering Láb": 16.0,
        "Športový klub Sandberg": 302.0,
        "Klub OB Sokol Pezinok": 225.0,
        "KOBRA Bratislava": 21.0,
        "ŠK Farmaceut Bratislava": 84.0,
        "ŠK VAZKA Bratislava": 159.0,
        "TJ Ioan 1209": 8.0,
        "Neregistrovani/ No Club/ Vereinslos": 0.0,
        "Neregistrovaný": 7.0,
        "Slávia Žilinská univerzita": 8.0,
        "Pukinov dvor": 8.0,
        "Korytnačky": 16.0,
        "Roxor": 8.0,
        "Viatoris": 0.0,
        "GAMČA": 5.0,
        "(AUT) Naturfreunde Wien": 8.0,
        "(AUT) HSV OL Wiener Neustadt": 29.0,
        "(AUT) OJE Wappler": 8.0,
        "ŠK HADVEO Banská Bystrica": 44.0,
        "Slovenská triatlonová akadémia": 26.0,
        "": 0.0,
    },
)

for person_entry in tree.getroot().findall("iof:PersonEntry", NS):
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
