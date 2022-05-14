import { useAPI, getAbsoluteURL } from "./helpers.js";

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


function submitChanges() {

    const username = document.getElementById("username").value.replace(/\s/g, '');
    const password = document.getElementById("password").value.replace(/\s/g, '');
    const email = document.getElementById("email").value.replace(/\s/g, '');

    if(username != "") {
        useAPI("POST", "/api/user/set_username/", {username:username}, (data) => {

        });
    }

    if(password != "") {
        useAPI("POST", "/api/user/set_password/", {password:password}, (data) => {

        });
    }

    if(email != "") {
        useAPI("POST", "/api/user/set_email/", {email:email}, (data) => {

        });
    }

}

function redirect(){
    let absoluteURL = getAbsoluteURL(); // helper function
    window.location.href = absoluteURL + "/choose-school/" 
}

window.onload = () => {
    checkCookie();
    console.log("hi ive just loaded in");
    document.getElementById("year").onclick = redirect;
    document.getElementById("changeprofile").onclick = submitChanges;
};