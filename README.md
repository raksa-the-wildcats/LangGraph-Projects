## 🚀 Projects Overview

### 1. **Drafter** - AI-Powered Document Editor
**File:** `Drafter.py`

An intelligent writing assistant that helps users interactively create and edit documents using natural language commands.

**Features:**
- Interactive document creation and editing
- Natural language commands for content updates
- Automatic file saving with custom filenames
- Maintains document state throughout the session

**Usage:**
```bash
python Drafter.py
```

**Example Commands:**
- "Create a blog post about AI trends"
- "Add a conclusion paragraph"
- "Save this as 'ai-trends-blog.txt'"

---

### 2. **RAG Agent** - Document Q&A System
**File:** `RAG_Agent.py`

A Retrieval-Augmented Generation system that answers questions about PDF documents using vector search and LLM reasoning.

**Features:**
- PDF document processing and chunking
- Vector embeddings with ChromaDB
- Intelligent document retrieval
- Context-aware question answering

**Requirements:**
- Place `Stock_Market_Performance_2024.pdf` in the same directory
- ChromaDB will be created automatically

**Usage:**
```bash
python RAG_Agent.py
```

**Example Queries:**
- "What was Apple's stock performance in 2024?"
- "Which companies were part of the Magnificent 7?"
- "How did Tesla's earnings compare to its stock price?"

---

### 3. **Memory Agent** - Conversational Bot with Persistence
**File:** `Memory_Agent.py`

A conversational AI that maintains context throughout the session and saves conversation history.

**Features:**
- Persistent conversation memory
- Full conversation logging
- Context-aware responses
- Session transcript export

**Usage:**
```bash
python Memory_Agent.py
```

**Output:** Saves conversation to `logging.txt`

---

### 4. **ReAct Agent** - Reasoning and Acting
**File:** `React.py`

Implements the ReAct (Reasoning and Acting) pattern with mathematical tools, demonstrating how agents can think through problems step-by-step.

**Features:**
- Mathematical operations (add, subtract, multiply)
- Step-by-step reasoning
- Tool selection and execution
- Multi-step problem solving

**Usage:**
```bash
python React.py
```

**Example:** "Add 40 + 12 and then multiply the result by 6"

---

### 5. **Basic Agent Bot** - Simple Conversational AI
**File:** `Agent_Bot.py`

A minimal implementation showcasing the fundamentals of LangGraph for simple conversations.

**Features:**
- Basic conversation handling
- Simple state management
- Easy to understand and modify

**Usage:**
```bash
python Agent_Bot.py
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key

### Install Dependencies
```bash
pip install langchain-openai langgraph langchain-core python-dotenv
pip install langchain-community pypdf chromadb  # For RAG Agent
```

### Environment Setup
1. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_api_key_here
```

2. For RAG Agent, ensure you have the PDF file:
   - Download or place `Stock_Market_Performance_2024.pdf` in the project directory

### Quick Start
```bash
# Clone the repository
git clone https://github.com/raksa-the-wildcats/LangGraph-Projects.git
cd LangGraph-Projects

# Install dependencies
pip install -r requirements.txt

# Set up your OpenAI API key in .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run any agent
python Drafter.py
```

---

## 📁 Project Structure

```
LangGraph-Projects/
├── Drafter.py                          # Document editing assistant
├── RAG_Agent.py                        # PDF Q&A system
├── Memory_Agent.py                     # Conversational bot with memory
├── React.py                            # ReAct pattern implementation
├── Agent_Bot.py                        # Basic conversational agent
├── Stock_Market_Performance_2024.pdf   # Sample PDF for RAG agent
├── LinkedIn_Post_New_Job_At_Meta.txt   # Sample document
├── logging.txt                         # Generated conversation logs
├── .env                                # Environment variables (create this)
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

---

## 🔧 Key Technologies

- **[LangGraph](https://langchain-ai.github.io/langgraph/)** - State-based agent framework
- **[OpenAI GPT-4o](https://openai.com/)** - Large language model
- **[LangChain](https://langchain.com/)** - LLM application framework
- **[ChromaDB](https://www.trychroma.com/)** - Vector database for RAG
- **[PyPDF](https://pypdf.readthedocs.io/)** - PDF processing

---

## 🎯 Learning Objectives

Each agent demonstrates different concepts:

| Agent | Concepts Demonstrated |
|-------|----------------------|
| **Drafter** | Tool usage, state persistence, interactive workflows |
| **RAG Agent** | Vector search, document processing, retrieval-augmented generation |
| **Memory Agent** | Conversation memory, session management, logging |
| **ReAct Agent** | Reasoning patterns, multi-step problem solving, tool chaining |
| **Basic Agent** | LangGraph fundamentals, simple state management |

---

## 🚀 Advanced Usage

### Customizing Agents
Each agent can be extended with additional tools and capabilities:

```python
# Example: Adding a new tool to React Agent
@tool
def divide(a: int, b: int):
    """Division function"""
    if b == 0:
        return "Cannot divide by zero"
    return a / b

# Add to tools list
tools = [add, subtract, multiply, divide]
```

### Extending RAG Agent
```python
# Add support for multiple PDF files
pdf_files = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
for pdf_file in pdf_files:
    # Process each PDF...
```

---

## 🤝 Contributing

Feel free to contribute by:
1. Adding new agent patterns
2. Improving existing implementations
3. Adding more sophisticated tools
4. Enhancing documentation

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Raksa** - Student at Kansas State University

---

## 📞 Support

If you have questions or need help:
1. Check the code comments for detailed explanations
2. Review the LangGraph documentation
3. Open an issue on GitHub

---

**Happy Coding! 🎉**
