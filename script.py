import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv()

client = genai.Client(api_key=os.getenv("APIKEY"))

def get_story():

    class response(BaseModel):
        hook: str = Field(description="generate a hook for the story")
        story: str = Field(description="This contains the story")
        voice: str = Field(description="This specifies which voice to use")
        
    response = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input = """
            Generate a Reddit story for a YouTube Short.
            voices available : ['aiden', 'dylan', 'eric', 'ono_anna', 'ryan', 'serena', 'sohee', 'uncle_fu', 'vivian']

            Requirements:
            - Hook: 15-20 words.
            - Story: 65-85 words.
            - The story MUST have a complete ending and a satisfying twist.
            - Do not stop mid-story.
            - End with a final sentence that resolves the story.
        """,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": response.model_json_schema()
        },
    )

    return response.output_text 
