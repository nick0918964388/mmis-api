from flask import Blueprint, jsonify, request
import ibm_db
from db_connection import get_db_connection

person_bp = Blueprint('person', __name__)

@person_bp.route('/person', methods=['GET'])
def query_person():
    try:
        search_text = request.args.get('search', '')
        
        conn = get_db_connection()
        
        sql = """
        SELECT personid, displayname, status FROM maximo.person
        WHERE LOWER(displayname) LIKE ?
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
        return jsonify({"status": "error", "message": str(e)}), 500
