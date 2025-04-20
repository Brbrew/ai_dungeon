"""AI Generator for the dungeon project."""
import os
import re
from groq import Groq
from .ai_prompt import AIPrompt

class AIGenerator:
    """A class for generating content using AI."""
    
    def __init__(self):
        """Initialize the AI Generator."""
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )
        
        """
        The following models are available:
            deepseek-r1-distill-llama-70b
            llama-3.3-70b-versatile
            mistral-saba-24b
        """

        self.ai_model = "deepseek-r1-distill-llama-70b"
        print(f"DEBUG: AIGenerator initialized with model: {self.ai_model}")
    
    def remove_between_tags(self, text, tag_name):
        """Removes text between specified tags in a string.
        
        Args:
            text: The text to process
            tag_name: The name of the tag to remove content between
            
        Returns:
            The text with content between the specified tags removed
        """
        pattern = r'<{tag_name}.*?</{tag_name}>'.format(tag_name=tag_name)
        return re.sub(pattern, '', text, flags=re.DOTALL)
    
    def room_description_generate(self, room_id: str, room=None) -> str:
        """Generate a room description using AI.
        
        Args:
            room_id: The ID of the room to generate a description for
            room: Optional Room object to use instead of looking it up
            
        Returns:
            A string containing the generated room description
        """
        try:
            # Use provided room or get room information from the dungeon
            if not room:
                from .dungeon import Dungeon
                dungeon = Dungeon()
                room = dungeon.map.get_room(room_id)
            
            if not room:
                print(f"DEBUG: Room with ID {room_id} not found")
                return "A mysterious room with stone walls and a dim light source."
            
            # Create a prompt with room information
            prompt = f'''
            Using the following input fields:
            "description": "{room.description}",
            "theme": "{room.theme.name if room.theme else 'default'}",
            "room_type": "{room.room_type.name if room.room_type else 'room'}"
            "room_direction_info": "{room.room_direction_info}"
            Write a brief, one or two paragraph description of the room from the player's perspective upon first entering. 
            Channel the evocative, immersive style of Patrick Rothfuss, Robert Jordan, or Brandon Sanderson. 
            Focus on sensory details, mood, and subtle worldbuilding. Do not repeat the input text verbatim; instead, expand and enrich the scene with original, atmospheric language. 
            Ensure the description aligns with the provided theme and room type.
            '''
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": AIPrompt.ROOM.value},
                    {"role": "user", "content": prompt}
                ],
                #max_tokens=150,
                temperature=0.7
            )
            
            raw_description = response.choices[0].message.content.strip()
            description = self.remove_between_tags(raw_description, 'think')
            print(f"DEBUG: Generated room description for room {room.name}: {description[:50]}...")
            return description
        
        except Exception as e:
            print(f"DEBUG: Error generating room description: {e}")
            return "A mysterious room with stone walls and a dim light source."
    
    def npc_description_generate(self) -> str:
        """Generate an NPC description using AI.
        
        Returns:
            A string containing the generated NPC description
        """
        try:
            prompt = "Generate a brief description for a fantasy NPC that might be found in a dungeon. " \
                     "Include their appearance, demeanor, and any notable characteristics. " \
                     "Keep it under 75 words and make it interesting."
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a creative dungeon master who creates vivid descriptions for fantasy characters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            description = response.choices[0].message.content.strip()
            print(f"DEBUG: Generated NPC description: {description[:50]}...")
            return description
        except Exception as e:
            print(f"DEBUG: Error generating NPC description: {e}")
            return "A mysterious figure with a hooded cloak and weathered hands."
    
    def item_description_generate(self) -> str:
        """Generate an item description using AI.
        
        Returns:
            A string containing the generated item description
        """
        try:
            prompt = "Generate a brief description for a fantasy item that might be found in a dungeon. " \
                     "Include its appearance, any magical properties, and its condition. " \
                     "Keep it under 50 words and make it intriguing."
            
            response = self.client.chat.completions.create(
                model=self.ai_model,
                messages=[
                    {"role": "system", "content": "You are a creative dungeon master who creates vivid descriptions for fantasy items."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=75,
                temperature=0.7
            )
            
            description = response.choices[0].message.content.strip()
            print(f"DEBUG: Generated item description: {description[:50]}...")
            return description
        except Exception as e:
            print(f"DEBUG: Error generating item description: {e}")
            return "A small, intricately carved object with faint magical runes." 