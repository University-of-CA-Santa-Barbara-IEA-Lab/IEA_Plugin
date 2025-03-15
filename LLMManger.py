from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from langchain_core.exceptions import OutputParserException

class LLMManager:
    def __init__(self):
        self.llm = ChatOpenAI(model="o3-mini", temperature=1)

    async def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> AIMessage:
        """
        This method invokes the language model with the given prompt and additional keyword arguments.

        Args:
            prompt (ChatPromptTemplate): The prompt template to format messages.
            **kwargs: Additional keyword arguments to format the prompt.

        Returns:
            AIMessage: The response from the language model.
        """
        try:
            messages = prompt.format_messages(**kwargs)
            response = await self.llm.ainvoke(messages)
            return response
        except OutputParserException as e:
            print(f"Output parsing failed: {e}")
            return AIMessage(content="Error: Unable to parse the model response.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return AIMessage(content="An error occurred while processing your request.")