from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from graph import graph  # Importing your compiled graph with MemorySaver
import uvicorn

app = FastAPI(title="HR Chatbot API")

# 1. Define Request/Response Schemas
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    category: str
    thread_id: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 2. Maintain memory using thread_id from request
        config = {"configurable": {"thread_id": request.user_id}}

        # 3. Invoke your existing graph logic
        # We pass the message into the state's message list
        inputs = {"messages": [HumanMessage(content=request.message)]}
        
        # This triggers the intent_classifier and the respective handler nodes
        result = graph.invoke(inputs, config=config)

        # 4. Return the response as JSON
        return ChatResponse(
            response=result.get("response", "I'm sorry, I couldn't process that."),
            category=result.get("category", "unknown"),
            thread_id=request.user_id
        )

    except Exception as e:
        # Catch errors from nodes or LLM calls
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)