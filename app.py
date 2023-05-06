from dotenv import load_dotenv
import os
import streamlit as st


def main():
    load_dotenv()
    print('Hello World')
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask yout PDF 😁")

    pdf = st.file_uploader("Upload your PDF",type="pdf")
    # print(os.getenv("OPENAI_API_KEY"))

if __name__ == '__main__':
    main()