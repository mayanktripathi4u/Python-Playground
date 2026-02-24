from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langcjain_core.runnable import RunnablePassthrough
from langchain_common.vectorstores import Chroma
from langchain_openai.chat_models import ChatOpenAI
from unstructured.partition.auto import partition
import streamlit as st
from langchain import hub
import os
import logging
from dotenv import load_dotenv

load_dotenv()

prompt = hub.pull("rlm/rag-prompt", refresh=True)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.6)

# Load and extract text from one or multiple files (pdf, docx, txt, pptx, csv, xlsx etc.)
def load_documents(file_path):
    all_text = []
    for file in file_path:
        elements = partition(filename = file)
        text_elements = [el.text for el in elements if el.text is not None]
        # all_text.extend(text_elements)
        all_text.append("\n\n".join(text_elements))

    print(f"Loaded {len(all_text)} documents")
    return "\n\n".join(all_text)    


# Split a long text into smaller chunks, uses token-based splitting
def split_text(text):
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size = 1000,
        chunk_overlap = 300,
        # length_function = len,
    )
    print(f"Original text length: {len(text)}")
    print(f"Splitting text into chunks of size {text_splitter.chunk_size} with overlap {text_splitter.chunk_overlap}")
    chunks = text_splitter.split_text(text)
    print(f"Split into {len(chunks)} chunks")
    return chunks


# Create embeddings and load chunks to Vector Stores. Here we use Chroma, you can also use FAISS or Pinecone etc.
def get_vectorstore(chunks):
    # embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    embeddings = OpenAIEmbeddings()
    # vectorstore = FAISS.from_texts(chunks, embedding)
    vectorstore = Chroma.from_texts(chunks, embeddings, collection_name="rag-collection")
    print(f"Created vectorstore with {vectorstore._collection.count()} vectors")
    return vectorstore


# Format Retrieved documents into a single string
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])


# Build and run the RAG chain
def rag_chain(vectorstore, query):
    qa_chain = (
        {
            "context": vectorstore.as_retriever() |format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return qa_chain.invoke({"question": query})

# Generate temporary file path for uploaded files
def _get_file_path(file_upload):
    temp_dir = "tempDir"
    os.makedirs(temp_dir, exist_ok=True) # enure temp directory exists

    if isinstnace(file_upload, str):
        file_path = file_upload
    else:
        file_path = os.path.join(temp_dir, file_upload.name)
        with open(file_path, "wb") as f:
            f.write(file_upload.getbuffer())
    return file_path


# Streamlit UI: Main function to run the app
def main():
    st.title("RAG Chatbot for multiple document types")
    logging.info("App started")

    if 'message' not in st.session_state:
        st.session_state['message'] = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I am a RAG chatbot. Upload your documents and ask me anything about them."
                ),
            }
        ]

    file_upload = st.sidebar.file_uploader(
        label="Upload",
        type=["pdf", "docx", "txt", "pptx", "csv", "xlsx"],
        accept_multiple_files=True,
        key="file_uploader",
    )

    if file_upload:
        st.success("File(s) uploaded successfully! \n You can now ask questions about the content.")

    # Display existing messages
    for msg in st.session_state['message']:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_prompt = st.chart_input("Ask a question about the documents")

    # For user message
    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)
    
        # Stream assistant response
        with st.chat_message("assistant"):
            logging.info("Processing user query")
            with st.spinner("Thinking..."):

                file_paths = [_get_file_path(f) for f in file_upload] if file_upload else []
                text = load_documents(file_paths)
                chunked_text = split_text(text)
                vectorstore = get_vectorstore(chunked_text)
                assistant_response = rag_chain(vectorstore, user_prompt)

                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                st.markdown(assistant_response)
                logging.info("Response generated")


if __name__ == "__main__":
    main()
    