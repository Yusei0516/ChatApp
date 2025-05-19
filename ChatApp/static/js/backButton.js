// 戻るボタンの作成 //

const backButton = document.getElementsByClassName("backButton");

backButton.addEventListener("click",() =>{
    window.history.back(); // 前のページに戻る
});
