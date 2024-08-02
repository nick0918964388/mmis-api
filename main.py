import os
from flask import Flask
from asset_routes import asset_bp
from item_routes import item_bp

os.add_dll_directory('./db2cli/clidriver/bin') 

app = Flask(__name__)

app.register_blueprint(asset_bp)
app.register_blueprint(item_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)