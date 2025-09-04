#!/usr/bin/env python3
"""
Rule-based newsroom story idea generator based on survey & trend signals.
(No ML, transparent logic.)
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def load_data(base: Path):
    survey = pd.read_csv(base/"data"/"raw_survey_data.csv")
    trends = pd.read_csv(base/"data"/"ga_mock_trends.csv")
    return survey, trends

def story_recommendations(survey: pd.DataFrame, trends: pd.DataFrame) -> list[str]:
    ideas = []

    # Late night signal
    freq = survey.groupby("order_time")["order_frequency_per_week"].mean()
    late = float(freq.get("Late Night", 0))
    dinner = float(freq.get("Dinner", 1e-9))
    if dinner > 0 and late >= 0.7 * dinner:
        ideas.append("Youth culture & the rise of Bengaluru’s late‑night food economy (data-backed).")

    # Healthy share
    healthy_share = (survey["cuisine_preference"].eq("Healthy").mean())*100
    if healthy_share >= 12:
        ideas.append("The subscription salad: Bengaluru’s health-focused eating habits are mainstreaming.")

    # Regional comfort foods
    cuisine_share = survey["cuisine_preference"].value_counts(normalize=True)
    ni = float(cuisine_share.get("North Indian", 0))
    si = float(cuisine_share.get("South Indian", 0))
    if (ni + si) >= 0.40:
        ideas.append("Regional comfort foods still rule delivery menus despite fusion trends.")

    # Trends uplift (late night / healthy)
    for kw in ["late night food bangalore", "healthy meal subscription"]:
        kw_df = trends[trends["keyword"].str.lower().eq(kw)]
        if len(kw_df) >= 2 and kw_df["search_volume_index"].iloc[-1] > kw_df["search_volume_index"].iloc[0]:
            if "late night" in kw:
                ideas.append("Search interest in 'late night food' is trending up — timing is right for a culture piece.")
            if "healthy" in kw:
                ideas.append("Rising search interest in healthy meal subscriptions suggests a subscription‑economy angle.")
    if not ideas:
        ideas.append("Dinner still dominates: explore the battle for prime meal‑time mindshare.")
    return ideas

def main():
    base = Path(__file__).resolve().parents[1]
    survey, trends = load_data(base)
    ideas = story_recommendations(survey, trends)
    print("\n".join(f"- {i}" for i in ideas))

if __name__ == "__main__":
    main()
