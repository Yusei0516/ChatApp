from flask import Flask, request, redirect, render_template, session, flash, abort, url_for
from datetime import timedelta
import hashlib, uuid, re, os
from models import User, Group, GroupMessage, OpenChat
from models import User, Group, GroupMessage, Opc
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

# #管理者：グループチャット一覧へ
# @app.route('/admin/group/list', methods=['GET'])
# def group_list_view():
#     return render_template('admin/group_list.html')

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

#メニューまとめ(オープンチャット作成)
@app.route('/menu/open/create', methods=['GET'])
def create_open_view():
    return render_template('menu/create_open.html')

#オープンチャット作成処理
app.route('/open_chat/create', methods=['POST'])
def create_open_chat():
    uesr_id = session.get('uid')
    name = request.form.get('name')
    description = request.form.get('description')

    if uesr_id:
        try:
            OpenChat.create(name, description, uesr_id)
            flash('オープンチャットを作成しました。')
        except Exception as e:
            flash(f'エラーが発生しました： {str(e)}')
        #遷移先を判定
        if uesr_id == 'admin@example.com':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))


#まとめ(オープンチャット削除)
@app.route('/menu/open/delete', methods=['GET'])
def delete_open_view():
    return render_template('menu/delete_open.html')
        
#オープンチャットの削除
@app.route('/open_chat/delete/<int:chat_id>', methods=['POST'])        
def delete_open_chat(chat_id):
    user_id = session.get('uid')

    if user_id:
        chat = OpenChat.get(chat_id)
        if chat['creator_id'] == user_id or user_id == 'admin@example.com':
            try:
                OpenChat.delete(chat_id)
                flash('チャットが削除されました')
            except Exception as e:
                flash(f'エラーが発生しました： {str(e)}')
        else:
            flash('権限がありません')
        #遷移先を判定
        if user_id == 'admin@example.com':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))



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

# #ユーザーメニューまとめ(オープンチャット作成)
# @app.route('/user_menu/open/create', methods=['GET'])
# def user_create_open_view():
#     return render_template('user/create_open.html')

# #ユーザーメニューまとめ(オープンチャット削除)
# @app.route('/user_menu/open/delete', methods=['GET'])
# def user_delete_opem_view():
#     return render_template('user/delete_open.html')

# #ユーザーメニューまとめ(オープンチャット作成)
# @app.route('/user_menu/open/create', methods=['GET','POST'])
# def user_create_open_view():
#     uid = session.get('uid')
#     if uid is None:
#         return redirect(url_for('login_view'))
    
#     if request.method =='POST':
#         name = request.form.get('name')
#         opc_room = Opc.find_by_name(name)
#         if opc_room == None:
#             description = request.form.get('open_description')
#             Opc.create(uid, name, description, is_open=False)
#             flash("オープンチャットを作成しました")
#             return redirect(url_for('user_dashboard'))
#         else:
#             flash("既に同じ名前のチャンネルが存在しています")
#             return redirect(url_for('/user_menu/open/create'))
    
#     return render_template('user/create_open.html')

# #ユーザーメニューまとめ(オープンチャット削除ルーム)
# @app.route('/user_menu/open/delete', methods=['GET'])
# def user_delete_open_view():
#     uid = session.get('uid')
#     if uid is None:
#         return redirect(url_for('login_view'))
    
#     return render_template('user/delete_open.html')

# #オープンチャット削除ボタン
# @app.route('/user_menu/open/delete/<int:room_id>', methods=['POST'])
# def delete_button(room_id):
#     uid = session.get('uid')
#     if uid is None:
#         return redirect(url_for('login_view'))
    
#     room = Opc.find_by_room_id(room_id)
    
#     if room['create_id'] != uid:
#         flash('チャンネルは制作者のみ削除可能です')
#     else:
#         Opc.delete(room_id)
#     return redirect(url_for('/user_menu/open/delete'))

#グループチャット(リダイレクト)
@app.route('/group_view', methods=['GET'])
def group_chat_redirect():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    group = Group.find_by_user_id(uid)
    if group is None:
        flash("グループに所属していません")    
        return redirect(url_for('user_dashboard'))

    return redirect(url_for('group_view',group_id=group['id']))

#管理者用グループチャット
@app.route('/admin/group_list', methods=['GET'])
def admin_group_chat_redirect():
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    
    if not Group.is_admin(uid):
        return redirect(url_for('login_view'))

    groups = Group.get_all()
    return render_template('admin/group_list.html', groups=groups)

#グループチャット(管理者、一般ユーザ共通)
@app.route('/group_view/<int:group_id>/messages', methods=['GET','POST'])
def group_view(group_id):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))

    group = Group.find_by_id(group_id)
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            GroupMessage.create(uid, group_id, message)
        return redirect(url_for('group_view', group_id=group_id))

    messages = GroupMessage.get_all(group_id)
    return render_template('user/group_chat.html', group=group, messages=messages)

#管理者用グループチャット右上編集ボタン→管理者用チャンネル編集
@app.route('/admin/create_group/<int:group_id>', methods=['GET','POST'])
def create_group(group_id):
    uid = session.get('uid')
    if uid is None or not Group.is_admin(uid):
        flash("管理者専用ページです")
        return redirect(url_for('login_view'))
    
    group = Group.find_by_id(group_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            Group.update(group_id, name, description)
            flash("グループ情報を更新しました")
            return redirect(url_for('create_group', group_id=group_id))
    
    return render_template('admin/create_group.html', group=group)

#管理者用メンバー登録、削除(ページ遷移のみ)
@app.route('/admin/member_create/<int:group_id>', methods=['GET'])
def member_create(group_id):
    uid = session.get('uid')
    if uid is None or not Group.is_admin(uid):
        flash("管理者専用ページです")
        return redirect(url_for('login_view'))
    
    group = Group.find_by_id(group_id)
    return render_template('admin/member_create.html', group=group)

#グループ一覧→オープンチャット(ページ遷移のみ)
@app.route('/open_chat/<int:opc_id>', methods=['GET'])
def open_chat(opc_id):
    uid = session.get('uid')
    if uid is None:
        return redirect(url_for('login_view'))
    return render_template('user/open_chat.html',opc_id=opc_id)

if __name__ == '__main__': 
    app.run(host="0.0.0.0", debug=True)