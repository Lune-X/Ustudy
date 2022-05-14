// The "main" method of this file will be declared after the class declaration



// Here's a useful helper function that I made for AJAX requests
import { useAPI, getAbsoluteURL } from "./helpers.js";

class ModuleDashboard {
    constructor() {
        // You declare your class attributes/fields here (which isn't like other languages, because javascript is weird),
        // and also logic for setting things up

        // some class attributes using "this" keyword
        this.mainDiv = document.getElementById("main-container");
        
        // Logic - since this page (the modules dashboard) doesn't have much dynamic stuff,
        // we won't likely need other methods besides our constructor here.
        
        // For this URL endpoint, reference the project's api/viewsprofile.py file
        useAPI("GET", "/api/profile/get_my_modules_this_year/", null, (data) => {
            
            // The response sent to us is a string, so let's convert it
            // to a usable Javascript object
            // This should be an array (since it's multiple modules)
            // It should look like this:
            // [
            //      { id: 6, name: "Networks and Security" },
            //      { id: 8, name: "Functional Programming" },
            //      ...  
            // ] or something like that.
            let myModules;

            try {
                myModules = JSON.parse(data);

                if(!Array.isArray(myModules)) {
                    if (myModules['detail'] == "Authentication credentials were not provided.") {
                        window.location.href = getAbsoluteURL() + "/login/";
                    }
                    else if (myModules['detail'] == "Not found.") {
                        window.location.href = getAbsoluteURL() + "/choose-school/";
                    }
                }
            } catch (e) {
                window.location.href = getAbsoluteURL() + "/choose-school/";
                return;
            }
            
            // Let's populate the HTML file programmatically
            let rowWidth = 3;
            for(let i = 0; i < myModules.length/rowWidth; i++) {
                // Create a row element
                let newRow = document.createElement("div");
                newRow.className = "row";

                for(let j = 0; j < rowWidth; j++) {
                    let currentModule = myModules[i * rowWidth + j];

                    // Create the button element
                    let template = document.createElement("template");
                    // ^ The element type is not a "button", here, it's simply because
                    // the styling and everything has already been written, so we'll use
                    // a template to create our new button element
                    // https://stackoverflow.com/questions/494143/creating-a-new-dom-element-from-an-html-string-using-built-in-dom-methods-or-pro/35385518#35385518
                    let btnHtml = '<button type="button" style="margin-top: 100px;margin-left: 100px;width: 250px;height: 100px;font-size: large;font-weight: bold;"></button>';
                    // (I've just used single quotes this timem because the HTML text I copied had double quotes)
                    btnHtml = btnHtml.trim(); // clean up the string a little
                    template.innerHTML = btnHtml;
                    let newBtn = template.content.firstChild; // finally create our new button

                    newBtn.moduleId = currentModule.id;
                    // ^ Now, if you load up the page when the server is running,
                    // and press f12 to get the console up,
                    // You'll see that the button element has a custom data attribute labelled
                    // data-module-id="..."
                    // This is because HTML will convert it from camelCase to dashed-variable-name
                    // (with "data-" attached to the front of it)
                    // To access this in future in javascript, you would do newBtn.moduleId,
                    // just like how it is here.

                    newBtn.innerText = currentModule.name;

                    // Let's make the button do something when we click it
                    newBtn.onclick = () => {
                        this.onModuleClick(currentModule.id);
                    }

                    // Actually attach the new button to the new row
                    newRow.appendChild(newBtn);
                }

                // Attach the new row to the main div
                this.mainDiv.appendChild(newRow);
            }
        
            
        });
    }

    exampleMethod() {
        console.log("Hi I'm just an example method in the class, sitting here (I'm not being used anywhere)");
    }

    onModuleClick(module_id) {
        let urlArgs = "?id=" + module_id + "&type=" + "module";
        let absoluteURL = getAbsoluteURL(); // helper function
        window.location.href = absoluteURL + "/list-videos/" + urlArgs;
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

// The "main" function after the window finishes loading
window.onload = () => {
    checkCookie();
    console.log("A just loaded in");
    let moduleDashboard = new ModuleDashboard();
}
