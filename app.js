function makeRequest(method, url) { // https://stackoverflow.com/a/48969580
    return new Promise(function (resolve, reject) {
        let xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.onload = function () {
            if (this.status >= 200 && this.status < 300) {
                resolve(xhr.response);
            } else {
                reject({
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        };
        xhr.onerror = function () {
            reject({
                status: this.status,
                statusText: xhr.statusText
            });
        };
        xhr.send();
    });
}

// Get channel data and generate content
let $trailer = document.getElementById('trailer');
window.YT.ready(async () => {
    let trailerId = $trailer.getAttribute('videoId')
    let trailer = new YT.Player('trailer', {
        height: '349',
        width: '560',
        videoId: trailerId,
        host: 'https://www.youtube-nocookie.com',
        playerVars: {
            'playsinline': 1,
            'controls': 0,
            'disablekb': 1,
            'loop': 1,
            'playlist': trailerId,
            'modestbranding': 1
        },
        events: {
            'onReady': () => {
                trailer.mute();
                trailer.setPlaybackRate(0.8);
                trailer.playVideo();

                $trailer = trailer.h;
                $trailer.classList.add('sizingToWidth');
                resizeTrailer();
            }
        }
    });
});

function resizeTrailer() {
    if ($trailer.classList.contains('sizingToHeight')) {
        if (window.innerHeight > $trailer.clientHeight) {
            $trailer.classList.remove('sizingToHeight');
            $trailer.classList.add('sizingToWidth');
        }
    } else {
        if (window.innerWidth > $trailer.clientWidth) {
            $trailer.classList.remove('sizingToWidth');
            $trailer.classList.add('sizingToHeight');
        }
    }
}
window.addEventListener('resize', () => resizeTrailer());