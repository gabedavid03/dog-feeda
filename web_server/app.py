from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

JSON_FILE_PATH = 'feeds.json'

def read_feeds():
    try:
        with open(JSON_FILE_PATH, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"feeds": [], "autodispense": 0}

def write_feeds(data):
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    feeds_data = read_feeds()

    if request.method == 'POST':
        if 'add_feed' in request.form:
            new_feed = {
                "feed_number": len(feeds_data['feeds']) + 1,
                "start_time": request.form.get('start_time'),
                "end_time": request.form.get('end_time'),
                "amount": float(request.form.get('amount')),
                "completed": 0
            }
            feeds_data['feeds'].append(new_feed)

        elif 'delete' in request.form:
            feed_number_to_delete = int(request.form.get('delete'))
            feeds_data['feeds'] = [feed for feed in feeds_data['feeds'] if feed['feed_number'] != feed_number_to_delete]

        elif 'feed_now' in request.form:
                    feeds_data['feed_now'] = {
                        "valid": 1,
                        "amount": float(request.form.get('feed_now_amount'))
                    }

        feeds_data['autodispense'] = 1 if 'autodispense' in request.form else 0

        write_feeds(feeds_data)
        return redirect(url_for('index'))

    return render_template('index.html', feeds=feeds_data['feeds'], autodispense=feeds_data['autodispense'], feed_now=feeds_data.get('feed_now', {'valid': 0, 'amount': 0}))

if __name__ == '__main__':
    app.run(debug=True)
