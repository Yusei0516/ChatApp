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
const openBurgerButton = document.getElementById("admin-burger-icon")
const closeBurgerButton = document.getElementById("admin-burger-close-icon");
const menu = document.getElementById("admin_menu");

openBurgerButton.addEventListener("click", openMenu);
function openMenu() {
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