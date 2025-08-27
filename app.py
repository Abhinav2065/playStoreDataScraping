from flask import Flask, render_template, request, jsonify
from google_play_scraper import app

app_flask = Flask(__name__)

# Store app data globally (for demo purposes)
app_data = {}
current_app_id = ""

@app_flask.route('/')
def index():
    return render_template('index.html')

@app_flask.route('/get_app_data', methods=['POST'])
def get_app_data():
    global app_data, current_app_id
    
    try:
        app_url = request.form['app_url']
        app_id = app_url.split('id=')[1].split('&')[0]  # Extract clean app ID
        current_app_id = app_id
        
        # Get app data from Google Play
        app_data = app(
            app_id,
            lang='en',
            country='us'
        )
        
        return jsonify({
            'success': True,
            'app_id': app_id,
            'app_name': app_data.get('title', 'Unknown App')
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app_flask.route('/get_installs')
def get_installs():
    global app_data
    try:
        installs = app_data.get("realInstalls", "N/A")
        return jsonify({
            'success': True,
            'installs': f"{installs:,}" if isinstance(installs, int) else installs
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app_flask.route('/get_reviews')
def get_reviews():
    global app_data
    try:
        review_score = app_data.get("score", "N/A")
        return jsonify({
            'success': True,
            'review_score': review_score,
            'review_count': f"{app_data.get('ratings', 0):,}"
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app_flask.run(debug=True)