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
var xmlHttp = getXmlHttpRequest();
function submit_data_login() {
    xmlHttp.open("POST", login_url, true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp.setRequestHeader("x-requested-with","XMLHttpRequest")
    var csrf = login_from.csrfmiddlewaretoken.value;
    var email = getID("email").value;
    var paswd = getID("paswd").value;
    var code = getID("code").value;
    if(email && paswd && code){
        xmlHttp.send("email=" + email +"&paswd=" + paswd +"&code=" + code + "&csrfmiddlewaretoken=" + csrf);
        xmlHttp.onreadystatechange = server_responce_process_login;
    }else{
        var showword = getID("show_word");
        showword.innerText = "提示:请将数据补充完整";
        showword.style.opacity = 1;
    }
}
function server_responce_process_login() {
    if(xmlHttp.readyState == 4 & xmlHttp.status == 200){
        var state = toJson(xmlHttp.responseText)["login_info"]
        if(state == 0){
            window.location.reload([bForceGet=true]);
        }else if(state == 2){
            /*验证码错误*/
            getID("code_worong").style.opacity = 1;
            var showword = getID("show_word");
            showword.innerText = "提示:验证码错误";
            showword.style.opacity = 1;
        }else if(state == 1){
            getID("email_worong").style.opacity = 1;
            getID("pswd_worong").style.opacity = 1;
            var showword = getID("show_word");
            showword.innerText = "提示:邮箱或密码错误错误";
            showword.style.opacity = 1;
        }else if(state == 3){
            // getID("email_worong").style.opacity = 1;
            // getID("pswd_worong").style.opacity = 1;
            var showword = getID("show_word");
            showword.innerText = "提示:用户已禁用";
            showword.style.opacity = 1;
        }
    }
    if(xmlHttp.readyState == 4 & xmlHttp.status == 400){
        /*
         *错误的请求
         */
        alert("Bad Request");
    }
}

function toJson(str) {
    var json = (new Function("return"+str))();
    return json;
}
/*判断email 是否符合格式*/
function isEmail(str){
    var reg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+((\.[a-zA-Z0-9_-]{2,3}){1,2})$/;
    return reg.test(str);
}
/*倒计时 并发送请求邮件*/
var timer_email;
function countdown(ths) {
    /*先要判断email是否符合格式以及不能为空*/
    var my_email = getID("email_reg").value;
    if(my_email!="" & isEmail(my_email)){
        var wait = 60;
        ths.setAttribute("disabled", true);
        timer_email = setInterval(function () {
            wait --;
            ths.value = "重新发送(" + wait +"s)";
            if(wait == 0){
                ths.value = "获取验证码";
                ths.removeAttribute("disabled");
                clearInterval(timer_email);
            }
        },1000);
        questemailcode(my_email,ths);
    }else{
        getID("email_reg_worong").style.opacity = 1;
        var showword = getID("show_word");
        showword.style.opacity = 1;
        showword.innerText = "提示：邮箱格式错误";
    }
}

/*请求邮箱验证码*/
function questemailcode(email, ths) {
    var xmlHttp_reg = getXmlHttpRequest();
    xmlHttp_reg.open("POST", email_code_url, true);
    xmlHttp_reg.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp_reg.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = register_from.csrfmiddlewaretoken.value;
    var data = "email="+email + "&csrfmiddlewaretoken=" + csrf;
    xmlHttp_reg.send(data);
    xmlHttp_reg.onreadystatechange = function () {
        if(xmlHttp_reg.readyState == 4){
            if (xmlHttp_reg.status == 200){
            }
            if(xmlHttp_reg.status == 400){
                getID("email_reg_worong").style.opacity = 1;
                var showword = getID("show_word");
                showword.style.opacity = 1;
                showword.innerText = "提示：邮箱已注册";
                clearInterval(timer_email);
                ths.value = "获取验证码";
                ths.removeAttribute("disabled");
            }
        }
    }
}
/*数据验证(基本验证，是否为空，传到后台还需在过滤一遍 防止XSS)*/
function data_process() {
    var flag = true;
    var email = getID("email_reg");
    var name = getID("name_reg");
    var paswd = getID("paswd_reg");
    var paswd_agin = getID("paswd_reg_agin");
    var email_code = getID("email_code");
    var email_tag = getID("email_reg_worong");
    var name_tag = getID("name_reg_worong");
    var paswd_tag = getID("paswd_reg_worong");
    var paswd_agin_tag =  getID("paswd_reg_agin_worong");
    var email_code_tag = getID("email_code_reg_worong");
    var data = [email,name,paswd,paswd_agin,email_code];
    var tags = [email_tag,name_tag,paswd_tag,paswd_agin_tag,email_code_tag];
    var showword = getID("show_word");
    var word = "提示:"
    for(var i=0;i<5;i++){
        if(data[i].value == ""){
            flag = false;
            tags[i].style.opacity = 1;
            showword.style.opacity = 1;
            word += "提交的内容不能为空";
            showword.innerText = word;
            return flag;
        }else if(i==0){
            if (!isEmail(data[i].value)){
                flag = false;
                tags[i].style.opacity = 1;
                showword.style.opacity = 1;
                word += "邮箱格式错误 ";
                showword.innerText = word;
                return flag;
            }
        }else if (i==3){
            if(data[i].value != data[i-1].value){
                flag = false;
                tags[i].style.opacity = 1;
                showword.style.opacity = 1;
                word += "两次密码不一致";
                showword.innerText = word;
                return flag;
            }
        }
    }
    showword.innerText = word;
    return flag;
}
function cheakdata(tag) {
    var showword = getID("show_word");
    showword.innerText = "";
    showword.style.opacity = 1;
    var email = getID("email_reg");
    var name = getID("name_reg");
    var paswd = getID("paswd_reg");
    var paswd_agin = getID("paswd_reg_agin");
    var email_code = getID("email_code");
    var email_tag = getID("email_reg_worong");
    var name_tag = getID("name_reg_worong");
    var paswd_tag = getID("paswd_reg_worong");
    var paswd_agin_tag =  getID("paswd_reg_agin_worong");
    var email_code_tag = getID("email_code_reg_worong");
    switch (tag){
        case "email":
            if(!isEmail(email.value)){
                email_tag.style.opacity = 1;
                showword.innerText = "提示:邮箱格式不对";
            }else{
                email_tag.style.opacity = 0;
                showword.innerText = "";
            }
            /*检测邮箱是否已经注册*/
            break;
        case "name":
            /*检测用户名是否已经存在*/
            break;
    }
}
function cheakdata_login() {
    var email =getID("email");
    var email_tag =getID("email_worong");
    var showword = getID("show_word");
    showword.innerText = "";
    showword.style.opacity = 1;
    if(!isEmail(email.value)){
        email_tag.style.opacity = 1;
        showword.innerText = "提示:邮箱格式不对";
    }else{
        email_tag.style.opacity = 0;
        showword.innerText = "";
    }
}
/*注册请求*/
function submit_data_reg() {
    var email = getID("email_reg").value.trim();
    var name = getID("name_reg").value.trim();
    var paswd = getID("paswd_reg").value.trim();
    var email_code = getID("email_code").value.trim();
    var showword = getID("show_word");
    var email_tag = getID("email_reg_worong");
    var name_tag = getID("name_reg_worong");
    var paswd_tag = getID("paswd_reg_worong");
    var email_code_tag = getID("email_code_reg_worong");
    if(data_process()){
        var xmlHttp_reg = getXmlHttpRequest();
        xmlHttp_reg.open("POST", register_url, true);
        xmlHttp_reg.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
        xmlHttp_reg.setRequestHeader("x-requested-with","XMLHttpRequest");
        var csrf = register_from.csrfmiddlewaretoken.value;
        var reg_data = "email=" + email + "&name=" + name + "&paswd=" + paswd
        + "&email_code=" + email_code + "&csrfmiddlewaretoken=" + csrf;
        xmlHttp_reg.send(reg_data);
        xmlHttp_reg.onreadystatechange = function () {
            if(xmlHttp_reg.readyState == 4 & xmlHttp_reg.status == 200){
                var tag = toJson(xmlHttp_reg.responseText)["reg_info"];
                switch (tag){
                    case 0:
                        showword.innerText = "";
                        showword.style.opacity = 1;
                        showword.innerText = "提示:邮箱验证码错误";
                        email_code_tag.style.opacity = 1;
                        break;
                    case 1:
                        showword.innerText = "";
                        showword.style.opacity = 1;
                        showword.innerText = "提示:邮箱已经注册";
                        email_tag.style.opacity = 1;
                        break;
                    case 2:
                        showword.innerText = "";
                        showword.style.opacity = 1;
                        showword.innerText = "提示:用户已经存在";
                        name_tag.style.opacity = 1;
                        break;
                    case 3:
                        showword.innerText = "";
                        showword.style.opacity = 1;
                        showword.innerText = "提示:密码太短";
                        paswd_tag.style.opacity = 1;
                        break;
                    case 4:
                        window.location.reload([bForceGet=true]);
                        break;
                }
            }
        }
    }
}

function cancelworong(ths) {
    ths.style.opacity = 0;
}


/*处理淡入淡出效果*/
var Fadeflag = true;
var st ;
function Fade() {
    /**
     * 淡入效果
     */
    this.show = function(obj) {
        clearInterval(st);
        var num = 0;
        if (Fadeflag) {
            st = setInterval(function(){
                num++;
                Fadeflag = false;
                obj.style.opacity = num/10;
                if (num>=10) {
                    clearInterval(st);
                    Fadeflag = true;
                }
            },20);
        }
    }
    /**
     * 淡出效果
     */
    this.hide = function(obj) {
        clearInterval(st);
        var num = 10;
        if (Fadeflag) {
            st = setInterval(function(){
                num--;
                Fadeflag = false;
                obj.style.opacity = num/10;
                if (num<=0) {
                    clearInterval(st);
                    Fadeflag = true;
                }
            },20);
        }
    }
}
function show_login(ths) {
    var login_panel = getClassName("login_pane")[0];
    login_panel.style.display = "block";
    var fead = new Fade();
    fead.show(login_panel);
}
function hide_login() {
    var login_panel = getClassName("login_pane")[0];
    login_panel.style.display = "none";
    var fead = new Fade();
    fead.hide(login_panel);
}

/*忘记密码处理*/
function forgetpaswd(flg) {
    var a = getID("login_id_table");
    var b = getID("forget_id");
    if(flg){
        a.style.display = "none";
        b.style.display = "block";
        getword();
    }else{
        a.style.display = "block";
        b.style.display = "none";
    }
}
function forgetpasswd_v2(flg) {
    var a = getID("forget_from_id");
    var b = getID("change_paswd_id");
    if(flg){
        a.style.display = "none";
        b.style.display = "block";
    }else{
        a.style.display = "block";
        b.style.display = "none";
    }
}
function getword() {
    var goodword = getXmlHttpRequest();
    goodword.open("get", "https://sslapi.hitokoto.cn/?encode=json", true);
    goodword.send();
    goodword.onreadystatechange = function () {
        if (goodword.readyState == 4 & goodword.status == 200){
            var word = toJson(goodword.responseText);
            getID("for_goodword").innerText = word["hitokoto"];
            getID("for_goodword_author").innerText = word["from"];
        }
    }
}
function cheak_email(email, wor) {
    var xml = getXmlHttpRequest();
    xml.open("post", for_url, true);
    xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xml.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = forget_data.csrfmiddlewaretoken.value;
    var data = "email=" + email.value + "&csrfmiddlewaretoken=" + csrf;
    xml.send(data);
    var load_state = getID("spinner");
    load_state.style.display = "block";
    xml.onreadystatechange = function () {
        if(xml.readyState == 4 && xml.status == 200){
            var state = toJson(xml.responseText);
            if (state["isExit"] == 0){
                wor.style.opacity = 1;
                wor.innerText = "邮箱不存在";
                load_state.style.display = "none";
            }else if(state["isExit"] == 1){
                /*发送验证码 等待时间*/
                wor.style.opacity = 0;
                wor.innerText = "X";
                alert("校验码已发送至你的邮箱");
                email.value = "";
                getword();
                forgetpasswd_v2(true);
                load_state.style.display = "none";
            }
        }
    }
}
function forget_email(ths) {
    var wor = getID("for_email");
    if(!isEmail(ths.value)){
        wor.style.opacity = 1;
    }else{
        wor.style.opacity = 0;
        cheak_email(ths, wor);
    }
}
function changepaswd() {
    var code = change_paswd_from.change_code.value;
    var newpaswd = change_paswd_from.newpaswd.value;
    if(code!="" & newpaswd !=""){
        var xml = getXmlHttpRequest();
        xml.open("post", change_url, true);
        xml.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
        xml.setRequestHeader("x-requested-with","XMLHttpRequest");
        var csrf = change_paswd_from.csrfmiddlewaretoken.value;
        var data = "code=" + code + "&newpasswd=" + newpaswd + "&csrfmiddlewaretoken=" + csrf;
        xml.send(data);
        xml.onreadystatechange = function () {
            if(xml.readyState == 4 & xml.status == 200){
                var state = toJson(xml.responseText);
                if(state["changinfo"] == 0){
                    alert("校验码错误");
                    getID("chang_code").style.opacity = 1;
                }else if(state["changinfo"] == 1){
                    alert("修改成功");
                    getID("chang_code").style.opacity = 0;
                    window.location.reload([bForceGet=true]);
                }
            }
        }
    }else{
        alert("请将数据填写完整");
    }
}
/*
var person = (new Function("return"+"name:bob"));
alert(person()["name"]);
*/