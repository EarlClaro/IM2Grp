mysql = None

def set_database(mysql_instance):
    global mysql
    mysql = mysql_instance

def get_connection():
    return mysql.connection

def get_cursor():
    return get_connection().cursor()

def execute(query, params=(), commit=False):
    cur = get_cursor()
    cur.execute(query, params)
    if commit:
        get_connection().commit()
    return cur

def fetchone(query, params=()):
    cur = execute(query, params)
    return cur.fetchone()

def fetchall(query, params=()):
    cur = execute(query, params)
    return cur.fetchall()
