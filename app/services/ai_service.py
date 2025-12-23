# import openai
#
# openai.api_key = "YOUR_API_KEY"
#
# def analyze_ticket(text: str):
#     prompt = f"Classify category and priority:\n{text}"
#
#     response = openai.ChatCompletion.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prompt}]
#     )
#
#     return response.choices[0].message.content


from google import genai

import app.config as config

from pydantic import BaseModel


class TicketClassification(BaseModel):
    category: str
    priority: str


client = genai.Client(api_key=config.AI_API_KEY)

model = "gemini-2.5-flash-lite"


def analyze_ticket(text: str):
    prompt = f"""Analyze the support ticket and return json only.
            Ticket:{text}
            Output format:{{
            "category":"billing  | technical | authentication |general",
            "priority":"low  | medium | high",
            }}
    """

    response = client.models.generate_content(model=model,
                                              contents=prompt,
                                              config={
                                                  'response_mime_type': 'application/json',
                                                  'response_schema': TicketClassification,
                                              })
    print(response.parsed)
    return response.parsed
