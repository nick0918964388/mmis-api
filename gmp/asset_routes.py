from flask import Blueprint, jsonify, request
import logging
from db_connection import get_db_connection
from db_utils import execute_query

gmp_asset_bp = Blueprint('gmp_asset', __name__)

@gmp_asset_bp.route('/gmp/asset', methods=['GET'])
def query_asset():
    search_text = request.args.get('search', '')
    logging.info(f"Received search text: {search_text}")  # 記錄接收到的搜索文本
    
    sql = """
    SELECT * FROM maximo.asset 
    """
    params = []
    
    result = execute_query(sql, params)
    
    # 構建回傳的結果，包含欄位與值
    if result["status"] == "success":
        response_data = {
            "status": "success",
            "data": result["data"]
        }
    else:
        response_data = {
            "status": "error",
            "message": result["message"]
        }
    
    logging.info(f"Query result: {response_data}")  # 記錄查詢結果
    
    return jsonify(response_data)