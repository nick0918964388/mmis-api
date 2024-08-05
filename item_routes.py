from flask import Blueprint, jsonify, request
import os
# os.add_dll_directory('./db2cli/clidriver/bin')
import ibm_db
from db_connection import get_db_connection

item_bp = Blueprint('item', __name__)


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
@item_bp.route('/item', methods=['GET'])
def query_item():
    search_text = request.args.get('search', '')
    sql = """
    select itemnum,description,in21,in26 from (SELECT a.itemnum,b.description as description , in21, in26 FROM maximo.item a left join maximo.l_item b on a.itemid = b.ownerid)
    WHERE LOWER(description) LIKE ?
    """
    params = [f'%{search_text.lower()}%']
    result = execute_query(sql, params, limit=50)
    return jsonify(result)

@item_bp.route('/item/invbalances', methods=['GET'])
def query_inventory():
    itemnum = request.args.get('itemnum', '')
    
    if not itemnum:
        return jsonify({"status": "error", "message": "itemnum is required"}), 400
    
    sql = """
    SELECT  itemnum , location ,binnum, conditioncode, curbal 
    FROM maximo.invbalances 
    WHERE CURBAL > 0  and itemnum = ?
    """
    params = [itemnum]
    result = execute_query(sql, params)
    return jsonify(result)

@item_bp.route('/item/transaction', methods=['GET'])
def query_transaction():
    itemnum = request.args.get('itemnum', '')
    
    if not itemnum:
        return jsonify({"status": "error", "message": "itemnum is required"}), 400
    
    sql = """
    SELECT itemnum, transdate, transtype, quantity, fromstoreloc, tostoreloc 
    FROM maximo.matrectrans 
    WHERE itemnum = ?
    ORDER BY transdate DESC
    """
    params = [itemnum]
    result = execute_query(sql, params, limit=50)
    return jsonify(result)

@item_bp.route('/item/storeroom', methods=['GET'])
def query_storeroom():
    location = request.args.get('location', '')
    
    if not location:
        return jsonify({"status": "error", "message": "location is required"}), 400
    
    sql = """
    SELECT  location , description,ZZ_LOCGROUPNAME ,ZZ_SECTION
    FROM maximo.locations 
    WHERE type='STOREROOM' and LOWER(description) like ?
    """
    params = [f'%{location.lower()}%']    
    result = execute_query(sql, params)
    return jsonify(result)