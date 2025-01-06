import os
import streamlit as st
import pickle
import time
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from dotenv import load_dotenv
from get_details import extract_linkedin_job_html 

load_dotenv()
st.title("Get your Cold email for job!")
st.sidebar.title("Edit Details for yourself")


# Define file paths
faiss_index_path = "faiss_index"
metadata_path = "metadata.pkl"
# Define LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

with st.sidebar:
        st.header("Enter Your Details")
    #Input fields
        name = st.text_input("Name")
        college = st.text_input("College")
        skills = st.text_area("Skills (comma-separated)")
        achievements = st.text_area("Achievements")
    # Display input summary
        st.subheader("Your Profile Details")
        st.write(f"**Name:** {name}")
        st.write(f"**College:** {college}")
        st.write(f"**Skills:** {skills}")
        st.write(f"**Achievements:** {achievements}")

    # Storing inputs in a dictionary
profile_data = {
        "name": name,
        "college": college,
        "skills": skills.split(",") if skills else [],
        "achievements": achievements
    }

st.subheader("Enter Job Posting Link")
job_url = st.text_input("Job URL", placeholder="Paste the job posting link here")

raw_html=""
if st.button("Generate cold email"):
        if not job_url:
                st.error("Enter a valid job URL")
        elif not name or not skills:
                st.error("Enter valid profile details")
        else:
                st.info("Generating job posting and cold email for you")

        username=os.environ["LINKEDIN_USERNAME"]
        password=os.environ["LINKEDIN_PASSWORD"]
        
        
        # username = st.secrets["LINKEDIN_USERNAME"]
        # password = st.secrets["LINKEDIN_PASSWORD"]
        raw_html = extract_linkedin_job_html(job_url, username, password)

result=""
email_text=""
if raw_html:
        #extract meaningful content from HTML
        text_splitter=RecursiveCharacterTextSplitter(
                chunk_size=1000,chunk_overlap=100
        )
        job_docs=text_splitter.split_text(raw_html)
        #creating vector embedding
                    # Embed job descriptions
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_texts(job_docs, embeddings)

            # Save FAISS index
        vector_store.save_local(faiss_index_path)

            # Generate cold email
        query = (
                f"Write a cold email for the following job description using this profile: "
                f"\n\nJob Description: {job_docs[:2]}..."  # Include a snippet of job docs
                f"\n\nProfile: {profile_data}"
                "in the very beginning show a list of things required for the job description(requirements),regardless if i have them in my  profile or not"
        )
        result = llm.generate([query])
        print(result)
        print("hi")
# Assuming result contains the response as described
if hasattr(result, 'generations') and isinstance(result.generations, list):
    # Access the first list in 'generations'
    if len(result.generations) > 0 and isinstance(result.generations[0], list):
        # Access the first ChatGeneration object in the nested list
        first_chat_generation = result.generations[0][0]
        
        # Check if it has the 'text' attribute
        if hasattr(first_chat_generation, 'text'):
            email_text = first_chat_generation.text
            print(f"Extracted email text:\n{email_text}")
        else:
            print("Error: The first ChatGeneration object does not have a 'text' attribute.")
    else:
        print("Error: The 'generations' list is empty or improperly formatted.")
else:
    print("Error: The 'result' object does not have a 'generations' attribute or it's not a list.")
st.write(email_text)