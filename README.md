# はぎゅっとチャット
2025年ハッカソン春の陣入門コース（チーム開発 / 期間：2か月間 / メンバー：5人）

Webブラウザで動作するチャットアプリ。

**オープンチャット / グループチャット / 個別チャット** をサポートしています。

---
## 🚀使用技術
- **フロントエンド**：HTML, CSS, JavaScript
- **バックエンド**：Python（Flask）, MySQL
- **インフラ**：Docker
- **開発管理**：GitHub

---
## 👤自分の担当
**認証機能**
- ログイン機能を実装

**個別チャット**
- 管理者とユーザー間の1対1チャット機能を担当
- メッセージ送受信APIを実装

**グループチャット**
- 管理者のみが作成可能なグループチャットを実装
- 招待機能、メンバー削除機能を担当
- グループ内のメッセージ送受信APIを実装

---
## 🗂️機能概要
**オープンチャット**
- 全ユーザーが作成可能、誰でも参加可能
- 作成者 or 管理者が編集・削除可能

**グループチャット**
- 管理者のみ作成可能
- 管理者が招待・削除を行う
- 各ユーザーは最大1グループ所属

**個別チャット**
- 管理者⇔各ユーザーの1対1チャット（ユーザー同士は不可）

**共通機能**
- ユーザー登録 / ログイン
- メッセージ送受信（作成・取得）

---
## 📑 API一覧（抜粋）
### 認証
- `POST /auth/register` … 新規登録
- `POST /auth/login` … ログイン

### オープンチャット
- `GET /open-chats` … 一覧取得  
- `POST /open-chats` … 作成（全ユーザー可）  
- `PATCH /open-chats/{room_id}` … 編集（作成者 or 管理者）  
- `GET /open-chats/{room_id}/messages` … メッセージ一覧  
- `POST /open-chats/{room_id}/messages` … メッセージ送信

## グループチャット
- `POST /groups` … 作成（管理者のみ）  
- `POST /groups/{group_id}/invites` … 招待（管理者のみ）  
- `DELETE /groups/{group_id}/members/{user_id}` … メンバー削除（管理者のみ）  
- `GET /groups/{group_id}/messages` … メッセージ一覧（所属者のみ）  
- `POST /groups/{group_id}/messages` … メッセージ送信（所属者のみ）  

### 個別チャット
- `POST /private-chats` … 開始（ユーザー↔管理者）  
- `GET /private-chats/{chat_id}/messages` … メッセージ一覧  
- `POST /private-chats/{chat_id}/messages` … メッセージ送信

---
## 📂ディレクトリ構成
```
ChatApp
|--- chatApp
|    |--- app.py
|    |--- __init__.py
|    |--- models.py
|    |--- static
|    |--- templates
|         |___ util
|--- Docker  
|    |--- Flask
|    |    |___ Dckerfile  #Flask(Python)用Dockerファイル
|    |___ MySQL
|         |--- Dockerfile  #MySQL用Dockerファイル
|         |--- int.sql  #MySQL初期設定ファイル
|         |___ my.cnf
|--- .env.sample #環境変数のテンプレート  
|--- docker-compose.yml  
|--- requirements.txt  
|___ README.md
```

## ▶️  起動方法
```bash
# 環境変数ファイルの作成
cp .env.example .env

# ビルド
docker compose build

# 起動
docker compose up

# ブラウザで確認
http://localhost:5500
```

### 起動イメージ
<img width="386" height="837" alt="image" src="https://github.com/user-attachments/assets/a5fccb67-b9ff-4023-a9a2-3bece3d83d5e" />
