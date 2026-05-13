# GitHub Webhook Setup for Auto-Sync

This guide explains how to set up automatic synchronization between your GitHub repository and agentskill.sh.

## Why Set Up Auto-Sync?

- **Daily sync** (automatic): agentskill.sh checks for changes every 24 hours
- **Instant sync** (recommended): Updates appear immediately after `git push`

## Setup Instructions

1. Navigate to your GitHub repository
2. Go to **Settings** → **Webhooks** → **Add webhook**
3. Configure the webhook:
   - **Payload URL**: Obtain from agentskill.sh submission page after submitting your repository
   - **Content type**: `application/json`
   - **Secret**: Leave empty or use value provided by agentskill.sh
   - **Which events**: Select "Just the push event"
   - **Active**: Checked
4. Click **Add webhook** to save

## Verification

After setup, make a test push to your repository and verify the skill updates on agentskill.sh within minutes.

## Troubleshooting

- If syncs fail, check the webhook delivery logs in GitHub Settings → Webhooks → [Your webhook] → Recent Deliveries
- Ensure the Payload URL is correct and accessible
