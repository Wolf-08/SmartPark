# import mysql en cursors
from pymysql.cursors import DictCursor
from flaskext.mysql import MySQL

class Database:
    def __init__(self, app, user, password, db, host='localhost', port=3306):
        # MySQL configuraciones
        app.config['MYSQL_DATABASE_USER'] = user
        app.config['MYSQL_DATABASE_PASSWORD'] = password
        app.config['MYSQL_DATABASE_PORT'] = port
        app.config['MYSQL_DATABASE_DB'] = db
        app.config['MYSQL_DATABASE_HOST'] = host
        print("Conexion a la base -Hecho-")
        mysql = MySQL(cursorclass=DictCursor)  # cursor para base
        mysql.init_app(app)
        self.mysql = mysql

    def get_data(self, sql, params=None, single=False):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        result = None

        print("Obteniendo Datos")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            if single:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
        conn.close()

        # Se retorna la informacion com oun diccionario
        return result

    def set_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print("Se agregada o actualiza  informacion")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            return 'Error: {0}'.format(e)
        conn.close()

        return cursor.lastrowid

    def delete_data(self, sql, params=None):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print("Borrando informacion")
        try:
            print(sql)
            cursor.execute(sql, params)
            conn.commit()
            cursor.close()
        except Exception as e:
            print(e)
            return 'Error: {0}'.format(e)

        conn.close()

        return cursor.rowcount
