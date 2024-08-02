import os
# os.add_dll_directory('C:/Users/nickyin/clidriver/bin')
import ibm_db

# 設置DB2連接參數
db2_host = os.environ.get('DB2_HOST', '10.10.10.115')
db2_port = os.environ.get('DB2_PORT', '50005')
db2_database = os.environ.get('DB2_DATABASE', 'MAXDB76')
db2_username = os.environ.get('DB2_USERNAME', 'maximo')
db2_password = os.environ.get('DB2_PASSWORD', 'maximo')

# 建立DB2連接字串
conn_str = f"DATABASE={db2_database};HOSTNAME={db2_host};PORT={db2_port};PROTOCOL=TCPIP;UID={db2_username};PWD={db2_password};"

def get_db_connection():
    return ibm_db.connect(conn_str, "", "")