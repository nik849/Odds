import time

from flask import Flask, render_template, request

from odds.api import telegram
from odds.config import CONFIG, test_token
from odds.scraper import scrape

app = Flask(__name__)
s = scrape()
t = telegram(token=test_token)


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        data = request.json
        print(data)
        return render_template('/index.html')
    elif request.method == 'GET':
        return render_template('/index.html')


@app.route('/index.html', methods=['POST', 'GET'])
def index():
    return render_template('/index.html')


@app.route('/basic_table.html', methods=['POST', 'GET'])
def raw_data():
    r = s.get_odds()
    with app.app_context():
        return render_template('/basic_table.html', tables=[r])


@app.route('/responsive_table.html', methods=['POST', 'GET'])
def filtered_data():
    r = s.get_odds(CONFIG)
    with app.app_context():
        return render_template('/responsive_table.html', tables=[r])


@app.route('/config.html', methods=['POST', 'GET'])
def config():
    return render_template('/config.html')


@app.route('/download', methods=['POST', 'GET'])
def download():
    r = s.download(CONFIG)
    r.to_csv('download_{}.csv'.format(time.strftime("%Y-%m-%d_%H-%M")))
    return (''), 204


if __name__ == "__main__":
    app.run(debug=True)
