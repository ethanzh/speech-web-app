function gotDevices(deviceInfos) {
    for (let i = 0; i !== deviceInfos.length; ++i) {
        const deviceInfo = deviceInfos[i];
        const option = document.createElement("option");
        option.value = deviceInfo.deviceId;
        if (deviceInfo.kind === "audioinput") {
            option.text =
                deviceInfo.label || "microphone " + (audioSelect.length + 1);
            audioSelect.appendChild(option);
        } else if (deviceInfo.kind === "videoinput") {
            option.text = deviceInfo.label || "camera " + (videoSelect.length + 1);
            videoSelect.appendChild(option);
            videoSelect.value = deviceInfo.deviceId
        }
    }
}

function getStream() {
    if (window.stream) {
        window.stream.getTracks().forEach(function(track) {
            track.stop();
        });
    }
    const constraints = {
        audio: {
            deviceId: {
                exact: audioSelect.value
            },
        },
        video: {
            deviceId: {
                exact: videoSelect.value
            },
            width: {
                exact: 640
            },
            height: {
                exact: 480
            }
        },
    };


    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(gotStream)
        .catch(handleError);
}

function gotStream(stream) {
    window.stream = stream;
    videoElement.srcObject = stream;
}

function handleError(error) {
    console.error("Error: ", error);
}



const delay = ms => new Promise(res => setTimeout(res, ms));

function cancelRecording() {
    isCancelled = true;
    stopRecording()
}

function stopRecording() {
    mediaRecorder.stop();
    audioSelect.disabled = false;
    videoSelect.disabled = false;
    startButton.disabled = false;
    cancelButton.disabled = true;
    endButton.disabled = true;
}


const video = document.querySelector("video");

const videoElement = document.querySelector("video");
const audioSelect = document.querySelector("select#audioSource");
const videoSelect = document.querySelector("select#videoSource");

const startButton = document.querySelector("button#start")
const cancelButton = document.querySelector("button#cancel")
const endButton = document.querySelector("button#end")
cancelButton.disabled = true;
endButton.disabled = true;

var mediaRecorder;
var recordedChunks = [];
var isCancelled = false;

function startRecording() {
    audioSelect.disabled = true;
    videoSelect.disabled = true;
    startButton.disabled = true;
    cancelButton.disabled = false;
    endButton.disabled = false;

    const constraints = {
        audio: {
            deviceId: {
                exact: audioSelect.value
            },
        },
        video: {
            deviceId: {
                exact: videoSelect.value
            },
            width: {
                exact: 640
            },
            height: {
                exact: 480
            }
        },
    };
    navigator.getUserMedia(constraints, stream => {
        mediaRecorder = new MediaRecorder(stream);
        const options = {
            mimeType: 'video/webm;codecs=vp9'
        };
        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data)
            } else {}
        };
        mediaRecorder.onstop = e => {
            if (isCancelled) {
                isCancelled = false;
                return
            }
            let blob = new Blob(recordedChunks, {
                'type': 'video/mp4'
            })
            createDownloadLink(blob)
            recordedChunks = []
        }
        mediaRecorder.start();


    }, e => console.log(e))
}

navigator.mediaDevices
    .enumerateDevices()
    .then(gotDevices)
    .then(getStream)
    .catch(handleError);

audioSelect.onchange = getStream;
videoSelect.onchange = getStream;

function createDownloadLink(blob) {
    var url = URL.createObjectURL(blob);
    var link = document.createElement('a');

    link.href = url;
    link.download = new Date().toISOString() + '.webm';
    link.innerHTML = link.download;

    var filename = new Date().toISOString();
    var xhr = new XMLHttpRequest();
    xhr.onload = function(e) {
        if (this.readyState === 4) {
            console.log("Server returned: ", e.target.responseText);
        }
    };
    var fd = new FormData();
    fd.append("data", blob, filename);
    xhr.open("POST", "/sample", true);
    xhr.send(fd);
}