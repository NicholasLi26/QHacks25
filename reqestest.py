import PIL.Image
import google.generativeai as genai
import time

# with open('keys/gemini.txt', 'r') as file:
#     key = file.read()

# genai.configure(api_key=key)
# model = genai.GenerativeModel(model_name = "gemini-1.5-flash")

def ask_gemini(model, prompt, images):
    responses = []
    course_code = None

    if "NO_IMPORTANT_DATES" in prompt:
        course_code = model.generate_content(["Please print only the course code for this class. Thank you!", PIL.Image.open(images[0])])

    for image_path in images:
        image = PIL.Image.open(image_path)
        response = model.generate_content([prompt, image])

        # print(image_path)
        # print(response.text)
        # print("\n\n")

        day = [line[1:] if line.startswith(',') else line for line in response.text.split("\n")]  
        day = list(filter(lambda x: x != '', day))

        if course_code!=None: day.append(course_code.text)


        responses.append(day)

        time.sleep(2)

    return responses



def process_gemini(responses):
    schedule = [[], [], [], [], [], [], []]
    events = []

    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    months = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]

    for response in responses:

        isitschedule = 0

        for i, day in enumerate(days):
            if day in response[0].lower():
                schedule[i] = response[1:]
                isitschedule = 1

        if isitschedule==0:
            course_code = response[-1]
            response = response[:-1]

            if any(month in response[0].lower() for month in months) and any(month in response[1].lower() for month in months) and not any(month in response[2].lower() for month in months):
                #proceed as ranges

                start_dates = []
                for i in range(len(response)-1):
                    if any(month in response[i].lower() for month in months) and any(month in response[i+1].lower() for month in months):
                        start_dates.append(i)

                for i in range(len(start_dates)):
                    start = start_dates[i]
                    end = start_dates[i+1] if i+1<len(start_dates) else len(response)
                    events.append(response[start:end])
                    events[-1].append(course_code)

            else:
                #proceed as single dates

                for i in range(int(len(response)/2)):
                    events.append([response[i], response[i+int(len(response)/2)]])
                    events[-1].append(course_code)

    return (schedule, events)

# ask_gemini test
images = [
    "images/syllabus1.png",
    "images/syllabus2.png",
    "images/syllabus3.png",
]

prompt_schedule = """
What day of the week is this, what classes do I have, and what are the start and end times of each class? Please print it in a list format like this: day of the week, class 1, class 1 start time, class 1 end time, class 2, class 2 start time, etc. for all class times, with a line break after each item. Please only print the list, no other text. Thank you!
"""


prompt_syllabus = """
What are the important dates for this course? Please provide me with a list describing what is happening on what day. Please print each item in a list format like this: date 1 (line break), date 2 if there is a date range (line break), description (line break) (line break). A line should not contain more than one date, so all second dates must be written on a new line. All dates should be formatted as: Month Day. Please only print the list, no other text. If there are no important dates, please respond with NO_IMPORTANT_DATES. Thank you!
"""


# responses = ask_gemini(model, prompt_syllabus, images)

# for response in responses:
#     print(response)
#     print("\n\n")

# schedule, events = process_gemini(responses)

# print(schedule)
# print("\n\nHAIIIII")
# print(events)