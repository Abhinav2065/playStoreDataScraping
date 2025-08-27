from flask import Flask, render_template, request, jsonify
from google_play_scraper import app
import os

# Initialize Flask app
app_flask = Flask(__name__)

# Store app data (in production, consider using Redis or database)
app_data = {}
current_app_id = ""

@app_flask.route('/')
def home():
    """Main page"""
    return render_template('index.html')

@app_flask.route('/get_app_data', methods=['POST'])
def get_app_data():
    """Fetch app data from Google Play Store"""
    global app_data, current_app_id
    
    try:
        app_url = request.form.get('app_url', '').strip()
        
        if not app_url:
            return jsonify({'success': False, 'error': 'Please enter a URL'})
            
        if 'id=' not in app_url:
            return jsonify({'success': False, 'error': 'URL must contain "id=" parameter'})
        
        # Extract app ID from URL
        app_id = url.split('id=')[1].split('&')[0]
        current_app_id = app_id
        
        # Fetch app data from Google Play
        app_data = app(
            app_id,
            lang='en',
            country='us'
        )
        
        return jsonify({
            'success': True,
            'app_id': app_id,
            'app_name': app_data.get('title', 'Unknown App'),
            'icon': app_data.get('icon', '')
        })
    
    except IndexError:
        return jsonify({'success': False, 'error': 'Invalid URL format'})
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error fetching app data: {str(e)}'})

@app_flask.route('/get_installs')
def get_installs():
    """Get install count"""
    try:
        if not app_data:
            return jsonify({'success': False, 'error': 'Please load app data first'})
            
        installs = app_data.get("realInstalls", "N/A")
        formatted_installs = f"{installs:,}" if isinstance(installs, int) else installs
        
        return jsonify({
            'success': True,
            'installs': formatted_installs,
            'app_name': app_data.get('title', 'Unknown App')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app_flask.route('/get_reviews')
def get_reviews():
    """Get review data"""
    try:
        if not app_data:
            return jsonify({'success': False, 'error': 'Please load app data first'})
            
        review_score = app_data.get("score", "N/A")
        review_count = app_data.get("ratings", 0)
        
        return jsonify({
            'success': True,
            'review_score': review_score,
            'review_count': f"{review_count:,}",
            'app_name': app_data.get('title', 'Unknown App')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app_flask.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({'status': 'healthy', 'message': 'Flask app is running'})

# Error handlers
@app_flask.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app_flask.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run in production mode
    app_flask.run(host='0.0.0.0', port=port, debug=False)