function getID(ID) {
    return document.getElementById(ID);
}
function getClassName(classname) {
    return document.getElementsByClassName(classname);
}
function getname(name) {
    return document.getElementsByName(name);

}
function add_info() {
    var sp = getID("data_total");
    sp.innerHTML = data_num;
   /* var mypage = getID("data_page");
    mypage.innerHTML=data_page;
    var allpagenum = getID("data_all_page_num");
    allpagenum.innerHTML = Math.ceil(data_num/10);*/
}
add_info();
