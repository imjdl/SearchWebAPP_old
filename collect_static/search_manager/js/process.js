var timer;
var newPercentage;
var $progress = $('#pro_01');
var index = 0;
function runprogress() {
    var currentClass = $progress.attr('class').split(' ')[1];
    var currentPercentage = currentClass.substring(9,12);
    newPercentage = (parseInt(currentPercentage) + 1);
    if (newPercentage > 100) {
        clearInterval(timer);
        $progress = $('#pro_02');
        $progress.css("opacity","1");
        timer = setInterval(runprogress,10);
    }
    var newClass = 'progress-' + newPercentage;
    $progress.removeClass(currentClass).addClass(newClass);
}
timer = setInterval(runprogress,10);