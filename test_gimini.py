from google import genai

try:
        client = genai.Client(api_key="test")
        print("Listing available models:")
        # The list_models method is your key to current information
        for model in client.models.list():
            print(f"- Name: {model.name}")
            print(f"  Description: {model.description}")
            # print(f"  Supported methods: {model.supported_methods}")
            print("-" * 20)
except Exception as e:
        print(f"An error occurred while listing models: {e}")


client = genai.Client(api_key="test")

res = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    # model="gemini-2.0-flash",
    contents="Say hello"
)

print(res.text)