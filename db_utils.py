import os
import ibm_db
import cx_Oracle
import logging
from contextlib import contextmanager

# 假設 get_db_connection 函數在 db_connection 模塊中
from db_connection import get_db_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def db_connection():
    conn = None
    try:
        conn = get_db_connection()
        yield conn
    finally:
        if conn:
            if os.environ.get('DB_TYPE', 'db2') == 'oracle':
                conn.close()
            else:
                ibm_db.close(conn)

def execute_query(sql, params, limit=None):
    db_type = os.environ.get('DB_TYPE', 'db2')
    
    if limit:
        if db_type == 'oracle':
            sql += f" AND ROWNUM <= {limit}"
        else:
            sql += f" FETCH FIRST {limit} ROWS ONLY"
    
    logger.info(f"執行的SQL語句: {sql}")
    logger.info(f"參數: {params}")
    
    try:
        with db_connection() as conn:
            if db_type == 'oracle':
                return execute_oracle_query(conn, sql, params)
            else:
                return execute_db2_query(conn, sql, params)
    except Exception as e:
        logger.error(f"執行錯誤的SQL語句: {sql}")
        logger.error(f"參數: {params}")
        logger.error(f"錯誤信息: {str(e)}")
        return {"status": "error", "message": str(e)}

def execute_oracle_query(conn, sql, params):
    with conn.cursor() as cursor:
        cursor.execute(sql, params)
        data = cursor.fetchall()
    return {"status": "success", "data": data}

def execute_db2_query(conn, sql, params):
    stmt = ibm_db.prepare(conn, sql)
    for i, param in enumerate(params, start=1):
        ibm_db.bind_param(stmt, i, param)
    ibm_db.execute(stmt)
    
    data = []
    result = ibm_db.fetch_assoc(stmt)
    while result:
        data.append(result)
        result = ibm_db.fetch_assoc(stmt)
    return {"status": "success", "data": data}