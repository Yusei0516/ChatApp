import hashlib
from models import db_pool

def create_admin():
    uid = 'admin123'
    name = '管理者'
    email = 'admin@example.com'
    raw_password = 'adminpassFteam'
    password = hashlib.sha256(raw_password.encode()).hexdigest()

    conn = db_pool.get_conn()
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (uid, name, email, password))
            conn.commit()
            print("✅管理者登録が完了しました")
    except Exception as e:
        print("⚠️エラー：", e)
    finally:
        db_pool.release(conn)


if __name__ == '__main__':
    create_admin()
    