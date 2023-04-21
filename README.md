# Dolar Bot

## Objective

Get notified on Telegram throughout the day if USD/BRL rate is up/down by at least a given threshold (defaults to 1%) compared to the last day.

## Technical Details

- Use OpenExchangeRates API (free tier)
- Limited to 1.000 requests/month (need to use it wisely)
  - Estimated usage:
    - 10 hours/day - check every 45 minutes
    - 600/45 = 13,333 requests per day
    - 14 requests * 22 working days (approx.) = 308 requests on avg
    - If you change the schedule interval, it'll require more API calls
- Only runs during working days & hours (Mon-Fri - 9am-7pm)
  - If it was on Weekend (Saturday/Sunday) - compare with Friday instead
- Checks historical value (last day) to compare against.
