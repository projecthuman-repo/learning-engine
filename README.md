# Table of Contents

- [Partner Introduction](#partner-intro)
- [Description](#description)
- [Key Features](#key-features)
- [User Stories](#user-stories)
- [Architecture](#architecture)
  - [Technology Stack](#technology-stack)
  - [Functionality Description](#functionality-description)
- [Configuration Files](#configuration-files)
- [Accessing Application](#accessing-application)
  - [Base URL](#base-url)
  - [Documentation URL](#documentation-url)
  - [Test Key](#test-key)
- [Instructions](#instructions)
  - [Using it through Swagger](#using-it-through-swagger)
  - [Using it through API calls](#using-it-through-api-calls)
- [Local Setup and Local Testing](#local-setup-and-local-testing)
  - [Installation](#installation)
  - [Testing](#testing)
  - [Usage Instructions](#usage-instructions)
- [Demo](#demo) 
- [Deployment and GitHub Workflow](#deployment-and-github-workflow)
  - [Auto-Deployment Setup](#auto-deployment-setup)
  - [Further Testing](#further-testing)
- [Coding Standards and Guidelines](#coding-standards-and-guidelines)
- [Licenses](#licenses)
- [Additional Documentation](#additional-documentation)


## Partner Introduction
Primary Contact: James Rhule (jamesrhule@projecthumancity.com), 
Dev Contact: ZeLong Liu (jack.liu1600@gmail.com) 

This project is in collaboration with [Project: Human City](https://projecthumancity.com/), a non-profit organization dedicated to addressing human inequality, remediate social injustice and bridge the lack of access to human needs globally. They create solutions to cater to several real-world issues ranging from recycling to electricity to education.


## Description 
Lotus Learning, is an educational platform that leverages AI to assist educators in enhancing their study materials. It offers a range of features, including educational games, test evaluation tools and paper critiquing. 

Our primary objective is to streamline educators' workflow by reducing the time spent on creating materials and assessments for students. Currently, educators visit several platforms and require large amounts of manual effort to curate content for their classes. With Lotus Learning, we aim to make this a quick and easy process using AI.

This project focuses on the backend aspect by creating an API that utilizes a LLM to generate questions.

## Key Features
- Authorization: Users will be able to login to securly access the API.
- Database: Games and texts will be stored in the database for easy access.
- Text Extraction: Users will be able to extract text from word documents and pdfs to use with the LLM.
- Games: Users will be able to create games using the LLM. Some of these games will be created directly by the LLM and some will pricess data from the LLM to create other games. Games include: Crossword, Wordsearch, Fill In The Blanks, Multiple Choice Questions and Short Answers.


## User stories

- **"As a high school teacher, I want to make learning fun by generating questions in the form of games to engage my students better and so that I can prepare lecture materials quickly."**
- **"As a parent, I want my children to learn in a fun way so that they enjoy the learning process and develop a lifelong love for learning."**
- **"As a school principal, I want my teachers to incorporate fun games to help students excel and remember the course content better."**

Our API is designed to effectively address all goals in our user stories. For high school teachers, it provides a tool to easily create engaging games, making learning more enjoyable for students and simplifying the preparation of lecture materials. Parents benefit from the interactive learning environment, encouraging a fun learning environment for their children. School principals appreciate the range of game types available, empowering teachers to boost student performance and improve content retention through diverse and enjoyable educational experiences.

## Architecture

### Technology Stack

![Architecture](https://github.com/csc301-2023-fall/project-33-project-human-city-t/assets/60537067/42360adb-e157-493e-a7da-a98f12dc35d0)

You can find the architecture diagram [here](https://lucid.app/lucidchart/794e3572-2c79-4b85-ac56-a98fe630b56d/edit?invitationId=inv_bfde18e8-c2e5-4e81-be93-d251f18863b4).

This application is deployed on the Google Cloud platform, utilizing the following technology stack:

1. **Backend (Flask)** - Responsible for handling core logic and functionality, facilitating communication between components and external services.
2. **Database (MongoDB)** - Stores and manages data essential for the application's operation, utilized for persistently storing games created by the LLM.
3. **Language Model (Vertex AI for LLM)** - Employs Vertex AI services for natural language processing and understanding, managing interactions for game creation using provided content.

### Functionality Description

- LLM APIs: Responsible for coordinating interactions with the Language Model to create games using supplied content.
- Game API: Primarily dedicated to storing games in the database generated by the LLM, ensuring seamless integration for efficient storage and retrieval.
- Database API: Retrieves content and games stored in the database, designed to provide data for the frontend and other APIs as required.
- Authentication Feature: The application incorporates a robust authentication mechanism based on token systems, ensuring secure and authorized access for users interacting with the application.


## Configuration Files

The following configuration files are used in the application:

**Language Model (LLM)**
- Credentials: `api/models/llm/credentials.json`
- Configuration: `api/models/llm/configuration.py`

**Database**
- MongoDB URI: `api/database/mongodb_uri`


## Accessing Application:

**Base URL**: in slack chat

**Documentation URL**: in slack chat

**Test Key**: in slack chat


## Instructions
### Using it through Swagger
- Visit the Documentation URL: 
- Click on the Authorize button on the top right
- Enter the Test Key (``) and click Authorize and Close
    - You can also use a token generated by the `/api/auth/gettoken` endpoint by following the instructions below and using the example login credentials (Username: `test`, Password: `test`).
- Click on the endpoint you want to test
- Click on the Try it out button
- Enter the required parameters or leave them to use the default parameters
- Click Execute
- The response will be displayed below

### Using it through API calls
- Send a POST request to /api/auth/gettoken with a body of your username and password (Example login credentials: Username: `test`, Password: `test`)
```json
{
  "password": "test",
  "username": "test"
}
```
- Using the token that was returned by the last POST request we can create a header file to authorize us for all future calls
```json
{
  "token": "1234567"
}
```
- For all future API calls, send POST requests to the appropriate URL as shown in the documentation, with the header file and the appropriate body as shown in the documentation

## Local Setup and Local testing

### Installation
- [Install Python 3](https://www.python.org/downloads/) (Tested on Python 3.10.9)
- Clone the repo using git on the terminal - `git clone https://github.com/csc301-2023-fall/project-33-project-human-city-t.git`
    - If you don’t have git,
        - [Download the files](https://github.com/csc301-2023-fall/project-33-project-human-city-t/archive/refs/heads/main.zip)
        - Extract them using a zip extractor
        - Open terminal and change directory to the folder they were extracted to
        - Change directory to the repo `cd deliverable-2-33-2-jaindee4-nandwan8`
- Install dependencies using `python -m pip install -r requirements.txt`

### Testing
- Run tests using `python -m pytest`

### Usage Instructions
- Run using `python -m api.index`.
- This launches the API locally and note the local address that is given (Usually http://127.0.0.1:80).
- Now you can test the API through the swagger that is generated at http://127.0.0.1:80/apidocs/
    - Replace http://127.0.0.1:80 with your local address
    - Instructions above
- Or you can use your API through local API calls to http://127.0.0.1:80/ (note this is not deployed on the internet and can only be accessed by your system)
    - Replace http://127.0.0.1:80 with your local address
    - Instructions above

## Demo
You can find a recorded demo of our project [here](https://www.youtube.com/watch?v=2QgT8U4H8d0).

## Deployment and Github Workflow
In the course of our development, we have successfully prioritized a streamlined deployment and GitHub workflow, ensuring efficiency and reliability. GitHub's robust features have been instrumental in our approach, where we effectively utilize issues to track and manage tasks, fostering transparency and organization within our development process. The implementation of branches and pull requests has significantly enhanced collaboration, providing a structured environment for code review and discussion, leading to a seamless integration of new features.

Furthermore, GitHub Actions has played a pivotal role in our workflow, automating testing procedures to ensure the reliability and stability of our codebase. The use of automated deployment processes orchestrated by GitHub Actions has contributed to maintaining a consistent and error-resistant release cycle. This integrated approach, covering issues, pull requests, branches, and GitHub Actions, has not only accelerated our development speed but also upheld a high standard of code quality, resulting in more efficient and reliable software delivery. Our commitment to refining and optimizing this workflow remains steadfast, ensuring continuous improvement in our development practices.

### Auto-Deployment Setup

To setup the auto-deployment on forks, a few environment variables need to be set up in the GitHub repository to allow the GitHub workflow to deploy the application to the virtual machine. The following environment variables need to be set up:
- `REMOTE_HOST`: The IP address of the VM.
- `REMOTE_PORT`: The port number of the VM.
- `REMOTE_USER`: The username of the VM.
- `SSH_PRIVATE_KEY`: The private key of the VM.

### Further Testing

Our workflow is set up to run tests using the pytest framework automatically whenever there's an update to the code as mentioned previously. If you would like to add more test cases, they can be added to the `tests` folder following the pytest framework. You can either create a new file or edit existing ones to include new test scenarios. We've already have test cases for the Language Model (LLM), authentication, database, and games API. The GitHub script is configured to facilitate automatic deployment and testing and mandates no further modifications.

## Coding Standards and Guidelines
In our development workflow, we will continue to prioritize the implementation and adherence to rigorous coding standards and guidelines. These standards serve as a foundational framework, promoting consistency, readability, and maintainability throughout our codebase. By establishing best practices and conventions, we will ensure not only the functionality of our software but also streamline the code review process, facilitating efficient collaboration among team members. This ongoing commitment to coding standards will enhance the overall quality of our code, fostering a shared understanding that enables seamless collaboration, maintenance, and scalability of our project.
​
## Licenses
This software operates on a closed-source (proprietary) model, a strategic decision initiated by the company's founder to prevent its utilization by competitors. While this approach offers advantages such as safeguarding intellectual property, it introduces challenges such as limited 3rd party integrations and reliance on the owner for maintenance. Additionally, the closed-source nature restricts public contributions to the source code, which, although ensuring control, eliminates the collaborative potential that open-source development often provides for accelerated innovation.

## Additional Documentation
You can find additional documentation here:
- Swagger documentation for APIs endpoints [here](http://34.130.158.81/apidocs/).
- Database documentation for collections [here](https://docs.google.com/document/d/11Y-4c06jkkvkbvdH-SN80MEQgBQIvSuUN_u_r_sv79I/edit?usp=sharing).