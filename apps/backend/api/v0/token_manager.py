import sqlite3
import sys

from flask import current_app

from config.config import Config
cfg = Config().get()


class TokenManager:
    def __init__(self, ):
        return

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        dbname=cfg["storage"]["sqllitedb"]
        try:
            conn = sqlite3.connect(dbname)

            return conn
        except sqlite3.Error as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)

        return None

    def create_token_table(self, conn):

        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS iot_token
                 (token text, status int, createdat real, updatedat real)''')
        # Save (commit) the changes
        conn.commit()

    def check_token(self, token_id):
        conn = self.create_connection()
        try:
            current_app.logger.debug(token_id)

            c = conn.cursor()

            # Create table
            sql = "select status from iot_token where token=?"
            c.execute(sql, (token_id,))
            result = c.fetchone()

            if result:
                return result[0]
            else:
                return -1
        except sqlite3.Error as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            return "error!!"
        finally:
            conn.close()

    def validate_token(self,token_id):
        conn = self.create_connection()
        try:
            current_app.logger.debug(token_id)

            c = conn.cursor()

            # Create table
            sql="select status from iot_token where token=?"
            c.execute(sql, (token_id,))
            result = c.fetchone()

            if result:
                if result[0] == 0:
                    sql="update iot_token set status=1,updatedat=julianday('now') where token=?"
                    c.execute(sql, (token_id,))
                    conn.commit()
                    return '1'
                else:
                    return 'Used Token'
            else:
                return 'Invalid Token'

        except sqlite3.Error as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            return "error!!"
        finally:
            conn.close()

    def insert_token(self,token_id):

        try:
            current_app.logger.debug(token_id)
            conn = self.create_connection()
            self.create_token_table(conn)
            c = conn.cursor()

            # Create table
            sql = "INSERT INTO iot_token VALUES (?,0,julianday('now'),julianday('now'))"
            c.execute(sql, (token_id,))

            # Save (commit) the changes
            conn.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            conn.close()
            return True
        except sqlite3.Error as e:
            current_app.logger.error("Unexpected error:" + sys.exc_info()[0])
            current_app.logger.error("Error description: " + e)
            return False

