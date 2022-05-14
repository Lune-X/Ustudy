
import { useAPI, getAbsoluteURL, getURLParam } from "./helpers.js";

class ListVideos {
    constructor() {
        this.mainDiv = document.getElementById("main-container");

        let listId = getURLParam("id");
        let pageType = getURLParam("type")

        let apiQuery = "/api/video/";

        if(pageType == "module") {
            apiQuery += "get_module_videos/";
        }
        else if (pageType == "saved") {
            apiQuery += "get_my_saved_videos/";
        }
        else if (pageType == "posted") {
            apiQuery += "get_my_posted_videos/";
        }
        apiQuery += "?id=" + listId;

        useAPI("GET", apiQuery, null, (data) => {
            let videos = JSON.parse(data);

            let listTitleEle = document.getElementById("list-title");
            if(pageType == "module") {
                listTitleEle.innerText = "Module videos";
            }
            else if (pageType == "saved") {
                listTitleEle.innerText = "My saved videos";
            }
            else if (pageType == "posted") {
                listTitleEle.innerText = "My posted videos";
            }


            let rowWidth = 3;
            for(let i = 0; i < videos.length / rowWidth; i++) {
                let newRow = document.createElement("div");
                newRow.className = "row";

                for(let j = 0; j < rowWidth; j++) {
                    let currentVideo = {};
                    Object.assign(currentVideo, videos[i * rowWidth + j]);

                    let videoDiv = document.createElement("div");
                    videoDiv.classList.add("col");

                    let thumbDiv = document.createElement("div");
                    thumbDiv.classList.add("d-flex");
                    thumbDiv.classList.add("justify-content-center");

                    videoDiv.appendChild(thumbDiv);

                    let thumbImg = document.createElement("img");
                    thumbImg.width = 250;
                    thumbImg.height = 150;
                    thumbImg.alt = "picture";

                    thumbImg.src = "https://i1.ytimg.com/vi/" + currentVideo.link + "/default.jpg";

                    thumbDiv.appendChild(thumbImg);

                    let linkToOneVideo = getAbsoluteURL() + "/one-video/?id=" + currentVideo.id;

                    thumbImg.onclick = () => {
                        window.location.href = linkToOneVideo;
                    };

                    let aElement = document.createElement("a");
                    aElement.classList.add("d-flex");
                    aElement.classList.add("justify-content-center");
                    aElement.innerText = currentVideo.title;

                    aElement.href = linkToOneVideo;

                    videoDiv.appendChild(aElement);

                    if(currentVideo.link != undefined) {
                        newRow.appendChild(videoDiv);
                    }
                }

                this.mainDiv.appendChild(document.createElement("br"));
                this.mainDiv.appendChild(newRow);
            }

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
    console.log("hi ive just loaded in");
    let listVideos = new ListVideos();
};