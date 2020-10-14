[![Logo](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Logo.png)](http://the-family-cookbook.herokuapp.com/)

# __The Family Cookbook__

## __Contents__

- [Aim of The Site](#aim-of-the-site)
- [UX](#ux)
    - [Client Stories](#client-stories)
    - [Database Plan](#database-plan)
    - [Wireframes](#wireframes)
- [Features](#features)
- [Future Goals](#future-goals)
- [Technology Used](#technology-used)
- [Testing](#testing)
    - [Validation](#validation)
    - [Screen Sizes](#screen-sizes)
    - [Site Links](#site-links)
    - [Deployment Test](#deployment-test)
    - [Multiple Browsers](#multiple-browsers)
    - [Feedback](#feedback)
- [Deployment](#deployment)
- [Credits](#credits)
- [Acknowledgements](#acknoledgements)
- [Disclaimer](#disclaimer)


## __Aim of the Site__

The aim of the site was to provide a platform where friends and family could share recipes.
It was also important for the users to be able to amend and tweek these recipes and be able to access these adjusted recipes at any time.

Please click the following link to the live website: http://the-family-cookbook.herokuapp.com/
## __UX__

### __Client Stories__

There were a number of stories that the site was aimed at fulfilling, they are listed below:

* "I am looking for a recipe, but do not want to sign up"
* "I want to share my recipes with friends and family"
* "I like to share, and also check to see if my recipes are popular"
* "I want to find and save recipes for the future"
* "I want to find recipes and if I want to change a part of the recipe save this on the same platform"

### __Database Plan__

At the start of the project it was important to plan out how the database was to be structured and select which platform it was to be hosted on.

I decided that MongoDB was the option that gave reliablity and flexibility to carry out the fuction needed to meet the user stories.

I have attached the original database plan below:

![Database Design](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Database-design.png)

During the development process I quickly realised that the 'recipe' database needed to have 2 additional fields:
 - Orginal: This was required for a view in the website.
 - Love: This kept a track of the number of adds per recipe to meet the 3rd user story.

These were then added to the Database.

### __Wireframes__

The wireframes were then produced to try to plan out how the site would look and feel.

The wireframes are detailed below:

![Site Map](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/New%20Wireframe%201.png)  
![Home - No Login](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Home%20-%20no%20login.png)  
![Sign up](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Login%20Page.png)  
![Home Logged in](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Home%20page%20-%20logged%20in.png)  
![Find Recipe](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Find%20a%20Recipe.png)  
![Add Recipe](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Add%20a%20Recipe.png)  
![My Cookbook](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/My%20Cookbook.png)  
![Amend Recipe](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Amend%20a%20Recipe.png)  
![Recipe View](https://github.com/Baldpet/Family-cookbook/blob/master/static/wireframes/Recipe%20View.png)  

There were a few adjustments to the wireframes were a few additional features were brought in late into the development process.

## __Features__

The current list of features that the app offers is the following:

* Feature 1 - Search for recipes that others have uploaded.

* Feature 2 - Within the search can filter by main ingredient and/or recipe name.

* Feature 3 - Can login and own a 'cookbook' of saved recipes.

* Feature 4 - Can amend the recipes in the users cookbook.

* Feature 5 - Can add a recipe to the site.

* Feature 6 - Can track how many other users have added their recipe.

## __Future Goals__

There are a number of areas that the site can improve or expand after going live:

* Password/account recovery
    * I would like to incorporate an automated service that allows users to recover their account. This could be through the Flask-Security addon.
* Pagination
    * When there are a number of recipes added it would be much better for the user to be able to scroll through pages rather than scroll down the screen.
* API/ajax search
    * Currently the search is completely handled through Javascript, however tied in with the pagination it would be better user experience to switch this to an ajax call.
* API import
    * There are a number of other recipe sites which may be able to export their recipes. If the site can import this then it will mean the users do not need to type all the recipe.
* Recipe comments
    * User comments on recipes are nice for people to read and can give them different ideas on the recipes themselves. Therefore it would be noce to implement this.
* Recipe pictures
    * To allow users to upload pictures to go along with the recipes that they upload.

## __Technology Used__

I have listed the following languages and technology used to produce this project below:

* Markdown
    * For the ReadMe file.
* HTML 5
    * For the base information and structure of the webpages.
* CSS 3
    * For the styling and beauty of the webpages.
* Materialise
    * Was used as a base structure for the front-end styling and grid.
* Javascript
    * For dynamic inputs onto the html and for initialisation of some interactive elements.
* Jquery
    * For easier targetting and functionality within Javascript.
* Python/Flask Framework
    * Used for the backend structure for liasing with the front-end and the database.
* MongoDB
    * This was where the database is stored and accessed. 

## __Testing__

Testing was conducted throughout the project, each new feature that was added was checked and tested through using the development browser and via the chrome development tools.

### Validation

HTML, CSS, Javascript and Python code has been checked by online validators and any suggestions adjusted.
 

### Screen Sizes

There was testing throughout the project to make sure that the project looks good and works on multiple screen sizes and devices.  
This was done through the Chrome developer tools by reducing the width of the screen and also utilising their mobile device view.

During this testing there were a few challenges to responsiveness which have required some media queries CSS to resolve.  

### Site Links

I have fully tested all the links on the site to make sure that they go through to the correct page.  
I have also made sure that any which are linked to outside sites open in a new window.  

### Deployment Test

The website was tested on deployment through the app hosting site Heroku, no bugs or problems were detected upon deployment.  

### Multiple Browsers

I have undertaken some tests on other popular browsers to see if there are any bugs that I have picked up.  
The website has loaded on all browsers and devices tested which are shown:  
 
    * Microsoft Edge
    * Firefox
    * Chrome
    * Samsung Mobile (Android)
    * Safari Mobile

No visual or other bugs were detected on any of the browsers mentioned.

### Feedback

I recieved feedback from multiple friends and family who were able to give the app a try.

In general there were no major issues or failures, however it was a good chance to see which areas required some touch ups for the user experience.


## __Known Issues & Resolutions__

There are no currently known issues.

There were some issues which arose that resolutions were found, they are documented below:

* Amend Form
    * There was an issue where the form would load with the recipe information, however the dropdown select would not load properly and causing an issue on submission.
    * This was fixed by removing the 'requirement' to fill out this field and pre fill it with the recipe ingredient.

* Search function
    * There was an issue where the search for the recipe name was not combining properly with the main ingredient search. Therefore showing the wrong recipes.
    * A workaround was devised that utilises the addClass Jquery function.

* Cookbook route whilst not logged in
    * If the cookbook link was clicked on the header whilst not logged in it would create an error as the URL would not match.
    * This was resolved by adding an additional decorator for the 'cookbook' route. It now reroutes the user back to the login page.


## __Deployment__

There were a number of steps taken to deploy the website onto Heroku App.

1. The code was written on an online IDE - Gitpod, the major changes were written via branches.
2. The branches were then merged together with the master using Git.
3. The code was then pushed to GitHub where it is stored on a public repository.
4. An app was registered on Heroku Apps and then set as a remote git.
5. A Procfile and a requirement.txt file was created so that Heroku can process the git push.
6. The app was then pushed to Heroku
7. The Heroku key variables were then entered to allow the app to run.
    * PORT
    * IP
    * MONGO_URI
8. The app is then upladed and live.
9. This would be the deployed version, any changes would be saved on the development version which would be on a branch in github.

The code can be run locally through clone or download on github.  
By opening the repository and and being in the main 'code' section there is a button 'clone or download'.  
This button will provide a link that you can use on your desktop or download as a ZIP file.

## __Credits__

There were a number of sources used throughout the project which I would like to credit:

* Pictures were sourced through various places:
    * Icons
        * Material Icons
    * Link Images
        * Linkedin
        * Github
    * Background picture and recipe pictures:
        * https://pexels.com/

There was also some code utilised which is highlighted in comments within the code.

* Code Institute Slack Channel
* Stack Overflow

## __Acknoledgements__

I would like to acknoledge my mentor Anthony Ngene who has helped me out on some key points for where the project should be heading. 

Lastly I would like to acknoledge my fiancee, family and friends who have helped with their feedback and suggestions on the structure and the testing of the project.

## __Disclaimer__

This project has been made solely for educational purposes and is not for commercial use.