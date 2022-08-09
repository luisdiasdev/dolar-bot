# Dolar Bot

## Objective

Open Google with "dolar hoje" search when:

- Current USD/BRL rate is up by at least 5% compared to the previous day

## Technical Details

- Use OpenExchangeRates API (free tier)
- Limited to 1.000 requests/month (need to use it wisely)
  - 1000 requests / 22 working days = 45.45 requests/day
  - 45.45 requests / day = **5.68 requests / hour** (considering 8 hour work period)
  - 45 requests/day - 1 to grab the historical data (consider storing everything from the API into a DB)
  - 44 requests/8 hours = 5.5/hour
  - 1 request per 15 minutes = 4 requests/hour = 32 requests/day

- Previous Day
  - If it was on Weekend (Saturday/Sunday) - compare with Friday instead
