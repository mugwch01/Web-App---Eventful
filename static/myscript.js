

function showEvents() {
  var xhttp;
  var str = document.getElementById("txt").value;
  xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     
      document.getElementById("demo").innerHTML = this.responseText;
      console.log(this.responseText);
    }
  };
  xhttp.open("GET", "/api/v1/eventsperformers?data="+str, true);
  xhttp.send();
}
