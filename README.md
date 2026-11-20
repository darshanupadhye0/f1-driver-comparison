# 🏁 F1 Driver Comparison Dashboard

An end-to-end data analytics project that compares Formula 1 drivers on pace, sector performance, top speed and consistency. Race data is pulled from the OpenF1 API with Python, stored and cleaned in MySQL, and shown in an F1-themed Power BI dashboard.

---

| **Question** | Which driver is faster, where do they gain time, and who is most consistent? |
| **Race analysed** | São Paulo GP 2026 (built on Monza 2025, switchable to any race) |
| **Data size** | ~20 drivers and ~1,000 laps per race |
| **Source** | OpenF1 API (free, historical) |
| **Tools** | Python → MySQL → Power BI (DAX) |
| **Output** | Interactive dashboard with slicer, KPI cards, charts and a timing tower |

---

## 🎯 What This Project Is

In Formula 1, a few tenths of a second decide a race. This project takes the lap-by-lap timing data of a Grand Prix and turns it into a dashboard where you pick any drivers and instantly see:

- who set the quickest lap,
- who is faster on average,
- who is steadier lap after lap,
- which of the three track sectors each driver wins,
- who reached the highest top speed.

It's a complete analytics workflow: getting data, storing it, cleaning it, analysing it and presenting it.

---

## 🛠️ What I Did, Step by Step

1. **Collected the data.** Wrote a Python script that asks the OpenF1 API for a chosen race and downloads the drivers and every lap.
2. **Stored it.** Saved the data into two MySQL tables, `drivers` and `laps`.
3. **Cleaned it.** Built a SQL view (`v_laps`) that joins the tables and removes laps that would distort the results, such as the standing start, pit-out laps and very slow laps.
4. **Analysed it.** Wrote DAX measures in Power BI for fastest lap, average lap, top speed, consistency and sector averages.
5. **Visualised it.** Designed an F1-style dashboard with a driver slicer, KPI cards, a lap-time chart, a sector chart and a timing tower table.
6. **Made it reusable.** Changing one line of the script and clicking Refresh loads a different Grand Prix.

---

## 🔄 Pipeline

```
OpenF1 API  ──►  Python  ──►  MySQL  ──►  Power BI
 (source)      (extract      (store &     (measures &
                & load)       clean)       dashboard)
```

| Stage | Tool | What happens |
|---|---|---|
| Extract | Python (`requests`) | Calls the API for a race session and downloads drivers and laps |
| Load | Python (`mysql-connector-python`) | Writes the data into `drivers` and `laps` |
| Clean | MySQL view `v_laps` | Joins the tables and filters invalid laps |
| Analyse | Power BI (DAX) | Calculates the performance metrics |
| Visualise | Power BI | Interactive F1-themed dashboard |

Python and Power BI never connect to each other. Both connect to the same MySQL database (`f1_compare`): Python writes to it and Power BI reads from it.

---

## 📖 Data Dictionary

**drivers**

| Column | Meaning |
|---|---|
| `driver_number` | Car number (primary key) |
| `acronym` | Three-letter code, e.g. NOR |
| `full_name` | Driver's name |
| `team_name` | Constructor, e.g. McLaren |

**laps**

| Column | Meaning |
|---|---|
| `driver_number` | Links to `drivers` |
| `lap_number` | Lap of the race |
| `lap_time` | Lap duration in seconds |
| `sector1`, `sector2`, `sector3` | Sector times in seconds |
| `top_speed` | Speed-trap top speed in km/h |
| `is_pit_out` | True if the lap started in the pit lane |

**v_laps** is the cleaned view Power BI reads: the lap columns plus the driver's name, code and team.

---

## 🧹 Data Cleaning

All cleaning happens in one place, the SQL view `v_laps`:

| Rule | Reason |
|---|---|
| Remove rows with no lap time | Incomplete laps can't be compared |
| Remove lap 1 | The standing start distorts the time |
| Remove pit-out laps | Slow laps leaving the pits |
| Remove laps over 92 seconds | Safety car, in-laps and incidents |

---

## 📊 Dashboard and DAX Measures

**Features:** driver slicer, KPI cards (Fastest Lap, Avg Lap, Top Speed, Consistency, Fastest Driver), lap time by lap chart, sector times chart, timing tower table with team colours, custom dark F1 theme with a red header, checkered strips and a track map.

```DAX
Fastest Lap  = MIN('f1_compare v_laps'[lap_time])
Avg Lap      = AVERAGE('f1_compare v_laps'[lap_time])
Top Speed    = MAX('f1_compare v_laps'[top_speed])
Consistency  = STDEV.P('f1_compare v_laps'[lap_time])   -- lower = steadier

Fastest Driver =
MINX(
    TOPN(1, 'f1_compare v_laps', 'f1_compare v_laps'[lap_time], ASC),
    'f1_compare v_laps'[acronym]
)
```

---

## 🚀 How to Run

Requirements: Python 3.11+, MySQL Server and Workbench, Power BI Desktop (Windows).

1. Create the database: open `schema.sql` in MySQL Workbench and run it.
2. Install packages: `pip install requests mysql-connector-python`
3. Set your password in the `DB` line of `ingest.py`.
4. Load the race: `python ingest.py`
5. Open `F1_Driver_Comparison.pbix`, point the source to `localhost` / `f1_compare` if asked, and click Home → Refresh.

```
f1-driver-comparison/
├── ingest.py                  # API → MySQL loader
├── schema.sql                 # database, tables and cleaning view
├── F1_Driver_Comparison.pbix  # Power BI report
├── f1_theme.json              # custom Power BI theme
├── assets/                    # screenshots and images
└── README.md
```

---

## 🔁 Switching to a Different Race

1. In `ingest.py`, change the race:
   ```python
   session = get("sessions", year=2025,
                 circuit_short_name="Silverstone", session_name="Race")[0]
   ```
2. Clear the old race by adding these lines right after `cur = db.cursor()`:
   ```python
   cur.execute("DELETE FROM laps")
   cur.execute("DELETE FROM drivers")
   ```
3. Run `python ingest.py`.
4. In Power BI: Refresh, clear the slicer with the eraser icon, and pick drivers again.

---

## 🔍 Key Insights

- _Write what you see in your dashboard here._
- _Example: Driver A set the fastest lap, but Driver B had the lower average lap time._
- _Example: Driver C gains most time in Sector 2._

---

## 💼 Skills Demonstrated

- **Data extraction:** calling a REST API from Python
- **Database work:** designing tables, loading data, writing a cleaning view in SQL
- **Data cleaning:** filtering outliers and invalid records
- **DAX:** measures for aggregation, ranking and variability
- **Dashboard design:** slicers, KPI cards, charts, a custom theme and consistent branding
- **End-to-end thinking:** a reusable pipeline from source to report

---

## 🧠 What I Learned

- How data moves through a pipeline: source, storage, cleaning, analysis, report.
- Why cleaning belongs in one place, and how a SQL view keeps raw data untouched.
- That Power BI only sees changes after a Refresh, and that slicer selections can hide data until cleared.
- How to turn raw numbers into a dashboard that answers a clear question.

## 🙏 Credits and Disclaimer

Data from the OpenF1 API. Track outline generated from the open f1-circuits dataset. This is an unofficial, educational project, not affiliated with or endorsed by Formula 1, the FIA or any team. F1, Formula 1 and related marks belong to their owners.

Darshan Upadhye.
