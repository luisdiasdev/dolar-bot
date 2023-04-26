# Dolar Bot

## Objective

Get notified on Telegram throughout the day if USD/BRL rate is up/down by at least a given threshold (defaults to 1%) compared to the last day.

## Technical Details

- Use [OpenExchangeRates](https://openexchangerates.org) API (free tier)
- Limited to 1.000 requests/month (need to use it wisely)
  - Estimated usage:
    - 10 hours/day - check every 45 minutes
    - 600/45 = 13,333 requests per day
    - 14 requests * 22 working days (approx.) = 308 requests on avg
    - If you change the schedule interval, it'll require more API calls
- Only runs during working days & hours (Mon-Fri - 9am-7pm)
  - If it was on Weekend (Saturday/Sunday) - compare with Friday instead
- Checks historical value (last day) to compare against.

## Running

1. Make sure to Docker and Docker Compose installed
2. Prepare `.env` file:
  - `cp .env.example .env`
  - Fill with your settings, more details below.
3. Run: `docker compose up`

## Debugging

There are VSCode settings for debugging in place, just open with VSCode and make sure to have Docker Plugin.

### Environment variables

| **Environment Variable** | **Description**                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------|
| `OXR_APP_ID`             | The OpenExchangeRates App ID                                                               |
| `TELEGRAM_TOKEN`         | The Telegram Bot Token provided by `@botfather`                                            |
| `TELEGRAM_CHAT_ID`       | The Telegram Chat where the Bot will send the message                                      |
| `USE_MOCK_OXR_API`       | If you want to test something and don't want to use your OXR API calls, set this to `true` |
| `RUN_INTERVAL`           | Interval in minutes which the check should run. Defaults to `25`.                          |
| `DIFF_THRESHOLD`         | The percentage difference to trigger the alert message.                                    |
| `APP_LOCALE`         | The locale for the application logs & messages (available values: `en,pt`).                                    |
