/*
サイドバーの制御
*/


const list =document.querySelectorAll(".list");
function activeLink(){          
    list.forEach((item) => item.classList.remove("active")); 
    this.classList.add("active");
}
//itemは何をさしているのか。

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
    console.log("111")
    openBurgerButton.style.display = "none"; 
    closeBurgerButton.style.display = "block"; 
    menu.style.display = "flex"; 
    }

// メニューを閉じる
closeBurgerButton.addEventListener("click", closeMenu);
function closeMenu() {
    closeBurgerButton.style.display = "none"; 
    openBurgerButton.style.display = "block"; 
    menu.style.display = "none";
}





// JavaScriptはプログラミング言語。HTMLやCSSと組み合わせて使われ、Webアプリケーションやサイトの動的な部分を作成するために不可欠な技術です。
// querySelectorAll:JavaScriptを使ってHTMLドキュメント内のすべての要素を選択するためのものです。
// const(定数) list:listという定数を宣言する。
// JavaScriptでdocument.querySelectorやdocument.querySelectorAllを使って、クラス名がlistの要素を取得する際に使います。
// ノードリストとは、タグ・タグの中に記載のあるテキスト・コメントのこと
// function activelink():特定のリンクが選択されている状態を示すために使用される。
// forEachは、配列やNodeListなどの反復可能なオブジェクトに対して、各要素に対して指定した関数を実行するためのメソッドです。

// 配列をループさせ、中身を取得する。
// document.getElementById("burger-icon"): getElementByIdメソッドを使って、id属性が"burger-icon"の要素を取得します。このメソッドは、指定したidを持つ最初の要素を返します。
// getElementByIdは、JavaScriptのDOM操作メソッドの一つで、指定したid属性を持つHTML要素を取得するために使用されます。
// addEventListenerは、JavaScriptでイベントを処理するためのメソッドです。このメソッドを使うことで、特定の要素に対してイベントリスナーを追加し、ユーザーのアクション（クリック、キーボード入力、マウス移動など）に応じて特定の処理を実行できます。
// .classListは、JavaScriptでHTML要素のクラス属性を操作するためのプロパティです。このプロパティを使うことで、要素のクラスを簡単に追加、削除、確認することができます。
// openMenuという関数は、通常、ナビゲーションメニューやハンバーガーメニューを開くための処理を行うために使われます。以下は、基本的なopenMenu関数の例です。
// フレックスボックス（Flexbox）は、CSSのレイアウトモデルの一つで、要素の配置やサイズを柔軟に制御するための方法です。主に、コンテナ内のアイテムを効率的に配置するために使用されます。