window.addEventListener("load", function(){
// [1] GET ALL THE HTML ELEMENTS
var video = document.getElementById("vid-show"),
    canvas = document.getElementById("vid-canvas"),
    take = document.getElementById("vid-take");

// [2] ASK FOR USER PERMISSION TO ACCESS CAMERA
// WILL FAIL IF NO CAMERA IS ATTACHED TO COMPUTER
navigator.mediaDevices.getUserMedia({ video : true })
.then(function(stream) {
  // [3] SHOW VIDEO STREAM ON VIDEO TAG
  video.srcObject = stream;
  video.play();

  // [4] WHEN WE CLICK ON "TAKE PHOTO" BUTTON
  take.addEventListener("click", function(){
    // Create snapshot from video
    var draw = document.createElement("canvas");
    draw.width = video.videoWidth;
    draw.height = video.videoHeight;
    var context2D = draw.getContext("2d");
    context2D.drawImage(video, 0, 0, video.videoWidth, video.videoHeight);
    // Output as file
    var guestName = document.getElementById("id_name");
    var visitDate = new Date();
    var fmtdVisitDate = visitDate.getDate() + "-" + (visitDate.getMonth() + 1) + "-" + visitDate.getFullYear();

    console.log(guestName.value);

    var anchor = document.createElement("a");
    anchor.href = draw.toDataURL("image/jpg");
    anchor.download = guestName.value.replace(/\s+/g, '_') + "_" + fmtdVisitDate + ".jpg";
    anchor.innerHTML = "Click to download";
    canvas.innerHTML = "";
    canvas.appendChild(anchor);
  });
})
.catch(function(err) {
  document.getElementById("vid-controls").innerHTML = "Please enable access and attach a camera";
});
});
