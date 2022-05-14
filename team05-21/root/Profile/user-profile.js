import { useAPI } from "./helpers.js";

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
        document.cookie= "username=1; expires=Sun, 31 Dec 2023 12:00:00 UTC;path=/;";
    }
    else if(colornum == 1){
        document.cookie= "username=0; expires=Sun, 31 Dec 2023 12:00:00 UTC;path=/;";
    }
}

window.onload = () => {

    useAPI("GET","/api/user/get_me/",null,(data) => {
        let me =JSON.parse(data);
        document.getElementById("username").innerText=me.username;
        document.getElementById("year").innerText=me.year_of_study;
        document.getElementById("email").innerText=me.email;
    });

    checkCookie();
    console.log("hi ive just loaded in");

    document.getElementById("change-appearance").onclick = changecookie;
};

