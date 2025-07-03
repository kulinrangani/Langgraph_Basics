from dotenv import load_dotenv
load_dotenv()
from typing import Annotated
from typing_extensions import TypedDict
from langchain.chat_models import  init_chat_model
from langgraph.graph import START,StateGraph
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode , tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt,Command

class State(TypedDict):
    # Messages  have the type "list" ,
    # the add_message function in annotation defines how this state key should be update
    # in this case it appends the message to the list rather than replacing them
    messages : Annotated[list , add_messages]

@tool
def get_stock_price(stock_name:str) ->float :
    """Return the current stock price for a given stock symbol."""
    return {
        "MSFT":200,
        "AAPL":300,
        "GOOG":400,
        "TSLA":500,
    }.get(stock_name, 0.0)

@tool
def buy_stocks(symbol:str,quantity:int, total:float) -> str:
    """Buy stocks for a given symbol and quantity."""
    user_response = interrupt(f"Approve buying {quantity} shares of {symbol} for total price ${total:.2f} ?")\

    if user_response == "yes":
        return f"You bought {quantity} shares of {symbol} for total price  {total}"
    else:
        return f"You declined to buy {quantity} shares of {symbol} for total price  {total}"

tools = [get_stock_price , buy_stocks]

llm = init_chat_model("google_genai:gemini-2.0-flash")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state:State)->State:
    return {"messages" : llm_with_tools.invoke(state["messages"])}

builder = StateGraph(State)
builder.add_node("chatbot",chatbot)
builder.add_node("tools" , ToolNode(tools))

builder.add_edge(START , "chatbot")
builder.add_conditional_edges("chatbot" , tools_condition)
builder.add_edge("tools","chatbot" )
memory = MemorySaver()

config = {"configurable": {"thread_id":"buy_stock"}}

graph = builder.compile(checkpointer=memory)


#1
state = graph.invoke({"messages":[{"role":"user","content":"What is the current price of AAPL stocks?"}]},config=config)
print(state["messages"][-1].content)

#2
state = graph.invoke({"messages":[{"role":"user","content":"Buy 10 stokes of AAPL for me at current price"}]},config=config)
print(state.get("__interrupt__"))

decision = input("Approve (yes/no)")
state = graph.invoke(Command(resume=decision), config=config)
print(state["messages"][-1].content)
