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

window.onload = function () {
    var tir;
    var tirv2;
    try {
        tir = setInterval(get_msg,1000);
    }catch (e){
        clearInterval(tirv2);
    }
    try{
        tirv2 = setInterval(get_system_msg,2000);
    }catch(e) {
        clearInterval(tirv2);
    }
    var tirv3 = setInterval(get_process,1000);
}
function get_msg() {
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("get",get_new_msg_url,true);
    xmlHttp.send();
    xmlHttp.onreadystatechange = function () {
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                var info = toJson(xmlHttp.responseText)["data_list"];
                var send_speed = toJson(xmlHttp.responseText)["send_speed"];
                var recv_speed = toJson(xmlHttp.responseText)["recv_speed"];
                var boot_time = toJson(xmlHttp.responseText)["boot_time"];
                getID("send_speed").innerText = "上传:" + send_speed + "/s";
                getID("recv_speed").innerText = "下载:" + recv_speed + "/s";
                getID("boot_time").innerText = "运行" + boot_time;
                if(info.length >0){
                    // getID("new_Messages").innerText = info.length + " New Message";
                    getID("message_num").innerText = info.length + " New";
                    getID("message_num").style.display = "inline-block";
                    getID("new_msg_flag").style.display = "inline-block";
                    getID("new_mesg_list").innerHTML = "<h6 class=\"dropdown-header\">New Messages:</h6>";
                    for(var i=0;i<info.length;i++){
                        var msg = '<div class="dropdown-divider"></div>\n' +
                            '                        <a class="dropdown-item" href="#">\n' +
                            '                            <strong>'+ info[i]["name"] +'</strong>\n' +
                            '                            <span class="small float-right text-muted">'+ info[i]["date"] +'</span>\n' +
                            '                            <div class="dropdown-message small">'+ info[i]["text"] +'</div>\n' +
                            '                        </a>';
                        getID("new_mesg_list").innerHTML = getID("new_mesg_list").innerHTML + msg;
                    }
                    getID("new_mesg_list").innerHTML = getID("new_mesg_list").innerHTML + "<div class=\"dropdown-divider\"></div>\n" +
                        "            <a class=\"dropdown-item small\" href=\"#\">View all messages</a>";
                }else {
                    getID("new_msg_flag").style.display = "none";
                    getID("message_num").style.display = "none";
                    // getID("new_Messages").innerText = 0 + " New Message";
                }
            }
        }
    }
}
function get_system_msg() {
    var xmlHttp = getXmlHttpRequest();
    try{
        xmlHttp.open("get", get_system_msg_url, true);
        xmlHttp.send();
        xmlHttp.onreadystatechange = function () {
            if (xmlHttp.readyState == 4) {
                if (xmlHttp.status == 200) {
                    var data = toJson(xmlHttp.responseText);
                    //处理cpu信息
                    var cpu = data["cpu"];

                    getID("disk1").innerHTML = '<p style="font-size: 50px">' + cpu[0] + '%</p>'
                        +'<p style="font-size: 20px">CPU1</p>\n';
                    getID("disk2").innerHTML = '<p style="font-size: 50px">' + cpu[1] + '%</p>'
                        +'<p style="font-size: 20px">CPU2</p>\n';

                    var memory = data["memory"];
                    getID("sys_meorry").innerHTML = '                    <p style="font-size: 50px">' + memory["percent"] + '%</p>'
                        + '<p style="font-size: 20px">内存共:'+ memory["total"] +'G</p>\n' +
                        '                    <p style="font-size: 20px">已用:' + memory["used"] + 'G</p>';
                }
            }
        }
    }catch (e){

    }
}
function get_process() {
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("get", get_process_url, true);
    xmlHttp.send();
    xmlHttp.onreadystatechange = function () {
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                var data = toJson(xmlHttp.responseText);
                var procress = data["procress"];
                getID("my_procress").innerHTML = "";
                for(var i=0;i<procress.length;i++){
                    getID("my_procress").innerHTML = getID("my_procress").innerHTML +'<tr>\n' +
                        '                  <td>'+ procress[i]['pid'] +'</td>\n' +
                        '                  <td>'+ procress[i]['name'] +'</td>\n' +
                        '                  <td>'+ procress[i]['username'] +'</td>\n' +
                        '                  <td>'+ procress[i]['cpu_percent'] +'%</td>\n' +
                        '                  <td>'+ procress[i]['create_time'] +'</td>\n' +
                        '                </tr>';
                }
            }
        }
    }
}