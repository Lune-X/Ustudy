// Here's a useful helper function that I made for AJAX requests
import { useAPI, getAbsoluteURL } from "./helpers.js";

class SchoolMenu {
    constructor() {
        
        // some class attributes using "this" keyword
        this.mainDiv = document.getElementById("main-container");
        
        // For this URL endpoint, reference the project's api/viewsprofile.py file
        useAPI("GET", "/api/profile/get_all_schools/", null, (data) => {
            
            let schools = JSON.parse(data);
            
            let newRow = document.createElement("div");
            newRow.classList.add("col-sm-9d");

            console.log(schools);
            
            for(let i = 0; i < schools.length; i++) {
                let currentSchool = schools[i];

                let newRow = document.createElement("div");
                newRow.classList.add("col-sm-9d");

                // Create the button element
                let template = document.createElement("template");
                    
                let btnHtml = '<button type="submit", style="margin-top:30px;height:50px;width:500px;margin-left:170px;"></button>';
                    
                btnHtml = btnHtml.trim(); // Clean up
                template.innerHTML = btnHtml;
                let newBtn = template.content.firstChild; // Create new button

                newBtn.moduleId = currentSchool.id;

                newBtn.innerText = currentSchool.name;

                // button redirects to chosen school's courses menu when we click it
                newBtn.onclick = () => {
                    this.onSchoolClick(currentSchool.id);
                }

                // Attachs the new button to the new row
                newRow.appendChild(newBtn);

                // Attachs the new row to the main div
                this.mainDiv.appendChild(newRow);
            }
        
            
        });
    }

    onSchoolClick(school_id) {
        let urlArgs = "?id=" + school_id;
        let absoluteURL = getAbsoluteURL(); // helper function
        window.location.href = absoluteURL + "/choose-course/" + urlArgs;
    }
}




// The "main" function after the window finishes loading
window.onload = () => {
    console.log("Just loaded in");
    let schoolMenu = new SchoolMenu();
}

