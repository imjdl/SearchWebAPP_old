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
    var json = (new Function("return" + str))();
    return json;
}
var data_total;
function get_artical() {
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("post", artical_url, true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var page = getID("page").value;
    var csrf = get_artical_data.csrfmiddlewaretoken.value;
    var data = "page=" + page + "&csrfmiddlewaretoken=" + csrf;
    xmlHttp.send(data);
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                // alert(xmlHttp.responseText);
                var data = toJson(xmlHttp.responseText);
                data_total =  data["total"];
                var data_artical = data["artical_list"];
                var tbody = getID("table_data2artical");
                tbody.innerHTML="";
                for(var i=0; i<data_artical.length;i++){
                    var tr = document.createElement("tr");
                    var td_name = document.createElement("td");
                    var td_type = document.createElement("td");
                    var td_date = document.createElement("td");
                    var td_state = document.createElement("td");
                    var td_look = document.createElement("td");
                    var td_look_but = document.createElement("input");
                    var td_look_hiden = document.createElement("input");
                    td_look_hiden.value = data_artical[i]["id"];
                    td_look_hiden.type = "hidden";
                    td_look_but.value = "查看内容";
                    td_look_but.type = "button";
                    //事件
                    td_look_but.onclick = function () {
                        get_detial(this.parentNode.parentNode);
                    };
                    td_look.appendChild(td_look_but);
                    td_name.innerText = data_artical[i]["name"];
                    td_type.innerText = data_artical[i]["title"];
                    td_date.innerText = data_artical[i]["date"];
                    td_state.innerText = data_artical[i]["flag"];
                    tr.appendChild(td_name);
                    tr.appendChild(td_type);
                    tr.appendChild(td_date);
                    tr.appendChild(td_state);
                    tr.appendChild(td_look);
                    tr.appendChild(td_look_hiden);
                    tbody.appendChild(tr);
                }
                run();
            }
        }
    }
}
get_artical();

function get_detial(node) {
    var id = node.lastChild.value;
    var xmlhttp = getXmlHttpRequest();
    xmlhttp.open("post", artical_detal_url, true);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = get_artical_data.csrfmiddlewaretoken.value;
    var data = "id=" + id + "&csrfmiddlewaretoken=" + csrf;
    xmlhttp.send(data);
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            if(xmlhttp.status == 200){
                var text = toJson(xmlhttp.responseText)["text"];
                alert(text);
                get_artical();
            }
        }
    }
}