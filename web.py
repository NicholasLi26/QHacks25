import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
from io import BytesIO
from PIL import Image
from imageParsing import imageParse
import os
from pdf2image import convert_from_bytes
import queriesObj as qo
import main as m

if "page" not in st.session_state:
    st.session_state.page = 0

if "main" not in st.session_state:
    st.session_state.main = m.mainManagement()

def nextpage():
    st.session_state.page += 1

def upload():
    st.session_state.page +=1
    im = Image.open(uploadedSched)
    im.save(path)

def uploadSylabus():
    st.session_state.page += 1
    
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
    # st.write("# Hello! Welcome to Palendar!")
    # st.write("### Palendar is a web app that helps to allocate your time efficiently by generating a schedule based on your courses and preferences.")
    # st.write("### To get started, please upload an image of your schedule.")
    
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
    st.write_stream(stream_data("Note - you don't have to put in study times! We will do that for you"))
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

elif st.session_state.page == 4:
    st.write_stream(stream_data("# How much time would you like to spend studying per week?"))
    # slider: 0-50 hours (TOTALHOURS variable)

    # st.write_stream(stream_data(f"That would be around {TOTALHOURS} hours per day!"))

    st.write_stream(stream_data("# On a scale of 1 to 5, how difficult is each class?"))
    # slider:

    # TOTAL HOURS * SLIDERVALUE / TOTALSLIDERVALUES = CLASSHOURS time spent studying for that class
    # for each class:
    # st.write_stream(stream_data(f"{int(CLASSHOURS)} hours per week for {CLASSNAME}"))