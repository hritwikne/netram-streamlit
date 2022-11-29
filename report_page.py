import streamlit as st
def space(num_lines=1):
    """Adds empty lines to the Streamlit app."""
    for _ in range(num_lines):
        st.write("")

def report_page():
    st.info("⚙️ The report is under development.")
    space(1)

    st.markdown('''
    ### References  
    > [*Mathew et al* &nbsp; - &nbsp; Benchmarking Scene Text Recognition in Devanagari, Telugu and Malayalam]("https://cdn.iiit.ac.in/cdn/cvit.iiit.ac.in/images/ConferencePapers/2017/Benchmarkingtelugu_malayalam.pdf")  
    > [*Tian et al* &nbsp; - &nbsp; Detecting Text in Natural Image with Connectionist Text Proposal Network]("https://arxiv.org/abs/1609.03605")  
    ***  
    ''')