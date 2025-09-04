# Consumer Insights & Media Engagement Dashboard (Bengaluru – Cloud Kitchens)

This repository analyzes consumer segments for Bengaluru’s cloud-kitchen ecosystem and creates a media-focused insight layer, including a simple rules-based story recommender.

## Folder Structure
- `data/` – raw survey, founders list, meetings schedule, GA mock trends
- `analysis/` – Excel workbook with summaries & charts
- `sql/` – MySQL-ready schema & queries for segmentation and CRM
- `docs/` – Outreach scripts, insights report, personas, story ideas
- `dashboard/` – Steps to build the Power BI dashboard locally

## Quick Start
1. Open `analysis/consumer_segments.xlsx` for charts & summaries.
2. Load `sql/segment_queries.sql` and `sql/crm_meetings.sql` in MySQL (enable LOCAL INFILE if using CSV imports).
3. In Power BI, follow `dashboard/PowerBI_instructions.md`.
4. Share `docs/insights_report.md` with stakeholders; tailor `docs/outreach_email_samples.md` as needed.

## Notes
- Data is simulated for a realistic demo.
- Update CSVs with your own survey responses for better accuracy.
