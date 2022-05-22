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
})
function startVideo() {
    $bgImg.classList.add('hide');
    $bgVideo.playbackRate = .6;
    $bgVideo.play();
}
$bgVideo.addEventListener('ended', () => {
    $bgVideo.currentTime = 0;
    $bgVideo.play();
})