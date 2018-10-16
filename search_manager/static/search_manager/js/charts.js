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

function get_seardata() {
    var xmlHttp_getseardata = getXmlHttpRequest();
    xmlHttp_getseardata.open("get",getdata,true);
    xmlHttp_getseardata.send();
    xmlHttp_getseardata.onreadystatechange = function () {
        if (xmlHttp_getseardata.readyState == 4) {
            if (xmlHttp_getseardata.status == 200) {
                var data = toJson(xmlHttp_getseardata.responseText);
                var webdata = data["webdata"];
                // var product = data["product"];
                var myChart =  echarts.init(getID("myAreaChart"));
                myChart.showLoading();
                var category = [];
                var barData = [];
                for (var i = 0; i < webdata.length - 1; i++) {
                    category.push(webdata[i]["name"]);
                    barData.push(webdata[i]["value"]);
                }
                myChart.hideLoading();

                var option = {
                    title: {
                        text: '搜索引擎数据'
                    },
                    tooltip: {},
                    xAxis: {
                        data: category
                    },
                    yAxis: {},
                    series: [{
                        name: '数量',
                        type: 'bar',
                        data: barData
                    }],
                    // backgroundColor: '#2c343c'
                    textStyle: {
                        color: 'rgba(2, 25, 25, 0.6)'
                    },
                    itemStyle: {
                        normal: {
                            // 设置扇形的颜色
                            color: 'rgba(255,100,14,0.8)',
                            shadowBlur: 200,
                            shadowColor: 'rgba(255,100,14,0.5)'
                        }
                    }
                };
                myChart.setOption(option);
            }
        }
    };
};
get_seardata();
var data_page;
var data_num;
function get_tabledata() {
    var xmlHttp = getXmlHttpRequest();
    var page = getID("page").value;
    var msg = getID('msg').value;
    xmlHttp.open("get", getsearchdata + "?page=" + page + "&msg=" + msg, true);
    xmlHttp.send()
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState == 4) {
            if (xmlHttp.status == 200) {
                var data = toJson(xmlHttp.responseText);
                // alert(data['all_hits'].length);
                msg.value = data['tag'];
                data_page = data['page'];
                data_num = data['total'];
                getID("table_data").innerHTML = "";
                for (var i = 0; i < data["all_hits"].length; i++) {
                    var tr = document.createElement("tr");
                    var td_ip = document.createElement("td");
                    td_ip.innerText = data["all_hits"][i]["ip"];
                    var td_server = document.createElement("td");
                    td_server.innerText = data["all_hits"][i]["server"];
                    var td_prowerd = document.createElement("td");
                    td_prowerd.innerText = data["all_hits"][i]["prowerd"];
                    var td_title = document.createElement("td");
                    td_title.innerText = data["all_hits"][i]["title"];
                    var td_delete = document.createElement("td");
                    var but = document.createElement("input");
                    but.style.cursor = "pointer";
                    but.type = "button";
                    but.value = "删除";
                    but.onclick = function () {
                        delete_node(this.parentNode.parentNode.firstChild);
                    };
                    td_delete.appendChild(but);
                    tr.appendChild(td_ip);
                    tr.appendChild(td_server);
                    tr.appendChild(td_prowerd);
                    tr.appendChild(td_title);
                    tr.appendChild(td_delete);
                    getID("table_data").appendChild(tr);
                }
                run();
            }
        }
    }
}
function delete_node(ths) {
    var xmlhttp = getXmlHttpRequest();
    xmlhttp.open("post",delete_data_sr,true);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    var csrf = csrf_token.csrfmiddlewaretoken.value;
    xmlhttp.send("ip="+ths.innerText+"&csrfmiddlewaretoken=" + csrf);
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            if(xmlhttp.status == 200){
                var info = toJson(xmlhttp.responseText);
                if(info["info"] == 1){
                    alert("删除失败");
                }else {
                    ths.parentNode.parentNode.removeChild(ths.parentNode);
                }
            }
        }
    }
}
get_tabledata();
GateOne.init({ url: "https://127.0.0.1" });