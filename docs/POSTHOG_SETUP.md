# PostHog Analytics Setup

This document describes how PostHog analytics is integrated into Palabrai.com for tracking user behavior, retention, and product insights.

## Overview

PostHog is integrated to track:
- **User identification**: Track individual users across sessions
- **Event tracking**: Capture all major user actions
- **Retention analysis**: Understand Day 1, Day 7, Day 30 retention
- **Session recordings**: Optional visual playback of user sessions
- **Feature flags**: A/B testing capabilities (future use)

## Setup Instructions

### 1. Create PostHog Account

1. Sign up at [https://posthog.com](https://posthog.com)
2. Create a new project
3. Copy your Project API Key from Settings

### 2. Configure Environment Variables

Add the following to your `.env` file:

```bash
# Analytics Configuration (PostHog)
POSTHOG_API_KEY=phc_your_api_key_here
POSTHOG_HOST=https://eu.i.posthog.com  # Use https://app.posthog.com for US, https://eu.i.posthog.com for EU
```

For production (EC2 server), add these to your `/etc/environment` or systemd service file.

### 3. Verify Integration

After deploying with the PostHog API key:

1. Visit your site and perform some actions (create words, study, etc.)
2. Go to PostHog dashboard → Activity
3. You should see events appearing in real-time

## Events Being Tracked

### Authentication Events
- **`user_signed_up`**: New user registration
- **`user_logged_in`**: User login

### Word Management Events
- **`words_added`**: Bulk word creation
  - Properties: `count`, `duplicates`, `rejected`
- **`word_edited`**: Word update
  - Properties: `word_id`, `word_type`
- **`word_deleted`**: Word deletion
  - Properties: `word_id`

### Study Page Events
- **`study_session_started`**: User views a flashcard
  - Properties: `word_id`
- **`examples_generated`**: AI examples created
  - Properties: `word_id`, `example_count`
- **`word_learned`**: User marks word as learned
  - Properties: `word_id`
- **`word_unlearned`**: User unmarks learned word
  - Properties: `word_id`

### Revision Page Events
- **`revision_session_started`**: User views revision page
  - Properties: `word_id`
- **`sentence_revised`**: User submits sentence for feedback
  - Properties: `word_id`, `feedback_level`, `has_corrections`

## User Identification

PostHog automatically identifies authenticated users with:
- **User ID**: `current_user.id` (database ID)
- **Email**: `current_user.email`

This enables:
- Cohort analysis by user
- Retention tracking per user
- Session recordings tied to specific users

## Key Metrics to Track

### 1. Retention Analysis

In PostHog, create retention insights:

**Day 1 Retention**:
- Initial event: `user_signed_up`
- Returning event: Any activity (study, create, revise)
- Period: 1 day

**Day 7 Retention**:
- Initial event: `user_signed_up`
- Returning event: Any activity
- Period: 7 days

**Day 30 Retention**:
- Initial event: `user_signed_up`
- Returning event: Any activity
- Period: 30 days

### 2. Activation Metrics

Track user activation:
- Users who create their first word
- Users who complete first study session
- Users who mark first word as learned

### 3. Engagement Metrics

Monitor engagement:
- Average words added per user
- Study sessions per user per week
- Revision sentences per user

### 4. Feature Usage

Track feature adoption:
- Create page usage
- Study page usage
- Revise page usage
- Filter usage patterns

## Creating PostHog Dashboards

### Dashboard 1: User Acquisition & Activation

**Metrics**:
1. Total signups (trend over time)
2. Day 1 retention rate
3. Users who added first word (activation %)
4. Users who completed first study session

### Dashboard 2: Engagement

**Metrics**:
1. Daily active users (DAU)
2. Weekly active users (WAU)
3. Average words added per user
4. Average study sessions per active user
5. Revision sentences submitted per day

### Dashboard 3: Retention

**Metrics**:
1. Day 1, 7, 30 retention curves
2. Cohort retention table
3. Churned users (no activity in 14 days)
4. Reactivated users

## Privacy Considerations

PostHog setup includes:
- User email (for identification)
- User actions (events)
- No sensitive data (passwords, API keys, etc.)

To anonymize further, you can:
1. Hash user IDs before sending
2. Remove email from identification
3. Disable session recordings

## Troubleshooting

### Events not appearing in PostHog

1. Check browser console for errors
2. Verify `POSTHOG_API_KEY` is set correctly
3. Check if ad blockers are blocking PostHog
4. Verify `window.posthog` is defined in browser console

### User identification not working

1. Check if user is authenticated (`current_user.is_authenticated`)
2. Verify `posthog.identify()` is called after login
3. Check PostHog → Persons to see if users are being identified

### Events missing properties

1. Check event payload in browser Network tab (filter for `posthog`)
2. Verify properties are being passed in `posthog.capture()` calls
3. Check template variables are rendering correctly

## Advanced Features

### Session Recordings

Enable in PostHog settings:
1. Go to Settings → Recordings
2. Enable "Record user sessions"
3. Optionally mask sensitive inputs

### Feature Flags

Use for A/B testing:
```javascript
if (posthog.isFeatureEnabled('new-ui')) {
    // Show new UI
} else {
    // Show old UI
}
```

### Cohorts

Create user cohorts based on behavior:
- "Active learners": Users with 5+ study sessions
- "Word creators": Users who added 20+ words
- "At risk": No activity in 7 days

## Cost Management

PostHog free tier includes:
- 1M events/month
- Unlimited users
- 1 year data retention

To optimize costs:
- Use sampling for high-frequency events
- Archive old data
- Use event autocapture selectively

## Support

For issues with PostHog integration:
1. Check PostHog docs: [https://posthog.com/docs](https://posthog.com/docs)
2. PostHog community Slack
3. Check this repo's GitHub issues
