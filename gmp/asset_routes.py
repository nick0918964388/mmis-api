from flask import Blueprint, jsonify, request
import os
from db_connection import get_db_connection
from db_utils import execute_query

gmp_asset_bp = Blueprint('gmp_asset', __name__)

@gmp_asset_bp.route('/gmp/asset', methods=['GET'])
def query_asset():
    # 紀錄請求的參數
    search_text = request.args.get('search', '')
    print(f"Received search text: {search_text}")  # 除錯輸出
    
    sql = """
    SELECT * FROM maximo.asset 
    """
    params = []
    
    result = execute_query(sql, params, limit=10)
    
    # 紀錄結果
    print(f"Query result: {result}")  # 除錯輸出
    
    return jsonify(result)