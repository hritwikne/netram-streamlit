import time
from english import demo
from malayalam import demo_mal
from text_detection import ctpn_predict
import streamlit as st
import os

def predict_menu(file, process, crop, language, displayOriginal, takePicture=False):
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

        if file:
            os.remove(img_path)
    return None