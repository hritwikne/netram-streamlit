import time
from english import demo
from malayalam import demo_mal
from text_detection import ctpn_predict
import streamlit as st
import os
import requests

def predict_menu(file, process, crop, language, displayOriginal, doTTS, takePicture=False):
    for i in range(len(file)):
        with open(os.path.join("temp",file[i].name),"wb") as f:
            f.write(file[i].getbuffer())

        img_path = f'temp/{file[i].name}'

        if process:
            with st.spinner(text='Processing your image'):
                time.sleep(0.5)
                if crop or takePicture:
                    try:
                        ctpn_predict.crop(img_path)
                    except Exception as e:
                        #st.write(e)
                        st.error("Couldn't process, please retake the image.")
                        st.stop()

                if language=='English':
                    pred = demo.predict(img_path)
                elif language=='Malayalam':
                    pred = demo_mal.predict(img_path)

                if not pred:
                    st.error("Please select the language appropriately!")
                else:
                    st.markdown(" ")
                    st.markdown("**Predicted Text**")
                    st.success(pred)
                    if displayOriginal:
                        st.markdown("**Cropped Input Image**")
                        st.image(img_path)  
                    
                    if doTTS:
                        url = f'http://ivrapi.indiantts.co.in/tts?type=indiantts&text={pred}&api_key=2d108780-0b86-11e6-b056-07d516fb06e1d&user_id=80&action=play&lang=ml_mohita'
                        response = requests.get(url) 
                        if response.status_code == 200: 
                            with open("tts.wav", 'wb') as file: 
                                file.write(response.content) 
                        else: 
                            st.write("Couldn't process text to speech module")

        if file:
            os.remove(img_path)
    return None