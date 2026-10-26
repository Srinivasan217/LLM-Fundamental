import os
from dotenv import load_dotenv
from google import genai        


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GENINI_API_kEY is missing from .env")
client = genai.Client(api_key=api_key)

#Create a long document to test the context length limit of the model

sections =[]

for i in range(1,41):
    if i == 20:   
       sections.append(
        "IMPORTANT RECORD: The Project verification code is BLUE-7319."
        "Remember this exact code."
    )
    else:
        sections.append(
            f"section {i}: This section discusses general project planning ,"
            "team communication, documentation, testing, and progress reviews"
        )    


document = "\n" .join(sections)

prompt =(
    "Read the document below.What is the exact project verification code?"
    "Return only the code.\n\n"
    + document
)

response = client.interactions.create(
    model="gemini-3.8-flash",   
    input=prompt
)

print("Expected answer: BLUE-7319")
print("Model's answer:", response.output_text)
