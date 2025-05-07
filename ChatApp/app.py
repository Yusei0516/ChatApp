from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib, uuid, re, os
from models import User, Group, GroupMessage
# from util.assets import bundle_css_files
 
# 定数定義
EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
SESSION_DAYS = 30

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4().hex)
app.permanent_session_lifetime = timedelta(days=SESSION_DAYS)

# 静的ファイルをキャッシュする設定。開発中はコメントアウト
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 2678400
#bundle_css_files(app)


# ルートページのリダイレクト処理
@app.route('/', methods=['GET'])
def index():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    if uid == 'admin123':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))


# サインアップページの表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')


# サインアップ処理
@app.route('/signup', methods=['POST'])
def signup_process():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    passwordConfirmation = request.form.get('password-confirmation')

    if name == '' or email =='' or password == '' or passwordConfirmation == '':
        flash('未入力の項目があります')
    elif password != passwordConfirmation:
        flash('パスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式が正しくありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        registered_user = User.find_by_email(email)

        if registered_user != None:
            flash('すでに登録されているようです')
        else:
            User.create(uid, name, email, password)
            UserId = str(uid)
            session['uid'] = UserId
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('signup_process'))


# ログインページの表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email =='' or password == '':
        flash('未入力の項目があります')
        return redirect(url_for('login_view'))

    user = User.find_by_email(email)
    if user is None:
        flash('このユーザーは存在しません')
        return redirect(url_for('login_view'))
    
    hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
    if hashPassword != user["password"]:
        flash('パスワードが間違っています')
        return redirect(url_for('login_view'))
    
    #正しくログインできたのでセッションに保存
    session['uid'] = user["uid"]
    session['email'] = user["email"]

    #管理者の判定
    if user['email'] == 'admin@example.com':
        return redirect(url_for('admin_dashboard'))
    #一般ユーザー
    else:
        return redirect(url_for('user_dashboard'))
    
# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

#管理者用ダッシュボード
@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

#管理者：グループチャット一覧へ
@app.route('/admin/group/list', methods=['GET'])
def group_list_view():
    return render_template('admin/group_list.html')

#管理者：オープンチャット一覧へ
@app.route('/admin/open/list', methods=['GET'])
def open_list_view():
    return render_template('admin/open_list.html')

#管理者：個人チャット一覧へ
@app.route('/admin/private/list', methods=['GET'])
def private_list_view():
    return render_template('admin/private_list.html')

#管理者メニューまとめ(グループチャット作成)
@app.route('/admin_menu/group/create', methods=['GET'])
def create_group_view():
    return render_template('admin/create_group.html')

#管理者メニューまとめ(グループチャット削除)
@app.route('/admin_menu/group/delete', methods=['GET'])
def delete_group_view():
    return render_template('admin/delete_group.html')

#管理者メニューまとめ(オープンチャット作成)
@app.route('/admin_menu/open/create', methods=['GET'])
def create_open_view():
    return render_template('admin/create_open.html')

#管理者メニューまとめ(オープンチャット削除)
@app.route('/admin_menu/open/delete', methods=['GET'])
def delete_opem_view():
    return render_template('admin/delete_open.html')



#一般ユーザー用ダッシュボード
@app.route('/user_dashboard')
def user_dashboard():
    return render_template('user/dashboard.html')

#ユーザー：グループチャットへ
@app.route('/user/group/chat', methods=['GET'])
def enter_group_chat():
    if 'uid' not in session:
        return redirect(url_for('login_view'))
    
    user_id = session['uid']
    group_chat_id = User.get_group(user_id)

    if group_chat_id:
        return redirect(url_for('group_chat_view', group_chat_id=group_chat_id))
    else:
        flash('あなたはまだグループに招待されていません。')
        return redirect(url_for('user_dashboard'))

#ユーザー：個人チャットへ
@app.route('/user/private/chat', methods=['GET'])
def enter_private_chat():
    return render_template('user/private_chat.html')

#ユーザーメニューまとめ(オープンチャット作成)
@app.route('/user_menu/open/create', methods=['GET'])
def user_create_open_view():
    return render_template('user/create_open.html')

#ユーザーメニューまとめ(オープンチャット削除)
@app.route('/user_menu/open/delete', methods=['GET'])
def user_delete_opem_view():
    return render_template('user/delete_open.html')


#グループチャット(リダイレクト)
@app.route('/group_chat', methods=['GET'])
def group_chat_redirect():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    group = Group.find_by_user_id(uid)
    if group is None:
        flash("グループに所属していません")    #ここではユーザIDでグループに所属しているか確認
        return redirect(url_for('user_dashboard'))

    return redirect(url_for('group_chat',group_id=group['id']))

#管理者用グループチャット(リダイレクト)
@app.route('/admin/group_list', methods=['GET'])
def admin_group_chat_redirect():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    if not User.is_admin(uid):
        return redirect(url_for('login_view'))

    groups = Group.get_all()
    return render_template('admin/group_list.html', groups=groups)


#グループチャット
@app.route('/group_chat/<int:group_id>/messages', methods=['GET','POST'])
def group_chat(group_id):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))

    group = Group.find_by_id(group_id)
    if group is None:
        flash("グループが存在しません")
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            GroupMessage.create(uid, group_id, message)
        return redirect(url_for('group_chat', group_id=group_id))

    messages = GroupMessage.get_all(group_id)
    return render_template('xxxx.html', group=group, messages=messages)    #xxxx.htmlは決まってから記述します

if __name__ == '__main__': 
    app.run(host="0.0.0.0", debug=True)