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
window.onload = function () {
   xmlHttp.open("get",getdata,true);
   xmlHttp.send();
   xmlHttp.onreadystatechange = anylandata;
}
function anylandata() {
    if(xmlHttp.readyState ==4 ){
        if(xmlHttp.status == 200){
            var data = toJson(xmlHttp.responseText);
            var webdata = data["webdata"];
            var product = data["product"];
            getID("webapp_value").innerText = webdata[webdata.length-1]["nums"];
            getID("zujian_value").innerText = product[product.length-1]["nums"];
            var myChart = echarts.init(document.getElementById('main1'));
            myChart.showLoading();
            var category = [];
            var barData = [];
            for(var i = 0;i<webdata.length-1;i++){
                category.push(webdata[i]["name"]);
                barData.push(webdata[i]["value"]);
            }
            myChart.hideLoading();
            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: true
                    },
                    position: 'top'
                },
                yAxis: {
                    type: 'category',
                    data: category,
                    splitLine: {
                        show: false
                    },
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: false
                    },
                    offset: 10,
                    nameTextStyle: {
                        fontSize: 15
                    }
                },
                series: [{
                    name: '数量',
                    type: 'bar',
                    data: barData,
                    barWidth: 14,
                    barGap: '20%',
                    smooth: true,
                    label: {
                        normal: {
                            show: true,
                            position: 'right',
                            offset: [5, -2],
                            textStyle: {
                                color: '#F68300',
                                fontSize: 13
                            }
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            barBorderRadius: 7
                        },
                        normal: {
                            barBorderRadius: 7,
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 1, 0, [{
                                    offset: 0,
                                    color: '#3977E6'
                                }, {
                                    offset: 1,
                                    color: '#37BBF8'
                                }

                                ]
                            )
                        }
                    }
                }]
            };
            myChart.setOption(option);
            var myChart = echarts.init(document.getElementById('main2'));
            myChart.showLoading();
            var category = [];
            var barData = [];
            for(var i = 0;i<product.length-1;i++){
                category.push(product[i]["name"]);
                barData.push(product[i]["value"]);
            }
            myChart.hideLoading();
            var option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: true
                    },
                    position: 'top'
                },
                yAxis: {
                    type: 'category',
                    data: category,
                    splitLine: {
                        show: true
                    },
                    axisLine: {
                        show: true
                    },
                    axisTick: {
                        show: false
                    },
                    offset: 10,
                    nameTextStyle: {
                        fontSize: 15
                    }
                },
                series: [{
                    name: '数量',
                    type: 'bar',
                    data: barData,
                    barWidth: 14,
                    barGap: '20%',
                    smooth: true,
                    label: {
                        normal: {
                            show: true,
                            position: 'right',
                            offset: [5, -2],
                            textStyle: {
                                color: '#F68300',
                                fontSize: 13
                            }
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            barBorderRadius: 7
                        },
                        normal: {
                            barBorderRadius: 7,
                            color: new echarts.graphic.LinearGradient(
                                0, 0, 1, 0, [{
                                    offset: 0,
                                    color: '#3977E6'
                                }, {
                                    offset: 1,
                                    color: '#37BBF8'
                                }

                                ]
                            )
                        }
                    }
                }]
            };
            myChart.setOption(option);
        }
    }
}
function toJson(str) {
    var json = (new Function("return"+str))();
    return json;
}