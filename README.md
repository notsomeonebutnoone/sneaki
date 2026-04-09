email: hip145944@gmail.com
username: notsomeonebutnoone

# AI-Powered Activity to Google Calendar

This project automatically logs your computer activity into Google Calendar with task categorization and productivity scoring, using AI to process application/window activity data.

It captures activity from a webhook, extracts relevant details using an AI (like Ollama), and creates structured Google Calendar events.

---

## Features

- Logs application usage, window title, and URL.
- Extracts task and category information using AI.
- Computes a productivity score for each activity.
- Creates Google Calendar events automatically.
- Handles missing data gracefully (shows "N/A" if task/score/URL unavailable).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Webhook Setup](#webhook-setup)
5. [Code Overview](#code-overview)
6. [Running the Node](#running-the-node)
7. [Sample Output](#sample-output)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, make sure you have the following:

- Node.js >= 18
- Access to a Google account with Calendar enabled
- A webhook source sending activity data (e.g., browser extension, Zen Browser, or custom logger)
- Optional: Ollama AI API or any AI capable of returning JSON task categorization

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/activity-to-google-calendar.git
cd activity-to-google-calendar
```

2. Install dependencies:

```bash
npm install
```

3. Set up Google API credentials:

- Go to Google Cloud Console.
- Create a new project.
- Enable the Google Calendar API.
- Create OAuth 2.0 credentials (Service Account or OAuth Client ID).
- Download the credentials JSON and save it in your project folder.

---

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following:

```
GOOGLE_CREDENTIALS=./credentials.json
GOOGLE_CALENDAR_ID=primary
WEBHOOK_PORT=5678
```

- `GOOGLE_CREDENTIALS` → Path to the Google credentials JSON.
- `GOOGLE_CALENDAR_ID` → Calendar where events will be created (default: `primary`).
- `WEBHOOK_PORT` → Port to listen for incoming webhook events.

### AI Configuration (Optional)

If using Ollama or another AI API, configure your API endpoint and model:

```
AI_ENDPOINT=http://localhost:11434
AI_MODEL=ollama-model
```

---

## Webhook Setup

Your AI or logging system needs to send activity data in JSON format via a webhook.

Example JSON payload:

```json
{
  "app_name": "Google Chrome",
  "window_title": "YouTube - funny cat video",
  "url": "https://youtube.com/watch?v=abc123",
  "duration_seconds": 180,
  "timestamp": "2026-04-07T21:30:00"
}
```

- `app_name` → Name of the application.
- `window_title` → Current window title.
- `url` → URL of the active tab (if applicable).
- `duration_seconds` → Duration of the activity in seconds.
- `timestamp` → ISO 8601 timestamp when activity started.

---

## Code Overview

The main workflow:

1. Receive Webhook Data
2. Capture activity data from a webhook.
3. Process AI Response
4. Parse AI JSON to extract task name, category, and productivity score.
5. Compute Event Duration
6. Convert `duration_seconds` to start and end timestamps.
7. Build Calendar Event
8. Create a structured Google Calendar event:

Title: `{Task Category} — {Window Title} ({Minutes} min)`

Description:

```
App: {app_name}
URL: {url}
Task: {task_name}
Productivity Score: {productivity_score}
```

9. Send to Google Calendar
10. Push the event to the configured Google Calendar.

---

## Running the Node

Start the Node.js process:

```bash
node index.js
```

It will listen for incoming webhook activity and automatically push events to Google Calendar.

---

## Sample Output

Google Calendar Event Example:

Title: `Task — YouTube - funny cat video (3 min)`

Description:

```
App: Google Chrome
URL: https://youtube.com/watch?v=abc123
Task: YouTube - funny cat video
Productivity Score: 85
```

Start: `2026-04-07T21:30:00Z`  
End: `2026-04-07T21:33:00Z`

---

## Troubleshooting

- Task shows N/A:
  Ensure AI response JSON includes `task_name`.
- Productivity Score stuck at default:
  Check AI output JSON includes `productivity_score`.
- URL not visible:
  Make sure the webhook payload includes the `url` field.
- Google Calendar errors:
  Confirm OAuth credentials are correct and Calendar API is enabled.
