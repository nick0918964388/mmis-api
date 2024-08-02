from flask import Blueprint, jsonify, request
import os
os.add_dll_directory('./db2cli/clidriver/bin')
import ibm_db
from db_connection import get_db_connection

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/asset', methods=['GET'])
def query_asset():
    try:
        search_text = request.args.get('search', '')
        
        conn = get_db_connection()
        
        sql = """
        SELECT * FROM maximo.asset 
        WHERE LOWER(description) LIKE ? or LOWER(assetnum) LIKE ?
        FETCH FIRST 10 ROWS ONLY
        """
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, f'%{search_text.lower()}%')
        ibm_db.bind_param(stmt, 2, f'%{search_text.lower()}%')
        
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

@asset_bp.route('/asset/<string:assetnum>', methods=['GET'])
def get_asset_by_assetnum(assetnum):
    try:
        conn = get_db_connection()
        
        sql = """
        SELECT * FROM maximo.asset 
        WHERE LOWER(assetnum) = ?
        """
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, assetnum.lower())
        
        ibm_db.execute(stmt)
        
        result = ibm_db.fetch_assoc(stmt)
        
        ibm_db.close(conn)
        
        if result:
            return jsonify({"status": "success", "data": result})
        else:
            return jsonify({"status": "not found", "message": "Asset not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500