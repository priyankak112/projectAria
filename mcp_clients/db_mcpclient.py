from typing import Optional, Dict, Any
from dotenv import load_dotenv
import sqlite3
from datetime import datetime
import json

load_dotenv()
class DatabaseMCPClient:
    
    
    def __init__(self, connection_string: Optional[str] = None, db_type: str = "sqlite"):
        print("DB filename:",connection_string)
        self.db_type = db_type
        self.connection_string = connection_string or "corai.db"
        self.create_tables()
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.connection_string)
            cursor = conn.cursor()
            
            # Create escalations table (simplified)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS escalations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    escalation_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create complaints table (simplified)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    complaint_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            conn.commit()
            conn.close()
            print("✅ Database tables created/verified")
    
    def insert_escalation(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
        print("Inserting escalation record into database...")
     
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                # Extract only required columns
                escalation_record = {
                    "escalation_id": record.get("escalation_id"),
                    "user_id": record.get("user_id"),
                    "user_query": record.get("user_query"),
                    "created_at": record.get("created_at")
                }
                
                # Build INSERT query
                columns = ", ".join(escalation_record.keys())
                placeholders = ", ".join(["?" for _ in escalation_record.keys()])
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                
                cursor.execute(query, tuple(escalation_record.values()))
                conn.commit()
                record_id = cursor.lastrowid
                conn.close()
                
                print(f"✅ Escalation recorded in DB (ID: {record_id})")
                
                return {
                    "success": True,
                    "message": f"📝 Escalation record inserted",
                    "record_id": record_id,
                    "escalation_id": escalation_record.get("escalation_id")
                }
        
        except sqlite3.IntegrityError as e:
            print(f"❌ Database integrity error: {e}")
            return {
                "success": False,
                "message": "Database integrity error (duplicate escalation_id)",
                "error": str(e),
                "record_id": None
            }
        
        except Exception as e:
            print(f"❌ Database insert error: {e}")
            return {
                "success": False,
                "message": f"Failed to insert record: {str(e)}",
                "error": str(e),
                "record_id": None
            }
    
    def insert_complaint(self, table: str, record: Dict[str, Any]) -> Dict[str, Any]:
      
        print("Inserting complaint record into database...")
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                # Extract only required columns
                complaint_record = {
                    "complaint_id": record.get("complaint_id"),
                    "user_id": record.get("user_id"),
                    "user_query": record.get("user_query"),
                    "created_at": record.get("created_at")
                }
                
                # Build INSERT query
                columns = ", ".join(complaint_record.keys())
                placeholders = ", ".join(["?" for _ in complaint_record.keys()])
                query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
                
                cursor.execute(query, tuple(complaint_record.values()))
                conn.commit()
                record_id = cursor.lastrowid
                conn.close()
                
                print(f"✅ Complaint recorded in DB (ID: {record_id})")
                
                return {
                    "success": True,
                    "message": f"📝 Complaint record inserted",
                    "record_id": record_id,
                    "complaint_id": complaint_record.get("complaint_id")
                }
        
        except sqlite3.IntegrityError as e:
            print(f"❌ Database integrity error: {e}")
            return {
                "success": False,
                "message": "Database integrity error (duplicate complaint_id)",
                "error": str(e),
                "record_id": None
            }
        
        except Exception as e:
            print(f"❌ Database insert error: {e}")
            return {
                "success": False,
                "message": f"Failed to insert complaint: {str(e)}",
                "error": str(e),
                "record_id": None
            }
    
    def get_escalation(self, escalation_id: str) -> Dict[str, Any]:
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT escalation_id, user_id, user_query, created_at FROM escalations WHERE escalation_id = ?",
                    (escalation_id,)
                )
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return {
                        "success": True,
                        "data": {
                            "escalation_id": result[0],
                            "user_id": result[1],
                            "user_query": result[2],
                            "created_at": result[3]
                        }
                    }
                else:
                    return {
                        "success": False,
                        "message": "Escalation not found",
                        "data": None
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def get_complaint(self, complaint_id: str) -> Dict[str, Any]:
            
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                cursor.execute(
                    "SELECT complaint_id, user_id, user_query, created_at FROM complaints WHERE complaint_id = ?",
                    (complaint_id,)
                )
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return {
                        "success": True,
                        "data": {
                            "complaint_id": result[0],
                            "user_id": result[1],
                            "user_query": result[2],
                            "created_at": result[3]
                        }
                    }
                else:
                    return {
                        "success": False,
                        "message": "Complaint not found",
                        "data": None
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": None
            }
    
    def get_all_escalations(self, user_id: Optional[str] = None) -> Dict[str, Any]:
       
        
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                if user_id:
                    cursor.execute(
                        "SELECT escalation_id, user_id, user_query, created_at FROM escalations WHERE user_id = ? ORDER BY created_at DESC",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT escalation_id, user_id, user_query, created_at FROM escalations ORDER BY created_at DESC"
                    )
                
                results = cursor.fetchall()
                conn.close()
                
                escalations = [
                    {
                        "escalation_id": row[0],
                        "user_id": row[1],
                        "user_query": row[2],
                        "created_at": row[3]
                    }
                    for row in results
                ]
                
                return {
                    "success": True,
                    "data": escalations,
                    "count": len(escalations)
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": []
            }
    
    def get_all_complaints(self, user_id: Optional[str] = None) -> Dict[str, Any]:
       
        
        try:
            if self.db_type == "sqlite":
                conn = sqlite3.connect(self.connection_string)
                cursor = conn.cursor()
                
                if user_id:
                    cursor.execute(
                        "SELECT complaint_id, user_id, user_query, created_at FROM complaints WHERE user_id = ? ORDER BY created_at DESC",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT complaint_id, user_id, user_query, created_at FROM complaints ORDER BY created_at DESC"
                    )
                
                results = cursor.fetchall()
                conn.close()
                
                complaints = [
                    {
                        "complaint_id": row[0],
                        "user_id": row[1],
                        "user_query": row[2],
                        "created_at": row[3]
                    }
                    for row in results
                ]
                
                return {
                    "success": True,
                    "data": complaints,
                    "count": len(complaints)
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": []
            }