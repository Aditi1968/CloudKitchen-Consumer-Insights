
-- Founders outreach CRM
CREATE TABLE founder_outreach (
    founder_id INT PRIMARY KEY,
    name VARCHAR(100),
    company VARCHAR(100),
    email VARCHAR(120),
    segment_focus VARCHAR(30),
    status VARCHAR(30),
    preferred_mode VARCHAR(30),
    meeting_date DATE
);

-- To seed data from CSV (adjust path):
-- LOAD DATA LOCAL INFILE 'PATH/TO/founders_list.csv'
-- INTO TABLE founder_outreach
-- FIELDS TERMINATED BY ','
-- ENCLOSED BY '"'
-- IGNORE 1 LINES
-- (founder_id, name, company, email, segment_focus, status, preferred_mode, @meeting_date)
-- SET meeting_date = NULLIF(@meeting_date, '');

-- Follow-ups needed
SELECT name, company, email FROM founder_outreach WHERE status='contacted';

-- Calendar for upcoming 14 days
SELECT name, company, preferred_mode, meeting_date
FROM founder_outreach
WHERE meeting_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 14 DAY)
ORDER BY meeting_date;
