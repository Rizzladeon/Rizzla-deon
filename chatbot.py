import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RizzlaTubeChatbot:
    """
    AI-powered chatbot for Rizzla Tube app.
    Helps users find entertainment, get recommendations, and answer questions.
    """
    
    def __init__(self, system_prompt=None):
        self.conversation_history = []
        self.system_prompt = system_prompt or self._get_default_system_prompt()
    
    def _get_default_system_prompt(self):
        """Default system prompt for the Rizzla Tube chatbot"""
        return """You are a helpful AI assistant for Rizzla Tube, an entertainment app.
Your role is to:
- Help users find great movies, comedies, and trending videos
- Provide personalized entertainment recommendations
- Answer questions about the app features
- Suggest content based on user preferences
- Be friendly, engaging, and entertaining

Always maintain a conversational tone and help users discover amazing entertainment!"""
    
    def chat(self, user_message):
        """
        Send a message to the chatbot and get a response.
        
        Args:
            user_message (str): The user's message
            
        Returns:
            str: The chatbot's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract assistant response
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_message = f"Error communicating with AI: {str(e)}"
            print(error_message)
            return error_message
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
    
    def get_recommendation(self, genre=None, mood=None):
        """
        Get a personalized content recommendation.
        
        Args:
            genre (str): Preferred genre
            mood (str): Current mood or preference
            
        Returns:
            str: AI-generated recommendation
        """
        prompt = f"Recommend an entertainment content for Rizzla Tube"
        if genre:
            prompt += f" in the {genre} genre"
        if mood:
            prompt += f" for someone who is {mood}"
        
        return self.chat(prompt)


# Example usage
if __name__ == "__main__":
    # Initialize chatbot
    chatbot = RizzlaTubeChatbot()
    
    # Example conversation
    print("Rizzla Tube AI Chatbot")
    print("=" * 50)
    
    # Test message
    user_input = "I'm looking for something funny to watch"
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"Chatbot: {response}\n")
    
    # Follow-up message
    user_input = "What about action movies?"
    print(f"User: {user_input}")
    response = chatbot.chat(user_input)
    print(f"Chatbot: {response}\n")
