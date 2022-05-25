const $bgImg = document.getElementById('backgroundImage');
const $bgVideo = document.getElementById('backgroundVideo');
let animationPartsDone = 0;

$bgImg.addEventListener('animationend', () => {
    animationPartsDone++;
    if (animationPartsDone == 2) startVideo();
});
$bgVideo.addEventListener('canplay', () => {
    animationPartsDone++;
    if (animationPartsDone == 2) startVideo();
});
function startVideo() {
    $bgImg.classList.add('hide');
    $bgVideo.playbackRate = .6;
    $bgVideo.play();
}
$bgVideo.addEventListener('ended', () => {
    $bgVideo.currentTime = 0;
    $bgVideo.play();
});



const $countDown = document.getElementById('countDown');
const $cdHrs = document.getElementById('cdHrs').getElementsByClassName('cdSegment')[0];
const $cdMin = document.getElementById('cdMin').getElementsByClassName('cdSegment')[0];
const $cdSec = document.getElementById('cdSec').getElementsByClassName('cdSegment')[0];

let cdInterval = setInterval(() => {
    updateCountdown();
}, 1000)

function updateCountdown() {
    const d = new Date();
    let hrs = d.getHours() + 1;
    let min = d.getMinutes() + 1;
    let sec = d.getSeconds() + 1;
    
    sec = 60 - sec;
    min = 60 - min;
    hrs = 16 - hrs;

    if (hrs < 0 || min < 0 || sec < 0) {
        clearInterval(cdInterval);
        $countDown.classList.add('done');
        $countDown.innerText = "De website wordt over enkele ogenblikken gelanceerd...";
        setTimeout(() => window.location.reload(true), 30000);
    } else {
        $cdSec.innerText = sec;
        $cdMin.innerText = min;
        $cdHrs.innerText = hrs;
    }
}