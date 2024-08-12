import os
from flask import Flask
from mmis.asset_routes import asset_bp
from mmis.item_routes import item_bp
from mmis.person_routes import person_bp
from gmp.asset_routes import gmp_asset_bp

# os.add_dll_directory('./db2cli/clidriver/bin') 

app = Flask(__name__)

app.register_blueprint(asset_bp)
app.register_blueprint(item_bp)
app.register_blueprint(person_bp)
app.register_blueprint(gmp_asset_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)