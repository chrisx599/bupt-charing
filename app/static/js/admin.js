function addScript(url){
	document.write("<script language=javascript src="+"https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"+"></script>");
}
  function loadContent1() {
    axios.get('/a/show/pilesinfo', {
        params:{
            pile_id: 1
        }
    })
      .then(function(response){
          handleResponse1(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  function handleResponse1(response) {
        var infodata = response.data
        fastbtn1 = document.getElementById("fastbtn1")
        fast11 = document.getElementById("fast11")
        fast15 = document.getElementById("fast15")
        fast12 = document.getElementById("fast12")
        fast13 = document.getElementById("fast13")
        fast14 = document.getElementById("fast14")
        var isUsing = infodata.isUsing ? "充电中" : "空闲"
        var isWorking = infodata.isWorking ? "工作中" : "关闭"
        var totalTimes = infodata.totalTimes
        var totalTime = infodata.totalTime
        var totalEnergy = infodata.totalEnergy
        fastbtn1.innerHTML = (infodata.isWorking) ? "关闭" : "开启"
        fastbtn1.disabled = infodata.isUsing
        fast11.innerHTML = "工作状态:  " + isWorking
        fast15.innerHTML = "使用状态:  " + isUsing
        fast12.innerHTML = "累计充电次数:  " + totalTimes
        fast13.innerHTML = "累计充电时长:  " + totalTime
        fast14.innerHTML = "累计充电量:  " + totalEnergy
        console.log(infodata)

  }

    function loadContent2() {
    axios.get('/a/show/pilesinfo', {
        params:{
            pile_id: 2
        }
    })
      .then(function(response){
          handleResponse2(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  function handleResponse2(response) {
        var infodata = response.data
        fastbtn2 = document.getElementById("fastbtn2")
        fast21 = document.getElementById("fast21")
        fast22 = document.getElementById("fast22")
        fast23 = document.getElementById("fast23")
        fast24 = document.getElementById("fast24")
        fast25 = document.getElementById("fast25")
        var isUsing = infodata.isUsing ? "充电中" : "空闲"
        var isWorking = infodata.isWorking ? "工作中" : "关闭"
        var totalTimes = infodata.totalTimes
        var totalTime = infodata.totalTime
        var totalEnergy = infodata.totalEnergy
        fastbtn2.innerHTML = (infodata.isWorking) ? "关闭" : "开启"
        fastbtn2.disabled = infodata.isUsing
        fast21.innerHTML = "工作状态:  " + isWorking
        fast25.innerHTML = "使用状态:  " + isUsing
        fast22.innerHTML = "累计充电次数:  " + totalTimes
        fast23.innerHTML = "累计充电时长:  " + totalTime
        fast24.innerHTML = "累计充电量:  " + totalEnergy
        console.log(infodata)

  }

    function loadContent3() {
    axios.get('/a/show/pilesinfo', {
        params:{
            pile_id: 3
        }
    })
      .then(function(response){
          handleResponse3(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  function handleResponse3(response) {
        var infodata = response.data
        slowbtn2 = document.getElementById("slowbtn1")
        slow11 = document.getElementById("slow11")
        slow12 = document.getElementById("slow12")
        slow13 = document.getElementById("slow13")
        slow14 = document.getElementById("slow14")
        slow15 = document.getElementById("slow15")
        var isUsing = infodata.isUsing ? "使用中" : "空闲"
        var isWorking = infodata.isWorking ? "工作中" : "关闭"
        var totalTimes = infodata.totalTimes
        var totalTime = infodata.totalTime
        var totalEnergy = infodata.totalEnergy
        slowbtn1.innerHTML = (infodata.isWorking) ? "关闭" : "开启"
        slowbtn1.disabled = infodata.isUsing
        slow11.innerHTML = "工作状态:  " + isWorking
        slow12.innerHTML = "累计充电次数:  " + totalTimes
        slow13.innerHTML = "累计充电时长:  " + totalTime
        slow14.innerHTML = "累计充电量:  " + totalEnergy
        slow15.innerHTML = "使用状态:  " + isUsing
        console.log(infodata)

  }

    function loadContent4() {
    axios.get('/a/show/pilesinfo', {
        params:{
            pile_id: 4
        }
    })
      .then(function(response){
          handleResponse4(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  function handleResponse4(response) {
        var infodata = response.data
        slowbtn2 = document.getElementById("slowbtn2")
        slow21 = document.getElementById("slow21")
        slow22 = document.getElementById("slow22")
        slow23 = document.getElementById("slow23")
        slow24 = document.getElementById("slow24")
        slow25 = document.getElementById("slow25")
        var isUsing = infodata.isUsing ? "使用中" : "空闲"
        var isWorking = infodata.isWorking ? "工作中" : "关闭"
        var totalTimes = infodata.totalTimes
        var totalTime = infodata.totalTime
        var totalEnergy = infodata.totalEnergy
        slowbtn2.innerHTML = (infodata.isWorking) ? "关闭" : "开启"
        slowbtn2.disabled = infodata.isUsing
        slow21.innerHTML = "工作状态:  " + isWorking
        slow22.innerHTML = "累计充电次数:  " + totalTimes
        slow23.innerHTML = "累计充电时长:  " + totalTime
        slow24.innerHTML = "累计充电量:  " + totalEnergy
        slow25.innerHTML = "使用状态:  " + isUsing
        console.log(infodata)

  }

    function loadContent5() {
    axios.get('/a/show/pilesinfo', {
        params:{
            pile_id: 5
        }
    })
      .then(function(response){
          handleResponse5(response);
      })
      .catch(error => {
        console.log(error);
      });
  }

  function handleResponse5(response) {
        var infodata = response.data
        slowbtn3 = document.getElementById("slowbtn3")
        slow31 = document.getElementById("slow31")
        slow32 = document.getElementById("slow32")
        slow33 = document.getElementById("slow33")
        slow34 = document.getElementById("slow34")
        slow35 = document.getElementById("slow35")
        var isUsing = infodata.isUsing ? "使用中" : "空空闲"
        var isWorking = infodata.isWorking ? "工作中" : "关闭"
        var totalTimes = infodata.totalTimes
        var totalTime = infodata.totalTime
        var totalEnergy = infodata.totalEnergy
        slowbtn3.innerHTML = (infodata.isWorking) ? "关闭" : "开启"
        slowbtn3.disabled = infodata.isUsing
        slow31.innerHTML = "工作状态:  " + isWorking
        slow32.innerHTML = "累计充电次数:  " + totalTimes
        slow33.innerHTML = "累计充电时长:  " + totalTime
        slow34.innerHTML = "累计充电量:  " + totalEnergy
        slow35.innerHTML = "使用状态:  " + isUsing
        console.log(infodata)

  }

  function change_state(event){
    const buttonId = event.target.id;
    pile_id = 0
    switch(buttonId){
        case "fastbtn1":pile_id = 1;break;
        case "fastbtn2":pile_id = 2;break;
        case "slowbtn1":pile_id = 3;break;
        case "slowbtn2":pile_id = 4;break;
        case "slowbtn3":pile_id = 5;break;
    }
    axios.get("/a/changeState", {
        params:{
            pile_id : pile_id
        }
    })
        .then(function(response){
            const button = document.getElementById(buttonId)
            if(button.innerHTML == "关闭"){
                button.innerHTML = "开启"
            }else{
                button.innerHTML = "关闭"
            }
        })
  }
