
DROP DATABASE chatapp;
DROP USER 'testuser';

CREATE USER 'testuser' IDENTIFIED BY 'testuser';
CREATE DATABASE chatapp;
USE chatapp;
GRANT ALL PRIVILEGES ON chatapp.* TO 'testuser';

CREATE TABLE users (
    uid VARCHAR(255) PRIMARY KEY,
    user_name VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE private_chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user1_id VARCHAR(255) NOT NULL,
    user2_id VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user1_id) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (user2_id) REFERENCES users(uid) ON DELETE CASCADE
    );

CREATE TABLE private_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    private_chats_id INT NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (private_chats_id) REFERENCES private_chats(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE TABLE group_chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_open BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE group_members (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    group_chats_id INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (group_chats_id) REFERENCES group_chats(id) ON DELETE CASCADE
);

CREATE TABLE group_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    group_chats_id INT NULL,
    user_id VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (group_chats_id) REFERENCES group_chats(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE TABLE open_chats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    creator_id VARCHAR(255) NOT NULL,
    is_open BOOLEAN DEFAULT TRUE,
    description VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(uid) ON DELETE CASCADE
);

CREATE TABLE open_chat_messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    opne_chat_id INT NOT NULL,
    user_id  VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (open_chat_id) REFERENCES open_chat(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(uid) ON DELETE CASCADE
);

INSERT INTO users (uid, user_name, email, password, is_admin) VALUES ('admin123', '管理者', 'admin@example.com', '9d73b154738103148a0baae3bb4b0067fbbb230b9cf50c04db70d6393d324c42', FALSE);
-- INSERT INTO users(uid, user_name, email, password) VALUES('970af84c-dd40-47ff-af23-282b72b7cca8','テスト','test@gmail.com','37268335dd6931045bdcdf92623ff819a64244b53d0e746d438797349d4da578');
INSERT INTO users(uid, user_name, email, password, is_admin) VALUES('b9ec6802-f2a2-4069-81ee-3909ec685','たなかまき','test@gmail.com','ae5deb822e0d71992900471a7199d0d95b8e7c9d05c40a8245a281fd2c1d6684', FALSE);
INSERT INTO group_chats(name, creator_id, is_open) VALUES('開発者グループ', 'admin123456789', FALSE);
INSERT INTO open_chats(name, creator_id, is_open, description) VALUES('アニメ好き集まれ', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなアニメについて話しましょう！');
INSERT INTO open_chats(name, creator_id, is_open, description) VALUES('ドラマ好き集まれ', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなドラマについて話しましょう！');
INSERT INTO open_chats(name, creator_id, is_open, description) VALUES('バンド好き集まれ', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなバンドについて話しましょう！');
-- INSERT INTO chat_rooms(name, type, creator_id, is_open) VALUES('開発者グループ', 'group', 'admin123456789', FALSE);
-- INSERT INTO chat_rooms(name, type, creator_id, is_open, description) VALUES('アニメ好き集まれ', 'open', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなアニメについて話しましょう！');
-- INSERT INTO chat_rooms(name, type, creator_id, is_open, description) VALUES('ドラマ好き集まれ', 'open', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなドラマについて話しましょう！');
-- INSERT INTO chat_rooms(name, type, creator_id, is_open, description) VALUES('バンド好き集まれ', 'open', 'b9ec6802-f2a2-4069-81ee-3909ec6851ad', TRUE, '好きなバンドについて話しましょう！');
-- INSERT INTO messages(id, uid, cid, message) VALUES(1, '970af84c-dd40-47ff-af23-282b72b7cca8', '1', '誰かかまってください、、')