/*
メッセージ送信の際、絵文字を選択
*/


const emojiButton = document.getElementById("showEmojiButton");
const messagearea = document.getElementById("message-area");

emojiButton.addEventListener("click", () => {
    //表示したい絵文字を指定
    const emoji = "😁";"😅";"😭";"😂";"🙇";"🙆";"🔥";"💦";"👍";"👏";
    messagearea.textContent = emoji; //"絵文字を表示
});