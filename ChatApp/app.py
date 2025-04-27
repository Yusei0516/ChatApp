from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib, uuid, re, os
from models import User, Group, Channel, Message
from util.assets import bundle_css_files
 
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

#管理者用ダッシュボード
@app.route('/admin/dashboard')
def admin_dashboard():
    return render_template('admin/dashboard.html')

#一般ユーザー用ダッシュボード
@app.route('/user/dashboard')
def user_dashboard():
    return render_template('user/dashboard.html')


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_view'))

# #グループチャット
# @app.route('/group_list', methods=['GET'])
# def group_chat():
#     uid = session.get('uid')
#     if uid is None:
#         return redirect(url_for('login_view'))
    
#     group = Group.find_by_user_id(uid)
#     if group is None:
#         flash("グループに所属していません")
#         return redirect(url_for('user_dashboard'))
#     return redirect(url_for('group_chat,group_id=group['id']'))