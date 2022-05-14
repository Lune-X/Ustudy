// Here's a little helper file, for things that will be used often
// It may be duplicated across apps??


// Inputs:
//  type: String (either "GET" or "POST")
//  url: String (since this is AJAX, likely to be something like "/api/...")
//  data: Object that you wish to send to the server (if needed) - like { id: 12, name: "peepee" }
//  callback: Function that will be called when the server is done
//      IMPORTANT! Define your function using the "arrow syntax" (a lambda function)
//      so do this: useAPI(..., (data) => { ... });
//  absolute: Boolean (optional) specifies if you want to query a relative path or the absolute path
//      By default it's set to true, which makes more sense for API calls
//      as they are defined at hostname:8000/api/...
//
// Results:
//  This helper sends an AJAX HTTP request to your specifed URL,
//  and afterwards, when a response is received from the back-end,
//  your specifed callback function "(data) => { stuff; }" will execute
//  (the callback is done asynchronously - meaning it's on another thread)
//  (so you don't have to worry about the webpage freezing or anything while waiting)
function useAPI(type, url, data, callback, absolute=true) {
    if(type !== "GET" && type !== "POST") {
        throw new Error("Hmm, the AJAX call type isn't a GET nor a POST");
    }

    let xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = () => {
        if(xhttp.readyState !== 4) {
            console.log("received onreadystatechange, but isn't ready yet");
            return; // not fully done yet, apparently onreadystatechange can be called multiple times
        }

        console.log("Response received for HTTP AJAX call to " + url + " here's the data:");
        console.log(xhttp.response);
        callback(xhttp.response);
    };

    const absoluteURL = getAbsoluteURL();
    let myUrl = (absolute ? absoluteURL + url : url);
    xhttp.open(type, myUrl, true);

    xhttp.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
    xhttp.setRequestHeader("Content-Type", "application/json");

    let myData = {};

    if(data != null || data != undefined) {
        myData = data;
    }

    myData.csrfmiddlewaretoken = "{{ csrf_token }}";
    
    xhttp.send(JSON.stringify(myData));

    console.log("Just sent a " + type + " request with data " + JSON.stringify(myData) + " to " + url);
}


function getAbsoluteURL() {
    // Returns the front bit of the URL, eg https://ustudy.bham.team
    // or http://localhost:8000
    return window.location.protocol + "//" + window.location.host;
}


function getURLParam(paramName) {
    // Gives you the parameter value in the URL if it exists
    // (or null if not)
    let urlParams = new URLSearchParams(window.location.search);
    let result = urlParams.get(paramName);

    if(result == "" || result == null || result == undefined) {
        return null;
    }
    return result;
}


function getCookie(cname) {
    // From https://www.w3schools.com/js/js_cookies.asp
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


export { useAPI, getAbsoluteURL, getURLParam, getCookie };
