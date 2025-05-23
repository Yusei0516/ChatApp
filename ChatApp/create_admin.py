import hashlib
from models import User

def create_admin():
    uid = 'admin123456789'
    name = '管理者'
    email = 'adminFteam@example.com'
    raw_password = 'adminpassFteam'
    password = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

    try:
        #既存の管理者がいるか確認
        admin = User.find_by_email(email)
        if admin:
            print("⚠️管理者は既に登録されています")
        else:
            #新規管理者の作成
            User.create(uid, name, email, password, is_admin=1)
            print("✅管理者の登録が完了しました")
    except Exception as e:
        print("エラーが発生しました：{e}")


if __name__ == '__main__':
    create_admin()
