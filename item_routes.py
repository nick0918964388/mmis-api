from flask import Blueprint, jsonify, request
from db_utils import execute_query

item_bp = Blueprint('item', __name__)


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