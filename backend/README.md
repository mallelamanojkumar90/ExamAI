# ExamAI RAG Backend

This is the Python backend for the ExamAI platform. It handles question generation using RAG (Retrieval-Augmented Generation) and document ingestion.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment**:
    *   Open `rag_service.py`.
    *   Add your Pinecone API Key, OpenAI/Gemini API Key, and Index Name.
    *   Implement the `generate_questions` and `ingest_document` methods with your existing RAG logic.

3.  **Run the Server**:
    ```bash
    python main.py
    ```
    The server will start at `http://localhost:8000`.

## API Endpoints

*   `POST /generate-questions`: Generates questions based on subject and difficulty.
*   `POST /upload-document`: Uploads a PDF for indexing.
