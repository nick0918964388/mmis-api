from flask import Blueprint, jsonify, request
import os
import ibm_db
from db_connection import get_db_connection
from db_utils import execute_query

gmp_asset_bp = Blueprint('gmp_asset', __name__)

@gmp_asset_bp.route('/gmp/asset', methods=['GET'])
def query_asset():
    search_text = request.args.get('search', '')
    
    sql = """
    SELECT * FROM maximo.asset 
    WHERE LOWER(description) LIKE ? or LOWER(assetnum) LIKE ?
    """
    params = [f'%{search_text.lower()}%', f'%{search_text.lower()}%']
    
    result = execute_query(sql, params, limit=10)
    return jsonify(result)