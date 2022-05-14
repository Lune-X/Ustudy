import { useAPI, getAbsoluteURL, getURLParam } from "./helpers.js";

class CourseMenu {
    constructor() {
        
        // some class attributes using "this" keyword
        this.coursesDiv = document.getElementById("courses");
        
        let school_id = getURLParam("id")
        
        useAPI("GET", "/api/profile/get_courses_in_school/?id=" + school_id, null, (data) => {
            
            let courses = JSON.parse(data);
            
            let newRow = document.createElement("div");
            newRow.classList.add("col-sm-9d");

            console.log(courses);
            
            for(let i = 0; i < courses.length; i++) {
                let currentCourse = courses[i];

                let newRow = document.createElement("div");
                newRow.classList.add("col-sm-9d");

                // Create the button element
                let template = document.createElement("template");
                    
                let btnHtml = '<button type="submit", style="margin-top:30px;height:50px;width:500px;margin-left:170px;"></button>';
                    
                btnHtml = btnHtml.trim(); // Clean up
                template.innerHTML = btnHtml;
                let newBtn = template.content.firstChild; // Create new button

                newBtn.moduleId = currentCourse.id;

                newBtn.innerText = currentCourse.name;

                // button redirects to chosen school's courses menu when we click it
                newBtn.onclick = () => {
                    this.onCourseClick(currentCourse.id);
                }

                // Attachs the new button to the new row
                newRow.appendChild(newBtn);

                // Attachs the new row to the main div
                this.coursesDiv.appendChild(newRow);
            }
        
            
        });
        
        document.getElementById("year-select").onchange = this.onYearSelect;
        document.getElementById("confirm").onclick = this.onConfirmClick;
    }

    onCourseClick(course_id) {
        useAPI("POST", "/api/profile/set_my_course/", {id : course_id}, (data) => {
            console.log("successfully called set my course API call, data received: " + data);
        });
    }
               
    onYearSelect() {
        let year = document.getElementById("year-select").value;
        useAPI("POST", "/api/profile/set_my_year/", {year: year}, (data) => {
            console.log("successfully called set my year API call, data received: " + data);
        });
    }
    
    onConfirmClick() {
        useAPI("POST", "/api/profile/set_my_user_modules/", null, (data) => {
            console.log("successfully called set my user modules API call, data received: " + data);
            let absoluteURL = getAbsoluteURL(); // helper function
            window.location.href = absoluteURL + "/module-dashboard/";
        });
    }
}




// The "main" function after the window finishes loading
window.onload = () => {
    console.log("Just loaded in");
    let courseMenu = new CourseMenu();
}

