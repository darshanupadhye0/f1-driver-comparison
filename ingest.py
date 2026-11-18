import requests, mysql.connector

API = "https://api.openf1.org/v1"
DB = dict(host="localhost", user="root",
          password="koenigsegg0", database="f1_compare")

def get(endpoint, **params):
    r = requests.get(f"{API}/{endpoint}", params=params, timeout=60)
    r.raise_for_status()
    return r.json()

session = get("sessions", year=2026,
              circuit_short_name="Brazil", session_name="Race")[0]
sk = session["session_key"]
print("Session key:", sk)

drivers = get("drivers", session_key=sk)
laps = get("laps", session_key=sk)

db = mysql.connector.connect(**DB)
cur = db.cursor()

cur.execute("DELETE FROM laps")
cur.execute("DELETE FROM drivers")

cur.executemany(
    "REPLACE INTO drivers VALUES (%s,%s,%s,%s)",
    [(d["driver_number"], d["name_acronym"],
      d["full_name"], d["team_name"]) for d in drivers])

cur.executemany(
    "REPLACE INTO laps VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
    [(l["driver_number"], l["lap_number"], l["lap_duration"],
      l["duration_sector_1"], l["duration_sector_2"],
      l["duration_sector_3"], l["st_speed"],
      bool(l["is_pit_out_lap"])) for l in laps])

db.commit()
print(f"Saved {len(drivers)} drivers and {len(laps)} laps")