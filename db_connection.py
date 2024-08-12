import os
# os.add_dll_directory('C:/Users/nickyin/clidriver/bin')
import ibm_db
# 新增 Oracle 連接支援
import cx_Oracle
import logging

# 設置DB2連接參數
host = os.environ.get('HOST', '10.10.10.115')
port = os.environ.get('PORT', '50005')
database = os.environ.get('DATABASE', 'MAXDB76')
username = os.environ.get('USERNAME', 'maximo')
password = os.environ.get('PASSWORD', 'maximo')

# 建立DB2連接字串
conn_str = f"DATABASE={database};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"

db_type = os.environ.get('DB_TYPE', 'db2')  # 新增環境變數以選擇資料庫類型

def connect_to_oracle():
            dsn = cx_Oracle.makedsn(host, port, service_name=database)  # 使用服務名稱而不是SID
            connection = cx_Oracle.connect(user=username, password=password, dsn=dsn, mode=cx_Oracle.SYSDBA)  # 使用SYSDBA模式
            return connection
        
def get_db_connection():
    troubleshoot_oracle_connection()
    try:        
        # 根據資料庫類型選擇連接方式
        if db_type == 'oracle':
            conn = connect_to_oracle()
        else:
            conn = ibm_db.connect(conn_str, "", "")
        
        print("Database connection established.")  # 除錯輸出
        return conn
    except Exception as e:
        print(f"Connection error: {str(e)}")  # 除錯輸出
        return None
    
def troubleshoot_oracle_connection():
    # 1. 檢查環境變量
    required_vars = ['ORACLE_HOST', 'ORACLE_PORT', 'ORACLE_SERVICE_NAME', 'ORACLE_USER', 'ORACLE_PASSWORD']
    for var in required_vars:
        value = os.environ.get(var)
        logging.info(f"{var}: {'Set' if value else 'Not set'}")
    
    # 2. 嘗試建立 DSN
    try:
        host = os.environ.get('HOST', 'localhost')
        port = os.environ.get('PORT', '1521')
        service_name = os.environ.get('DATABASE')
        dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        logging.info(f"DSN created successfully: {dsn}")
    except Exception as e:
        logging.info(f"Error creating DSN: {e}")
    
    # 3. 嘗試連接
    try:
        connection = cx_Oracle.connect(
            user=os.environ.get('USERNAME'),
            password=os.environ.get('PASSWORD'),
            dsn=dsn,
            mode=cx_Oracle.SYSDBA
        )
        logging.info("Connection successful!")
        connection.close()
    except cx_Oracle.Error as error:
        logging.info(f"Error connecting to Oracle: {error}")
    
    # 4. 檢查 Oracle 客戶端庫
    logging.info(f"cx_Oracle version: {cx_Oracle.version}")
    logging.info(f"Oracle client version: {cx_Oracle.clientversion()}")