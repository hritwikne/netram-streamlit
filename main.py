import streamlit as st
from predict_menu import predict_menu
from report_page import report_page
from sidebar_page import sidebar_page
from datetime import datetime
import pandas as pd

COMMENT_TEMPLATE_MD = """**{} &nbsp;&nbsp; - &nbsp;&nbsp; {}** 
> {}"""

def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")


# Webpage title
st.set_page_config(
    page_title='Netram',
    page_icon="👁️"
    )

# sidebar
with st.sidebar:
    sidebar_page()


# Main headers
st.markdown('''
    # Netram  
    &nbsp;  
    **What does this app do?**  
    Given the image of a (isolated) word in a natural scene (like billboards, banners), 
    the app predicts the text in the image. This problem is formally stated as **Scene Text Recognition**.  
      
    *Check out the demo and report below for more details.*  

''')

app_view, demo_view, report_view, contact_view = st.tabs(["App", "Demo", "Report", "Contact"])
st.markdown("&nbsp;  ")

# demo 
with app_view:
    c1, c2 = st.columns(2)
    with c1:
        language = st.radio('Which language to look for in the image?', ["English", "Malayalam"], index=1)  

    with c2:
        choice = st.radio('Are you uploading an image cropped to the word?', 
                          ["Yes, don't crop (preferred)", "No, crop it automatically"],
                          help="💡 **For better prediction accuracy, provide an image that is cropped to just the word that needs to be recognised. Please refer the *demo* page for an example of what this means.**")
        crop = True if choice=="No, crop it automatically" else False

    #st.info("💡 Upload a cropped word image, rather than uncropped, for better prediction accuracy")
    st.markdown(" ")
    uploadTab, takePictureTab = st.tabs(["Upload", "Take a picture"])

    with uploadTab:
        st.markdown("   ")
        file = st.file_uploader(f'Please upload the word image(s):', accept_multiple_files=True)
        st.markdown(" "); st.markdown(" ")
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=1)
        st.markdown(" "); st.markdown(" ")
        
        process = st.button('Process', key=3)
        if process:
            predict_menu(file, process, crop, language, displayOriginal, False)

    with takePictureTab:
        space(1)
        cameraToggle = st.checkbox("Enable camera")
        st.info("Please provide camera access when prompted.")

        if cameraToggle:
            file = st.camera_input("Take a picture")

        space(2)
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=2)
        st.markdown(" "); st.markdown(" ")
        if "Process" not in st.session_state:
            st.session_state["Process"] = False
        if "Correct" not in st.session_state:
            st.session_state["Correct"] = False
        if "Incorrect" not in st.session_state:
            st.session_state["Incorrect"] = False

        process = st.button('Process', key=4)
        if process:
            file = [file]
            predict_menu(file, process, crop, language, displayOriginal, True) 
            st.session_state["Process"] = True
            
        if st.session_state["Process"]:
            if st.button("Correct :thumbsup:", key=12):
                st.session_state["Correct"] = True
            if st.button("Incorrect :thumbsdown:", key=13):
                st.session_state["Incorrect"] = True

        if st.session_state["Correct"]:
            st.balloons()
            st.success("Am I getting better than humans :smirk:")
            st.session_state["Correct"] = False
            st.session_state["Process"] = False
            
        if st.session_state["Incorrect"]:
            st.error("Sorry, maybe I should train more :confounded:")
            st.session_state["Incorrect"] = False
            st.session_state["Process"] = False


with demo_view:
    st.markdown("**How to use the app:**")
    st.video('media/sample.mov')
    st.markdown("***")
    st.markdown('''**What is a cropped word image?**''')
    
    with st.expander("View a normal word image"):
        st.image("media/demo_eng.jpg")
    
    with st.expander("View its cropped word image"):
        st.image("media/cropped_demo.png")

    st.markdown("***")

    st.markdown('''**Need some sample images for testing the application?**''')

    with open("media/demo_eng.jpg", "rb") as f:
        btn = st.download_button(
                label="Download English sample image",
                data=f,
                file_name="english_sample.jpg",
                mime="image/jpg"
                )

    with open("media/demo_mal.jpg", "rb") as f:
        btn = st.download_button(
                label="Download Malayalam sample image",
                data=f,
                file_name="malayalam_sample.jpg",
                mime="image/jpg"
                )

    

# report
with report_view:
    report_page()


with contact_view:
    st.markdown('''
    For any queries, concerns, or suggestions,  
    please send us a mail at **hritwikdileep@gmail.com**
    ''')