#!/usr/bin/env python3
from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from src.story_engine import story_recommendations
import sys

# Make sure repo root is in sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.story_engine import story_recommendations

st.set_page_config(page_title="Consumer Insights – Cloud Kitchens (Bengaluru)", layout="wide")

BASE = Path(__file__).resolve().parents[1]

@st.cache_data
def load_data():
    survey = pd.read_csv(BASE/"data"/"raw_survey_data.csv")
    founders = pd.read_csv(BASE/"data"/"founders_list.csv")
    meetings = pd.read_csv(BASE/"data"/"meetings_schedule.csv")
    trends = pd.read_csv(BASE/"data"/"ga_mock_trends.csv", parse_dates=["week_start"])
    return survey, founders, meetings, trends

survey, founders, meetings, trends = load_data()

st.title("Consumer Insights & Media Engagement – Bengaluru Cloud Kitchens")

with st.sidebar:
    st.header("Filters")
    age_filter = st.multiselect("Age group", sorted(survey["age_group"].unique().tolist()))
    time_filter = st.multiselect("Order time", sorted(survey["order_time"].unique().tolist()))
    cuisine_filter = st.multiselect("Cuisine", sorted(survey["cuisine_preference"].unique().tolist()))
    kw_filter = st.multiselect("Trend Keywords", sorted(trends["keyword"].unique().tolist()))

    df = survey.copy()
    if age_filter: df = df[df["age_group"].isin(age_filter)]
    if time_filter: df = df[df["order_time"].isin(time_filter)]
    if cuisine_filter: df = df[df["cuisine_preference"].isin(cuisine_filter)]
    trends_df = trends.copy()
    if kw_filter: trends_df = trends_df[trends_df["keyword"].isin(kw_filter)]

    st.caption("Download filtered survey CSV")
    st.download_button("Download CSV", df.to_csv(index=False), file_name="filtered_survey.csv")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "Personas & Segments", "Story Ideas", "Founder CRM", "Meetings Calendar"
])

with tab1:
    st.subheader("Overview")
    c1, c2, c3 = st.columns([1.1, 1.1, 1.0], gap="large")

    with c1:
        spend = df.groupby("age_group", as_index=False)["avg_spend_inr"].mean()
        fig = px.bar(spend, x="age_group", y="avg_spend_inr", title="Avg Spend (INR) by Age Group")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        freq = df.groupby("order_time", as_index=False)["order_frequency_per_week"].mean()
        fig2 = px.bar(freq, x="order_time", y="order_frequency_per_week", title="Avg Orders/Week by Time of Day")
        st.plotly_chart(fig2, use_container_width=True)

    with c3:
        cuisine_counts = df["cuisine_preference"].value_counts().rename_axis("cuisine_preference").reset_index(name="count")
        fig3 = px.pie(cuisine_counts, names="cuisine_preference", values="count", title="Cuisine Preference Share")
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")
    st.subheader("Search Trends (All Keywords or Selected)")
    trend_plot = trends_df.groupby("week_start", as_index=False)["search_volume_index"].sum()
    fig4 = px.line(trend_plot, x="week_start", y="search_volume_index", markers=True, title="Search Volume Index Over Time")
    st.plotly_chart(fig4, use_container_width=True)

with tab2:
    st.subheader("Personas & Segments")
    st.write("""
- **Late‑Night Coder**: 22–28, frequent late-night orders, value pricing.  
- **Health‑Conscious Professional**: 25–35, subscriptions, salads/grilled.  
- **Family Meal Planner**: 30–40, weekend bulk orders, North Indian combos.
    """)
    left, right = st.columns([1.2, 1])
    with left:
        pivot = pd.pivot_table(df, index="age_group", columns="order_time", values="order_frequency_per_week", aggfunc="mean").round(2)
        st.dataframe(pivot, use_container_width=True)
    with right:
        st.metric("Subscription %", f"{(df['uses_subscription'].mean()*100):.1f}%")
        st.metric("Veg Preference %", f"{(df['prefers_veg'].mean()*100):.1f}%")
        st.metric("Top Cuisine", df["cuisine_preference"].value_counts().idxmax())

with tab3:
    st.subheader("Newsroom Story Ideas (Rule‑based)")
    ideas = story_recommendations(df, trends_df)
    for idea in ideas:
        st.success(idea)

    st.markdown("### Pitch Email Generator")
    founder_names = ["(generic)"] + founders["name"].tolist()
    target = st.selectbox("Recipient", founder_names)
    company = ""
    if target != "(generic)":
        row = founders[founders["name"].eq(target)].iloc[0]
        company = row["company"]

    segment = st.selectbox("Angle", ["Late Night", "Healthy", "Family", "Budget", "Premium"])
    template = f"""
Subject: Quick chat about Bengaluru’s {segment.lower()} food trends

Hi {target if target!='(generic)' else 'there'},

I’ve been mapping delivery trends in Bengaluru and noticed a strong {segment.lower()} signal in recent weeks.
I’m speaking with a few operators like {company or 'leading cloud‑kitchen teams'} to understand what’s working.

Would you be open to a quick 15–20 min chat this week? Happy to share a short summary of my findings.

Thanks,
[Your Name]
"""
    st.code(template.strip())

with tab4:
    st.subheader("Founder CRM")
    status = st.multiselect("Status", sorted(founders["status"].unique().tolist()))
    crm = founders.copy()
    if status: crm = crm[crm["status"].isin(status)]
    st.dataframe(crm, use_container_width=True)
    st.caption("Export current view")
    st.download_button("Download CSV", crm.to_csv(index=False), file_name="founder_crm_filtered.csv")

with tab5:
    st.subheader("Meetings Calendar (Next 45 days)")
    if meetings.empty:
        st.info("No meetings scheduled yet. Change filters or update CRM.")
    else:
        meetings["meeting_date"] = pd.to_datetime(meetings["meeting_date"], errors="coerce")
        upcoming = meetings.sort_values("meeting_date")
        st.dataframe(upcoming, use_container_width=True)
        st.caption("Pro tip: paste this CSV into Google Calendar or Outlook import.")

st.markdown("---")
st.caption("Tip: Run `python src/generate_data.py` to refresh data. Then reload the app.")
