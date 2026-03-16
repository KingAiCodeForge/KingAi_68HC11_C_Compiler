import json
from collections import Counter

d = json.load(open("Enhanced_v1.json"))
addrs = [s["address"] for s in d["scalars"] if s.get("address")]
dupes = [(a,c) for a,c in Counter(addrs).items() if c > 1]
print(f"Duplicate scalar addresses: {len(dupes)}")
for addr, cnt in dupes[:5]:
    items = [s for s in d["scalars"] if s.get("address") == addr]
    print(f"  {addr}: {cnt} entries")
    for s in items:
        t = s.get("title","")[:60]
        v = s.get("value","")
        u = s.get("unit","")
        print(f"    - {t} = {v} {u}")
