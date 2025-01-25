import PIL.Image
import google.generativeai as genai
import time

with open('keys/gemini.txt', 'r') as file:
    key = file.read()

genai.configure(api_key=key)
model = genai.GenerativeModel(model_name = "gemini-1.5-flash")

def ask_gemini(prompt, images): # for schedule
    responses = []

    for image_path in images:
        image = PIL.Image.open(image_path)
        response = model.generate_content([prompt, image])

        print(image_path)
        print(response.text)
        print("\n\n")

        day = [line[1:] if line.startswith(',') else line for line in response.text.split("\n")]  
        responses.append(day)

        time.sleep(2)

    return responses

# ask_gemini test
images = [
    "images/syllabus1.png",
    "images/syllabus2.png",
    "images/syllabus3.png",
    "images/mon.png",
    "images/tue.png",
    "images/wed.png",
    "images/thu.png",
    "images/fri.png",
]

prompt = """
If this image appears to be a schedule, please follow the following prompt:
What day of the week is this, what classes do I have, and what are the start and end times of each class? Please print it in a list format like this: day of the week, class 1, class 1 start time, class 1 end time, class 2, class 2 start time, etc. for all class times, with a line break after each item. Please only print the list, no other text. Thank you!

Otherwise, please follow this prompt:
What are the important dates for this course? Please provide me with a list describing what is happening on what day. Please print each item in a list format like this: date 1 (line break), date 2 if there is a date range (line break), description (line break) (line break). Each item should consist of three lines at most: one or two lines for the dates, and then one line for the description. All dates should be formatted as: Month Day. Please only print the list, no other text. If there are no important dates, please respond with NO_IMPORTANT_DATES."""

responses = ask_gemini(prompt, images)

for response in responses:
    print(response)
    print("\n\n")