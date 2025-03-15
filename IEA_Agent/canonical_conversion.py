
from langchain_core.prompts import ChatPromptTemplate
from IEA_Agent.LLMManger import LLMManager
from IEA_Agent.parsers import parser
import re

prompt_thought = '''You are an advanced AI assistant specialized in semiconductor test data analysis.
Your will be asked to analyze and interpret a given **user query** in the specific context represented by the **prior user queries**. 
Your task has two parts:
1. Identify **missing information** in the given **user query**
2. Convert the **user query** into a **complete user query** by filling all the **missing information**. 

Please output the following three things:

1. **user query**: Copy of the given user query.
2. **complete user query**: The user query after you filling in all the missing information. 
3. **thoughts**: Your reasoning behind the conversion process. '''

class CanonicalConversion:
    def __init__(self):
        self.llm_manager = LLMManager()
 
    async def run(self, state: dict) -> dict:
        question = state['messages'][-1].content

        previous_questions = [q.content for q in state["messages"][:-1][-10:]]
        formatted_previous_questions = "\n".join(f"{i+1}. {q}" for i, q in enumerate(previous_questions))
        with open('conversation_examples.txt', 'r') as file:
            examples = file.read()

        prompt = ChatPromptTemplate.from_messages([
            ("system", '''{system_message}
             
{examples}
'''),
            ("human", """user query: {question}
prior user queries: {formatted_previous_questions}
Output:""")
        ])
        response = await self.llm_manager.invoke(prompt, system_message = prompt_thought, question = question, formatted_previous_questions = formatted_previous_questions, examples = examples) 
        
        return parser(response.content)
