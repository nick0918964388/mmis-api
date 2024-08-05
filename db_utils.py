import ibm_db
from db_connection import get_db_connection

def execute_query(sql, params, limit=None):
    try:
        conn = get_db_connection()
        if limit:
            sql += f" FETCH FIRST {limit} ROWS ONLY"
        
        # 打印SQL語句
        print(f"執行的SQL語句: {sql}")
        print(f"參數: {params}")
        
        stmt = ibm_db.prepare(conn, sql)
        
        for i, param in enumerate(params, start=1):
            ibm_db.bind_param(stmt, i, param)
        
        ibm_db.execute(stmt)
        
        result = ibm_db.fetch_assoc(stmt)
        data = []
        while result:
            data.append(result)
            result = ibm_db.fetch_assoc(stmt)
        
        ibm_db.close(conn)
        
        return {"status": "success", "data": data}
    except Exception as e:
        # 在發生錯誤時也打印SQL語句
        print(f"執行錯誤的SQL語句: {sql}")
        print(f"參數: {params}")
        print(f"錯誤信息: {str(e)}")
        return {"status": "error", "message": str(e)}