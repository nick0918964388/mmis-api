import os
import logging
from flask import Flask, request
from mmis.asset_routes import asset_bp
from mmis.item_routes import item_bp
from mmis.person_routes import person_bp
from gmp.asset_routes import gmp_asset_bp

# os.add_dll_directory('./db2cli/clidriver/bin') 

# 設置日誌配置
logging.basicConfig(
    filename='app.log',  # 日誌檔案名稱
    level=logging.INFO,  # 設置日誌級別
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日誌格式
)

app = Flask(__name__)

@app.before_request
def log_request_info():
    logging.info(f"Request path: {request.path}")  # 記錄請求路徑

app.register_blueprint(asset_bp)
app.register_blueprint(item_bp)
app.register_blueprint(person_bp)
app.register_blueprint(gmp_asset_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)