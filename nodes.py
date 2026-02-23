from state import HRState
from database import retriever
from langchain_core.messages import SystemMessage, HumanMessage
import json
from langchain_core.messages import SystemMessage
from config import llm

def get_intent_category(user_query, model):
    system_instructions = SystemMessage(content="""
        You are an HR intent classifier.
        Analyze the user's input and categorize it into exactly ONE of these labels:
        - 'leave' (vacation, time off, sick days)
        - 'claim' (reimbursements, expenses, money back)
        - 'policy' (questions about rules, handbook, or 'how-to')
        - 'feedback' (suggestions, complaints, or compliments)
        - 'greet'('hi','i want help','hello')

        Return ONLY the label. Do not include any other text or punctuation.
    """)

    user_message = HumanMessage(content=user_query)

    # Send to LLM
    response = model.invoke([system_instructions, user_message])
    return response.content.strip().lower()

# 2. Interactive Test Loop


def intent_classifier_node(state: HRState):
    # 1. Check if messages exist
    if not state.get("messages"):      
        query = state.get("user_query", "")
        if not query:
            return {"category": "greet"}
         # Default if everything is empty
    else:
       
        query = state["messages"][-1].content

    # 3. Use your existing logic
    category = get_intent_category(query, llm)
    return {"category": category, "user_query": query}

def handle_claim(state: HRState):
    # specialized logic for leaves
    return {"response": "claim submitted to HR!"}

def handle_feedback(state: HRState):
    # specialized logic for leaves
    return {"response": "feedback submitted successfully"}



def handle_leave(state: HRState):
    # Set the baseline (In a real app, you'd fetch this from a DB)
    pto_balance = state.get("pto_available", 15)
    history = state.get("messages", [])
    
    # 1. Use LLM to extract "Dates" and "Reason" from the conversation history
    # This allows it to handle "all-in-one" or "step-by-step" inputs
    extraction_prompt = f"""
    You are an HR data extractor. Look at the conversation history and extract:
    1. The dates for the leave.
    2. The reason for the leave.
    3. The number of days requested (estimate if not clear).

    Return ONLY a JSON object: 
    {{"dates": "string or null", "reason": "string or null", "days": integer_or_null}}
    
    HISTORY: {[m.content for m in history[-4:]]}
    """
    
    extraction = llm.invoke(extraction_prompt)
    try:
        # We strip potential markdown code blocks from the LLM response
        clean_json = extraction.content.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
    except:
        data = {"dates": None, "reason": None, "days": 0}

    # 2. VALIDATION LOGIC (The Step-by-Step part)
    
    # Step A: Check for Dates
    if not data["dates"]:
        res = "I can help you with that. What dates are you looking to take off?"
        return {"response": res, "messages": [SystemMessage(content=res)]}
    
    # Step B: Check for Reason
    if not data["reason"]:
        res = f"Got it, for {data['dates']}. And what is the reason for your leave request?"
        return {"response": res, "messages": [SystemMessage(content=res)]}

    # Step C: PTO Check
    requested_days = data.get("days") or 1 # Default to 1 if not extractable
    
    if requested_days > pto_balance:
        extra = requested_days - pto_balance
        res = (f"You requested {requested_days} days for '{data['reason']}'. "
               f"You only have {pto_balance} days left. "
               f"The remaining {extra} day(s) will be processed as unpaid leave with a salary deduction. "
               "Should I proceed with the submission?")
    else:
        new_balance = pto_balance - requested_days
        res = (f"Perfect. I've noted your leave for {data['dates']} ({data['reason']}). "
               f"This will use {requested_days} days. You will have {new_balance} days remaining.")

    # 3. Return the data to the state
    return {
        "response": res,
        "messages": [SystemMessage(content=res)],
        "leave_dates": data["dates"],
        "leave_reason": data["reason"]
    }

def handle_policy(state: HRState):
    
    history = state.get("messages", [])
    contextualize_prompt = f"""Given the following conversation, rewrite the last user question 
    to be a standalone question for a search engine.  
    CHAT HISTORY: {history[-3:]}
    """
    standalone_query_res = llm.invoke(contextualize_prompt)
    search_query = standalone_query_res.content

    # 2. Retrieval using the "Better" query
    docs = retriever.invoke(search_query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 3. Answer using both context AND conversation history
    # This allows the LLM to see its previous long answer and simplify it.
    prompt = [
        SystemMessage(content=f"You are a helpful HR Assistant. Use the provided policy context to answer the question. If the context doesn't contain the answer, say you don't know—don't make it up.Use this context: {context}"),
    ] + history  # We append the actual history here!

    ans = llm.invoke(prompt)
    
    return {
        "response": ans.content, 
        "messages": [ans] # VERY IMPORTANT: Save the AI's answer back to memory
    }

def handle_greet(state: HRState):
    res = llm.invoke(state["messages"])
    return {
        "response": res.content,
        "messages": [res] 
    }

