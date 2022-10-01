# Alerting Setup

Creating and delaing with alerts

## Notifications
formerly Destinations

### Python Webhook Receiver
- Set up a simple Python webhook so we have a place to send Alerts
  - Navigate to [Python Webhook](https://github.com/macatak/python/blob/master/webhookRecv.py) and run the code in a terminal window
  - This will run a Flask webhook on 127.0.0.1:5000 that will echo any text or ctx values passed
  
### Dev Tools
- List supported Notification Channel types
  - GET /_plugins/_notifications/features  
- List active notification channels
  - GET _plugins/_notifications/configs  
- Create a Notfication channel that uses the Python webhook
- <coode>POST /_plugins/_notifications/configs/
{
  "config_id": "notification_api_1",
  "name": "webhook_notify_api1",
  "config": {
    "name": "Sample webhook Channel",
    "description": "webhook channel from API",
    "config_type": "webhook",
    "is_enabled": true,
    "webhook": {
      "url": "http://127.0.0.1:5000"
    }
  }
}</code>
### cURL command

