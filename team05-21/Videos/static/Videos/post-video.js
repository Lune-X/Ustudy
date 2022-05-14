import { useAPI, getAbsoluteURL } from "./helpers.js";

class PostedVideos {
    constructor() {

        let modulesSelectEle = document.getElementById("modules");

        useAPI("GET", "/api/profile/get_all_my_modules/", null, (data) => {
            let modules = JSON.parse(data);

            for(let module of modules) {
                let optionEle = document.createElement("option");
                optionEle.textContent = module.name;
                optionEle.value = module.name;
                optionEle.setAttribute("module-id", module.id);

                modulesSelectEle.appendChild(optionEle);
            }
        });


        document.getElementById("post-button").onclick = () => {

            const title = document.getElementById("title").value || "";
            const link = document.getElementById("url").value || "";
            const description = document.getElementById("description").value;
            const modules = getSelectModules(modulesSelectEle);
            const subtitles = document.getElementById("subtitles").checked;

            if(title === "" || link === "" || link.length != 11) {
                alert("Please provide a title and valid youtube ID!")
                return;
            }

            const videoData = {
                title: title,
                link: link,
                description: description,
                module_ids: modules,
                has_captions: subtitles
            }

            useAPI("POST", "/api/video/post_video/", videoData, (data) => {
                this.listPostedVideos();
            });
        }
    }

    listPostedVideos() {
        let urlArgs = "?type=posted";
        let absoluteURL = getAbsoluteURL();
        window.location.href = absoluteURL + "/list-videos/" + urlArgs;
    }
}

// Return an array of the selected opion values
// select is an HTML select element
function getSelectModules(ele) {
    var result = [];
    var options = ele && ele.options;
    var opt;
  
    for (var i=0, iLen=options.length; i<iLen; i++) {
      opt = options[i];
  
      if (opt.selected) {
        result.push(opt.getAttribute("module-id"));
      }
    }
    return result;
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
    console.log(colornum);
    if (colornum!=""){
        color(colornum);
    }
    else{
        setCookie("newuser","0",365);
        color(0);
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
    console.log("Just loaded in");
    let videoMenu = new PostedVideos();
}