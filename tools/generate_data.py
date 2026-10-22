"""Génère la nuit d'aurores du 27 novembre 2026 en Islande : prévisions du ciel et réservations (graine 1717)."""
import csv, math, random, datetime as dt
from pathlib import Path
random.seed(1717)
ROOT = Path(__file__).resolve().parent.parent / "data"
ZONES = {  # zone : nuages de base (%), décalage du pic de nuages
    "Reykjavik": (38, 0.0), "Thingvellir": (14, 0.0), "Snaefellsnes": (82, 0.0), "Vik": (30, 2.5)}
start = dt.datetime(2026, 11, 27, 18, 0)
sky = []
for h in range(10):                      # 18 h à 03 h
    t = start + dt.timedelta(hours=h)
    kp = 2.0 + 2.7 * math.exp(-((h - 5.0) ** 2) / 4.0)     # l'activité culmine vers 23 h
    for z, (base, sh) in ZONES.items():
        cloud = base + 18 * math.sin((h - sh) / 2.2) + random.uniform(-6, 6)
        sky.append(["2026-11-27", z, t.strftime("%Y-%m-%d %H:%M"), round(kp + random.uniform(-0.15, 0.15), 1),
                    int(min(100, max(0, cloud)))])
with open(ROOT / "sky" / "sky_2026-11-27.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["night", "zone", "hour_local", "kp_index", "cloud_pct"]); w.writerows(sky)
OPS = ["Arctic Lights", "Nordurljos Tours", "Hekla Hunters", "Polar Path", "Fjord & Fire"]
book, tid = [], 900
for z, n in (("Reykjavik", 7), ("Thingvellir", 6), ("Snaefellsnes", 5), ("Vik", 4)):
    for i in range(n):
        tid += 1
        cap = random.choice([19, 19, 33, 50])
        book.append(["2026-11-27", f"T{tid}", random.choice(OPS), z, f"2026-11-27 {random.choice(['20:30', '21:00', '21:30', '22:00'])}",
                     cap, random.randint(int(cap * 0.55), cap)])
with open(ROOT / "bookings" / "bookings_2026-11-27.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["night", "tour_id", "operator", "zone", "departure", "capacity", "booked"]); w.writerows(book)
