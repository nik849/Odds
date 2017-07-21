import aiohttp
import asyncio

from flask import *
from odds.scraper import scrape

app = Flask(__name__)


s = scrape()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/basic_table.html', methods = ['POST', 'GET'])
def raw_data():
    r = s._get()
    with app.app_context():
        return render_template('/table_results.html', result=r)


if __name__ == "__main__":
    app.run(debug=True)
