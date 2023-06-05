function addScript(url, callback) {
  var script = document.createElement('script');
  script.src = url;
  script.onload = callback;
  document.head.appendChild(script);
}
document.addEventListener('DOMContentLoaded', function() {
      var jsonData;
      addScript('https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js', function() {
          axios.get("/a/getreports")
      .then(function(response) {
        jsonData = response.data;

        // 从后端获取的 JSON 数据（示例数据）
        console.log(jsonData);

        var tbody = document.getElementById("tableBody");

        // 动态生成表格的行
        for (var i = 0; i < jsonData.rows.length; i++) {
          var row = document.createElement("tr");
          for (var j = 0; j < jsonData.rows[i].length; j++) {
            var cell = document.createElement("td");
            cell.innerHTML = jsonData.rows[i][j];
            row.appendChild(cell);
          }
          tbody.appendChild(row);
        }
      })
      .catch(function(error) {
        console.error(error);
      });
  });
});






