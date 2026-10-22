"""Recalcule la décision attendue de Decide aurora à partir des deux CSV (règle GO : Kp 3 ou plus, 40 % de nuages au plus)."""
import csv
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
sky = list(csv.DictReader(open(DATA / "sky" / "sky_2026-11-27.csv", encoding="utf-8")))
book = list(csv.DictReader(open(DATA / "bookings" / "bookings_2026-11-27.csv", encoding="utf-8")))
ok = [r for r in sky if float(r["kp_index"]) >= 3 and int(r["cloud_pct"]) <= 40]
best = {}
for r in ok:
    key = (float(r["kp_index"]), -int(r["cloud_pct"]))
    if r["zone"] not in best or key > best[r["zone"]][0]:
        best[r["zone"]] = (key, r)
tours = defaultdict(lambda: [0, 0])
for b in book:
    tours[b["zone"]][0] += 1
    tours[b["zone"]][1] += int(b["booked"])
print("Heures GO :")
for r in ok:
    print(f"  {r['zone']:<12} {r['hour_local']}  Kp {r['kp_index']}  nuages {r['cloud_pct']} %")
print("\nDécision par zone :")
for z, (t, p) in tours.items():
    if z in best:
        r = best[z][1]
        print(f"  {z:<12} GO       meilleure heure {r['hour_local'][11:]}, Kp {r['kp_index']}, {r['cloud_pct']} %  · {t} tours, {p} voyageurs")
    else:
        print(f"  {z:<12} ANNULÉ   {t} tours, {p} voyageurs")
go = [z for z in tours if z in best]
print(f"\nGO pour {len(go)} zones sur {len(tours)} · {sum(tours[z][0] for z in go)} tours, {sum(tours[z][1] for z in go)} voyageurs")
