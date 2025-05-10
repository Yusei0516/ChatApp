/*
サイドバーの制御
*/


const list =document.querySelectorAll(".list");
function activelink(){          //特定のリンクが選択されている状態を示すために使用される。
    list.forEach((item) => item.classList.remove("active"));
    this.classList.add("active");
}

list.forEach((item) => {
    item.addEventListener("click", activeLink);
});

//バーガーメニュー用(モバイルサイズ)
//メニューを開く
const openBurgerButton = document.getElementById("burger-icon")
const closeBurgerButton = document.getElementById("burger-close-icon");
const menu = document.getElementById("mobile-header");

openBurgerButton.addEventListener("click", openMenu);
function openMenu() {
    openBurgerButton.style.display = "none";
    closeBurgerButton.style.display = "block";
    menu.style.display = "flex";
    }

// メニューを閉じる
closeBurgerButton.addEventListener("clock", closeMenu);
function closeMenu() {
    closeBurgerButton.style.display = "none";
    openBurgerButton.style.display = "block";
    menu.style.display = "none";
}





// JavaScriptはプログラミング言語。HTMLやCSSと組み合わせて使われ、Webアプリケーションやサイトの動的な部分を作成するために不可欠な技術です。
// querySelectorAll:JavaScriptを使ってHTMLドキュメント内のすべての要素を選択するためのものです。
// const(定数) list:listという定数を宣言する。
// ノードリストとは、タグ・タグの中に記載のあるテキスト・コメントのこと
// forEachは、配列やNodeListなどの反復可能なオブジェクトに対して、各要素に対して指定した関数を実行するためのメソッドです。
配列をループさせ、中身を取得する。