import os
import psycopg2
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file



def execute_query(query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DATABASE"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432")
    )
    with conn:
        with conn.cursor() as cursor:
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            res = cursor.fetchall()
    return res


def create(table: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING *"
    return  execute_query(query, list(data.values()))


def read(table: str, columns: str, condition: str = 'TRUE') -> List[Dict[str, Any]]:
    query = f"SELECT {columns} FROM {table} WHERE {condition}::text = 'TRUE'::text"
    return  execute_query(query)


def update(table: str, data: Dict[str, Any], condition: str) -> List[Dict[str, Any]]:
    sets = ', '.join([f"{key} = %s" for key in data.keys()])
    query = f"UPDATE {table} SET {sets} WHERE {condition} RETURNING *"
    return  execute_query(query, list(data.values()))


def del_(table: str, condition: str) -> List[Dict[str, Any]]:
    query = f"DELETE FROM {table} WHERE {condition} RETURNING *"
    return  execute_query(query)


