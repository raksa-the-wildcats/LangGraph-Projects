"""
Simple Conversational AI Agent with GPT-4o and LangGraph

This script creates a basic conversational AI chatbot using OpenAI’s GPT-4o model and LangGraph's state-based workflow system.

✨ What it does:

1. Environment Setup:
   - Loads environment variables using `dotenv` (e.g., your OpenAI API key).

2. Chat Model Initialization:
   - Uses `ChatOpenAI` with the `gpt-4o` model to power the AI's responses.

3. LangGraph Workflow:
   - Defines a simple LangGraph with one node called `process`:
     - The node sends the current conversation (all past messages) to the model.
     - The AI response is added to the conversation history.
     - The updated state is printed for debugging.

4. Interactive Chat Loop:
   - The user types a message.
   - The message is sent to the model along with the conversation history.
   - The model responds and the reply is printed.
   - The chat continues until the user types `exit`.

5. Conversation Logging:
   - Once the chat ends, the full conversation is saved to a file called `logging.txt`.
   - The log includes a transcript of all user and AI messages.

Ideal for:
   - Quick demos of GPT-4o in a state-based framework.
   - Users learning LangGraph and building simple stateful chat agents.
"""


import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model="gpt-4o")

def process(state: AgentState) -> AgentState:
    """ This node will solve the request you input """
    response = llm.invoke(state['messages'])

    state['messages'].append(AIMessage(content = response.content))
    print(f"\nAI: {response.content}")
    print("CURRENT STATE: ", state['messages'])

    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent = graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content = user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result['messages']
    user_input = input("Enter: ")

with open("loggin.txt", "w") as file:
    file.write("Your Convwersation Log: \n")

    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")
