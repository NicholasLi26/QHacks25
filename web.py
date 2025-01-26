import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
from io import BytesIO
from PIL import Image
from imageParsing import imageParse
import os
from pdf2image import convert_from_bytes

if "page" not in st.session_state:
    st.session_state.page = 0

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
        st.write_stream(stream_data("### If you would like to submit your Sylabus', please upload them now."))
        uploadedSylabus = st.file_uploader("Upload Sylabus'", type=['pdf', 'docx', 'png', 'jpg'], accept_multiple_files=True)
        for i in range(len(uploadedSylabus)):
        #for id, name, type, size in uploadedSylabus[i]:
            if uploadedSylabus[i].type == 'application/pdf':
                # st.write("pdf")
                if not os.path.exists(f"images/syllabus{i}"):
                    os.mkdir(f"images/syllabus{i}")
                docAsBytes = uploadedSylabus[i].read()
                pages = convert_from_bytes(docAsBytes, output_folder= f"images/syllabus{i}", output_file=f"img", fmt="jpeg", poppler_path = r'C:\Users\Nicholas\poppler-24.08.0\Library\bin',)
                
                

            elif uploadedSylabus[i].type == 'image/png' or uploadedSylabus[i].type == 'image/jpg':
                # st.write("image")
                if not os.path.exists(f"images/syllabus{i}"):
                    os.mkdir(f"images/syllabus{i}")
                im = Image.open(uploadedSylabus[i])
                im.save(f"images/syllabus{i}/page1.png")

        if uploadedSylabus:
            st.button("Upload",on_click=uploadSylabus)

elif st.session_state.page == 2:
    container = st.empty()
    st.write_stream(stream_data("# Sylabus' Uploaded Successfully!"))
    st.write_stream(stream_data("## Feel free to type in any other activities you would like to add to your schedule! provide the days and start and end times please!"))
    st.write_stream(stream_data("Note - you don't have to put in study time! I will do that for you"))
    st.write_stream(stream_data("When you are done, click the button below!"))
    
    extraOptions.append(st.text_input(""))
    if lastIndx + 1 == len(uploadedSylabus):
        st