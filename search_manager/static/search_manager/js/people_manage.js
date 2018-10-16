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
    var json = (new Function("return"+str))();
    return json;
}
var total = 0;
function getpeople() {
    var xmlHttp = getXmlHttpRequest();
    xmlHttp.open("post", getpeope_url, true);
    xmlHttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlHttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var page = getID("page").value;
    var csrf = get_people_data.csrfmiddlewaretoken.value;
    var data = "page=" + page + "&csrfmiddlewaretoken=" + csrf;
    xmlHttp.send(data);
    xmlHttp.onreadystatechange = function () {
        if(xmlHttp.readyState == 4){
            if(xmlHttp.status == 200){
                var data_list = toJson(xmlHttp.responseText)["data_list"];
                total = toJson(xmlHttp.responseText)["total"];
                var tbody = getID("table_data2people");
                tbody.innerHTML = "";
                for(var i=0;i<data_list.length;i++){
                    var tr = document.createElement("tr");
                    var td_name = document.createElement("td");
                    var td_email = document.createElement("td");
                    var td_flag = document.createElement("td");
                    var td_oper = document.createElement("td");
                    var input_but = document.createElement("input");

                    td_name.innerText = data_list[i]["name"];
                    td_email.innerText = data_list[i]["email"];
                    td_flag.innerText = data_list[i]["flag"];
                    if(data_list[i]["flag"]=="正常"){
                        input_but.value = "禁用";
                        input_but.style = "background-color:red";
                    }else{
                        input_but.value = "解禁";
                        input_but.style = "background-color:green";
                    }
                    input_but.type = "button";
                    input_but.onclick = function () {
                        chang_state_people(this.parentNode.parentNode);
                    };
                    td_oper.appendChild(input_but);
                    tr.appendChild(td_name);
                    tr.appendChild(td_email);
                    tr.appendChild(td_flag);
                    tr.appendChild(td_oper);
                    tr.id= i;
                    tbody.appendChild(tr);
                }
                run();
            }
        }
    }
}
getpeople();
// run();
function chang_state_people(node) {
    var id = node.id ;
    var name = node.firstChild.innerText;
    var xmlhttp = getXmlHttpRequest();
    xmlhttp.open("post",change_url,true);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = get_people_data.csrfmiddlewaretoken.value;
    xmlhttp.send("name="+name+"&id="+id + "&csrfmiddlewaretoken="+csrf);
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            if(xmlhttp.status == 200){
                var tbody = getID("table_data2people");
                var trs = tbody.childNodes;
                var id = toJson(xmlhttp.responseText)["id"];
                var tr = trs[id];
                tds = tr.childNodes;
                var state = tds[2];
                var state_but = tds[3].firstChild;
                if(state.innerText == "正常"){
                    state.innerText = "已禁用";
                    state_but.value = "解禁";
                    state_but.style = "background-color:green";
                }else{
                    state.innerText = "正常";
                    state_but.value = "禁用";
                    state_but.style = "background-color:red";
                }
                // alert(trs[0].firstChild.innerText);
            }
        }
    }
}
