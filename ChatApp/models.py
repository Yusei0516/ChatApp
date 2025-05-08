from flask import abort
import pymysql
from util.DB import DB

#初期起動時にコネクションプールを作成し接続を確率
db_pool = DB.init_db_pool()

#ユーザークラス
class User:
    @classmethod
    def create(cls, uid, name, email, password):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s)"
                cur.execute(sql, (uid, name, email, password,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_email(cls, email):
        conn = db_pool.get_conn()
        try:
                with conn.cursor() as cur:
                    sql = "SELECT * FROM users WHERE email=%s"
                    cur.execute(sql, (email,))
                    user = cur.fetchone()
                return user
        except pymysql.Error as e:
            print(f'エラーが発生しています：{e}')
            abort(500)
        finally:
            db_pool.release(conn)
    
    @classmethod
    def get_usr_group(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql ="SELECT group_chat_id FROM group_members WHERE user_id = %s"
                cur.execute(sql, (user_id,))
                result = cur.fetchone()
                return result[0] if result else None
        finally:
            db_pool.release(conn)

#グループクラス
class Group:            
    @classmethod
    def find_by_user_id(cls, user_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                SELECT group_chats.id, group_chats.name
                FROM group_members
                JOIN group_chats ON group_members.group_chat_id = group_chats.id
                WHERE group_members.user_id = %s 
                LIMIT 1
                """
                cur.execute(sql, (user_id,))
                group = cur.fetchone()
                return group
        except pymysql.Error as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def find_by_id(cls, group_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = "SELECT id, name FROM group_chats WHERE id = %s"
                cur.execute(sql, (group_id,))
                group = cur.fetchone()
                return group
        except pymysql.Error as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            db_pool.release(conn)
            
    @classmethod
    def update(cls, group_id, name, description):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "UPDATE group_chats SET name=%s, description=%s WHERE id=%s"
                cur.execute(sql, (name, description, group_id))
                conn.commit()
        finally:
            db_pool.release(conn)

    @classmethod
    def is_admin(cls, uid):
        return uid == "admin123"

#グループメッセージクラス
class GroupMessage:
    @classmethod
    def create(cls, user_id, group_id, content):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = """
                    INSERT INTO group_messages (user_id, group_chat_id, content, created_at)
                    VALUES (%s, %s, %s, NOW())
                """
                cur.execute(sql, (user_id, group_id, content))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get_all(cls, group_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = """
                    SELECT users.user_name, group_messages.content
                    FROM group_messages
                    JOIN users ON group_messages.user_id = users.id
                    WHERE group_messages.group_chat_id = %s
                    ORDER BY group_messages.created_at ASC
                """
                cur.execute(sql, (group_id,))
                messages = cur.fetchall()
                return messages
        except pymysql.Error as e:
            print(f'エラーが発生しています: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

#オープンチャット
class OpenChat:
    @classmethod
    def create(cls, name, description, creator_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO open_chats (name, description, creator_id) VALUES (%s, %s, %s)"
                cur.execute(sql, (name, description, creator_id))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しました: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def get(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cur:
                sql = "SELECT * FROM open_chats WHERE id = %s"
                cur.execute(sql, (chat_id,))
                return cur.fetchone()
        except pymysql.Error as e:
            print(f'エラーが発生しました: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

    @classmethod
    def delete(cls, chat_id):
        conn = db_pool.get_conn()
        try:
            with conn.cursor() as cur:
                sql = "DELETE FROM open_chats WHERE id = %s"
                cur.execute(sql, (chat_id,))
                conn.commit()
        except pymysql.Error as e:
            print(f'エラーが発生しました: {e}')
            abort(500)
        finally:
            db_pool.release(conn)

# #オープンチャット
# class Opc:
#     @classmethod
#     def create(cls, uid, name, description, is_open):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = """
#                     INSERT INTO open_chats(create_id, name, description, is_open, created_at)
#                     VALUES(%s, %s, %s, NOW())
#                 """
#                 cur.execute(sql, (uid, name, description, is_open))
#                 conn.commit()
#         except pymysql.Error as e:
#             print(f'エラー: {e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)
            
#     @classmethod
#     def get_all(cls):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "SELECT * FROM open_chats;"
#                 cur.execute(sql)
#                 opc_room = cur.fetchall()
#                 return opc_room
#         except pymysql.Error as e:
#             print(f'エラーが発生しています : {e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)
            
#     @classmethod
#     def find_by_room_id(cls, room_id):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "SELECT * FROM open_chats WHERE id=%s;"
#                 cur.execute(sql, (room_id,))
#                 opc_room = cur.fetchone()
#                 return opc_room
#         except pymysql.Error as e:
#             print(f'エラーが発生しています : {e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)
            
#     @classmethod
#     def find_by_name(cls, name):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "SELECT * FROM open_chats WHERE name=%s:"
#                 cur.execute(sql, (name,))
#                 opc_room = cur.fetchone()
#                 return opc_room
#         except pymysql.Error as e:
#             print(f'エラーが発生しています : {e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)
    
#     @classmethod
#     def delete(cls, room_id, uid):
#         conn = db_pool.get_conn()
#         try:
#             with conn.cursor() as cur:
#                 sql = "DELETE FROM open_chats WHERE id = %s AND create_id = %s;"
#                 cur.execute(sql, (room_id, uid))
#                 conn.commit()
#         except pymysql.Error as e:
#             print(f'エラーが発生しています : {e}')
#             abort(500)
#         finally:
#             db_pool.release(conn)