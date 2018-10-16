var xmlHttp_logout = getXmlHttpRequest();
function logout() {
    var uname = getID("username").text;
    xmlHttp_logout.open("GET", logout_url + "?user="+ uname, true);
    xmlHttp_logout.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp_logout.setRequestHeader("x-requested-with","XMLHttpRequest")
    xmlHttp_logout.send();
    xmlHttp_logout.onreadystatechange = server_responce_process_logout;
}
function server_responce_process_logout() {
    if(xmlHttp_logout.readyState == 4 & xmlHttp_logout.status == 200){
        window.location.reload([bForceGet=true]);
    }
}