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

### cURL command

