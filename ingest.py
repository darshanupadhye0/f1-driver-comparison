import requests, mysql.connector

YEAR = 2026

API = "https://api.openf1.org/v1"
DB = dict(host="localhost", user="root",
          password="koenigsegg0", database="f1_compare")

def get(endpoint, **params):
    r = requests.get(f"{API}/{endpoint}", params=params, timeout=60)
    r.raise_for_status()
    return r.json()

sessions = get("sessions", year=2026, circuit_short_name="Las Vegas", session_name="Race")
if not sessions:
    print("NO DATA FOUND for", CIRCUIT, YEAR)
    print("Races available that year:")
    for s in get("sessions", year=YEAR, session_name="Race"):
        print(" -", s["circuit_short_name"], s["date_start"][:10])
    raise SystemExit

sk = sessions[0]["session_key"]
print("Loading:", sessions[0]["circuit_short_name"], YEAR, "| session", sk)

drivers = get("drivers", session_key=sk)
laps = get("laps", session_key=sk)

db = mysql.connector.connect(**DB)
cur = db.cursor()
cur.execute("TRUNCATE TABLE laps")
cur.execute("TRUNCATE TABLE drivers")

cur.executemany("REPLACE INTO drivers VALUES (%s,%s,%s,%s)",
    [(d["driver_number"], d["name_acronym"], d["full_name"], d["team_name"]) for d in drivers])
cur.executemany("REPLACE INTO laps VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
    [(l["driver_number"], l["lap_number"], l["lap_duration"],
      l["duration_sector_1"], l["duration_sector_2"], l["duration_sector_3"],
      l["st_speed"], bool(l["is_pit_out_lap"])) for l in laps])
db.commit()

cur.execute("SELECT COUNT(*), MIN(lap_time), MAX(lap_number) FROM laps")
print("Loaded (laps, fastest lap, last lap):", cur.fetchone())