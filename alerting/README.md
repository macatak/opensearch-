# Alerting Setup

Creating and dealing with alerts

## Notifications (
formerly Destinations which is deprecated

### Python Webhook Receiver
- Set up a simple Python webhook so we have a place to send Alerts
  - Navigate to [Python Webhook](https://github.com/macatak/python/blob/master/webhookRecv.py), download and run the code in a terminal window
  - This will run a Python Flask webhook on 127.0.0.1:5000 that will echo any text or ctx values passed
    - Does require Pyhon Flask package to be installed
  - Open this in a terminal and just let it run
  <code>python3 /*path to script*/webHookRecv.py</code>
  
### Dev Tools
*NOTE - View raw text to maintain Dev Tools formatting*

- List supported Notification Channel types  
  GET /_plugins/_notifications/features  

- List active notification channels  
  GET _plugins/_notifications/configs  

- Create a Notfication channel that uses the Python webhook
  
  POST /_plugins/_notifications/configs/
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
}


- Get the settings for the channel  

  GET _plugins/_notifications/configs/notification_api_1

- Update the channel
  
  PUT _plugins/_notifications/configs/notification_api_1
{
  "config": {
    "name": "webhook_notify_1",
    "description": "webhook channel from API",
    "config_type": "webhook",
    "is_enabled": true,
    "webhook": {
      "url": "http:127.0.0.1:5000"
    }
  }
}

- Send a test notification
- 
  GET _plugins/_notifications/feature/test/notification_api_1


- Delete the channel  

  DELETE /_plugins/_notifications/configs/notification_api_1


### cURL command

- List supported Notification Channel types
  curl -XGET -u admin:admin --insecure "https://localhost:9200/_plugins/_notifications/features"

- List active notification channels
  curl -XGET -u admin:admin --insecure "https://localhost:9200/_plugins/_notifications/configs"

- Create a Notfication channel that uses the Python webhook  
  curl -XPOST -u admin:admin --insecure "https://localhost:9200/_plugins/_notifications/configs/" -H 'Content-Type: application/json' -d'
{
    "config_id": "notification_curl_1",
    "name": "webhook_notify_curl1",
    "config": {
      "name": "Sample webhook Channel",
      "description": "webhook channel from cURL",
      "config_type": "webhook",
      "is_enabled": true,
      "webhook": {
        "url": "http://127.0.0.1:5000"
     }
  }
}'

- Get the settings for the channel  
  curl -XGET -u admin:admin --insecure "https://localhost:9200/_plugins/_notifications/configs/notification_curl_1"

- Send a test notification (should cause webhook receiver terminal to show data)
  curl -XGET -u admin:admin --insecure "https://localhost:9200/_plugins/_notifications/feature/test/notification_curl_1"
  
  
- Delete the channel  
