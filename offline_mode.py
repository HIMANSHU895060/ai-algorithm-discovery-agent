"""Offline Mode for AI Algorithm Discovery Agent
Allows running without internet/external dependencies.
Stores everything locally with SQLite.
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Any
import pickle


class OfflineDatabase:
    """Local SQLite database for offline storage"""
    
    def __init__(self, db_path: str = 'offline_data.db'):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.init_db()
    
    def init_db(self):
        """Initialize database with tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Discoveries table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS discoveries (
                id INTEGER PRIMARY KEY,
                problem_type TEXT,
                input_size INTEGER,
                algorithm TEXT,
                fitness_score REAL,
                timestamp TEXT,
                data TEXT
            )
        ''')
        
        # Algorithm performance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY,
                algorithm TEXT,
                test_cases_passed INTEGER,
                test_cases_total INTEGER,
                success_rate REAL,
                execution_time REAL,
                timestamp TEXT
            )
        ''')
        
        # User solutions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS solutions (
                id INTEGER PRIMARY KEY,
                problem_type TEXT,
                solution_code TEXT,
                language TEXT,
                timestamp TEXT,
                notes TEXT
            )
        ''')
        
        # Learning history
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_history (
                id INTEGER PRIMARY KEY,
                state TEXT,
                action TEXT,
                reward REAL,
                timestamp TEXT
            )
        ''')
        
        self.conn.commit()
    
    def save_discovery(self, discovery: Dict[str, Any]):
        """Save algorithm discovery"""
        self.cursor.execute('''
            INSERT INTO discoveries 
            (problem_type, input_size, algorithm, fitness_score, timestamp, data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            discovery.get('problem_type'),
            discovery.get('input_size'),
            discovery.get('selected_algorithm'),
            discovery.get('fitness_score'),
            datetime.now().isoformat(),
            json.dumps(discovery)
        ))
        self.conn.commit()
    
    def save_performance(self, perf: Dict[str, Any]):
        """Save algorithm performance metrics"""
        self.cursor.execute('''
            INSERT INTO performance
            (algorithm, test_cases_passed, test_cases_total, success_rate, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            perf.get('algorithm'),
            perf.get('passed_tests'),
            perf.get('failed_tests', 0) + perf.get('passed_tests', 0),
            perf.get('success_rate'),
            perf.get('avg_execution_time'),
            datetime.now().isoformat()
        ))
        self.conn.commit()
    
    def save_solution(self, problem_type: str, code: str, language: str = 'python', notes: str = ''):
        """Save user's problem solution"""
        self.cursor.execute('''
            INSERT INTO solutions (problem_type, solution_code, language, timestamp, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (problem_type, code, language, datetime.now().isoformat(), notes))
        self.conn.commit()
    
    def get_discoveries(self, limit: int = 10) -> List[Dict]:
        """Get recent discoveries"""
        self.cursor.execute('''
            SELECT * FROM discoveries ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = self.cursor.fetchall()
        return [{
            'id': row[0],
            'problem_type': row[1],
            'input_size': row[2],
            'algorithm': row[3],
            'fitness_score': row[4],
            'timestamp': row[5],
            'data': json.loads(row[6])
        } for row in rows]
    
    def get_solutions(self, problem_type: str = None) -> List[Dict]:
        """Get saved solutions"""
        if problem_type:
            self.cursor.execute('SELECT * FROM solutions WHERE problem_type = ?', (problem_type,))
        else:
            self.cursor.execute('SELECT * FROM solutions')
        
        rows = self.cursor.fetchall()
        return [{
            'id': row[0],
            'problem_type': row[1],
            'code': row[2],
            'language': row[3],
            'timestamp': row[4],
            'notes': row[5]
        } for row in rows]
    
    def get_performance_stats(self, algorithm: str = None) -> Dict[str, Any]:
        """Get performance statistics"""
        if algorithm:
            self.cursor.execute('''
                SELECT AVG(success_rate), AVG(execution_time), COUNT(*)
                FROM performance WHERE algorithm = ?
            ''', (algorithm,))
        else:
            self.cursor.execute('''
                SELECT AVG(success_rate), AVG(execution_time), COUNT(*)
                FROM performance
            ''')
        
        avg_success, avg_time, count = self.cursor.fetchone()
        return {
            'avg_success_rate': avg_success,
            'avg_execution_time': avg_time,
            'total_tests': count
        }
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


class OfflineCache:
    """In-memory cache with persistence"""
    
    def __init__(self, cache_file: str = 'cache.json'):
        self.cache_file = cache_file
        self.cache = self.load_cache()
    
    def load_cache(self) -> Dict:
        """Load cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Save cache to file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get(self, key: str) -> Any:
        """Get value from cache"""
        return self.cache.get(key)
    
    def set(self, key: str, value: Any):
        """Set value in cache"""
        self.cache[key] = value
        self.save_cache()
    
    def clear(self):
        """Clear cache"""
        self.cache = {}
        self.save_cache()


class OfflineMode:
    """Main offline mode manager"""
    
    def __init__(self):
        self.db = OfflineDatabase()
        self.cache = OfflineCache()
        self.is_offline = True
        self.sync_queue = []  # For syncing when online
    
    def enable_offline(self):
        """Enable offline mode"""
        self.is_offline = True
        return {'status': 'offline_enabled', 'message': 'Working in offline mode'}
    
    def disable_offline(self):
        """Disable offline mode"""
        self.is_offline = False
        return {'status': 'offline_disabled', 'message': 'Online mode enabled'}
    
    def save_for_sync(self, action: str, data: Dict):
        """Queue action for syncing when online"""
        self.sync_queue.append({
            'action': action,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_sync_queue(self) -> List[Dict]:
        """Get pending sync actions"""
        return self.sync_queue.copy()
    
    def clear_sync_queue(self):
        """Clear sync queue after successful sync"""
        self.sync_queue = []
    
    def get_offline_status(self) -> Dict[str, Any]:
        """Get offline mode status and stats"""
        perf_stats = self.db.get_performance_stats()
        discoveries = self.db.get_discoveries(5)
        
        return {
            'offline_mode': self.is_offline,
            'database': self.db.db_path,
            'cache_file': self.cache.cache_file,
            'pending_syncs': len(self.sync_queue),
            'statistics': perf_stats,
            'recent_discoveries': discoveries
        }
    
    def export_data(self, filepath: str):
        """Export all offline data"""
        discoveries = self.db.get_discoveries(999)
        solutions = self.db.get_solutions()
        
        export_data = {
            'discoveries': discoveries,
            'solutions': solutions,
            'cache': self.cache.cache,
            'sync_queue': self.sync_queue,
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return {'status': 'success', 'file': filepath}
    
    def import_data(self, filepath: str):
        """Import data from export file"""
        try:
            with open(filepath, 'r') as f:
                import_data = json.load(f)
            
            # Import discoveries
            for disc in import_data.get('discoveries', []):
                self.db.save_discovery(disc['data'])
            
            # Import solutions
            for sol in import_data.get('solutions', []):
                self.db.save_solution(
                    sol['problem_type'],
                    sol['code'],
                    sol['language'],
                    sol['notes']
                )
            
            # Merge cache
            for key, value in import_data.get('cache', {}).items():
                self.cache.set(key, value)
            
            return {'status': 'success', 'message': 'Data imported'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    def cleanup(self):
        """Clean up resources"""
        self.db.close()
