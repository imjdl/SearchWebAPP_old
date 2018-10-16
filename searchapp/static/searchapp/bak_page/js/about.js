$(document).ready(function() {
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    context.beginPath();
    context.moveTo(480, 0);
    context.lineTo(480, 250);
    context.lineWidth = 1;
    context.fillStyle = "#000";
    context.stroke();
    context.closePath();

    context.beginPath();
    context.fillStyle = "#9ca4bf";
    var circle = { x: 480, y: 40, r: 10 };
    context.arc(circle.x, circle.y, circle.r, 0, Math.PI * 2, true);
    // context.stroke();
    context.fill();
    context.closePath();


});