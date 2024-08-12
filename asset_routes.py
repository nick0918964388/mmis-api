from flask import Blueprint, jsonify, request
import os
# os.add_dll_directory('./db2cli/clidriver/bin')
import ibm_db
from db_connection import get_db_connection
from db_utils import execute_query

asset_bp = Blueprint('asset', __name__)

@asset_bp.route('/asset', methods=['GET'])
def query_asset():
    search_text = request.args.get('search', '')
    
    sql = """
    SELECT * FROM maximo.asset 
    WHERE LOWER(description) LIKE ? or LOWER(assetnum) LIKE ?
    """
    params = [f'%{search_text.lower()}%', f'%{search_text.lower()}%']
    
    result = execute_query(sql, params, limit=10)
    return jsonify(result)

@asset_bp.route('/asset/<string:assetnum>', methods=['GET'])
def get_asset_by_assetnum(assetnum):
    sql = """
    SELECT * FROM maximo.asset 
    WHERE LOWER(assetnum) = ?
    """
    params = [assetnum.lower()]
    
    result = execute_query(sql, params)
    
    if result["status"] == "success" and result["data"]:
        return jsonify(result)
    elif result["status"] == "success" and not result["data"]:
        return jsonify({"status": "not found", "message": "資產未找到"}), 404
    else:
        return jsonify({"status": "error", "message": result["message"]}), 500

@asset_bp.route('/asset/<string:assetnum>/maintenance-history', methods=['GET'])
def get_maintenance_history(assetnum):
    sql = """
    SELECT 
        wojp3 as workorder_number,
        status,
        woeq14 as vehicle_number,
        worktype,
        description,
        actfinish as completion_date,
        targstartdate as planned_maintenance_date
    FROM maximo.workorder 
    WHERE wojp4=1 and assetnum = ?
    ORDER BY actfinish DESC
    """
    params = [assetnum]
    
    result = execute_query(sql, params)
    
    if result["status"] == "success":
        if result["data"]:
            return jsonify({"status": "success", "data": result["data"]})
        else:
            return jsonify({"status": "not found", "message": "未找到該資產的保養履歷"}), 404
    else:
        return jsonify({"status": "error", "message": result["message"]}), 500