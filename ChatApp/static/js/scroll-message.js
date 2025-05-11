/*
各チャンネル詳細ページ内、ページ読み込み時に自動でしまたでスクロールする
*/

const element = document.getElementById("message-area")
const offset = (16 * window.innerHeight) / 100; // 16vhを計算
const elementBottom = element.getBoundingClientRect().bottom;

window.scrollBy({
    top:elementBottom - window.innerHeight + offset,
    behavior:"auto",
});

// const element = document.getElementById("message-area") document:HTMLドキュメント、 message-areというidをもつ要素を取得。
// offset:補正する。このオフセット値は、要素の位置を調整したり、スクロール位置を計算したりする際に役立ちます。
// このコードを実行すると、ウィンドウの高さの16%に相当するピクセル数がコンソールに表示されます。
// getBoundingClientRect(): このメソッドは、要素のサイズとその位置を含むオブジェクトを返します。このオブジェクトには、要素のtop、right、bottom、left、width、heightなどのプロパティが含まれています。