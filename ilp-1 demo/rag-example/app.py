import streamlit as st
import pandas as pd
import os
from groq import Groq

# Set API Key
GROQ_API_KEY = "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"
if not GROQ_API_KEY:
    st.error("Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Initialize Groq Client
groq_client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI
st.title("📊 Advanced Excel Data Analyzer with AI")
st.write("Upload an Excel file and ask questions like 'What is the mean of this column?'")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "csv"])

if uploaded_file:
    # Read Excel File
    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(".xlsx") else pd.read_csv(uploaded_file)
    
    # Display Data
    st.subheader("📜 Uploaded Data Preview")
    st.dataframe(df.head(10))  # Show first 10 rows for better context

    # Allow users to select a column for analysis
    selected_column = st.selectbox("📊 Select a column to analyze:", df.columns)

    if selected_column:
        st.subheader(f"📈 Analysis for: {selected_column}")

        # Display basic statistics
        st.write(df[selected_column].describe())

        # Plot histogram for numeric columns
        if pd.api.types.is_numeric_dtype(df[selected_column]):
            st.bar_chart(df[selected_column])

    # User Question
    query = st.text_input("🧐 Ask a question about the data:")

    if query:
        # Convert DataFrame to summarized text for better AI context
        summary = df.describe().to_string()
        sample_data = df.head(5).to_string()

        # AI-enhanced prompt
        prompt = f"""You are a data analyst. Use the following dataset to answer the user's query.
        \n\n📊 Data Summary:\n{summary}
        \n\n📝 Sample Data:\n{sample_data}
        \n\nUser Question: {query}
        \n\nProvide a detailed but concise answer:"""

        st.write("🤖 AI is analyzing your data...")
        response_area = st.empty()

        # Stream response from Groq
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an AI data analyst."},
                {"role": "user", "content": prompt},
            ],
            stream=True
        )

        result_text = ""
        for chunk in response:
            if chunk.choices:
                result_text += chunk.choices[0].delta.content or ""
                response_area.markdown(result_text)
