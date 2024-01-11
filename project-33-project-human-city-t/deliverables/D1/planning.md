# Lotus Learning


## Product Details
 
#### Q1: What is the product?

Our product, Lotus Learning, is an educational platform that leverages AI to assist educators in enhancing their study materials. It offers a range of features, including educational games, test evaluation tools and paper critiquing. Our primary objective is to streamline educators' workflow by reducing the time spent on creating materials and assessments for students.

This project is in collaboration with [Project: Human City](https://projecthumancity.com/), a non-profit organization dedicated to creating solutions to tackle human inequality, remediate social injustice and bridge the lack of access to human needs globally.

In this project, we will be developing an API that will generate questions based on learning materials passed in. When an educator invokes creation of learning materials, information such as learning materials and type of resource requested (e.g. multiple choice questions, true or false questions, fill in the blank, etc) will be passed into the API. Additionally, we will use other APIs for large language models. For instance: OpenAI API’s to invoke GPT based on the resource requested. The resources generated will then be stored and displayed accordingly.

If we finish the learning engine early, we are open to pivoting our efforts to help other teams work on their database implementation and front end development.

Our partner provided us with a mockup in [Figma](https://www.figma.com/file/HePmhvMmf52GxeakdrDHF4/Mockups). Link also in mockup.txt.


#### Q2: Who are your target users?

Our target users include a diverse range of educators and students across various academic levels from primary school to university. The learning platform supports users of all levels to generate questions of varying difficulties for students. Educators can also utilize the platform to create review materials, tailor course content to their students and prepare various activities for their students.Students will be able to use this platform to engage in quizzes, games and review materials as part of their coursework or for review purposes. Currently, Lotus Learning is still under development and is only available to limited educators and students for testing.
In later development phases, this Lotus Learning will be available to a larger market so educators outside Project: Human City can also use it.

 
#### Q3: Why would your users choose your product? What are they using today to solve their problem/need?

If an educator wants to create materials, they would have to resort to manually copying and pasting text into their choice of LLM which in return would generate plain text. Then, they will have to convert plain text into appropriate games. Lotus learning streamlines this process of delivering interactive games that can be easily integrated into courses by using appropriate machine learning models and invoking them automatically.

Today, students use their choice of LLM to get new ideas, give suggestions on their assignments, enhance their writing and understand concepts better. With Lotus Learning, we would like to further enhance this experience by training students to think independently. We aim to do this by prompting LLM to create papers based on a particular content and the student will be asked to critique it. Additionally, students will still be able to use LLM to better understand concepts.


#### Q4: What are the user stories that make up the Minumum Viable Product (MVP)?

- As a highschool teacher, I want to make learning fun by generating questions in the form of games in order to engage my students better and so that I can prepare lecture materials quickly.
- As a university professor, I would like to track my students' progress in learning new concepts in order to know what I need to focus on during lectures.
- As a highschool student who struggles to learn new definitions, I want to be able to use the application to help me pick and learn definitions in an interesting way.
- As a parent, I want my children to learn in a fun way so that they enjoy the learning process and develop a lifelong love for learning.
- As a school principal, I want my teachers to incorporate fun games in order to help students excel and remember the course content better.
- As a university professor, I would like my students to develop independent thinking so that students excel in their workplace.

Proof of Approval:
<img width="1178" alt="Screenshot 2023-09-29 at 15 27 48" src="https://github.com/csc301-2023-fall/project-33-project-human-city-t/assets/60537067/fa841d8e-a722-4bbb-94e1-42dc93d7c372">


#### Q5: Have you decided on how you will build it? Share what you know now or tell us the options you are considering.

There is previous code on the learning engine built by Project: Human City’s team, but upon discussion with the team and the interns at P:HC, we have decided to start from scratch in-order to migrate the large language model that is used. We will be investigating Llama and OpenAI outputs to find the best LLM to use for Lotus Learning. Then, we will use their APIs accordingly along with prompt engineering to produce games for each course. This will be built using Python, using flask to accept requests, and python requests to interact with the chosen LLM.. The API we build will then be deployed through google cloud. 

Our architetcural diagram can be found [here](https://www.figma.com/file/NdCB5KSFm82lX4yJ3kKVhX/D1?type=design&node-id=0%3A1&mode=design&t=zVn3QfqtcHseZkgV-1). Link also in mockup.txt.



## Intellectual Property Confidentiality Agreement 
### Briefly describe which option you have agreed to.

We have agreed to option 5 (You will only reference the work you did in your resume, interviews, etc. You agree to not share the code or software in any capacity with anyone unless your partner has agreed to it.). The partner is also willing to make the source code publicly available one year after the project's completion. The rationale stems from the high demand for AI learning right now. As a non-profit organization, they will not be able to make frequent updates and want to be  cautious about the possibility of competitors reusing their code before they can grow as a company.



## Teamwork Details

#### Q6: Have you met with your team?

Yes, we met via Zoom and gathered in a group study room in the Engineering and Computer Science library at Sanford Fleming. We spent some time getting to know each other and connecting our laptops to HDMI.  Subsequently, worked on deliverable 1, and came up with questions to ask our partner in our next meeting. Later, we went out to grab bubble tea and chatted to get to know one another better.

**Fun Facts**
- Tanya and Khushaal hate cheesecakes
- Nathan hates drinking boiled water because it tastes funky
- Ashvat loves playing tennis


![IMG_3537](https://github.com/csc301-2023-fall/project-33-project-human-city-t/assets/60537067/109ed5dc-b0da-414a-9e0a-1ecfb79371e3)


#### Q7: What are the roles & responsibilities on the team?

- LLM Implementation Team: Nathan, Ashvat, Deep
  - Responsibilities:
    - Investigate Llama 2 and ChatGPT
    - Learn how to properly write prompts to get the expected output with chosen LLM
    - Learn and implement usage of the third party LLM  API using Python
    - Code the interactions with the LLM API
      
- Deployment Team: Tanya, Deep, Ashvat
  - Responsibilities:
    - Figure out the best way to deploy our API
    - Deploy the API

- Security Team: Deep, Khushaal
  - Responsibilities:
    - Ensure that our API is secure (OAuth, etc.)
    - Ensure that API keys are hidden

- Game Design: Tanya, Khushaal, Nathan
  - Responsibilities:
    - Design LLM responses into actual games
    - Find alternative machine learning models to design games

- Database Team:  TBD (There is another team working on database implementation, we will need to discuss in what aspect can we contribute to it)
  - Responsibilities:
    - Read/write games to MongoDB
    - Implement the module which will fetch, send data to the the database

- Communication with Partner: Tanya

##### Why we chose our roles?
- Tanya has some experience deploying on cloud, specifically AWS and OCP. She would like to expand her skills to be able to deploy software on other cloud platforms. Additionally, she has work with OpenAI before hence wants to explore other models that could potentially produce better outputs.
- Deep has some experience deploying projects and OAuth. He is interested in testing and implementing different LLMs.
- Ashvat chose the LLM implementation since he wants to learn about that topic in depth. He wants to work in the deployment sub team to test skills obtained via prior projects and build on them.
- Nathan has experience working with Machine Learning and is very interested in learning prompt engineering to ensure that the outputs from the LLM's are accurate to our specifications.
- Khushaal is interested in Machine Learning, so finding the right ML model for designing the game is something he looks forward to. He has experience in Authentication from his past projects, so he will also be contributing in the Security Team.


#### Q8: How will you work as a team?

Our team has decided upon a fixed weekly meeting every Saturday at 1 pm, conducted either online or in a library study room. These meetings are crucial for sharing progress updates, addressing questions, discussing roadblocks, aligning on next steps, providing updates on the past week's work, and conducting code reviews. In addition to our meetings, we utilize a GitHub repository to organize our code effectively, which not only simplifies our combined efforts but also ensures transparency and ease of access for our partner. This structured approach to communication and code management facilitates smoother interactions within our team and with our external partner, ensuring we stay on track and maintain a high standard of work.

In addition to our weekly team meetings, we will also have weekly project meetings with the partner, a general operations meeting with the organization. Our weekly meetings will be on Thursdays from 12-1pm. The timings of the other meetings are yet to be decided.


  
#### Q9: How will you organize your team?

To efficiently organize our team, we will use a combination of tools to manage and assign tasks, track progress. These tools include:
- **Task Lists**: We will maintain detailed task lists using project management software such as Jira. Each task will be categorized, assigned a priority level, and provided with clear descriptions and deadlines.
- **Task Boards**: Task boards in Jira will help us visualize the flow of work, with columns like "To-Do," "In Progress," "Testing," and "Completed" to monitor task status.
- **Schedules & Deadlines**: We will create project schedules and timelines using tools like Outlook Calendar or online project management platforms. This will help us allocate time effectively. Jira will also be configured to send notifications for task updates.
- **Meeting Minutes**: For every team meeting, we will document meeting minutes that capture discussions, decisions, and action items. These will be shared with team members and stakeholders.
- **Status Reports**: Regular status reports will summarize project progress, highlighting completed tasks, pending work, and any issues or risks.
- **Priority Framework**: We will establish a clear framework for prioritizing tasks based on the effort a task takes and the value it will return. This will ensure that we don’t work on a task that requires high effort but produces low reward.
- **Task Assignment**: Tasks will be assigned in Jira, considering team members' skills and availability.


#### Q10: What are the rules regarding how your team works?

Our team has weekly meetings, both in-person and on Zoom, and uses Discord for regular text updates. For communication with external partners, we use Slack and Zoom, with a designated group representative managing these communications. We adhere to strict deadlines to ensure on time submissions. Deadline reminders are sent out, and if a member falls behind, they receive friendly warnings to keep them on track. Since we all live near campus and share some classes, reaching out in person for urgent matters is also convenient.

In handling a situation where a team member isn't contributing adequately or being responsive, initially, we'd respectfully remind them of the course requirements and the project goals set during our initial ideation phase. The goal is to realign them with the team's objectives and the standards we aim to uphold. Following the reminder, we'd provide constructive feedback, highlighting specific areas where their work may not be meeting the necessary standards. This dialogue aims to help them understand the aspects that need improvement, offering a pathway to enhance their contribution towards the collective team effort.
