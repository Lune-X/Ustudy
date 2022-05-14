import { useAPI, getAbsoluteURL, getURLParam } from "./helpers.js";

class OneVideoPage {
    constructor() {
        
        let args = "?id=" + getURLParam("id");

        useAPI("GET", "/api/video/get_video/" + args, null, (data) => {
                let video = JSON.parse(data);

                let videoTitleEle = document.getElementById("video-title");
                videoTitleEle.innerText = video.title;

                let url = "https://www.youtube.com/embed/" +  video.link + "?enablejsapi=1";

                let template = document.createElement("template");
                let iframeHtml = '<iframe id="existing-iframe-example" : width="780" : height="460" : src= url : frameborder="0" : style="border: solid 4px #37474F;margin-left: 180px;margin-top: 50px"></iframe>';
                iframeHtml = iframeHtml.trim(); // clean up the string a little
                template.innerHTML = iframeHtml;
                let newIframe = template.content.firstChild;
                newIframe.src = url;

                var tag = document.createElement('script');
                tag.id = 'iframe-demo';
                tag.src = 'https://www.youtube.com/iframe_api';
                var firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

                document.getElementById("videoContainer").appendChild(newIframe); 

                var player;
                function onYouTubeIframeAPIReady() {
                    player = new YT.Player('existing-iframe-example', {
                        events: {
                            'onReady': onPlayerReady,
                            'onStateChange': test
                        }
                    });
                }
                function test(){
                    console.log("video playerStateChange");
                }
                function onPlayerReady(event) {
                    document.getElementById('existing-iframe-example').style.borderColor = '#000000';
                }

        });
        
        document.getElementById("saved-button").onclick = () => {
            this.onSaveClick(getURLParam("id"));
        };
     }
    
    
    onSaveClick(video_id) {
        useAPI("POST", "/api/profile/set_my_saved_video/", {id : video_id}, (data) => {
            console.log("successfully called set my saved videos API call, data received: " + data);
        });
    }
}

function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*24*60*60*1000));
    var expires = "expires="+d.toGMTString();
    document.cookie = cname+"="+cvalue+"; "+expires+";path=/;";
}

function getCookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
}

function checkCookie(){
    console.log("hi");
    var colornum=getCookie("username");
    if (colornum!=""){
        color(colornum);
    }
    else{
        setCookie("username","0",365);
    }
}


function color(colorNum){
	var box = document.getElementById("main-container");
    if(colorNum == 0){
        box.style.backgroundColor="skyblue";
    }
    else if(colorNum == 1){
        box.style.backgroundColor="grey";
    }
}

function changecookie(){
    var colornum = getCookie("username");
    if(colornum == 0){
        document.cookie= "username=1; expires=Sun, 31 Dec 2023 12:00:00 UTC;";
    }
    else if(colornum == 1){
        document.cookie= "username=0; expires=Sun, 31 Dec 2023 12:00:00 UTC;";
    }
}

window.onload = () => {
    checkCookie();
    console.log("just loaded in");
    let oneVideoPage = new OneVideoPage();
}
