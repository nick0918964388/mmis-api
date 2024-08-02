from flask import Blueprint, jsonify, request
import os
# os.add_dll_directory('./db2cli/clidriver/bin')
import ibm_db
from db_connection import get_db_connection

item_bp = Blueprint('item', __name__)

@item_bp.route('/item', methods=['GET'])
def query_item():
    try:
        search_text = request.args.get('search', '')
        
        conn = get_db_connection()
        
        sql = """
        select * from (SELECT a.itemnum,b.description as description , in21, in26 FROM maximo.item a left join maximo.l_item b on a.itemid = b.ownerid)
        WHERE LOWER(description) LIKE ?
        FETCH FIRST 10 ROWS ONLY
        """
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, f'%{search_text.lower()}%')
        
        ibm_db.execute(stmt)
        
        result = ibm_db.fetch_assoc(stmt)
        data = []
        while result:
            data.append(result)
            result = ibm_db.fetch_assoc(stmt)
        
        ibm_db.close(conn)
        
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})