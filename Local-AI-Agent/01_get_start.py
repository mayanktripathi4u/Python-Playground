from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = """
You are an expert in answering questions about a pizza resturants.

Here are some relevant reviews: {reviews}

Here is the question to answer: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model

result = chain.invoke(
    {
        "reviews": "The pizza was great! The crust was crispy and the toppings were fresh.",
        "question": "What did the customer think about the pizza?"
    }
)
# This code uses the LangChain library to create a simple question-answering chain.

print(result)
