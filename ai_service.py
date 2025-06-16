"""
This module handles Azure OpenAI integration for keyword generation
"""

import os
from typing import List
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from keywords import ALL_KEYWORDS

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure GitHub AI client
endpoint = "https://models.github.ai/inference"
model_name = "microsoft/Phi-4"
token = os.getenv("GITHUB_TOKEN")

if not token:
    raise ValueError("GitHub token not found. Please set GITHUB_TOKEN in .env file")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def generate_keywords(user_story: str) -> List[str]:
    """
    Generate relevant keywords from a user story using GitHub AI models.
    
    Args:
        user_story (str): The user story to analyze
        
    Returns:
        List[str]: List of relevant keywords from our existing keyword list
    """
    try:
        # Create a prompt that instructs the model to match the story with existing keywords
        prompt = f"""
        Given the following user story about a speaking request:
        "{user_story}"
        
        And this list of available keywords:
        {ALL_KEYWORDS}
        
        Please identify the most relevant keywords from the provided list that match the user story.
        Only return keywords from the provided list, separated by commas.
        Return between 2 and 5 keywords maximum.
        """
        
        response = client.complete(
            messages=[
                SystemMessage("You are a helpful assistant that matches user stories with relevant keywords."),
                UserMessage(prompt)
            ],
            temperature=0.3,
            top_p=1.0,
            max_tokens=150,
            model=model_name
        )
        
        # Extract keywords from response
        keywords_text = response.choices[0].message.content.strip()
        # Split by comma and clean up each keyword
        keywords = [k.strip() for k in keywords_text.split(",")]
        # Only return keywords that are in our original list
        valid_keywords = [k for k in keywords if k in ALL_KEYWORDS]
        
        return valid_keywords
        
    except Exception as e:
        print(f"Error generating keywords: {str(e)}")
        return []
