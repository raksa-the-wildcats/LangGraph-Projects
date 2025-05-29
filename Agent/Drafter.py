"""
DRAFTER: AI-Powered Document Editing Assistant with LangGraph and GPT-4o

This script creates an intelligent writing assistant called **Drafter** that helps users interactively update and save text documents using natural language.

✨ What this system does:

1.*Environment Setup:
   - Loads environment variables (like your OpenAI API key) using `dotenv`.

2. Document Tools:
   - `update`: Replaces the current document with new content.
   - `save`: Saves the document to a `.txt` file on your local machine.

3. State Management:
   - Maintains the full message history (system, user, AI, and tool messages) using a typed agent state.

4. AI Agent with Tools:
   - Uses OpenAI’s `gpt-4o` model to interpret user commands.
   - The AI decides when to call tools (like `update` or `save`) based on your instructions.
   - It always shows the document’s current content after any change.

5. LangGraph Workflow:
   - Manages the flow of the interaction:
     - Starts with the agent.
     - Switches to tools if the AI wants to perform actions (e.g., update/save).
     - Ends the session if the document is saved.
     - Otherwise, loops back to continue editing.

6. Interactive Session:
   - Runs in a CLI (Command Line Interface).
   - Prompts users with questions like “What would you like to do with the document?”
   - Displays AI responses, tool results, and saved file confirmation.

Ideal for:
   - Quickly creating or editing documents using natural language.
   - Learning how to integrate LangChain tools with LangGraph and GPT.
   - Automating writing tasks with human-AI collaboration.

🛠 Example Usage:
   - User: "Add a summary to the beginning."
   - Drafter: Uses the `update` tool to apply changes.
   - User: "Save this as draft.txt"
   - Drafter: Uses the `save` tool and ends the session.
"""


from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv  
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

# This is the global variable to store document content
document_content = ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def update(content: str) -> str:
    """Updates the document with the provided content."""
    global document_content
    document_content = content
    return f"Document has been updated successfully! The current content is:\n{document_content}"


@tool
def save(filename: str) -> str:
    """Save the current document to a text file and finish the process.
    
    Args:
        filename: Name for the text file.
    """
    global document_content

    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"

    try:
        with open(filename, 'w') as file:
            file.write(document_content)
        print(f"\n💾 Document has been saved to: {filename}")
        return f"Document has been saved successfully to '{filename}'. Content saved:\n{document_content}"
    
    except Exception as e:
        return f"Error saving document: {str(e)}"
    

tools = [update, save]

model = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    global document_content
    
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    
    The current document content is: {document_content}
    """)

    # Check if this is the first run or if we have tool messages to process
    last_message = state["messages"][-1] if state["messages"] else None
    
    if not state["messages"] or isinstance(last_message, ToolMessage):
        if not state["messages"]:
            user_input = "I'm ready to help you update a document. What would you like to create?"
            user_message = HumanMessage(content=user_input)
            all_messages = [system_prompt, user_message]
        else:
            # Process tool results
            all_messages = [system_prompt] + list(state["messages"])
    else:
        # Get new user input
        user_input = input("\nWhat would you like to do with the document? ")
        print(f"\n👤 USER: {user_input}")
        user_message = HumanMessage(content=user_input)
        all_messages = [system_prompt] + list(state["messages"]) + [user_message]

    response = model.invoke(all_messages)

    print(f"\n🤖 AI: {response.content}")
    if hasattr(response, "tool_calls") and response.tool_calls:
        print(f"🔧 USING TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    # Add the new messages to state
    if not state["messages"] or isinstance(state["messages"][-1], ToolMessage):
        if not state["messages"]:
            return {"messages": [user_message, response]}
        else:
            return {"messages": list(state["messages"]) + [response]}
    else:
        user_input = input("\nWhat would you like to do with the document? ") if not isinstance(last_message, ToolMessage) else ""
        if user_input:
            user_message = HumanMessage(content=user_input)
            return {"messages": list(state["messages"]) + [user_message, response]}
        return {"messages": list(state["messages"]) + [response]}


def should_continue_agent(state: AgentState) -> str:
    """Determine if the agent should continue after generating a response."""
    messages = state["messages"]
    last_message = messages[-1] if messages else None
    
    # If the last message has tool calls, go to tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, continue with the agent
    return "continue"


def should_continue_tools(state: AgentState) -> str:
    """Determine if we should continue after tool execution."""
    messages = state["messages"]
    
    # Check if the last tool message was from a save operation
    for message in reversed(messages):
        if (isinstance(message, ToolMessage) and 
            "saved successfully" in message.content.lower()):
            return "end"
    
    # Continue to agent to process tool results
    return "agent"


def print_messages(messages):
    """Function to print the messages in a more readable format"""
    if not messages:
        return
    
    for message in messages[-3:]:
        if isinstance(message, ToolMessage):
            print(f"\n🛠️ TOOL RESULT: {message.content}")


graph = StateGraph(AgentState)

graph.add_node("agent", our_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")

# Add conditional edges from agent
graph.add_conditional_edges(
    "agent",
    should_continue_agent,
    {
        "tools": "tools",
        "continue": "agent",
    },
)

# Add conditional edges from tools
graph.add_conditional_edges(
    "tools",
    should_continue_tools,
    {
        "agent": "agent",
        "end": END,
    },
)

app = graph.compile()

def run_document_agent():
    print("\n ===== DRAFTER =====")
    
    state = {"messages": []}
    
    for step in app.stream(state, stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ===== DRAFTER FINISHED =====")

if __name__ == "__main__":
    run_document_agent()