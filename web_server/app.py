from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Path to the JSON file where feed details are stored
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
    if request.method == 'POST':
        feeds_data = read_feeds()
        
        if 'delete' in request.form:
            feed_number_to_delete = int(request.form.get('delete'))
            feeds_data['feeds'] = [feed for feed in feeds_data['feeds'] if feed['feed_number'] != feed_number_to_delete]
        
        elif 'add_feed' in request.form:
            new_feed = {
                "feed_number": len(feeds_data['feeds']) + 1,
                "start_time": request.form.get('start_time'),
                "end_time": request.form.get('end_time'),
                "amount": float(request.form.get('amount'))
            }
            feeds_data['feeds'].append(new_feed)
        
        feeds_data['autodispense'] = 1 if 'autodispense' in request.form else 0
        
        write_feeds(feeds_data)
        
        return redirect(url_for('index'))

    feeds_data = read_feeds()
    return render_template('index.html', feeds=feeds_data['feeds'], autodispense=feeds_data['autodispense'])

if __name__ == '__main__':
    app.run(debug=True)
