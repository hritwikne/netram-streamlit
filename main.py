import streamlit as st
from predict_menu import predict_menu
from report_page import report_page
from sidebar_page import sidebar_page

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
                          ["Yes, don't crop (preferred)", "No, crop it automatically"])
        crop = True if choice=="No, crop it automatically" else False

    with st.expander("Why is a cropped word image a preferred input?"):
        st.markdown('''
        For an input image that is not cropped down to the word, two machine learning models are used in this application: 
        (1) detecting text in the image and cropping it, and (2) recognising the word in that cropped image.  

        So providing an uncropped image would pass it through two different models, thus multiplying the error rates.
        Therefore, for better predictions, provide a cropped word image so that only the recognition system has to be activated.  

        *Check out the demo page to see what a cropped word image is.*
        ''')

    st.markdown(" ")
    uploadTab, takePictureTab = st.tabs(["Upload", "Take a picture"])

    with uploadTab:
        st.markdown("   ")
        file = st.file_uploader(f'Please upload the word image(s):', accept_multiple_files=True)
        st.markdown(" "); st.markdown(" ")
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=1)
        doTTS = st.checkbox("Do text to speech after recognising the text", key=9)
        st.markdown(" "); st.markdown(" ")
        
        process = st.button('Process', key=3)
        if process:
            predict_menu(file, process, crop, language, displayOriginal, doTTS, False)
            if doTTS:
                st.audio("tts.wav", format="audio/wav")

    with takePictureTab:
        space(1)
        cameraToggle = st.checkbox("Enable camera")
        st.info("Please provide camera access when prompted.")

        if cameraToggle:
            file = st.camera_input("Take a picture")

        space(2)
        displayOriginal = st.checkbox('Show the cropped input word image along with the result', key=2)
        doTTS = st.checkbox("Do text to speech after recognising the text", key=10)
        st.markdown(" "); st.markdown(" ")

        process = st.button('Process', key=4)
        if process:
            file = [file]
            predict_menu(file, process, crop, language, displayOriginal, doTTS, True) 
            if doTTS:
                st.audio("tts.wav", format="audio/wav")


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
    please send me a mail at **hritwikdileep@gmail.com**
    ''')