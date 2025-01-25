import PIL.Image
import google.generativeai as genai
import time

genai.configure(api_key="AIzaSyAXC_QCe5GQ6IbJvpKYRyB4eDQG3v8yBwA")
model = genai.GenerativeModel(model_name = "gemini-1.5-pro")

def ask_gemini(prompt, images):

    responses = []

    for image_path in images:
        image = PIL.Image.open(image_path)
        response = model.generate_content([prompt, image])

        

        day = [line.strip() for line in response.text.split(",") if line.strip()]    

        responses.append(day)


        time.sleep(8)

    return responses


# a list of all the image paths for the columns
images = [
    "images/mon.png",
    "images/tue.png",
    "images/wed.png",
    "images/thu.png",
    "images/fri.png",
]
prompt = "What day of the week is this, what classes do I have, and what are the start and end times of each class? Please print it in a list format like this: day of the week, class 1, class 1 start time, class 1 end time, class 2, class 2 start time, etc. for all class times, with each comma representing a line break. Thank you!"

responses = ask_gemini(prompt, images)

for response in responses:
    print(response)
    print("HAII\n\n")