# はぎゅっとチャット
2025年ハッカソン春の陣入門コースChatApp

### 起動イメージ
<img width="386" height="837" alt="image" src="https://github.com/user-attachments/assets/a5fccb67-b9ff-4023-a9a2-3bece3d83d5e" />

### 環境変数ファイル（.env）を作成します
```
#bash
cp .env.example .env
```

### 起動方法
1.イメージのビルド
```
#bash
docker comose build
```
2.コンテナの起動
```
#bash
docker compose up
```

### ブラウザで確認
```
http://localhost:5500
```

### ディレクトリ構成
```
Fteam
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


