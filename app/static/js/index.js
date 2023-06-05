function updateChargeArea(data) {
    // 更新快充桩
    for (let i=1; i<3; i++) {
        let str_i1 = ('fast' +i.toString()+ '_wait1')
        let str_i2 = ('fast' +i.toString()+ '_wait2')
        if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '0') {
            // document.getElementById(str_i1).textContent = '空闲';
            // document.getElementById(str_i2).textContent = '空闲';
        }
        else if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '1') {
            let img = document.createElement("img");
            img.src = "../../static/img/charging.png";
            let temp = document.getElementById(str_i1)
            temp.parentNode.replaceChild(img, temp);
        }
        else if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '2') {
            let img = document.createElement("img");
            img.src = "../../static/img/charging.png";
            let temp = document.getElementById(str_i1)
            temp.parentNode.replaceChild(img, temp);
            img = document.createElement("img");
            img.src = "../../static/img/fast_car.png";
            temp = document.getElementById(str_i2)
            temp.parentNode.replaceChild(img, temp);
        }
    }
    // 更新慢充桩
    for (let i=1; i<4; i++) {
        let str_i1 = ('slow' +i.toString()+ '_wait1')
        let str_i2 = ('slow' +i.toString()+ '_wait2')
        if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '0') {
            // // 将 img 元素添加到 body 元素中
            // let temp = document.getElementById(str_i1)
            // temp.parentNode.replaceChild(charging_img, temp);
            // // document.getElementById(str_i1).textContent = '空闲';
            // document.getElementById(str_i2).textContent = '空闲';
            //不做变动
        }
        else if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '1') {
            let img = document.createElement("img");
            img.src = "../../static/img/charging.png";
            let temp = document.getElementById(str_i1)
            temp.parentNode.replaceChild(img, temp);
        }
        else if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '2') {
            let img = document.createElement("img");
            img.src = "../../static/img/charging.png";
            let temp = document.getElementById(str_i1)
            temp.parentNode.replaceChild(img, temp);
            img = document.createElement("img");
            img.src = "../../static/img/slow_car.png";
            temp = document.getElementById(str_i2)
            temp.parentNode.replaceChild(img, temp);
        }
    }
}

var wait_area_imageAdded = [false, false, false, false, false, false];
function updateWaitArea(data) {
    var fast_wait_car_num = parseInt(data['wait_area']['fast_wait_car_number'])
    var slow_wait_car_num = parseInt(data['wait_area']['slow_wait_car_number'])
    for (let i=1; i<=fast_wait_car_num; i++) {
        let str_i = ('wait_area' +i.toString())
        // document.getElementById(str_i).textContent = '快车号';
        // 创建一个 img 元素
        if (!wait_area_imageAdded[i-1]){
            var img = document.createElement("img");
            // 设置图片的 src 属性
            img.src = "../../static/img/fast_car.png";
            // 将 img 元素添加到 body 元素中
            let temp = document.getElementById(str_i)
            temp.parentNode.replaceChild(img, temp);
            wait_area_imageAdded[i-1] = true; // 设置对应图片已经添加的标记
        }
    }
    let cnt=0
    for (let i=fast_wait_car_num+1; i<=6; i++) {
        if (cnt === slow_wait_car_num){
            break
        }
        let str_i = ('wait_area' +i.toString())
        // document.getElementById(str_i).textContent = '慢车号';
        if (!wait_area_imageAdded[i-1]){
            var img = document.createElement("img");
            // 设置图片的 src 属性
            img.src = "../../static/img/slow_car.png";
            // 将 img 元素添加到 body 元素中
            // document.getElementById(str_i).appendChild(img)
            let temp = document.getElementById(str_i)
            temp.parentNode.replaceChild(img, temp);
            wait_area_imageAdded[i-1] = true; // 设置对应图片已经添加的标记
        }
        cnt++
    }
}

function updateCharger(data) {
    if (data['charger_state']['fast_charger1'] === 'False') {
        document.getElementById('fast_charger1').textContent = '快充桩 1: 已关闭';
    }
    if (data['charger_state']['fast_charger2'] === 'False') {
        document.getElementById('fast_charger2').textContent = '快充桩 2: 已关闭';
    }
    if (data['charger_state']['slow_charger1'] === 'False') {
        document.getElementById('slow_charger1').textContent = '慢充桩 1: 已关闭';
    }
    if (data['charger_state']['slow_charger2'] === 'False') {
        document.getElementById('slow_charger2').textContent = '慢充桩 2: 已关闭';
    }
    if (data['charger_state']['slow_charger3'] === 'False') {
        document.getElementById('slow_charger3').textContent = '慢充桩 3: 已关闭';
    }
}

function updateData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            // 更新充电区
            updateChargeArea(data)
            // 更新等待区
            updateWaitArea(data)
            // 更新充电桩状态
            updateCharger(data)
        });
}

updateData()

// 每隔一定时间执行一次Ajax请求
// setInterval(fetchData, 3000);  // 每5秒更新一次数据
setInterval(updateData,3000)