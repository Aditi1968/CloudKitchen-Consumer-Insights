# Power BI Dashboard – Build Steps

1) Open Power BI Desktop → Get Data → CSV
   - Import `data/raw_survey_data.csv`
   - Import `data/ga_mock_trends.csv`

2) Create visuals:
   - **Heatmap:** `order_time` vs `order_frequency_per_week` (Matrix + conditional formatting).
   - **Bar Chart:** Avg `avg_spend_inr` by `age_group`.
   - **Pie Chart:** `cuisine_preference` distribution.
   - **Line Chart:** GA `search_volume_index` over `week_start` for selected keywords.

3) DAX (examples):
   - `Avg Spend = AVERAGE(survey[avg_spend_inr])`
   - `Orders/Week = AVERAGE(survey[order_frequency_per_week])`
   - `LateNight Share = DIVIDE( CALCULATE( [Orders/Week], survey[order_time]="Late Night" ), CALCULATE( [Orders/Week], survey[order_time]="Dinner" ))`

4) Story Panel:
   - Use KPI cards + text box to summarize “What to publish this week.”

5) Publish:
   - Save as `dashboard/cloud_kitchen_dashboard.pbix`.
