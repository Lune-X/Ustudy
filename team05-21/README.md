## Intructions to replicate the pipeline on a new server
1. Clone this repository
2. Go to Settings > General > Visibility, project features, permissions and enable CI/CD 
3. In order to deploy your application set up your runner and register it. Instructions to register your runner are included in Settings > CI/CD > Runners. We have used DigitalOcean to set up our runner. 
4. Go to Settings > CI/CD > Variables and add two variables : your private key and the server's ip that you are going to be using. For your private key use the _Key_ SSH_PRIVATE_KEY and add your key in the _Value_ section. For the server's ip use the _Key_ UBUNTU_SERVER and write the ip in the _Value_ section. 
5. Get a domain for you web application
6. Go to CI/CD > Editor and edit the yml file to accomodate your new domain. Where the variables are defined change the value of the current DOMAIN variable to be you new domain. Also change the EMAIL variable.

You are now all set to deploy your application!


## Project structure:
This django project is split into 4 apps:

- api (for serving JSON data to frontend)
- Accounts
- Profile
- Videos

The three main apps (Accounts, Profile, Videos) contain how the database tables are laid out, how to access them on the browser (eg. going to hostname:8000/login/ is handled through the Accounts/urls.py and views.py pages), and more importantly foor the Front end, is that these App folders are where the Templates are stored (the HTML files).

Within each App, there is a folder called templates/App-name. 
In there will be your HTML files.

### File Naming
Standard naming convention would be dashed-names, like post-video.html and module-dashboard.html

### Using Javascript
To use javascript in these HTML files, go to App-name/static/App-name to store your javascript files. Example: Profile/static/Profile contains module-dashboard.js which is referenced in mmodule-dashboard.html

### Using the API
Please reference the module-dashboard.js file to get an example of how the API calls should work in practice.

The API is a special app, because its purpose is Not to display templates (aka HTML files), but rather to exchange data between the Front-end and Back-end whilst the client's browser is still displaying the same page. This allows you to update the browser dynamically in the background, without having to refresh the page. You can use the API to ask the server to give you the modules you study, and you can create new clickable buttons for the user in real-time using Javascript on the Front-end.

To reference what the API method names are, and how to use them, please refer to the api/viewaccounts.py, api/viewprofile.py, and api/viewvideos.py files.

Note: Not all API functionality has been implemented yet, so if any are needed, let the team know. (e.g. fetching the number of likes on a comment & many others)

### Brief structure of important stuff
```
api/
├─ viewsaccounts.py
├─ viewsprofile.py
├─ viewsvideos.py
Accounts or Profile or Videos/
├─ static/
│  ├─ Accounts or Profile or Videos/
│  │  ├─ javascript-lives-here.js
├─ templates/
│  ├─ Accounts or Profile or Videos/
│  │  ├─ templates-live-here.html
```
