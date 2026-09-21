from time import perf_counter
import requests

from agents import function_tool, Agent, Runner


urls = ["python.org", "github.com", "openai.com"]


@function_tool
def check_website(url: str) -> str:
    """Check a website's HTTP status and response time."""
    
    start = perf_counter()

    try:
        response = requests.get(url, timeout=10)
        latency = perf_counter() - start

        return (
            f"{url}\n"
            f"Status: {response.status_code}\n"
            f"Response Time: {latency:.2f}s"        
        )
        
    except requests.RequestException as error:
        return f"{url}\nError: {error}"
    

agent = Agent(
    name="Website Monitor",
    model="gpt-5.6-luna",
    instructions="""
    Monitor websites using the available tool. Compare the results and explain the problems clearly.
    """,
    tools=[check_website],
)

result = Runner.run_sync(
    agent,
    f"Check{urls}"
    "Which one has the slowest response?"
)

print(result.final_output)