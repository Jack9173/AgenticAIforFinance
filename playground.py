import openai
from phi.agent import Agent
import phi.api
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from phi.model.groq import Groq

import os
import phi
from phi.playground import Playground, serve_playground_app

# Load environment variables from .env file
load_dotenv()
phi.api.API_KEY = os.getenv("PHI_API_KEY")

# Web search agent
web_search_agent = Agent(
    name='Web Search Agent',
    role="Search the web for the information",
    model=Groq(id="llama3-70b-8192-tool-use-preview"),  # Ensure this ID is correct
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

# Financial agent
finance_agent = Agent(
    name="Finance AI Agent",
    model=Groq(id="llama3-70b-8192-tool-use-preview"),  # Ensure this ID is correct
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True
        ),
    ],
    instructions=["Use tables to display the data"],
    show_tools_calls=True,
    markdown=True,
)

# Create Playground app
app = Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
