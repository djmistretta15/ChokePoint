"""
Web API Server for Tollbooth Seeker
Serves signal data to the frontend dashboard
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import asyncio
from datetime import datetime

from database import SignalDatabase
from signal_detector import SignalDetector

app = Flask(__name__, static_folder='web', static_url_path='')
CORS(app)

# Initialize components
db = SignalDatabase('data/signals.db')

@app.route('/')
def index():
    """Serve the main dashboard"""
    return send_from_directory('web', 'index.html')

@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard statistics"""
    stats = db.get_dashboard_stats()
    return jsonify(stats)

@app.route('/api/signals')
def get_signals():
    """Get active signals"""
    limit = 50
    signals = db.get_active_signals(limit)
    return jsonify(signals)

@app.route('/api/signals/high-priority')
def get_high_priority():
    """Get high-priority signals"""
    signals = db.get_high_priority_signals(8.5)
    return jsonify(signals)

@app.route('/api/signals/sector/<sector>')
def get_sector_signals(sector):
    """Get signals for a specific sector"""
    signals = db.get_signals_by_sector(sector)
    return jsonify(signals)

@app.route('/api/sectors')
def get_sectors():
    """Get sector statistics"""
    stats = db.get_sector_stats()
    return jsonify(stats)

@app.route('/api/watchlist')
def get_watchlist():
    """Get watchlisted signals"""
    signals = db.get_watchlist()
    return jsonify(signals)

@app.route('/api/watchlist/add/<int:signal_id>', methods=['POST'])
def add_to_watchlist(signal_id):
    """Add signal to watchlist"""
    db.add_to_watchlist(signal_id, "Added from web interface")
    return jsonify({'status': 'success'})

@app.route('/api/signal/<int:signal_id>/archive', methods=['POST'])
def archive_signal(signal_id):
    """Archive a signal"""
    db.archive_signal(signal_id, "Archived from web interface")
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    print("\n" + "="*80)
    print("⚡ TOLLBOOTH SEEKER - WEB DASHBOARD")
    print("="*80)
    print("\nStarting web server...")
    print("Dashboard: http://localhost:5000")
    print("API: http://localhost:5000/api/dashboard")
    print("\nPress Ctrl+C to stop")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
