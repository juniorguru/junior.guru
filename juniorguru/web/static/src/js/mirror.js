/*
  Big thanks to David Walsh!
  https://davidwalsh.name/browser-camera
*/

document.addEventListener('DOMContentLoaded', () => {
  Array.from(document.getElementsByClassName('mirror')).forEach((mirror) => {
    const errorHTML = extractNoScriptHTML(mirror.getElementsByTagName('noscript')[0]);
    let mirrorBackground;

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      console.error("navigator.mediaDevices isn't supported");
      mirror.prepend(createError(errorHTML));
      return;
    }

    const mirrorExpand = Array.from(mirror.getElementsByClassName('mirror-expand'))[0];
    mirrorExpand.disabled = true;

    const mirrorRun = Array.from(mirror.getElementsByClassName('mirror-run'))[0];
    mirrorRun.addEventListener('click', (event) => {
      event.preventDefault();

      mirrorBackground = document.createElement('div');
      mirrorBackground.classList.add('mirror-background');
      mirror.prepend(mirrorBackground);

      const mirrorVideo = document.createElement('video');
      mirrorVideo.classList.add('mirror-video');
      mirrorVideo.autoplay = true;

      navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        mirrorVideo.srcObject = stream;
        mirrorVideo.play();
        mirrorBackground.prepend(mirrorVideo);

        mirrorRun.disabled = true;
        mirrorExpand.disabled = false;
      }).catch((exception) => {
        console.error("Couldn't acquire permission to use camera", exception);
        mirror.prepend(createError(errorHTML));
        mirrorRun.disabled = true;
      });
    }, false);

    mirrorExpand.addEventListener('click', (event) => {
      event.preventDefault();
      mirrorBackground.classList.add('mirror-background-expanded');
      mirrorExpand.disabled = true;
    }, false);
  });
});

function createError(innerHTML) {
  const error = document.createElement('div');
  error.classList.add('mirror-error');
  error.innerHTML = innerHTML;
  return error;
}

function extractNoScriptHTML(noscript) {
  return noscript.childNodes[0].textContent;;
}
