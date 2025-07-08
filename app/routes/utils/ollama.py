from typing import Dict
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.1"


class OllamaService:
    @staticmethod
    def generate_student_summary(student: Dict) -> str:
        try:
            prompt = f"""
            Please generate a comprehensive summary for the following student profile:

            Student Information:
            - Name: {student['name']}
            - Age: {student['age']} years old
            - Email: {student['email']}
            - Profile Created: {student.get('created_at', 'N/A')}
            - Last Updated: {student.get('updated_at', 'N/A')}

            Generate a professional summary that includes:
            1. A brief introduction
            2. Key characteristics based on the age group
            3. Potential academic focus areas
            4. Communication preferences
            5. Any relevant observations
            
            The summary should be from the perspective of a third person

            Keep the summary concise but informative, around 50 - 100 words.
            """

            payload = {
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            }

            response = requests.post(OLLAMA_URL, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()
            return result.get('response', 'Unable to generate summary')

        except requests.exceptions.RequestException as e:
            return f"Error connecting to Ollama: {str(e)}"
        except Exception as e:
            return f"Error generating summary: {str(e)}"
