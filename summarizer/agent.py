from google.adk.agents import Agent

root_agent = Agent(
    name="summarizer_agent",
    model="gemini-2.0-flash",
    description="Summarizes any text into 2-3 clear sentences.",
    instruction="""
        You are a summarization assistant.
        When given any text, respond with a concise 2-3 sentence summary.
        Be clear, accurate, and preserve the key points.
    """,
)
