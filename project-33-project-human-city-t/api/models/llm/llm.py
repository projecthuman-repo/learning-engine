import json
import vertexai
from vertexai.language_models import TextGenerationModel
from . import configuration


class Model:
    """
    Class that handles the model and the generation of questions.
    """

    def __init__(self, project, location, credentials, candidateCount=1, maxOutputTokens=1024, temperature=0.1, topP=0.8, topK=40, model="text-bison"):
        """
        Authenticates the user, initializes the model and sets the model parameters.
        """
        vertexai.init(project=project, location=location,
                      credentials=credentials)
        self.parameters = {
            "candidate_count": candidateCount,
            "max_output_tokens": maxOutputTokens,
            "temperature": temperature,
            "top_p": topP,
            "top_k": topK
        }
        self.model = TextGenerationModel.from_pretrained(model)

        self.mcqContext = "You are a teacher who wants to create multiple-choice questions based on readings given to the students."
        self.mcqExample = "{\"Question\": \"What colour is fire?\", \"Answer\": \"A\", \"A\": \"Red\", \"B\": \"Green\", \"C\": \"Brown\", \"D\": \"Yellow\"}"

        self.shortQContext = "You are a teacher who wants to create short questions based on readings given to the students."
        self.shortQExample = "{\"Question\": \"What colour is fire?\", \"Answer\": \"Red\"}"

        self.wordDefinitionContext = "You are a teacher who wants to provide definitions for the important words in a given text."
        self.wordDefinitionExample = "{\"Word\": \"Capital\", \"Definition\": \"The city or municipality where a country's central government is located and where official governmental activities take place.\"}"

        self.fillInTheBlanksContext = "You are a teacher who wants to create fill in the blank questions based on the given text"
        self.fillInTheBlanksExample = "{\"Question\": \"It is a sunny __.\", \"Answer\": \"day\"}"

    def __createPrompt(self, qType, num, text):
        """
        Given the question type this function returns the prompt for the model to generate questions
        """
        if qType == 1:
            return f"""{self.mcqContext}
        
Using the following information and nothing else, generate {num} Multiple Choice questions based on the information above and return them in JSON format.
Exactly follow the JSON format of the example question below. Each question should be separated by "&&" and nothing else.
{self.mcqExample}

\"{text}\"
"""
        elif qType == 2:
            return f"""{self.shortQContext}
        
Using the following information and nothing else, generate {num} short answer questions based on the information above and return them in JSON format. The answer to each question should be a max of 4 words long.
Exactly follow the JSON format of the example question below. Each question should be separated by "&&" and nothing else.
{self.shortQExample}

\"{text}\"
"""
        elif qType == 3:
            return f"""{self.wordDefinitionContext}

Select the {num} most significant words from this text (and nowhere else) and give their definitions.
Exactly follow the JSON format of the example question below. Each word and definition should be separated by "&&" and nothing else.
        
{self.wordDefinitionExample}

\"{text}\"
"""

        elif qType == 4:
            return f"""{self.fillInTheBlanksContext}
Generate exactly {num} fill in the blanks questions. Each blank must only have one answer, dont give multiple posible answers for a blank
The questions must only be related to the given text and nothing else.
Generate questions based on the text with missing words (blanks). Then, provide the missing word(s) as answers. 
Exactly follow the JSON format of the example question below. Each question should be separated by "&&" and nothing else.

{self.fillInTheBlanksExample}

\"{text}\"
"""

    def __parseResponse(self, response, choice):
        """This function parses the response from the model and returns a list of JSONs.
        """
        split_response = response.text.split("&&")

        parsed_responses = []
        for item in split_response:
            item = item.strip()
            if not item:
                continue
            # Attempt to parse JSON
            try:
                parsed_item = json.loads(item)
                parsed_responses.append(parsed_item)
            except json.JSONDecodeError:
                # Try to handle non-JSON formatted strings
                try:
                    if choice == 3:  # Only need to check for word definition pair since the output is slightly different.
                        parsed_item = {}
                        questionPart, answerPart = item.split("Definition:")
                        parsed_item["Word"] = questionPart.split("Word:")[
                            1].strip()
                        parsed_item["Definition"] = answerPart.strip()
                        # Convert parsed_item to a JSON string and append it.
                        parsed_responses.append(
                            json.loads(json.dumps(parsed_item)))
                    elif choice == 1:  # handling mcq's
                        parsed_item = {}
                        questionPart, rest_of_data = item.split("\"Answer\":")
                        question = questionPart.split("\"Question\":")[
                            1].strip(" ,\"")
                        parsed_item["Question"] = question
                        answerChoice = rest_of_data.split(",")[0].strip(" \"")
                        parsed_item["Answer"] = answerChoice
                        for choice_char in ["A", "B", "C", "D"]:
                            start_idx = item.find(f"\"{choice_char}\":")
                            if start_idx == -1:  # This choice might not be present
                                continue
                            start_idx += len(f"\"{choice_char}\":")
                            end_idx = item.find(",", start_idx)
                            if end_idx == -1:
                                end_idx = item.find("}", start_idx)
                            choice_text = item[start_idx:end_idx].strip(" \"")
                            parsed_item[choice_char] = choice_text
                        parsed_responses.append(
                            json.loads(json.dumps(parsed_item)))
                    else:
                        parsed_item = {}
                        questionPart, answerPart = item.split("Answer:")
                        parsed_item["Question"] = questionPart.split("Question:")[
                            1].strip()
                        parsed_item["Answer"] = answerPart.strip()
                        parsed_responses.append(
                            json.loads(json.dumps(parsed_item)))
                except Exception as e:
                    print(f"Error processing item: {e}")
                    print(f"Faulty item: {item}")

        return parsed_responses

    def mcq(self, num, text):
        """Calls the model to generate multiple choice questions."""
        response = self.model.predict(
            self.__createPrompt(1, num, text),
            **self.parameters
        )
        return self.__parseResponse(response, 1)

    def shortAnswer(self, num, text):
        """Calls the model to generate short answer questions."""
        response = self.model.predict(
            self.__createPrompt(2, num, text),
            **self.parameters
        )
        return self.__parseResponse(response, 2)

    def wordDefinition(self, num, text):
        """Calls the model to generate word definition pairs."""
        response = self.model.predict(
            self.__createPrompt(3, num, text),
            **self.parameters
        )
        return self.__parseResponse(response, 3)

    def fillInTheBlanks(self, num, text):
        """Calls the model to generate fill in the blanks questions."""
        response = self.model.predict(
            self.__createPrompt(4, num, text),
            **self.parameters
        )
        return self.__parseResponse(response, 4)


def getModel():
    return Model(configuration.PROJECT, configuration.LOCATION, configuration.CREDENTIALS)

if __name__ == "__main__":
    model = Model(configuration.PROJECT, configuration.LOCATION, configuration.CREDENTIALS)
    text = "The Tinder Fire was a wildfire that burned 16,309 acres (66.00 km2) of the Coconino National Forest in the U.S. state of Arizona during April and May 2018. The 2017 Arizona wildfires had been followed by drought, including a historically dry winter season. The Tinder Fire was detected from a lookout tower of the U.S. Forest Service on April 27, and firefighters began working to contain its spread within the day. Stoked by strong winds, low humidity, and high temperatures, the fire grew rapidly over late April, prompting the closure of Arizona State Route 87 and evacuation orders for 1,000 houses in Coconino County. These orders remained until May 4. Almost 700 firefighters were involved in combating the fire, which was fully contained on May 24. It destroyed 96 buildings, including 33 homes, and cost $7,500,000 to contain and suppress. An investigation determined that the Tinder Fire was caused by an illegal campfire."
    print(model.mcq(1, text))
    print(model.shortAnswer(1, text))
    print(model.wordDefinition(1, text))
    print(model.fillInTheBlanks(1, text))
