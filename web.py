import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
from io import BytesIO
from PIL import Image
from imageParsing import imageParse
import os
from pdf2image import convert_from_bytes
import objects.queriesObj as qo
import main as m

if "page" not in st.session_state:
    st.session_state.page = 0

if "main" not in st.session_state:
    st.session_state.main = m.mainManagement()

if "sleeptime" not in st.session_state:
    st.session_state.sleeptime = 0

if "studytime" not in st.session_state:
    st.session_state.studytime = 0

if "prioLessBusy" not in st.session_state:
    st.session_state.prioLessBusy = False

if "wakeuptime" not in st.session_state:
    st.session_state.wakeuptime = 0

def nextpage():
    st.session_state.page += 1

def upload():
    st.session_state.page +=1
    im = Image.open(uploadedSched)
    im.save(path)

def uploadSylabus():
    st.session_state.page += 1

def getSleep():
    st.session_state.page += 1
    st.session_state.main.setSleepAndWake(st.session_state.sleeptime, st.session_state.wakeuptime)
    
        # else:
        #     # st.write("docx")
        #     document = Document(uploadedSylabus[i])
        #     imageStream = document.SaveImageToStreams(ImageType.Bitmap)
        #     temp = 1
        #     os.mkdir(f"images/syllabus{i}")
        #     for image in imageStream:
        #         im = Image.open(image)
        #         im.save(f"images/syllabus{i}/page{temp}.png")

        
        # i += 1
        # numOfSylabus += 1

def stream_data(string):
        for word in string.split(" "):
            yield word + " "
            time.sleep(0.05)

parse = False
path = "images/schedule.png"
container = st.empty()

numOfSylabus = 0
uploadedSched = None
uploadedSylabus = None
extraOptions = []



if st.session_state.page == 0:

    firstPage = """
    # Hello! Welcome to Palendar!
    ### Palendar is a web app that helps to allocate your time efficiently by generating a schedule based on your courses and preferences.
    ### To get started, please upload an image of your schedule.
    """    
    st.write_stream(stream_data(firstPage))

    uploadedSched = st.file_uploader("Upload Schedule Image", type=['png', 'jpg'])
    
    if uploadedSched:        
        st.image(image = uploadedSched)
        st.button("Upload",on_click=upload) 


elif st.session_state.page == 1:
    container = st.empty()
    if imageParse(path):
        st.write_stream(stream_data("# Schedule Image Uploaded Successfully!"))
        st.write_stream(stream_data("### If you would like to add your syllabus, please upload them now."))
        uploadedSylabus = st.file_uploader("Upload Syllabus'", type=['pdf', 'docx', 'png', 'jpg'], accept_multiple_files=True)
        for i in range(len(uploadedSylabus)):
        #for id, name, type, size in uploadedSylabus[i]:
            if uploadedSylabus[i].type == 'application/pdf':
                # st.write("pdf")
                if not os.path.exists(f"runtimeImages/syllabus{i}"):
                    os.mkdir(f"runtimeImages/syllabus{i}")
                docAsBytes = uploadedSylabus[i].read()
                pages = convert_from_bytes(docAsBytes, output_folder= f"runtimeImages/syllabus{i}", output_file=f"img", fmt="jpeg", poppler_path = r'C:\Users\Nicholas\poppler-24.08.0\Library\bin',)
                
                

            elif uploadedSylabus[i].type == 'image/png' or uploadedSylabus[i].type == 'image/jpg':
                # st.write("image")
                if not os.path.exists(f"iruntimeImages/syllabus{i}"):
                    os.mkdir(f"runtimeImages/syllabus{i}")
                im = Image.open(uploadedSylabus[i])
                im.save(f"runtimeImages/syllabus{i}/page1.png")

        if uploadedSylabus:
            st.button("Upload",on_click=uploadSylabus)

elif st.session_state.page == 2:
    container = st.empty()
    st.write_stream(stream_data("# Sylabus' Uploaded Successfully!"))
    st.write_stream(stream_data("## Feel free to type in any other activities you would like to add to your schedule! provide the days and start and end times please!"))
    st.write_stream(stream_data("Note - you don't have to put in study times! We will do that for you :3"))
    st.write_stream(stream_data("When you are done, click the button below!"))
    
    if 'something' not in st.session_state:
        st.session_state.something = ''

    if 'queryObj' not in st.session_state:
        st.session_state.queryObj = qo.queryObj()

    def submit():
        st.session_state.something = st.session_state.widget
        st.session_state.widget = ''

    st.text_input('To be added:', key='widget', on_change=submit)

    st.button("Submit", on_click=nextpage)

    st.session_state.queryObj.addQuery(st.session_state.something)
    for options in st.session_state.queryObj.getQuery():
        st.write(options)

elif st.session_state.page == 3:
    st.session_state.main.ProcessSchedule()
    st.session_state.main.ProcessSyllabus()
    st.write_stream(stream_data("# Proccessing!"))
    st.button("Done", on_click=nextpage)

elif st.session_state.page == 4:
    st.write("#This input section helps to optimize your schedule based on your preferences! It takes into account sleep as to set study times accordingly.")

    st.write("# How much time would you like to spend studying per week?")
    st.session_state.studytime = round(st.slider("Hours per Week", 0, 50, 0))

    st.write("# How many hours of sleep are you going to try to get a night?")
    st.session_state.sleeptime = round(st.slider("Hours per Day", 6, 12, 0))

    st.write("# How many hours does it take for you to get up?")
    st.session_state.wakeuptime = round(st.slider("Hours per Day", 0, 3, 0))

    st.write("#On days with no morning classes, what time would you like to wake up?")
    st.write("If your morning classes interfere, wake up times will automatically be adjusted.")
    st.session_state.main.setIdeal(st.time_input("Wake Up Time", 5, 12, 0))
    
    st.write("### Would you rather study more on days with less classes?")

    st.session_state.prioLessBusy = st.checkbox("Yes")

    st.button("Done", on_click=getSleep)

    



    # TOTAL HOURS * SLIDERVALUE / TOTALSLIDERVALUES = CLASSHOURS time spent studying for that class
    # for each class:
    # st.write_stream(stream_data(f"{int(CLASSHOURS)} hours per week for {CLASSNAME}"))