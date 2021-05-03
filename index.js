const express = require("express");
const app = express();
var id=0
app.listen(3000, function () {
  console.log("listening on 3000");
});

app.get("/:n", (req, res) => {
  n=req.params['n']
  id++
  for(var i=1;i<=n;i++){
    const ts = Date.now();
    let date_ob = new Date(ts);
    let date = ("0" + date_ob.getDate()).slice(-2);
    let month = ("0" + (date_ob.getMonth() + 1)).slice(-2);
    let year = date_ob.getFullYear();
    let hours = date_ob.getHours();
    let minutes = date_ob.getMinutes();
    let seconds = date_ob.getSeconds();
    console.log("Coverted time stamp:"+year + "-" + month + "-" + date + " " + hours + ":" + minutes + ":" + seconds + ".ts(" +ts+") JOB"+id+"NO"+i+"End")
  }
  res.send("Finished with job id:"+id+"\n");
});