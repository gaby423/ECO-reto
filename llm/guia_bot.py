import yaml
import time
from dotenv import load_dotenv
from groq import (
    Groq,
)

load_dotenv()


class LLamager:

    def __init__(self, prompt: str, especie: str) -> None:
        self.model = 'llama3-70b-8192'
        self.temperature = 0.5
        self.max_tokens = 1024
        self.stop = None
        self.stream = False
        self.client = Groq()
        self.especie = especie
        self.messages = self.get_system_prompt(prompt)

    @staticmethod
    def read_yaml_file():
        file_path = '/Users/gabrielamarquez/Desktop/eco-project/config.yaml'
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")
            return None

    def get_system_prompt(self, role: str):
        prompt = self.read_yaml_file()[role].format(especie=self.especie)
        return [{"role": "system", "content": prompt}]

    def conversation_handler(self, text: str, role: str):
        messages = {"role": role, "content": text}

        match role:
            case "user":
                self.messages.append(messages)
                if len(self.messages) > 6:
                    self.messages.pop(1)
                    self.messages.pop(2)
            case "assistant":
                self.messages.append(messages)
            case _:
                raise ValueError("Invalid role")

    def process(self, text: str, role: str):
        self.conversation_handler(text, role)

        start_time = time.time()
        completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=self.stream,
        )

        chat_completion = completion.choices[0].message.content
        end_time = time.time()
        elapsed_time = int((end_time - start_time) * 1000)
        print(f"LLM ({elapsed_time}ms): {chat_completion}")
        self.conversation_handler(chat_completion, 'assistant')

        return chat_completion


if __name__ == '__main__':
    question = "presntate y hablame un poco de esta especie que encontre"

    llm = LLamager('ecoreto_prompt', "Carpintero Pechiamarillo")
    llm_response = llm.process(question, "user")
