# Email App

This project is a proof-of-concept web application that was developed to help in expediting the creation of general information emails regarding Bachelor degrees offered by any university.

## Introduction

This project is designed to be used by customer service representatives who are repetitively responding to a large volume of emails on a daily basis. These emails always have a very predictable structure which is not so difficult to recreate using programming. This means that these representatives do not have to worry about manually copying and pasting information unique to each degree into already existing templates. Rather it collects the information from a simple database, alongside any additional templates that may be relavent to the customer's enquiry, and inputs the information into the template. The resulting HTML email can be copied to the user's clipboard and put into CRM software such as Salesforce, to be sent to enquirers. 

Future iterations will allow the user to adjust the order of the information in the emails in a drag and drop fashion. The enhance button will be linked to OpenAi's chatGPT so that the emails can be made unique if required and more synthesised.

## Description
### app.py
Contains the Flask application and server logic. Has each of the routes that make up the project.
### helper.py
Contains the functions and logic that assists with creation of the email templates. Various functions are responsible for getting the data, such as the actual html building blocks for the email and information about the degree, from the sqlite database. There is also a function that given the type of enquirer, the specific degree, and the date that the function was called, to provide a sensible sentence regarding the application dates for that course.
### database.db
Contains various tables which contain information about the degrees, the application dates that are applicable and the html_blocks which are essentially the additional bits of information that might be required. E.g. there is a different template for how to apply for a course depending if you are applying for the first time or you are transferring from another university. I am not confident of this being the best solution but thought this might be easier to maintiain and change rather than having the html code in the file system.

### HTML_blocks
This contains the aforementioned html_blocks as files.

### templates
Contains all the html templates for the web application.

### db_setup
Contains the code for setting up the sqlite schema.

## Video
Here is the video explaining the project here: https://youtu.be/3FRuaBVQ4TI

## Credits
This was project was created primarily using boiler plate templates that were supplied as part of the Harvard CS50 course that was repurposed for this project. You can sign up for the course free here: https://pll.harvard.edu/course/cs50-introduction-computer-science, or access all the lectures here: https://www.youtube.com/watch?v=IDDmrzzB14M&list=PLhQjrBD2T380F_inVRXMIHCqLaNUd7bN4.
