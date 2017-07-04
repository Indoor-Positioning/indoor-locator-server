
if ("WebSocket" in window)
{

   // Let us open a web socket
   var ws = new WebSocket("ws://localhost:8000/realtime");
   var msg = {
    // "command": "GET_FLOOR_PLANS",
    // "command": "GET_LOCATIONS",
    "command": "GET_FLOOR_PLANS",
    // "floorPlanId" : 10

  };

   ws.onopen = function()
   {
      // Web Socket is connected, send data using send()
      ws.send(JSON.stringify(msg));
   };

   ws.onmessage = function (evt)
   {
      var received_msg = evt.data;
      console.log(evt.data);
   };

}

else
{
   // The browser doesn't support WebSocket
   alert("WebSocket NOT supported by your Browser!");
}
