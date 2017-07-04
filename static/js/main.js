
if ("WebSocket" in window)
{

   // Museum Dashboard is connected to analytics channel
   var ws = new WebSocket("ws://localhost:8000/analytics");
   // No need to send a message CODE
   var msg = {
    // "command": "GET_FLOOR_PLANS",
    // "command": "GET_LOCATIONS",
    //"command": "GET_FLOOR_PLANS",
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
      /** TODO
          1. GET USER ID
          2. Find Table  if not create one
          3. Add the new entry in the first row
      **/
   };

}

else
{
   // The browser doesn't support WebSocket
   alert("WebSocket NOT supported by your Browser!");
}
