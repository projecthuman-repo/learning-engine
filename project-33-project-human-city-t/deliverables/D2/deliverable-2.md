# Deliverable 2: Project Report

## Summary of Software

This project is in collaboration with [Project: Human City](https://projecthumancity.com/), a non-profit organization dedicated to creating solutions to tackle human inequality, remediate social injustice and bridge the lack of access to human needs globally. Their product, Lotus Learning, is an educational platform that leverages AI to assist educators in enhancing their study materials. It offers a range of features, including educational games, test evaluation tools and paper critiquing. Our primary objective is to streamline educators' workflow by reducing the time spent on creating materials and assessments for students.

In this project, we will be developing an API that will generate questions based on learning materials passed in. When an educator invokes the creation of learning materials, information such as learning materials and type of resource requested (e.g. multiple choice questions, short answer, fill in the blank, etc) will be passed into the API. The API will then select the correct prompt to use, and send the prompt as well as the text to our LLM, PaLM 2. The response from PaLM 2 will then be parsed and returned to the caller of the API. 

Our partner did have existing software, but after meeting with our partner, we decided that we wanted to switch LLMs and remake their API from scratch because there were issues with their original implementation. Also, our partner provided us with a mockup in [Figma](https://www.figma.com/file/HePmhvMmf52GxeakdrDHF4/Mockups). Link also in mockup.txt.

## Project Division

After a thoughtful consideration of the project's complexity and the distinct expertise required in each area, we decided to split the project into three specific teams—LLM implementation, Deployment and Security, and Database gateway. This specific division allows for a focused approach, enabling each team to delve deeply into their area of expertise. By isolating these specialized tasks, the project benefits from the expertise of team members who can thoroughly explore their designated domains, leading to a comprehensive and well-integrated final product.

The LLM implementation team is tasked with the intricate challenge of generating questions from learning materials. This task demands expertise in natural language processing, deep learning, and understanding the nuances of different language models. By dedicating a team solely to this aspect, the project ensures a deep exploration of available models and the development of tailored prompts for generating high-quality educational content.

The Deployment and Security team focuses on the critical aspects of making the API functional, secure, and user-friendly. Deploying an API involves considering scalability, reliability, and integration capabilities, while ensuring security is vital to protect user data and maintain the integrity of the system. By having a dedicated team handle deployment strategies and authentication mechanisms, the project guarantees a robust, stable, and secure API that can seamlessly integrate into various educational platforms.

The Database gateway team is responsible for the storage and retrieval of generated questions. Database management is crucial for efficiently storing data, enabling educators to access generated content, and tracking usage metrics. By dedicating a team to this function, the project ensures that data management is optimized, leading to a responsive system that performs well under different loads and allows for efficient organization and retrieval of educational content.

## Responsibility of Each SubTeam

#### LLM Sub-Team

We conducted extensive research to compare different language models, including Mistral 7b, Llama 2, GPT 3.5, and PaLM 2. We focused on evaluating costs and consistency of responses across these models. We studied prompt engineering techniques, to ensure precise formulation of queries to elicit relevant responses. We also learned the use of the VertexAI SDK, to smoothly interact with the PaLM 2 LLM. Additionally, we designed and implemented essential classes and methods, enabling effective communication with the LLM, response generation, and parsing responses into JSON formats. Rigorous testing procedures were then established to validate output formats and the accuracy of helper functions. 

#### Deployment and Security Sub-Team
We employed Flask in Python to establish API endpoints. We also implemented games like crossword and word search, as well as text extraction functionality from documents (pdf and docx). Additionally, we devised a token-based system to restrict API access to authorised users. Moreover, we integrated a documentation framework, Swagger, to facilitate easy access to and comprehension of the API and its endpoints. We also created testing procedures to ensure reliability.


#### Database Sub-Team

I designed a MongoDB schema for the storage of game-related content and materials. I used mongoengine in Python to employ the Object-Document Mapping (ODM) framework to streamline the schema's creation and management. Additionally, I developed APIs that enabled interactions with the database, facilitating the retrieval and addition of game content and game entries. The endpoints are documented with Swagger. Furthermore, I enhanced the system by introducing a color coding feature for course material that allows instructors to highlight content they want the LLM to focus on. Additionally, I created testing procedures to ensure the outputs of the APIs are correct. Lastly, I also keep came up with an outline of back up and restore strategies for the database.
