"""
Database Module - Tracks infrastructure signals over time
"""
import sqlite3
import logging
import json
from typing import List, Dict, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class SignalDatabase:
    def __init__(self, db_path: str = 'data/signals.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Signals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                source TEXT,
                sector TEXT,
                url TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                inevitability_score REAL,
                moat_score REAL,
                timing_score REAL,
                total_score REAL,
                toll_mechanism TEXT,
                breadcrumbs TEXT,
                early_movers TEXT,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Signal updates table (track score changes over time)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS signal_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_score REAL,
                notes TEXT,
                FOREIGN KEY (signal_id) REFERENCES signals(id)
            )
        ''')
        
        # Watchlist table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (signal_id) REFERENCES signals(id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_score ON signals(total_score DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_sector ON signals(sector)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_signals_timestamp ON signals(timestamp DESC)')
        
        conn.commit()
        conn.close()
        
        logger.info(f"Database initialized at {self.db_path}")
    
    def signal_exists(self, title: str, hours_window: int = 24) -> bool:
        """Check if similar signal already exists"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_time = datetime.now() - timedelta(hours=hours_window)
        
        cursor.execute('''
            SELECT COUNT(*) FROM signals 
            WHERE title = ? AND timestamp > ?
        ''', (title, cutoff_time))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
    
    def save_signal(self, signal_data: Dict) -> int:
        """Save a new signal to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO signals (
                title, description, source, sector, url,
                inevitability_score, moat_score, timing_score, total_score,
                toll_mechanism, breadcrumbs, early_movers
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            signal_data['title'],
            signal_data['description'],
            signal_data['source'],
            signal_data['sector'],
            signal_data['url'],
            signal_data['inevitability_score'],
            signal_data['moat_score'],
            signal_data['timing_score'],
            signal_data['total_score'],
            signal_data['toll_mechanism'],
            json.dumps(signal_data.get('breadcrumbs', [])),
            json.dumps(signal_data.get('early_movers', []))
        ))
        
        signal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return signal_id
    
    def get_active_signals(self, limit: int = 50) -> List[Dict]:
        """Get active signals sorted by score"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals 
            WHERE status = 'active'
            ORDER BY total_score DESC 
            LIMIT ?
        ''', (limit,))
        
        signals = []
        for row in cursor.fetchall():
            signal = dict(row)
            signal['breadcrumbs'] = json.loads(signal['breadcrumbs']) if signal['breadcrumbs'] else []
            signal['early_movers'] = json.loads(signal['early_movers']) if signal['early_movers'] else []
            signals.append(signal)
        
        conn.close()
        return signals
    
    def get_high_priority_signals(self, threshold: float = 8.5) -> List[Dict]:
        """Get high-priority signals above threshold"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals 
            WHERE status = 'active' AND total_score >= ?
            ORDER BY total_score DESC
        ''', (threshold,))
        
        signals = []
        for row in cursor.fetchall():
            signal = dict(row)
            signal['breadcrumbs'] = json.loads(signal['breadcrumbs']) if signal['breadcrumbs'] else []
            signal['early_movers'] = json.loads(signal['early_movers']) if signal['early_movers'] else []
            signals.append(signal)
        
        conn.close()
        return signals
    
    def get_signals_by_sector(self, sector: str) -> List[Dict]:
        """Get all signals for a specific sector"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM signals 
            WHERE status = 'active' AND sector = ?
            ORDER BY total_score DESC
        ''', (sector,))
        
        signals = []
        for row in cursor.fetchall():
            signal = dict(row)
            signal['breadcrumbs'] = json.loads(signal['breadcrumbs']) if signal['breadcrumbs'] else []
            signal['early_movers'] = json.loads(signal['early_movers']) if signal['early_movers'] else []
            signals.append(signal)
        
        conn.close()
        return signals
    
    def get_sector_stats(self) -> Dict[str, Dict]:
        """Get statistics by sector"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                sector,
                COUNT(*) as count,
                AVG(total_score) as avg_score,
                MAX(total_score) as max_score
            FROM signals 
            WHERE status = 'active'
            GROUP BY sector
            ORDER BY avg_score DESC
        ''')
        
        stats = {}
        for row in cursor.fetchall():
            stats[row[0]] = {
                'count': row[1],
                'avg_score': round(row[2], 2),
                'max_score': round(row[3], 2)
            }
        
        conn.close()
        return stats
    
    def update_signal_score(self, signal_id: int, new_score: float, notes: str = ""):
        """Update signal score and log the change"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update signal
        cursor.execute('''
            UPDATE signals 
            SET total_score = ?
            WHERE id = ?
        ''', (new_score, signal_id))
        
        # Log update
        cursor.execute('''
            INSERT INTO signal_updates (signal_id, total_score, notes)
            VALUES (?, ?, ?)
        ''', (signal_id, new_score, notes))
        
        conn.commit()
        conn.close()
    
    def add_to_watchlist(self, signal_id: int, notes: str = ""):
        """Add signal to watchlist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO watchlist (signal_id, notes)
            VALUES (?, ?)
        ''', (signal_id, notes))
        
        conn.commit()
        conn.close()
    
    def get_watchlist(self) -> List[Dict]:
        """Get all watchlisted signals"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.*, w.added_at as watchlist_added, w.notes as watchlist_notes
            FROM signals s
            JOIN watchlist w ON s.id = w.signal_id
            WHERE s.status = 'active'
            ORDER BY s.total_score DESC
        ''')
        
        signals = []
        for row in cursor.fetchall():
            signal = dict(row)
            signal['breadcrumbs'] = json.loads(signal['breadcrumbs']) if signal['breadcrumbs'] else []
            signal['early_movers'] = json.loads(signal['early_movers']) if signal['early_movers'] else []
            signals.append(signal)
        
        conn.close()
        return signals
    
    def archive_signal(self, signal_id: int, reason: str = ""):
        """Archive a signal (mark as inactive)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE signals 
            SET status = 'archived'
            WHERE id = ?
        ''', (signal_id,))
        
        if reason:
            cursor.execute('''
                INSERT INTO signal_updates (signal_id, notes)
                VALUES (?, ?)
            ''', (signal_id, f"Archived: {reason}"))
        
        conn.commit()
        conn.close()
    
    def get_dashboard_stats(self) -> Dict:
        """Get overall dashboard statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total active signals
        cursor.execute('SELECT COUNT(*) FROM signals WHERE status = "active"')
        active_count = cursor.fetchone()[0]
        
        # Average score
        cursor.execute('SELECT AVG(total_score) FROM signals WHERE status = "active"')
        avg_score = cursor.fetchone()[0] or 0.0
        
        # High priority count
        cursor.execute('SELECT COUNT(*) FROM signals WHERE status = "active" AND total_score >= 8.5')
        high_priority = cursor.fetchone()[0]
        
        # Hidden gems (good scores but low visibility)
        cursor.execute('''
            SELECT COUNT(*) FROM signals 
            WHERE status = "active" AND total_score >= 7.5 AND total_score < 8.5
        ''')
        hidden_gems = cursor.fetchone()[0]
        
        # Recent signals (last 24 hours)
        cutoff = datetime.now() - timedelta(hours=24)
        cursor.execute('SELECT COUNT(*) FROM signals WHERE timestamp > ?', (cutoff,))
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'active_signals': active_count,
            'avg_score': round(avg_score, 1),
            'high_priority': high_priority,
            'hidden_gems': hidden_gems,
            'recent_24h': recent_count
        }
