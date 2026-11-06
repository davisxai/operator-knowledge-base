#!/usr/bin/env python3
# Usage: python3 gazetteer-to-csv.py 2024_Gaz_place_national.txt > city_centroids.csv
# Turns the US Census Gazetteer places file (public domain) into state,city,lat,lng rows
# for the city_centroids table. City names are normalized the same way the geocode
# UPDATE normalizes leads.city, so the join is a plain equality.
import csv
import re
import sys

DESIGNATORS = [
    "city and borough", "consolidated government", "metropolitan government",
    "metro government", "unified government", "urban county", "zona urbana",
    "comunidad", "municipality", "borough", "village", "township", "town", "city", "cdp",
]


def norm_city(raw):
    s = re.sub(r"\([^)]*\)", "", raw.lower())
    s = re.sub(r"[.'’]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    for _ in range(3):
        before = s
        for d in DESIGNATORS:
            if s.endswith(" " + d) and len(s) > len(d) + 1:
                s = s[: -len(d) - 1].strip()
                break
        if s == before:
            break
    for short, full in (("st ", "saint "), ("ft ", "fort "), ("mt ", "mount ")):
        if s.startswith(short):
            s = full + s[len(short):]
    return s


def main(path):
    best = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        rows = csv.reader(f, delimiter="\t")
        header = [h.strip() for h in next(rows)]
        i_state, i_name = header.index("USPS"), header.index("NAME")
        i_lat, i_lng = header.index("INTPTLAT"), header.index("INTPTLONG")
        for parts in rows:
            if len(parts) <= max(i_state, i_name, i_lat, i_lng):
                continue
            state, name = parts[i_state].strip(), parts[i_name].strip()
            try:
                lat, lng = float(parts[i_lat]), float(parts[i_lng])
            except ValueError:
                continue
            incorporated = not re.search(r"\bCDP$", name, re.I)
            key = (state, norm_city(name))
            # Prefer an incorporated city or town over a census-designated place of the same name.
            if key not in best or (incorporated and not best[key][2]):
                best[key] = (lat, lng, incorporated)
    out = csv.writer(sys.stdout)
    out.writerow(["state", "city", "lat", "lng"])
    for (state, city), (lat, lng, _) in sorted(best.items()):
        out.writerow([state, city, lat, lng])
    print(f"{len(best)} places", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python3 gazetteer-to-csv.py <Gaz_place_national.txt>")
    main(sys.argv[1])
