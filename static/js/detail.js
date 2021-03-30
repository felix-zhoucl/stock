//mini日线
function insertStr(soure, start, newStr){
   return soure.slice(0, start) + newStr + soure.slice(start);
}

function gettoday(){
            var temp = $('#stockid').text();
            var myChart = echarts.init(document.getElementById('echarts_container_mini'));
            var date=[]
            var gujia=[]
            var junxian=[]
            $.ajax({
                url:'http://img1.money.126.net/data/hs/time/today/'+temp+'.json',
                type:'GET',
                dataType : "jsonp",
                data: {},
                ContentType:"application/json",
                success:function(arg){
                   var data = arg.data
                   var max=data[0][1]
                   var min=data[0][1]
                   for(i=0;i<data.length;i++){
                        if(data[i][1]>max)
                        {
                            max=data[i][1]
                        }
                        if(data[i][1]<min)
                        {
                            min=data[i][1]
                        }
                   temptime=insertStr(data[i][0],2,":")
//                   console.log(temptime)
                   date.push(temptime)
                   gujia.push(data[i][1])
                   junxian.push(data[i][2])
                   }
                    var option = {
                        title: {
                            text: '日线图',
                            left:10,
                            top:5,
                        },
                        grid: {
                            left:'18%',
                            right:'16%',
//                            containLabel:true
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'cross'
                            }
                        },dataZoom: [
                            {
                                type: 'inside',
                                start: 0,
                                end: 100
                            },
                            {
                                show: true,
                                type: 'slider',
                                top: '90%',
                                start: 50,
                                end: 100
                            }
                        ],
                        legend: {
                            data:['股价','均线'],
                            left:105,
                            top:7,
                        },
                        xAxis: {
                            name:'时间',
                            data: date
                        },
                        yAxis: {
                            name:'价格',
                            type : 'value',
                            scale : true,
                            max : max + 0.2,
                            min : min - 0.2,
                            splitNumber : 0.1,
                        },
                        series: [
                            {
                              name: '均线',
                              type: 'line',
                              smooth: false,
                              data: junxian,
                              lineStyle: {
                                   color: "#FF3333",
                                   width: 2
                              }, //线条的样式
                              itemStyle: {
                                    color: "#FF3333",
                                   opacity: 0 //为0不会绘制图形拐点消失
                              } //拐点的样式
                          },
                           {
                              name: '股价',
                              type: 'line',
                              smooth: false,
                              data: gujia,
                              areaStyle: {
                                  normal: {
                                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                      { offset: 1, color: "#CCFFFF" }
                                    ])
                                  }
                                }, //填充区域样式
                              lineStyle: {
                                   color: "#00b5ff",
                                   width: 1
                              }, //线条的样式
                              itemStyle: {
                                   color: "#00b5ff",
                                   opacity: 0 //为0不会绘制图形拐点消失
                              } //拐点的样式
                           },

                        ]
                    };
                    myChart.setOption(option);
                },
                error:function(){
                    console.log('search failed')
                    }
               })
 }
 gettoday()


//K线图

function getKlineData(){
    let result = {}
    var temp = $('#stockid').text();
    $.ajax({
        url:'http://img1.money.126.net/data/hs/klinederc/day/history/2020/'+temp+'.json',
        type:'GET',
        dataType : "jsonp",
        data: {},
        ContentType:"application/json",
        success:function(arg){
//            console.log("___success__")
            klinedata = splitData(arg.data)
//            console.log(klinedata)
            makeKline(klinedata)

        },
        error:function(){
            console.log('search failed')
            }
       })
       return result;
}
getKlineData()

//分割数据
function splitData(rawData) {
    var categoryData = [];
    var values = []
    rawData.forEach(function (item,index,input) {
        categoryData.push(item.slice(0, 1)[0]);
        values.push(item.slice(1, item.length-2))
    })
    return {
        categoryData: categoryData,
        values: values
    };
}

//计算MA
function calculateMA(dayCount,data0) {
    var result = [];
    for (var i = 0, len = data0.values.length; i < len; i++) {
        if (i < dayCount) {
            result.push('-');
            continue;
        }
        var sum = 0;
        for (var j = 0; j < dayCount; j++) {
            sum += data0.values[i - j][1];
        }
        result.push(sum / dayCount);
    }
    return result;
}

//画图
function makeKline(data0){
    var dom = document.getElementById("echarts_container_kline");
    var myChart = echarts.init(dom);
    var app = {};
    option = null;
    var upColor = '#ec0000';
    var upBorderColor = '#8A0000';
    var downColor = '#00da3c';
    var downBorderColor = '#008F28';
    option = {
//        标题
        title: {

        },
//        提示工具
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        },
//        图例
        legend: {
            data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
        },
//        网格
        grid: {
            left: '10%',
            right: '10%',
            bottom: '15%'
        },
//        x轴
        xAxis: {
            type: 'category',
            data: klinedata.categoryData,
            scale: true,
            boundaryGap: false,//是否使用边界，false：使用
            axisLine: {onZero: false},
            splitLine: {show: false},
            splitNumber: 20,
            min: 'dataMin',
            max: 'dataMax'
        },
//        y轴
        yAxis: {
            scale: true,//缩放
            splitArea: {
                show: true
            }
        },
//        缩放
        dataZoom: [
            {
                type: 'inside',
                start: 90,
                end: 100
            },
//            默认显示
            {
                show: true,
                type: 'slider',
                top: '90%',
                start: 50,
                end: 100
            }
        ],
//        变量
        series: [
            {
                name: '日K',
                type: 'candlestick',
                data: klinedata.values,
                itemStyle: {
                    color: upColor,//阳线颜色
                    color0: downColor,//阴线颜色
                    borderColor: upBorderColor,// 阳线边框颜色
                    borderColor0: downBorderColor// 阳线边框颜色
                },
//                markPoint: {
//                    label: {
//                        normal: {
//                            formatter: function (param) {
//                                return param != null ? Math.round(param.value) : '';
//                            }
//                        }
//                    },
//                    data: [
//                        {
//                            name: 'highest value',
//                            type: 'max',
//                            valueDim: 'highest'
//                        },
//                        {
//                            name: 'lowest value',
//                            type: 'min',
//                            valueDim: 'lowest'
//                        }
//                    ],
//                    tooltip: {
//                        formatter: function (param) {
//                            return param.name + '<br>' + (param.data.coord || '');
//                        }
//                    }
//                },
                markLine: {
                    symbol: ['none', 'none'],
                    data: [
//                        [
//                            {
//                                name: 'from lowest to highest',
//                                type: 'min',
//                                valueDim: 'lowest',
//                                symbol: 'circle',
//                                symbolSize: 10,
//                                label: {
//                                    show: false
//                                },
//                                emphasis: {
//                                    label: {
//                                        show: false
//                                    }
//                                }
//                            },
//                            {
//                                type: 'max',
//                                valueDim: 'highest',
//                                symbol: 'circle',
//                                symbolSize: 10,
//                                label: {
//                                    show: false
//                                },
//                                emphasis: {
//                                    label: {
//                                        show: false
//                                    }
//                                }
//                            }
//                        ],
                        {
                            name: 'min line on close',
                            type: 'min',
                            valueDim: 'close'
                        },
                        {
                            name: 'max line on close',
                            type: 'max',
                            valueDim: 'close'
                        }
                    ]
                }
            },
            {
                name: 'MA5',
                type: 'line',
                data: calculateMA(5,data0),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                },
                itemStyle: {
                    opacity: 0 //为0不会绘制图形拐点消失
                } //拐点的样式
            },
            {
                name: 'MA10',
                type: 'line',
                data: calculateMA(10,data0),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                },
                itemStyle: {
                    opacity: 0 //为0不会绘制图形拐点消失
                } //拐点的样式
            },
            {
                name: 'MA20',
                type: 'line',
                data: calculateMA(20,data0),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                },
                itemStyle: {
                    opacity: 0 //为0不会绘制图形拐点消失
                } //拐点的样式
            },
            {
                name: 'MA30',
                type: 'line',
                data: calculateMA(30,data0),
                smooth: true,
                lineStyle: {
                    opacity: 0.5
                },
                itemStyle: {
                    opacity: 0 //为0不会绘制图形拐点消失
                } //拐点的样式
            },
        ]
    };
    if (option && typeof option === "object") {
        myChart.setOption(option, true);
    }
}


function alertnew()
{
alert("newtape")
}

function followButton(){
    var buttonText=$('#followButton').text();
    var isFollowed=0
    var temp = $('#stockname').text();
    $.ajax({
        url:'/stockapi/follow',
        type:'POST',
        data:{stock:temp},
        success:function(arg){
            if(obj.statuscode == 0){
                alert(" 操作失败")
            }
            else{
                getFavList()
            }
        },
        error:function(){
            console.log('search failed')
        }
    });
}
