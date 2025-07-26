"""
Database connection pooling for improved performance

This module provides a thread-safe SQLite connection pool to improve
database performance by reusing connections and reducing overhead.
"""

import sqlite3
import threading
from queue import Queue, Empty
from contextlib import contextmanager
from typing import Optional
import streamlit as st
import time


class SQLiteConnectionPool:
    """Thread-safe SQLite connection pool"""
    
    def __init__(self, database_path: str, max_connections: int = 10):
        """
        Initialize connection pool
        
        Args:
            database_path (str): Path to SQLite database file
            max_connections (int): Maximum number of connections in pool
        """
        self.database_path = database_path
        self.max_connections = max_connections
        self._pool = Queue(maxsize=max_connections)
        self._lock = threading.Lock()
        self._created_connections = 0
        self._active_connections = 0
        
        # Performance metrics
        self._total_requests = 0
        self._pool_hits = 0
        self._pool_misses = 0
        
        # Pre-create some connections
        self._initialize_pool()
    
    def _initialize_pool(self):
        """Initialize the connection pool with some connections"""
        initial_connections = min(3, self.max_connections)
        for _ in range(initial_connections):
            conn = self._create_connection()
            if conn:
                self._pool.put(conn)
    
    def _create_connection(self) -> Optional[sqlite3.Connection]:
        """Create a new database connection"""
        try:
            conn = sqlite3.connect(
                self.database_path,
                check_same_thread=False,  # Allow sharing between threads
                timeout=30.0,
                isolation_level=None  # Autocommit mode for better performance
            )
            
            # Configure connection for better performance
            conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging
            conn.execute("PRAGMA synchronous=NORMAL")  # Balance safety and speed
            conn.execute("PRAGMA cache_size=10000")  # Increase cache size
            conn.execute("PRAGMA temp_store=MEMORY")  # Store temp tables in memory
            
            conn.row_factory = sqlite3.Row  # Enable dict-like access
            
            with self._lock:
                self._created_connections += 1
            
            return conn
            
        except Exception as e:
            st.error(f"Failed to create database connection: {e}")
            return None
    
    @contextmanager
    def get_connection(self):
        """
        Get a connection from the pool (context manager)
        
        Yields:
            sqlite3.Connection: Database connection
            
        Example:
            with pool.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM table")
                results = cursor.fetchall()
        """
        conn = None
        start_time = time.time()
        
        try:
            with self._lock:
                self._total_requests += 1
            
            # Try to get existing connection from pool
            try:
                conn = self._pool.get_nowait()
                with self._lock:
                    self._pool_hits += 1
                    self._active_connections += 1
                    
            except Empty:
                # Pool is empty, create new connection if under limit
                with self._lock:
                    if self._created_connections < self.max_connections:
                        conn = self._create_connection()
                        if conn:
                            self._pool_misses += 1
                            self._active_connections += 1
                    else:
                        # Wait for available connection
                        try:
                            conn = self._pool.get(timeout=10.0)
                            self._pool_hits += 1
                            self._active_connections += 1
                        except Empty:
                            raise Exception("Connection pool timeout - no connections available")
            
            if conn is None:
                raise Exception("Could not obtain database connection")
            
            # Test connection is still valid
            try:
                conn.execute("SELECT 1")
            except sqlite3.Error:
                # Connection is stale, create a new one
                conn.close()
                conn = self._create_connection()
                if conn is None:
                    raise Exception("Could not create replacement connection")
            
            yield conn
            
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except:
                    pass
            raise e
            
        finally:
            if conn:
                try:
                    # Return connection to pool
                    self._pool.put_nowait(conn)
                    with self._lock:
                        self._active_connections -= 1
                        
                except:
                    # Pool is full, close the connection
                    conn.close()
                    with self._lock:
                        self._created_connections -= 1
                        self._active_connections -= 1
            
            # Log performance metrics periodically
            if self._total_requests % 100 == 0:
                self._log_performance_metrics()
    
    def _log_performance_metrics(self):
        """Log performance metrics for monitoring"""
        hit_rate = (self._pool_hits / self._total_requests) * 100 if self._total_requests > 0 else 0
        
        metrics = {
            'total_requests': self._total_requests,
            'pool_hit_rate': f"{hit_rate:.1f}%",
            'active_connections': self._active_connections,
            'created_connections': self._created_connections,
            'pool_size': self._pool.qsize()
        }
        
        print(f"Connection Pool Metrics: {metrics}")
    
    def get_stats(self) -> dict:
        """Get connection pool statistics"""
        hit_rate = (self._pool_hits / self._total_requests) * 100 if self._total_requests > 0 else 0
        
        return {
            'total_requests': self._total_requests,
            'pool_hits': self._pool_hits,
            'pool_misses': self._pool_misses,
            'hit_rate_percent': round(hit_rate, 2),
            'active_connections': self._active_connections,
            'created_connections': self._created_connections,
            'pool_size': self._pool.qsize(),
            'max_connections': self.max_connections
        }
    
    def close_all(self):
        """Close all connections in the pool"""
        closed_count = 0
        
        while not self._pool.empty():
            try:
                conn = self._pool.get_nowait()
                conn.close()
                closed_count += 1
            except Empty:
                break
        
        with self._lock:
            self._created_connections = 0
            self._active_connections = 0
        
        print(f"Closed {closed_count} connections from pool")
    
    def __del__(self):
        """Cleanup when pool is destroyed"""
        try:
            self.close_all()
        except:
            pass


# Global connection pool instance
_connection_pool = None
_pool_lock = threading.Lock()


def get_connection_pool() -> SQLiteConnectionPool:
    """
    Get the global connection pool instance (singleton pattern)
    
    Returns:
        SQLiteConnectionPool: Global connection pool instance
    """
    global _connection_pool
    
    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                _connection_pool = SQLiteConnectionPool('mind_sprite.db')
    
    return _connection_pool


def reset_connection_pool():
    """Reset the global connection pool (useful for testing)"""
    global _connection_pool
    
    with _pool_lock:
        if _connection_pool:
            _connection_pool.close_all()
        _connection_pool = None


# Convenience function for getting connections
def get_db_connection():
    """
    Get database connection from pool
    
    Returns:
        Context manager for database connection
    """
    return get_connection_pool().get_connection()
