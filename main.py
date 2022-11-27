import streamlit as st
from predict_menu import predict_menu
from report_page import report_page
from sidebar_page import sidebar_page
from PIL import Image

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

app_view, demo_view, report_view, comments_view = st.tabs(["App", "Demo", "Report", "Comments"])
st.markdown("&nbsp;  ")

# demo 
with app_view:
    c1, c2 = st.columns(2)
    with c1:
        language = st.radio('Which language to look for in the image?', ["English", "Malayalam"])    

    with c2:
        choice = st.radio('Are you uploading an image cropped to the word?', ["Yes, don't crop (preferred)", "No, crop it"])
        crop = True if choice=="No, crop it" else False

    #st.info("💡 Upload a cropped word image, rather than uncropped, for better prediction accuracy")
    st.markdown(" ")
    uploadTab, takePictureTab = st.tabs(["Upload", "Take a picture"])

    with uploadTab:
        st.markdown("   ")
        file = st.file_uploader(f'Please upload the word image(s):', accept_multiple_files=True)
        st.markdown(" "); st.markdown(" ")
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=1)
        st.markdown(" "); st.markdown(" ")
        if "Process" not in st.session_state:
            st.session_state["Process"] = False
        if "Correct" not in st.session_state:
            st.session_state["Correct"] = False
        if "Incorrect" not in st.session_state:
            st.session_state["Incorrect"] = False
        
        process = st.button('Process', key=3)

        if process:
            predict_menu(file, process, crop, language, displayOriginal, False) 
            st.session_state["Process"] = True

            
        if st.session_state["Process"]:
            if st.button("Correct", key=10):
                st.session_state["Correct"] = True
            if st.button("Incorrect", key=11):
                st.session_state["Incorrect"] = True

        if st.session_state["Correct"]:
            st.balloons()
            st.write("Am I getting better than humans :smirk:")
            st.session_state["Correct"] = False
            st.session_state["Process"] = False
            
        if st.session_state["Incorrect"]:
            st.write("Sorry, maybe I should train more :confounded:")
            st.session_state["Incorrect"] = False
            st.session_state["Process"] = False
            

    with takePictureTab:
        cameraToggle = st.checkbox("Enable camera")
        if cameraToggle:
            file = st.camera_input("Take a picture")

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
            st.write("Am I getting better than humans :smirk:")
            st.session_state["Correct"] = False
            st.session_state["Process"] = False
            
        if st.session_state["Incorrect"]:
            st.write("Sorry, maybe I should train more :confounded:")
            st.session_state["Incorrect"] = False
            st.session_state["Process"] = False


with demo_view:
    st.markdown("**How to use the app:**")
    st.video('sample.mov')

    st.markdown('''**Sample images for testing the application:**''')
    with st.expander("View English sample image:"):
        st.image("demo_eng.jpg")

    with open("demo_eng.jpg", "rb") as f:
        btn = st.download_button(
                label="Download English sample image",
                data=f,
                file_name="english_sample.jpg",
                mime="image/jpg"
                )
    
    with st.expander("View Malayalam sample image:"):
        st.image("demo_mal.jpg")

    with open("demo_mal.jpg", "rb") as f:
        btn = st.download_button(
                label="Download Malayalam sample image",
                data=f,
                file_name="malayalam_sample.jpg",
                mime="image/jpg"
                )

# report
with report_view:
    report_page()


with comments_view:
    st.info("⚙️ The comments section is under development.")