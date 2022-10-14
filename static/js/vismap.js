var myChart_map = echarts.init(document.getElementById('map'));//地图
var myChart_bartimeline = echarts.init(document.getElementById('bar'));//柱状图
var myChart_pie = echarts.init(document.getElementById('pie'));//饼图
var timeFn = null;
// 单击事件
myChart_map.on('click', async function (params) {
    clearTimeout(timeFn);
    //省级地图数据
    let provinceName = convertProvinceCN2EN(params.name);
    let provinceMapData = await get(`/static/json/province/${provinceName}.json`)
    echarts.registerMap(provinceName, provinceMapData);
    //族谱数量统计数据
    let chinaData = await get("/static/json/data.json");
    let provinceData = chinaData.find(r => r.provinceShortName === params.name)
    let { cities } = provinceData;
    var provinceZpData = cities.map(r => {
        return {
            name: r.cityname,
            value: r.ZpNumber
        }
    });
    drawPie(params.name, provinceZpData);
    var option = {
        visualMap: {
            min: 0,
            max: 500,
            left: 'left',
            top: 'bottom',
            text: ['高', '低'],           // 文本，默认为数值文本
            // seriesIndex: [1],          //必须设置此项,否则会覆盖标注点颜色
            realtime: true,
            calculable: true,
            inRange: {
                color: ['#e0ffff', '#ec9120', '#2525ec']
            },
            textStyle: {
                color: '#fff',
            }
        },
        title: {
            text: params.name + '族谱分布地图',
            //link:"http://baidu.com"   //链接
            textStyle: {
                color: 'blue',  //颜色
                fontSize: 30  //字号
            },
            left: "center", //居中
            padding: 15
        },
        tooltip: {},
        legend: { //图例
            data: [params.name + '族谱数量'],
            left: 'left'
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        series: [{
            name: params.name + '族谱数量',
            type: 'map',  //图表类型
            map: provinceName,
            label: {
                color: "#ff743e",
                normal: {
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    areaColor: "#ffefef",
                    borderColor: "#2e43ff",
                    borderWidth: 0.5
                },
                emphasis: {
                    areaColor: "#e6ee6a",
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    shadowBlur: 5,
                    borderWidth: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)"
                }
            },
            roam: true, //鼠标缩放与平移
            data: provinceZpData
        }]
    };
    myChart_map.setOption(option, true);
});
//双击事件
myChart_map.on('dblclick', function (params) {
    //当双击事件发生时，清除单击事件，仅响应双击事件
    clearTimeout(timeFn);
    timeFn = setTimeout(function () {
        initChina();
        initPie();
    }, 250);
});
// 初始化中国地图
initChina();
//初始化饼图
initPie();
//带时间轴的柱形图
timeLineBar();
//表格数据排序、分页处理
var sorter = new TINY.table.sorter("sorter");
sorter.head = "head";
sorter.asc = "asc";
sorter.desc = "desc";
sorter.even = "evenrow";
sorter.odd = "oddrow";
sorter.evensel = "evenselected";
sorter.oddsel = "oddselected";
sorter.paginate = true;
sorter.currentid = "currentpage";
sorter.limitid = "pagelimit";
sorter.init("table", 1);