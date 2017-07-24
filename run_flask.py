from flask import Flask, render_template

from odds.config import CONFIG, test_token
from odds.api import telegram
from odds.scraper import scrape

app = Flask(__name__)
s = scrape()
t = telegram(token=test_token)


@app.route('/')
def index():
    return render_template('index.html')


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


if __name__ == "__main__":
    app.run(debug=True)
