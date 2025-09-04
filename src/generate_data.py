#!/usr/bin/env python3
"""
Generate demo data for the Consumer Insights project.
This script reproduces the CSVs used by the dashboard and app.
"""
from __future__ import annotations
import random, string
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

def ensure_dirs(p: Path):
    (p / "data").mkdir(parents=True, exist_ok=True)

def seeded(seed: int = 42):
    random.seed(seed); np.random.seed(seed)

def make_survey(n_rows: int = 250) -> pd.DataFrame:
    age_groups = ["18-24", "25-34", "35-44", "45-54"]
    age_weights = [0.28, 0.44, 0.20, 0.08]
    order_times = ["Breakfast", "Lunch", "Dinner", "Late Night"]
    order_time_weights = [0.10, 0.28, 0.42, 0.20]
    cuisines = ["North Indian", "South Indian", "Chinese", "Fast Food", "Healthy", "Continental"]
    cuisine_weights = [0.22, 0.20, 0.18, 0.18, 0.14, 0.08]
    age_to_order_freq = {
        "18-24": (2, 6),
        "25-34": (2, 5),
        "35-44": (1, 4),
        "45-54": (0, 3)
    }
    age_to_spend_mean = {"18-24": 260, "25-34": 320, "35-44": 380, "45-54": 420}
    age_to_spend_sd   = {"18-24": 70,  "25-34": 85,  "35-44": 95,  "45-54": 110}

    rows = []
    for i in range(n_rows):
        ag = random.choices(age_groups, weights=age_weights, k=1)[0]
        ot = random.choices(order_times, weights=order_time_weights, k=1)[0]
        cu = random.choices(cuisines, weights=cuisine_weights, k=1)[0]
        lo, hi = age_to_order_freq[ag]
        of = int(np.clip(np.random.normal((lo+hi)/2, 1.0), lo, hi).round())
        spend = max(120, int(np.random.normal(age_to_spend_mean[ag], age_to_spend_sd[ag])))
        if ag == "18-24" and ot == "Late Night":
            spend = int(spend * np.random.uniform(0.9, 1.0))
        rows.append({
            "respondent_id": i+1,
            "city": "Bengaluru",
            "age_group": ag,
            "order_frequency_per_week": of,
            "avg_spend_inr": spend,
            "cuisine_preference": cu,
            "order_time": ot,
            "uses_subscription": random.choices([0,1], weights=[0.7,0.3])[0],
            "prefers_veg": random.choices([0,1], weights=[0.6,0.4])[0],
            "orders_via": random.choice(["Swiggy","Zomato","Direct App","WhatsApp"])
        })
    return pd.DataFrame(rows)

def email_for(name: str, domain: str) -> str:
    nm = name.lower().replace(" ", ".")
    dm = domain.lower().replace(" ", "").replace("&","and")
    return f"{nm}@{dm}.com"

def make_founders(n: int = 28, start_date: datetime | None = None) -> pd.DataFrame:
    first_names = ["Aarav","Vihaan","Vivaan","Aditya","Arjun","Reyansh","Muhammad","Sai","Ishaan","Kabir",
                   "Aanya","Aarohi","Anaya","Diya","Myra","Sara","Aadhya","Pari","Anika","Navya"]
    last_names = ["Sharma","Verma","Iyer","Menon","Reddy","Gowda","Khan","Patel","Mehta","Chopra",
                  "Nair","Sen","Das","Bose","Mukherjee","Kulkarni","Kapoor","Bhat","Shetty","Banerjee"]
    company_roots = ["SpiceBox","CloudBite","KitchenKart","MealMint","TiffinTales","CurryCrate","BowlBerry",
                     "FlavorForge","MasalaMate","CrunchCart","QuickQitchen","HealthHub","FitFeast","VegVibe",
                     "MidnightMorsel","Byte&Bite","ForkFuel","HungryHive","TasteTrail","UrbanPlates"]
    if start_date is None:
        start_date = datetime(2025, 9, 8)
    founders = []
    for i in range(n):
        fn = f"{random.choice(first_names)} {random.choice(last_names)}"
        comp = random.choice(company_roots) + " Labs"
        status = random.choices(["not contacted","contacted","meeting scheduled","closed"],
                                weights=[0.25,0.40,0.30,0.05])[0]
        mode = random.choice(["Zoom","Google Meet","Phone","In-person"])
        meeting_date = ""
        if status == "meeting scheduled":
            delta_days = random.randint(0, 40)
            dt = start_date + timedelta(days=delta_days)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)
            meeting_date = dt.strftime("%Y-%m-%d")
        founders.append({
            "founder_id": i+1,
            "name": fn,
            "company": comp,
            "email": email_for(fn, comp),
            "segment_focus": random.choice(["Healthy","Late Night","Family","Budget","Premium"]),
            "status": status,
            "preferred_mode": mode,
            "meeting_date": meeting_date
        })
    return pd.DataFrame(founders)

def make_meetings(founders_df: pd.DataFrame) -> pd.DataFrame:
    import numpy as np
    df = founders_df[founders_df["status"].eq("meeting scheduled")].copy()
    df["meeting_time"] = np.random.choice(["10:00","11:30","14:00","15:30","17:00"], size=len(df))
    def meet_link(mode: str) -> str:
        import random, string
        return "" if mode == "In-person" else "https://meet.example.com/" + "".join(random.choices(string.ascii_lowercase+string.digits,k=8))
    df["meeting_link"] = [meet_link(m) for m in df["preferred_mode"]]
    return df

def make_trends() -> pd.DataFrame:
    weeks = pd.date_range("2025-07-07", periods=9, freq="W-MON")
    keywords = [
        "cloud kitchen bengaluru", "late night food bangalore", "healthy meal subscription",
        "family combo meals", "budget lunch box", "south indian breakfast delivery"
    ]
    rows = []
    for kw in keywords:
        base = random.randint(40, 120)
        for w in weeks:
            vol = max(0, int(np.random.normal(base, base*0.15)))
            idx = weeks.get_indexer([w])[0]
            if "late night" in kw:
                vol = int(vol * (1 + 0.08 * idx))
            if "healthy" in kw:
                vol = int(vol * (1 + 0.05 * idx))
            rows.append({"week_start": w.strftime("%Y-%m-%d"), "keyword": kw, "search_volume_index": vol})
    return pd.DataFrame(rows)

def main():
    here = Path(__file__).resolve().parents[1]
    ensure_dirs(here)
    seeded(42)

    survey = make_survey()
    founders = make_founders()
    meetings = make_meetings(founders)
    trends = make_trends()

    survey.to_csv(here/"data"/"raw_survey_data.csv", index=False)
    founders.to_csv(here/"data"/"founders_list.csv", index=False)
    meetings.to_csv(here/"data"/"meetings_schedule.csv", index=False)
    trends.to_csv(here/"data"/"ga_mock_trends.csv", index=False)
    print("Data regenerated under:", here/"data")

if __name__ == "__main__":
    main()
