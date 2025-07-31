import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


class ReviewConversation:
    def __init__(self) -> None:
        load_dotenv()
        groq_api_key = os.getenv("groq_api_key")
        self.llm = ChatGroq(
            temperature=0.5,
            groq_api_key=groq_api_key,
            model_name="llama3-8b-8192"
        )

        prompt_template = """
        You are a conversation reviewer. Your job is to analyze the following conversation and generate structured feedback.

        Instructions:
        1. Identify **all unique speakers**.
        2. For each speaker:
        - Summarize their intent.
        - Analyze and assign a final sentiment: **Positive**, **Negative**, or **Neutral**.
        3. Provide the **overall sentiment** of the conversation: Positive / Negative / Neutral.
        4. Determine the **main topic** or intent of the entire conversation.
        5. Give a short, constructive **review** of the conversation quality and dynamics.

        Format the output as:

        Intent of Discussion:
        - Topic: <Detected Topic>
        - Overall Intent: <Main Intent>
        - Overall Sentiment: <Positive | Negative | Neutral>

        Speaker-wise Analysis:
        - <Speaker Name>:
        - Intent: <...>
        - Sentiment: <Positive | Negative | Neutral>
        - ...

        Review Summary:
        <Short review paragraph>

        Conversation:
        {conversation}
        """
        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=['conversation']
        )

        self.output_chain = self.prompt | self.llm | StrOutputParser()

    def output(self, conversation):
        search_output = self.output_chain.invoke({'conversation': conversation})
        return search_output
