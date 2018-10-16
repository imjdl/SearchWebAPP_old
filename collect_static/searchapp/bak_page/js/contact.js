function getID(ID) {
    return document.getElementById(ID);
}
function getClassName(classname) {
    return document.getElementsByClassName(classname);
}
function getname(name) {
    return document.getElementsByName(name);

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
function toJson(str) {
    var json = (new Function("return"+str))();
    return json;
}
function submit() {
    var text_data = getID("text_value").value;
    var choice = getID("select_choice").value;
    var code = getID("text_value_code").value;
    if(text_data == "" || choice == "" || code == ""){
        alert("请将数据补充完整");
        return;
    }
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("post",submit_data_url,true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = sugest_from.csrfmiddlewaretoken.value;
    var mydata = "text=" + text_data + "&code=" + code + "&choice="+ choice +  "&csrfmiddlewaretoken=" + csrf;
    xmlHttp.send(mydata);
    xmlHttp.onreadystatechange = function () {
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                var info = toJson(xmlHttp.responseText);
                if(info["info"] == 0){
                    alert("提交成功，感谢您的反馈！！");
                    window.location.reload([bForceGet=true]);
                }
                if(info["info"] == 1){
                    alert("验证码错误！！");
                }
            }
        }
    }
}

