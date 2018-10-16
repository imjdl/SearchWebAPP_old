window.onload = function () {
    var xmlhttp = getXmlHttpRequest();
    xmlhttp.open("get", get_port_url + "?ip="+send_ip, true);
    xmlhttp.setRequestHeader("Content-Type","application/x-www-form-urlencoded;charset=UTF-8");
    xmlhttp.setRequestHeader("x-requested-with","XMLHttpRequest");
    xmlhttp.send();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            if(xmlhttp.status == 500){
                getID("loaderv2").style.display = "none";
                getID("port_detial_list").style.display = "block";
                getID("port_detial_list").innerHTML = "<tr><td><span style='color: orangered'><h4>数据暂缺 <a target='_blank' href='http://127.0.0.1/contact/'>点此反馈</a></h4></span></td></tr>";
            }
            if(xmlhttp.status == 200){
                var data = toJson(xmlhttp.responseText);
                var os = data["os"];
                var hostname = data["hostname"];
                var ports = data["ports"];
                getID("loaderv2").style.display = "none";
                getID("port_detial_list").style.display = "block";
                if(os == ""){
                    getID("os").innerText = "Unknow";
                }else{
                    getID("os").innerText = os;
                }
                if(hostname == ""){
                    getID('hostname').innerText = "Unknow";
                }else{
                    getID('hostname').innerText = hostname;
                }
                port_table = getID("port_detial_list_table");
                port_table.innerHTML = " <tr>\n" +
                    "                        <th>端口</th>\n" +
                    "                        <th>STATE</th>\n" +
                    "                        <th>RESON</th>\n" +
                    "                        <th>NAME</th>\n" +
                    "                        <th>VERSION</th>\n" +
                    "                    </tr>"
                for(var i =0;i<ports.length;i++){
                    var port = ports[i];
                    var data = '<tr>' +
                        '<td>'+port["port"]+'</td>' +
                        '<td>'+port["value"]["state"]+'</td>' +
                        '<td>'+port["value"]["reason"]+'</td>' +
                        '<td>'+port["value"]["name"]+'</td>' +
                        '<td>'+port["value"]["version"]+'</td>' +
                        '</tr>';
                    port_table.innerHTML = port_table.innerHTML + data;
                }
            }
        }
    }
}