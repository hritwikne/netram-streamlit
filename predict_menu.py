import time
from english import demo
from malayalam import demo_mal
from text_detection import ctpn_predict
import streamlit as st
import os
import requests

def translate(text):  
    API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom" 
    instruction =  f"""Translation in Malayalam: {text.strip()}<end> Translation in English:"""  
 
    json_ = { 
        "inputs": instruction, 
        "parameters": { 
            "return_full_text": True, 
            "do_sample": False, 
            "max_new_tokens": 250, 
        },  
        "options": { 
            "use_cache": True, 
            "wait_for_model": True, 
            }, 
    } 
    response = requests.request("POST", API_URL,  json=json_).json()[0] 
    error = response.get('error') 
    output = response.get('generated_text') 
    output = output.replace(instruction, '', 1) 
    return output.split('\nTranslation in Malayalam:')[0], error 

def predict_menu(file, process, crop, language, displayOriginal, doTTS, doTranslate, takePicture=False):
    for i in range(len(file)):
        with open(os.path.join("temp",file[i].name),"wb") as f:
            f.write(file[i].getbuffer())

        img_path = f'temp/{file[i].name}'

        if process:
            with st.spinner(text='Processing your image'):
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
                    if doTranslate and language=='Malayalam':
                        search_word = pred
                        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"}
                        response = requests.get(f'https://www.shabdkosh.com/search-dictionary?lc=ml&sl=en&tl=ml&e={search_word}',headers=headers)
                        x = response.text.split('e in l ms-2')[1].split('<')[0].split('>')[1]
                        success_message = pred + ' - ' + x
                        st.success(success_message)
                    else:    
                        st.success(pred)
                    link = f'[Web Search](https://www.google.com/search?q={pred})'
                    st.markdown(link, unsafe_allow_html=True)
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if doTTS:
                            url = f'http://ivrapi.indiantts.co.in/tts?type=indiantts&text={pred}&api_key=2d108780-0b86-11e6-b056-07d516fb06e1d&user_id=80&action=play&lang=ml_mohita'
                            response = requests.get(url) 
                            if response.status_code == 200: 
                                with open("tts.wav", 'wb') as file: 
                                    file.write(response.content) 
                                    st.audio("tts.wav", format="audio/wav")
                            else: 
                                st.write("Couldn't process text to speech module")
                    if displayOriginal:
                        st.markdown("**Cropped Input Image**")
                        st.image(img_path)

        if file:
            os.remove(img_path)
    return None