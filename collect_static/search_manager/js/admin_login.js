function getID(ID) {
    return document.getElementById(ID);
}
function getClassName(classname) {
    return document.getElementsByClassName(classname);
}
function getname(name) {
    return document.getElementsByName(name);

}

function toJson(str) {
    var json = (new Function("return" + str))();
    return json;
}

/*Ajax异步提交*/
//获取 XMLHttpRequest对象

function getXmlHttpRequest() {
    if(window.XMLHttpRequest){
        return new XMLHttpRequest();
    }else {
        /*兼容低版本浏览器*/
        return new ActiveXObject("Microsoft.XMLHTTP");
    }
}
/* 后台登陆 */
function login() {
    if(getID("Inputname").value== "" |
    getID("InputPassword").value == ""){
        getID("header-msg").innerText = "不能提交空值";
    }else{
        getID("header-msg").innerText = "";
        submit();
    }
}
function submit() {
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("POST",login_url, true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var name = getID("Inputname").value;
    var paswd = getID("InputPassword").value;
    var csrf = login_from.csrfmiddlewaretoken.value;
    xmlHttp.send("name=" + name + "&paswd=" + paswd + "&csrfmiddlewaretoken=" + csrf);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                var info = toJson(xmlHttp.responseText)["info"];
                switch (info){
                    case 0:
                        window.location.reload([bForceGet=true]);
                        break;
                    case 1:
                        getID("header-msg").innerText = "账户或密码错误";
                        break
                    case 2:
                        alert("Bad Request");
                        break
                }
            }
        }
    }
}
function logout_manger() {
    var xmlhttp = getXmlHttpRequest();
    xmlhttp.open("get",logout_url,true);
    xmlhttp.send();
    window.location.reload([bForceGet=true]);
}