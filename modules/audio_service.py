"""
Audio Service for generating audio overviews
"""
from gtts import gTTS
import os

import tempfile


class AudioService:
    """Generate audio overviews from text"""
    
    @staticmethod
    def generate_overview(text: str, filename: str = "overview.mp3") -> str:
        """Generate audio overview from text using gTTS"""
        try:
            # Create a podcast-style introduction
            intro = "Welcome to your document overview. Here's what we found: "
            full_text = intro + text
            
            # Generate TTS
            tts = gTTS(text=full_text, lang='en', slow=False)
            
            # Save to temp file
            output_path = os.path.join(tempfile.gettempdir(), filename)
            tts.save(output_path)
            
            return output_path
            
        except Exception as e:
            return f"Error generating audio: {str(e)}"
    
    @staticmethod
    def create_podcast_style(summary: str, key_points: list) -> str:
        """Create a podcast-style script from document"""
        script = f"""
        Welcome to your personalized document overview.
        
        Here's a quick summary: {summary}
        
        Now, let me highlight the key points:
        """
        
        for i, point in enumerate(key_points, 1):
            script += f"\nPoint {i}: {point}"
        
        script += "\n\nThat concludes our overview. Thank you for listening!"
        
        return script
