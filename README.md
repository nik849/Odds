# Odds
Web scraping, data gathering from online odds
Requires Python 3.6+

Getting Started
==================
  * Installation:
```
  pip install -r requirements
```
  * Run ngrok:
```
  ./ngrok http 5000
```
  * Set up webhook:
Copy the ```https://...``` from ngrok to ```config.py -> WEBHOOK_URL```

  * Set up the Bot:
Replace test_token in ```config.py```  with your Telegram token, from when
you set up the bot with BotFather on Telegram.

  * Run the WebApp:
```python run_flask.py```
