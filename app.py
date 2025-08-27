from flask import Flask, render_template, request, jsonify
from google_play_scraper import app

app_flask = Flask(__name__)

# Store app data in session instead of global
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
        if 'id=' not in app_url:
            return jsonify({'success': False, 'error': 'URL must contain id='})
            
        app_id = app_url.split('id=')[1].split('&')[0]
        current_app_id = app_id
        
        app_data = app(app_id, lang='en', country='us')
        
        return jsonify({
            'success': True,
            'app_id': app_id,
            'app_name': app_data.get('title', 'Unknown App')
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app_flask.route('/get_installs')
def get_installs():
    try:
        installs = app_data.get("realInstalls", "N/A")
        return jsonify({
            'success': True,
            'installs': f"{installs:,}" if isinstance(installs, int) else installs
        })
    except:
        return jsonify({'success': False, 'error': 'Load app data first'})

@app_flask.route('/get_reviews')
def get_reviews():
    try:
        review_score = app_data.get("score", "N/A")
        return jsonify({
            'success': True,
            'review_score': review_score,
            'review_count': f"{app_data.get('ratings', 0):,}"
        })
    except:
        return jsonify({'success': False, 'error': 'Load app data first'})

if __name__ == '__main__':
    app_flask.run(debug=False)  # Set debug=False for production