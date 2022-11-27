import streamlit as st
from predict_menu import predict_menu
from report_page import report_page
from sidebar_page import sidebar_page

# Webpage title
st.set_page_config(page_title='Netram')

# sidebar
with st.sidebar:
    sidebar_page()


# Main headers
st.title("Netram")
demo_view, report_view = st.tabs(["Demo", "Report"])


# demo 
with demo_view:
    c1, c2 = st.columns(2)
    with c1:
        language = st.radio('Which language to look for in the image?', ["English", "Malayalam"])    

    with c2:
        choice = st.radio('Are you uploading a cropped word image?', ["Yes, don't crop", "No, crop it"])
        crop = False if choice=="Yes, don't crop" else True

    st.markdown(" "); st.markdown(" ")
    uploadTab, takePictureTab = st.tabs(["Upload", "Take a picture"])

    with uploadTab:
        st.markdown("   ")
        st.info("Upload a cropped word image for better prediction accuracy")
        file = st.file_uploader(f'Please upload the word image(s):', accept_multiple_files=True)
        st.markdown(" "); st.markdown(" ")
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=1)
        st.markdown(" "); st.markdown(" ")
        process = st.button('Process', key=3)

        if process:
            predict_menu(file, process, crop, language, displayOriginal, False)                    

    with takePictureTab:
        st.info("Upload a cropped word image for better prediction accuracy")
        cameraToggle = st.checkbox("Enable camera")
        if cameraToggle:
            file = st.camera_input("Take a picture")

        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=2)
        st.markdown(" "); st.markdown(" ")
        process = st.button('Process', key=4)
        
        if process:
            file = [file]
            predict_menu(file, process, crop, language, displayOriginal, True)


# report
with report_view:
    report_page()