import atexit
import time

import pandas
from apscheduler.scheduler import Scheduler
from flask import Flask, render_template, request, session

from odds.api import telegram
from odds.config import CONFIG, configs, telegram_id, test_token, tips
from odds.scraper import scrape
from odds.utils import predictions

app = Flask(__name__)
app.secret_key = 'key'
cron = Scheduler(daemon=True)
s = scrape()
t = telegram(token=test_token)
values = [0, 0, 0, 0, 0]
cron.start()


@app.route('/', methods=['POST', 'GET'])
def home():
    global values
    games = s.get_odds_obj()
    del games['Last 200 Started Games - Odds From 188bet.com']
    tables = []
    tips_page = []
    for name, game in games.items():
        print(name)
        p = predictions(game)
        data, preds = p.return_predictions()
        tables.append(data)
        game_time = data.ix[data.index[1], 0]
        checks = session.get('checks_', None)
        if checks:
            for key in checks:
                if preds[key] != 0:
                    tip = f'{game_time} : {name} - {tips[key]}'
                    tips_page.append(tip)
                    [t.send_message(tip, _id) for _id in telegram_id]
    df = pandas.DataFrame()
    for table in tables:
        df = df.append(table)
    session['tips_page'] = tips_page
    labels = ['00:00', '00:15', '00:30', '00:45', '01:00']
    values.append(len(tips_page))
    if len(values) > 5:
        del values[0]
    session['labels'] = labels
    session['values'] = values
    return render_template('/index.html',
                           tips=tips_page, labels=labels, values=values)


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    tips_page = session.get('tips_page')
    labels = session.get('labels')
    values = session.get('values')
    return render_template('/index.html',
                           tips=tips_page, labels=labels, values=values)


@app.route('/basic_table.html', methods=['POST', 'GET'])
def raw_data():
    r = s.get_odds_html()
    with app.app_context():
        return render_template('/basic_table.html', tables=r)


@app.route('/responsive_table.html', methods=['POST', 'GET'])
def filtered_data():
    games = s.get_odds_obj()
    del games['Last 200 Started Games - Odds From 188bet.com']
    tables = []
    for name, game in games.items():
        print(name)
        p = predictions(game)
        data, preds = p.return_predictions()
        data = data.to_html(classes="table table-hover")
        tables.append(data)
    tables = u''.join(tables)

    with app.app_context():
        return render_template('/responsive_table.html', tables=tables)


@app.route('/config.html', methods=['POST', 'GET'])
def config():
    return render_template('/config.html')


@app.route('/config_update', methods=['POST', 'GET'])
def config_update():
    checks = []
    for checkbox in configs:
        value = request.form.get(checkbox)
        if value:
            checks.append(checkbox)
        session['checks_'] = checks
    return render_template('/config.html', configs=checks, users=telegram_id)


@app.route('/user_update', methods=['POST', 'GET'])
def user_update():
    user = request.form.get("user_input")
    if request.form["submit"] == "add":
        if user:
            telegram_id.append(user)
            print(f'{user} added.')
    elif request.form["submit"] == "remove":
        if user in telegram_id:
            if user in telegram_id:
                telegram_id.remove(user)
                print(f'{user} removed.')
    checks = session.get('checks_', None)
    return render_template('/config.html', configs=checks, users=telegram_id)


@app.route('/download', methods=['POST', 'GET'])
def download():
    r = s.download(config=CONFIG)
    r.to_csv(f'download_{time.strftime("%Y-%m-%d_%H-%M")}.csv')
    return (''), 204


@app.route('/download_preds', methods=['POST', 'GET'])
def download_preds():
    games = s.get_odds_obj()
    del games['Last 200 Started Games - Odds From 188bet.com']
    tables = []
    for name, game in games.items():
        print(name)
        p = predictions(game)
        data, preds = p.return_predictions()
        tables.append(data)
    df = pandas.DataFrame()
    for table in tables:
        df = df.append(table)
    df.to_csv(f'download_preds{time.strftime("%Y-%m-%d_%H-%M")}.csv')
    return (''), 204


@app.route('/hook', methods=['POST', 'GET'])
def handle_messages():
    if request.method == 'POST':
        data = request.json
        text = {'user': data['message']['from']['id'],
                'message': data['message']['text']}
        result = t.process_message(text)
        reply = s.get_odds_obj(config=result)
        print(reply)
        t.send_message(reply, text['user'])
    return (''), 204


@cron.interval_schedule(minutes=15)
def interval_download():
    with app.test_request_context():
        games = s.get_odds_obj()
        del games['Last 200 Started Games - Odds From 188bet.com']
        tables = []
        tips_page = []
        for name, game in games.items():
            print(name)
            p = predictions(game)
            data, preds = p.return_predictions()
            tables.append(data)
            game_time = data.ix[data.index[1], 0]
            checks = session.get('checks_', None)
            if checks:
                for key in checks:
                    if preds[key] != 0:
                        tip = f'{game_time} : {name} - {tips[key]}'
                        tips_page.append(tip)
                        [t.send_message(tip, _id) for _id in telegram_id]
        df = pandas.DataFrame()
        for table in tables:
            df = df.append(table)
        df.to_csv(f'download_preds{time.strftime("%Y-%m-%d_%H-%M")}.csv')
        return (''), 204


atexit.register(lambda: cron.shutdown(wait=False))


if __name__ == "__main__":
    app.run(debug=True)
