# 33 - Team Paddle

## Iteration XX - Review & Retrospect

- When: 16th November 2023
- Where: Online via Zoom

## Process - Reflection

#### Q1. What worked well

Automated Testing: This allowed us to ensure that our code is robust and reliable throughout the development process. By automating test cases for critical functionalities, we could quickly identify and rectify issues, reducing the likelihood of introducing bugs into the codebase. We did this by leveraging Github Actions. 

Auto-Deployment: Implementing an automated deployment process played a pivotal role in ensuring the seamless and consistent release of our software. By automating the deployment pipeline, we minimized the risk of human error associated with manual deployments. We did this by leveraging Github Actions, Tmux and SSH.


#### Q2. What did not work well

Not using version control (git): At the start, we did not use git effectively. This meant that there were errors in the deployed version of our code but by the end of this deliverable, we were able to use git effectively to ensure that did not happen through communication, automated testing and deployments. 

Inconsistent Communication with Partner: Our communication with our partner was sporadic, leading to delays in project progress. The lack of structured communication hindered the exchange of crucial information, making it difficult to align strategies and address issues promptly. This led to delays in receiving necessary components such as API keys for the llm and access to Google Cloud.

#### Q3(a). Planned changes

We plan to continue using and improving the way we utilize git to our advantage. This includes using issues, pull requests and branches to make sure that code is tested and peer-reviewed before it is merged into the main branch and automatically deployed.\
We will also work with our partner to ensure better communication by providing regular updates.

#### Q3(b). Integration & Next steps

We started by merging the repo of the subteam that worked on the main framework first. Then we started merging parts from the other subteams (llm and database) by replacing the mock code that was used to simulate the llm and database with the code from the subteam’s repos. This initially presented challenges since the subteams had different function names and processes but we were able to standardize the function names and reconcile the processes through collaborative discussions and documentation.

## Product - Review

#### Q4. How was your product demo?

We prepared for our demo by discussing the critical feature addressing anticipated points of interest for our partner. We conducted internal rehearsals to ensure a polished and engaging presentation. 
Our demo of the API was done using the Swagger file. We demonstrated all endpoints and how they worked with each other including the authentication, llm, games, and database.

Our partner was pleased with our progress and suggested minor changes such as adding a new llm module to generate text summaries.
We learned the significance of effectively communicating the features of out software. This included creating a swagger file.
This process highlighted the importance of rigorous code testing to ensure seamless code integration between teams. Additionally, it highlighted the importance of client feedback and adaptability to build a product more suited to their needs.
