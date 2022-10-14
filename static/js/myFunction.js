//获取对应文件内容
function get(url) {
	return fetch(url).then(res => res.json())
}

async function initChina() {
	let chinaData = await get("/static/json/china.json");
	echarts.registerMap("china", chinaData);
	initProvinceData();
}

async function initProvinceData() {
	let provinceData = await get("/static/json/data.json");
	let data = provinceData.map(r => {
		return {
			name: r.provinceShortName,
			value: r.ZpNumber
		}
	});

	var option = {
		visualMap: {
			min: 0,
			max: 5000,
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
				color: '#343957',

			}
		},
		toolbox: {
			show: true,
			itemSize: 50,
			showTitle: true,
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

		title: {
			text: '族谱分布地图',
			textStyle: {
				color: 'blue',  //颜色
				fontSize: 30  //字号
			},
			//					subtext:"@郭茂", //副标题
			left: "center", //居中
			padding: 15
		},

		tooltip: {},

		legend: { //图例
			data: ['族谱数量'],//series里写了此处可不添加
			left: 'left'
		},

		series: [
			{
				name: '族谱数量',
				type: 'map',  //图表类型
				mapType: "china",
				label: {
					normal: {
						show: true
					},
					emphasis: {
						show: true
					}
				},
				selectedMode: 'multiple',
				roam: true, //鼠标缩放与平移
				itemStyle: {
					normal: {
						areaColor: "#ffefef",
						borderColor: "#2e43ff",
						borderWidth: 0.5
					},
					emphasis: {
						areaColor: "#ece39e",
						shadowOffsetX: 0,
						shadowOffsetY: 0,
						shadowBlur: 5,
						borderWidth: 0.5,
						shadowColor: "rgba(0, 0, 0, 0.5)"
					}
				},
				data
			}
		]
	};

	// 使用刚指定的配置项和数据显示图表。
	myChart_map.setOption(option, true);
}

//从数组中随机取出指定个数元素
function getRandomArrayElements(arr, count) {
	var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
	while (i-- > min) {
		index = Math.floor((i + 1) * Math.random());
		temp = shuffled[index];
		shuffled[index] = shuffled[i];
		shuffled[i] = temp;
	}
	return shuffled.slice(min);
}

//表格查询功能
function tableSearch(colNumber, idName) {
	// 声明变量
	var input, filter, table, tr, td, i;
	input = document.getElementById(idName);
	filter = input.value.toUpperCase();
	table = document.getElementById("table");
	tr = table.getElementsByTagName("tr");

	// 循环表格每一行，查找匹配项
	for (i = 0; i < tr.length; i++) {
		td = tr[i].getElementsByTagName("td")[colNumber];
		if (td) {
			if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
				tr[i].style.display = "";
			} else {
				tr[i].style.display = "none";
			}
		}
	}
}

//带时间轴柱形图
function timeLineBar() {
	var allData = {};
	function dataFormatter(obj) {
		var pList = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'];
		var temp;
		for (var year = 1975; year <= 2020; year = year + 5) {
			var max = 0;
			var sum = 0;
			temp = obj[year];
			for (var i = 0, l = temp.length; i < l; i++) {
				max = Math.max(max, temp[i]);
				sum += temp[i];
				obj[year][i] = {
					name: pList[i],
					value: parseInt(temp[i])
				}
			}
			obj[year + 'max'] = Math.floor(max / 100) * 100;
			obj[year + 'sum'] = sum;
		}
		return obj;
	}

	allData.dataZP = dataFormatter({
		//max : 3200,
		2020: [2215.41, 1156.5, 746.01, 519.32, 447.46, 755.57, 207.65, 370.78, 2277.4, 2600.11, 2730.29, 503.85, 862.41, 357.44, 1640.41, 868.2, 674.57, 501.09, 2916.13, 445.37, 105.24, 704.66, 868.15, 297.27, 456.23, 31.7, 432.11, 145.05, 62.56, 134.18, 288.77],
		2015: [1863.61, 972.99, 615.42, 448.3, 346.44, 639.27, 190.12, 304.59, 1950.96, 2105.92, 2326.58, 396.17, 767.58, 241.49, 1361.45, 697.68, 561.27, 463.16, 2658.76, 384.53, 78.12, 496.56, 654.7, 231.51, 375.08, 27.08, 384.75, 100.54, 54.53, 97.87, 225.2],
		2010: [1603.63, 861.2, 525.67, 361.64, 291.1, 560.2, 180.83, 227.54, 1804.28, 1596.98, 1899.33, 359.6, 612.2, 165.1, 1044.9, 499.92, 479.11, 402.57, 2283.29, 336.82, 65.73, 389.97, 524.63, 194.44, 351.74, 23.17, 336.21, 88.27, 45.63, 75.54, 198.87],
		2005: [1519.19, 768.1, 420.74, 290.91, 219.09, 455.07, 147.24, 177.43, 1414.21, 1298.48, 1653.45, 313.81, 497.65, 130.57, 880.28, 413.83, 393.05, 334.32, 1972.4, 249.01, 47.33, 303.01, 411.14, 151.55, 277.66, 22.42, 287.16, 72.49, 36.54, 64.8, 171.97],
		2000: [1302.77, 688.17, 347.65, 218.73, 148.3, 386.34, 126.03, 155.48, 1209.08, 1054.25, 1251.43, 223.85, 385.84, 101.34, 734.9, 302.31, 337.27, 260.14, 1705.08, 190.73, 34.43, 247.46, 359.11, 122.25, 168.55, 11.51, 231.03, 61.6, 27.67, 51.05, 149.22],
		1995: [982.37, 586.87, 284.04, 169.63, 108.21, 303.41, 100.75, 74.17, 825.2, 653.25, 906.37, 166.01, 243.9, 79.75, 524.94, 219.72, 174.99, 204.72, 899.91, 129.14, 16.37, 213.7, 299.5, 89.43, 143.62, 6.44, 152.25, 50.51, 23.69, 36.99, 99.25],
		1990: [840.2, 447.4, 213.47, 135.07, 72.52, 232.85, 83.63, 35.03, 675.12, 492.4, 686.32, 127.05, 186.12, 69.55, 448.36, 181.74, 127.32, 162.37, 661.81, 91.93, 13.16, 185.18, 262.26, 73.67, 130.5, 7.57, 127.58, 44.73, 20.36, 32.25, 80.34],
		1985: [713.79, 336.97, 209.1, 110.29, 55.89, 188.04, 77.17, 32.2, 612.45, 440.5, 523.49, 94.1, 171, 65.1, 343.37, 170.82, 118.85, 118.64, 602.68, 74, 11.56, 162.38, 236.5, 60.3, 118.4, 5.4, 90.1, 42.99, 19, 27.92, 70.3],
		1980: [635.56, 212.79, 199.87, 118.48, 55.89, 145.38, 73.15, 32.2, 517.97, 392.11, 451.54, 87.45, 150.09, 64.31, 329.71, 165.11, 107.31, 99.35, 534.28, 61.59, 10.68, 147.04, 206.24, 48.01, 105.48, 4.74, 77.87, 42.31, 17.98, 24.8, 64.92],
		1975: [561.91, 176.86, 179.6, 124.1, 148.39, 137.18, 175.45, 131.6, 485.25, 368, 347, 81.85, 138.28, 76.51, 310.07, 158.77, 96.95, 92.43, 454.65, 35.86, 10.08, 134.52, 183.13, 41.45, 102.39, 2.81, 67.3, 42.08, 16.75, 21.45, 52.18]
	});

	let option_timeLineBar = {
		baseOption: {
			timeline: {
				axisType: 'category',
				realtime: true,
				loop: true,
				autoPlay: true,
				currentIndex: 2,
				playInterval: 1500,
				// top:'1px',
				bottom: '1px',
				orient: 'horizontal',
				controlStyle: {
					show: true,
					showPlayBtn: true,
					showPrevBtn: true,
					showNextBtn: true,
					// position: 'left',
					color: '#fdfdff',
					borderColor: '#343957',
					borderWidth: 1,
					normal: {
						color: '#feffff',
						borderColor: '#feffff'
					},
					emphasis: {
						label: false,
						color: '#feffff',
						borderColor: '#aaa'
					}
				},
				lineStyle: {
					show: true,
					color: '#DAE1F5',
					opacity: 1,
				},
				data: [
					'1975-01-01', '1980-01-01', '1985-01-01', '1990-01-01',
					'1995-01-01', '2000-01-01', '2005-01-01', '2010-01-01',
					'2015-01-01', '2020-01-01',
				],
				label: {
					formatter: function (s) {
						return (new Date(s)).getFullYear();
					}
				},
				itemStyle: {
					color: '#343957'
				},
				checkpointStyle: {
					symbol: 'triangle',
					color: '#343957'
				},
			},
			title: {
				text: '族谱数量统计',
				textStyle: {
					color: 'blue',  //颜色
					fontSize: 20  //字号
				},
				//				subtext:"@郭茂", //副标题
				left: "center", //居中
			},
			tooltip: {
				trigger: 'axis',
				axisPointer: {
					type: 'shadow'
				}
			},
			legend: {
				data: ['各省族谱数量']
			},
			grid: {
				left: '3%',
				right: '4%',
				bottom: '5%',
				containLabel: true
			},
			calculable: true,
			// grid: {
			// 	top: 80,
			// 	bottom: 2
			// },
			yAxis: [
				{
					type: 'category',
					name: '省份',
					// axisLabel: {'interval': 0},
					data: [
						'北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江',
						'上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南',
						'湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州',
						'云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆'
					],
					splitLine: { show: false },
					axisLabel: {
						/*inside: true,*/
						interval: 0,
						textStyle: {
							color: 'rgb(52,57,87)',
							fontSize: 12
						}
					},
					axisTick: {
						show: false,
					},
					axisLine: {
						show: true,
						symbol: ['none', 'arrow'],
						symbolOffset: 12,
						lineStyle: {
							color: 'rgba(255,255,255,0.2)',
						}
					}
				}
			],
			xAxis: [
				{
					type: 'value',
					name: '族谱数量（部）',
					// max: 3200
					max: 3500,
					axisLine: {
						show: true,
						symbol: ['none', 'arrow'],
						symbolOffset: 12,
						lineStyle: {
							color: 'rgba(255,255,255,0)',
						}
					},
					axisTick: {
						show: false
					},
					axisLabel: {
						textStyle: {
							color: 'rgb(52,57,87)',
							fontSize: 12
						}
					}
				}
			],
			series: [
				{
					name: '族谱',
					type: 'bar',
					itemStyle: {
						normal: {
							color: 'rgba(131,103,172,0.94)'
						},
						emphasis: {
							color: 'rgba(255,240,157,0.94)'
						}

					}
				}
			]
		},
		options: [
			{
				title: { text: '1975年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['1975'] }
				]
			},
			{
				title: { text: '1980年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['1980'] }
				]
			},
			{
				title: { text: '1985年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['1985'] }
				]
			},
			{
				title: { text: '1990年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['1990'] }
				]
			},
			{
				title: { text: '1995年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['1995'] }
				]
			},
			{
				title: { text: '2000年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['2000'] }
				]
			},
			{
				title: { text: '2005年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['2005'] }
				]
			},
			{
				title: { text: '2010年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['2010'] }
				]
			},
			{
				title: { text: '2015年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['2015'] }
				]
			},
			{
				title: { text: '2020年各省族谱数量统计' },
				series: [
					{ data: allData.dataZP['2020'] }
				]
			}
		]
	};

	myChart_bartimeline.setOption(option_timeLineBar);
}

function checkSelect() {
	//获取select选中的text。
	var val = $("#pieSelect option:selected").text();
	//操作函数
	placeName = val;
	pieData = pieDataAll[val];
	drawPie(val, pieData);
}

async function initPie() {
	let provinceData = await get("/static/json/data.json");
	let data = provinceData.map(r => {
		return {
			name: r.provinceShortName,
			value: r.ZpNumber
		}
	});
	drawPie("全国", data);
}

async function drawBar(placeName, barData) {
	let provinceData = await get("/static/json/data.json");
	let data = provinceData.map(r => {
		return [
			r.ZpNumber
		]
	});
	option_bar = {
		title: {
			text: '族谱数量统计',
			textStyle: {
				color: 'blue',  //颜色
				fontSize: 20  //字号
			},
			//            subtext:"@郭茂", //副标题
			left: "center", //居中
		},
		tooltip: {
			trigger: 'axis',
			axisPointer: {
				type: 'shadow'
			}
		},
		legend: {
			data: ['各省族谱数量']
		},
		grid: {
			left: '3%',
			right: '4%',
			bottom: '3%',
			containLabel: true
		},
		xAxis: {
			name: '族谱数量',
			type: 'value',
			boundaryGap: [0, 0.01],
			axisLabel: {
				/*inside: true,*/
				interval: 0,
				textStyle: {
					color: '#fff',
					fontSize: 12
				}
			},
			axisTick: {
				show: false,
			},
			axisLine: {
				show: true,
				symbol: ['none', 'arrow'],
				symbolOffset: 12,
				lineStyle: {
					color: '#fff',
				}
			}
		},
		yAxis: {
			name: '省份',
			type: 'category',
			data: ['贵州', '湖北', '新疆', '西藏', '青海', '甘肃', '内蒙古', '宁夏', '陕西', '四川',
				'云南', '黑龙江', '吉林', '辽宁', '北京', '河北', '河南', '山西', '山东', '重庆',
				'江苏', '安徽', '上海', '浙江', '湖南', '江西', '福建', '台湾', '广东', '广西', '海南', '天津', '香港', '澳门'],
			axisLine: {
				show: true,
				symbol: ['none', 'arrow'],
				symbolOffset: 12,
				lineStyle: {
					color: '#000',
				}
			},
			axisTick: {
				show: false
			},
			axisLabel: {
				textStyle: {
					color: '#000',
					fontSize: 12
				}
			}
		},
		series: [
			{
				name: '数量',
				type: 'bar',
				itemStyle: {
					color: new echarts.graphic.LinearGradient(
						0, 0, 0, 1,
						[
							{ offset: 0, color: '#0efdff' },
							{ offset: 0.5, color: '#188df0' },
							{ offset: 1, color: '#188df0' }
						]
					)
				},
				emphasis: {
					itemStyle: {
						color: new echarts.graphic.LinearGradient(
							0, 0, 0, 1,
							[
								{ offset: 0, color: '#2378f7' },
								{ offset: 0.7, color: '#2378f7' },
								{ offset: 1, color: '#0efdff' }
							]
						)
					}
				},
				data: [201, 355, 41, 56, 621, 157, 238, 120, 255, 442, 284, 844, 503, 233, 187, 262, 442, 466, 205, 326, 293]
			}]
	};

	myChart_bar.setOption(option_bar);
}

async function drawPie(placeName, pieData) {
	var num = pieData.length;
	let colorarrays = ["#d4dda2", "#d9d87e", "#eee060", "#beb635",
		"#ffe4bf", "#eec583", "#ffba69", "#e0982d",
		"#eebffe", "#f696ff", "#eb5bff", "#f006ff",
		"#fec2c2", "#ff928d", "#ff5751", "#ff1205",
		"#b4b9fe", "#7f88ff", "#557eff", "#0817ff",
		"#1efec8", "#80ffb2", "#89ff8c", "#22ff04",
		"#630058", "#497748", "#722d23", "#1e1a4c",];
	let pieColor = getRandomArrayElements(colorarrays, num);
	option_pie = {
		title: {
			text: placeName + '族谱数量统计-饼图',
			//            subtext: '@郭茂',
			left: 'center',
			top: 0,
			textStyle: {
				color: '#2e43ff',
				fontSize: 25
			}
		},
		tooltip: {
			trigger: 'item',
			formatter: '{a} <br/>{b} : {c} ({d}%)'
		},
		legend: {
			// orient: 'vertical',
			// top: 'middle',

			bottom: '5%',

			data: pieData.map(r => {
				return r.name
			}),
			textStyle: {
				color: 'rgb(52,57,87)',
				fontSize: 12
			}
		},
		grid: {
			x: '-10%',
			y: 40,
			x2: 20,
			y2: 20,
		},
		color: pieColor,
		series: [
			{
				type: 'pie',
				radius: '65%',
				center: ['50%', '50%'],
				selectedMode: 'single',
				data: pieData,
				emphasis: {
					itemStyle: {
						shadowBlur: 10,
						shadowOffsetX: 0,
						shadowColor: 'rgba(0, 0, 0, 0.5)'
					}
				}
			}]
	};

	myChart_pie.setOption(option_pie);
}