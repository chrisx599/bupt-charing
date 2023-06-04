// function fetchData() {
//   // 发送Ajax请求获取数据
//   fetch('/api/data')
//     .then(response => response.json())
//     .then(data => {
//       // 更新页面上的数据
//       document.getElementById('data').innerText = data.value;
//     });
// }
function updateChargeArea(data) {
    // 更新快充桩
    for (let i=1; i<3; i++) {
        let str_i1 = ('fast' +i.toString()+ '_wait1')
        let str_i2 = ('fast' +i.toString()+ '_wait2')
        if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '0') {
            document.getElementById(str_i1).textContent = '空闲';
            document.getElementById(str_i2).textContent = '空闲';
        }
        else if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '1') {
            document.getElementById(str_i1).textContent = '使用';
            document.getElementById(str_i2).textContent = '空闲';
        }
        else if (data['charge_area']['fast_charger'][i-1]['charger_queue_size'] === '2') {
            document.getElementById(str_i1).textContent = '使用';
            document.getElementById(str_i2).textContent = '使用';
        }
    }
    // 更新慢充桩
    for (let i=1; i<4; i++) {
        let str_i1 = ('slow' +i.toString()+ '_wait1')
        let str_i2 = ('slow' +i.toString()+ '_wait2')
        if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '0') {
            document.getElementById(str_i1).textContent = '空闲';
            document.getElementById(str_i2).textContent = '空闲';
        }
        else if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '1') {
            document.getElementById(str_i1).textContent = '使用';
            document.getElementById(str_i2).textContent = '空闲';
        }
        else if (data['charge_area']['slow_charger'][i-1]['charger_queue_size'] === '2') {
            document.getElementById(str_i1).textContent = '使用';
            document.getElementById(str_i2).textContent = '使用';
        }
    }
}

function updateWaitArea(data) {
    let fast_wait_car_num = parseInt(data['wait_area']['fast_wait_car_number'])
    let slow_wait_car_num = parseInt(data['wait_area']['slow_wait_car_number'])
    for (let i=1; i<=fast_wait_car_num; i++) {
        let str_i = ('wait_area' +i.toString())
        document.getElementById(str_i).textContent = '快车号';
    }
    let cnt=0
    for (let i=fast_wait_car_num+1; i<=6; i++) {
        if (cnt === slow_wait_car_num){
            break
        }
        let str_i = ('wait_area' +i.toString())
        document.getElementById(str_i).textContent = '慢车号';
        cnt++
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
        });
}

updateData()

// 每隔一定时间执行一次Ajax请求
// setInterval(fetchData, 3000);  // 每5秒更新一次数据
setInterval(updateData,3000)