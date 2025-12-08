import os
import json
from typing import List, Dict, Any
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import random

# OCR dependencies
import fitz  # PyMuPDF for rendering pages
from PIL import Image
import pytesseract

# Configure Tesseract path for Windows
# Check common installation locations
tesseract_paths = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Users\malle\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
]
for path in tesseract_paths:
    if os.path.exists(path):
        pytesseract.pytesseract.tesseract_cmd = path
        print(f"Found Tesseract at: {path}")
        break

from dotenv import load_dotenv

class RAGAgent:
    def __init__(self):
        print("Initializing RAGAgent...")
        load_dotenv()
        # Initialize Pinecone
        print("Initializing Pinecone...")
        try:
            self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
            self.index = self.pc.Index(os.getenv("PINECONE_INDEX_NAME", "rag-questions"))
            print("Pinecone initialized.")
        except Exception as e:
            print(f"Error initializing Pinecone: {e}")
        
        # Initialize OpenAI
        print("Initializing OpenAI...")
        try:
            # Use text-embedding-3-small which produces 384-dimensional vectors
            # This matches the Pinecone index dimension configuration
            # IMPORTANT: Must explicitly set dimensions=384, as the model defaults to 1536!
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                dimensions=384,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            print(f"Embeddings model: {self.embeddings.model}")
            print(f"Embeddings dimensions: {self.embeddings.dimensions}")
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",  # Using GPT-4o-mini for better instruction following
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
            print("OpenAI initialized.")
        except Exception as e:
            print(f"Error initializing OpenAI: {e}")
        print("RAGAgent initialization complete.")

    def generate_questions(self, subject: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        subject = subject.strip()
        print(f"\n{'='*60}")
        print(f"QUESTION GENERATION REQUEST:")
        print(f"  Subject: {subject}")
        print(f"  Difficulty: {difficulty}")
        print(f"  Count: {count}")
        print(f"  Mode: RAG-ONLY (No LLM fallback)")
        print(f"{'='*60}\n")
        
        # Try up to 2 times to get the correct number of questions
        max_attempts = 2
        
        for attempt in range(max_attempts):
            # Initialize questions to avoid UnboundLocalError
            questions = []
            
            try:
                if attempt > 0:
                    print(f"\n🔄 Retry attempt {attempt + 1}/{max_attempts}...\n")
                
                # 1. Retrieve Context from Pinecone
                try:
                    # Enhanced query that includes difficulty level for better semantic matching
                    # Add negative context to push away other subjects
                    other_subjects = "Physics Chemistry" if subject.lower() == "maths" else \
                                   "Maths Chemistry" if subject.lower() == "physics" else \
                                   "Maths Physics" if subject.lower() == "chemistry" else "other subjects"
                                   
                    query_text = f"{difficulty} level {subject} concepts, problems, and theory. NOT {other_subjects}."
                    print(f"Querying Pinecone with: '{query_text}'")
                    print(f"  Subject Filter: {subject} (and 'mixed')")
                    print(f"  Difficulty Target: {difficulty}")
                    
                    # Create embedding for the query
                    query_embedding = self.embeddings.embed_query(query_text)
                    print(f"Generated embedding with {len(query_embedding)} dimensions")
                    
                    # Dynamic top_k based on requested count to ensure sufficient context
                    # Retrieve MORE chunks than needed to allow for random sampling (variety)
                    dynamic_top_k = max(60, count * 5)
                    print(f"Dynamic top_k set to: {dynamic_top_k} (for {count} questions) - Increased for variety")

                    # Try querying with subject filter first
                    # Allow 'mixed' subject tag as well to capture questions from mixed PDFs
                    results = self.index.query(
                        vector=query_embedding,
                        top_k=dynamic_top_k,
                        include_metadata=True,
                        filter={"subject": {"$in": [subject.lower(), "mixed"]}}
                    )
                    print(f"Pinecone query with filter returned {len(results['matches'])} matches")
                    
                    # ---------------------------------------------------------
                    # RANDOMIZATION STRATEGY FOR VARIETY
                    # ---------------------------------------------------------
                    all_matches = results['matches']
                    if all_matches:
                        # 1. Filter for valid matches
                        valid_matches = [m for m in all_matches if 'text' in m['metadata']]
                        
                        # 2. Randomly sample a subset if we have enough
                        # We want enough context for the LLM, but different subsets each time
                        target_context_count = max(20, count * 2)
                        
                        if len(valid_matches) > target_context_count:
                            print(f"  🎲 Randomly sampling {target_context_count} chunks from {len(valid_matches)} available to ensure variety...")
                            # Use random.sample to pick unique elements
                            selected_matches = random.sample(valid_matches, target_context_count)
                        else:
                            selected_matches = valid_matches
                            
                        # 3. Shuffle the selected matches to avoid order bias
                        random.shuffle(selected_matches)
                        
                        # Replace the original matches with our randomized selection
                        results['matches'] = selected_matches
                    # ---------------------------------------------------------
                    
                except Exception as rag_error:
                    print(f"⚠️ RAG RETRIEVAL FAILED: {rag_error}")
                    print("   Proceeding with empty context to trigger LLM fallback...")
                    results = {'matches': []}
                
                # Extract context text and log what we found
                print(f"\n{'─'*60}")
                print(f"📚 RETRIEVED CONTEXT FROM PINECONE:")
                print(f"{'─'*60}")
                
                contexts = []
                source_files = []
                source_details = []  # Track detailed source info
                using_rag = False
                
                for i, match in enumerate(results['matches']):
                    if 'text' in match['metadata']:
                        contexts.append(match['metadata']['text'])
                        using_rag = True
                        
                        # Extract metadata
                        metadata = match['metadata']
                        score = match['score']
                        source = metadata.get('source', 'Unknown')
                        subject_meta = metadata.get('subject', 'N/A')
                        page = metadata.get('page', 'N/A')
                        
                        # Store source file
                        if source not in source_files:
                            source_files.append(source)
                        
                        # Store detailed source info
                        source_details.append({
                            'file': source,
                            'page': page,
                            'score': score
                        })
                        
                        # Display detailed match info
                        print(f"\n  Match #{i+1}:")
                        print(f"    📄 Source File: {source}")
                        print(f"    📊 Subject: {subject_meta}")
                        print(f"    📖 Page: {page}")
                        print(f"    🎯 Relevance Score: {score:.4f}")
                        print(f"    📝 Text Preview: {metadata['text'][:100]}...")
                
                context_str = "\n\n".join(contexts)
                
                print(f"\n{'─'*60}")
                # Check if we have context
                prompt = None
                
                if not context_str or not using_rag:
                    print("⚠️ RAG STATUS: NO CONTEXT AVAILABLE - SWITCHING TO LLM FALLBACK")
                    print(f"   Reason: No relevant documents found in Pinecone for {subject}")
                    print(f"   Mode: LLM GENERATION (Using internal knowledge)")
                    print(f"{'─'*60}\n")
                    
                    prompt = f"""You are an expert exam setter for IIT/JEE exams.

CRITICAL INSTRUCTIONS:
1. Generate EXACTLY {count} questions about {subject} ONLY.
2. Difficulty: {difficulty}
3. Since no specific documents were found, use your extensive internal knowledge to generate high-quality, relevant questions.
4. STRICTLY ADHERE to the subject: {subject}. Do not generate questions for other subjects.
5. Return ONLY valid JSON.

Return a JSON array with EXACTLY {count} objects in this structure:
[
  {{
    "id": "1",
    "text": "Question text?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctAnswer": 0,
    "explanation": "Brief explanation"
  }},
  ...
]
"""
                else:
                    print(f"✅ RAG STATUS: Using RAG CONTEXT ONLY")
                    print(f"   📚 Total Context Chunks: {len(contexts)}")
                    print(f"   📁 Source Files Used:")
                    for sf in source_files:
                        print(f"      • {sf}")
                    print(f"   Mode: RAG-ONLY (Questions will be based strictly on uploaded documents)")
                    print(f"{'─'*60}\n")

                # 2. Build a strict RAG-only prompt
                if prompt is None and attempt == 0:
                    # First attempt - strict RAG-only prompt
                    # Add a random seed to the prompt to ensure variety
                    random_seed = random.randint(1, 10000)
                    prompt = f"""You are an expert exam setter for IIT/JEE exams.
                    
Randomization Seed: {random_seed} (Generate a unique set of questions different from previous runs)

CRITICAL INSTRUCTIONS - READ CAREFULLY:
1. Generate EXACTLY {count} questions - COUNT THEM: 1, 2, 3... up to {count}
2. ALL questions MUST be about {subject} ONLY.
   - ⚠️ WARNING: The context may contain mixed subjects (e.g., Physics questions in a Maths file).
   - ⚠️ ACTION: You must IGNORE any context that is not strictly {subject}.
   - If you see a Physics question and you need Maths, SKIP IT.
3. Difficulty level: {difficulty}
4. Each question must have exactly 4 options
5. **DATA CLEANING (CRITICAL)**:
   - Remove ALL source artifacts.
   - DO NOT include question numbers from the source (e.g., remove "Q.44", "12.", "Q1", "(a)").
   - The "text" field should contain ONLY the question content, starting with the actual question words.
6. **MOST IMPORTANT**: Generate questions ONLY from the context provided below
7. DO NOT use your general knowledge or training data - ONLY use the provided context
8. Return ONLY valid JSON - no markdown, no explanations, no extra text

DIFFICULTY LEVEL GUIDELINES FOR {difficulty.upper()} QUESTIONS:
{"- EASY: Focus on recall, definitions, basic concepts, and direct facts from the context" if difficulty.lower() == "easy" else ""}
{"- EASY: Questions should test recognition and understanding of fundamental principles" if difficulty.lower() == "easy" else ""}
{"- EASY: Use straightforward language and simple scenarios" if difficulty.lower() == "easy" else ""}
{"- MEDIUM: Require application of concepts, calculations, and problem-solving" if difficulty.lower() == "medium" else ""}
{"- MEDIUM: Combine multiple concepts from the context" if difficulty.lower() == "medium" else ""}
{"- MEDIUM: Include numerical problems and conceptual applications" if difficulty.lower() == "medium" else ""}
{"- HARD: Demand analysis, synthesis, and deep understanding" if difficulty.lower() == "hard" else ""}
{"- HARD: Create multi-step problems requiring integration of concepts" if difficulty.lower() == "hard" else ""}
{"- HARD: Include edge cases, derivations, and complex scenarios" if difficulty.lower() == "hard" else ""}

Context from uploaded documents (USE ONLY THIS INFORMATION):
{context_str}

STRICT REQUIREMENT: Base ALL questions exclusively on the context above. Do not add any information from your training data or general knowledge. Every question should be answerable using only the provided context.

Return a JSON array with EXACTLY {count} objects in this structure:
[
  {{
    "id": "1",
    "text": "Clean question text without Q numbers or artifacts?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctAnswer": 0,
    "explanation": "Brief explanation referencing the specific part of the context"
  }},
  {{
    "id": "2",
    "text": "Another clean {subject} question?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correctAnswer": 1,
    "explanation": "Brief explanation with context reference"
  }}
  ... continue until you have {count} questions total
]

CRITICAL REMINDERS:
- The array must contain EXACTLY {count} question objects
- FILTER OUT content that is not {subject}
- REMOVE "Q." or numbers from the start of question text
- Return ONLY the JSON array, nothing else
"""
                elif prompt is None:
                    # Retry with even more forceful RAG-only prompt
                    prompt = f'''IMPORTANT: You previously generated the wrong number of questions. This time, you MUST generate EXACTLY {count} questions.

CRITICAL: Use ONLY the context provided below. DO NOT use your general knowledge.

You are generating questions for: {subject}
Difficulty: {difficulty}
Number of questions required: {count}

Context from uploaded documents (YOUR ONLY SOURCE):
{context_str}

STRICT RULES:
1. DO NOT generate questions about any other subject. ONLY {subject}.
   - If the context contains Physics/Chemistry but you need Maths, IGNORE the irrelevant parts.
2. CLEAN THE DATA:
   - Remove "Q.", numbers, or artifacts from the start of the question.
   - Example: Change "Q44. What is..." to "What is..."
3. DO NOT use information outside this context.

Count your questions as you generate them:
Question 1: based on context about {subject}
Question 2: based on context about {subject}
Question 3: based on context about {subject}
... continue until Question {count}

Return a JSON array with EXACTLY {count} objects:
[
  {{"id": "1", "text": "Clean {subject} question text?", "options": ["A", "B", "C", "D"], "correctAnswer": 0, "explanation": "..."}},
  {{"id": "2", "text": "Clean {subject} question text?", "options": ["A", "B", "C", "D"], "correctAnswer": 1, "explanation": "..."}},
  ... {count - 2} more questions from the context ...
  {{"id": "{count}", "text": "Clean {subject} question text?", "options": ["A", "B", "C", "D"], "correctAnswer": 2, "explanation": "..."}}
]

The array MUST have {count} elements. Count them before returning.
Return ONLY the JSON array.
ALL questions must come from the provided context ONLY.
'''
                
                print(f"\nSending RAG-ONLY prompt to LLM (requesting {count} {subject} questions from uploaded documents)...")
                response = self.llm.invoke(prompt)
                content = response.content.strip()
                
                print(f"LLM Response length: {len(content)} characters")
                
                # Clean up potential markdown formatting
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                
                # Parse JSON response
                content = content.strip()
                try:
                    questions = json.loads(content)
                    print(f"✅ Successfully parsed JSON response with {len(questions)} questions")
                except json.JSONDecodeError as json_err:
                    print(f"❌ Failed to parse JSON response: {json_err}")
                    print(f"Response preview: {content[:200]}...")
                    raise  # Re-raise to be caught by outer exception handler
                
                # Validate we got the right number of questions
                if len(questions) == count:
                    print(f"✅ SUCCESS: Generated exactly {count} questions from uploaded documents!")
                    
                    # Add detailed source information summary
                    print(f"\n{'='*60}")
                    if source_files:
                        print(f"📊 QUESTION SOURCE SUMMARY (RAG MODE)")
                        print(f"{'='*60}")
                        print(f"✅ Questions generated from {len(source_files)} UPLOADED PDFs")
                        print(f"\n📁 Source Documents Used:")
                        for sf in source_files:
                            print(f"   • {sf}")
                        
                        # Show detailed page information
                        print(f"\n📖 Detailed Source Breakdown:")
                        for detail in source_details:
                            print(f"   • {detail['file']} (Page {detail['page']}) - Relevance: {detail['score']:.4f}")
                        
                        print(f"\n💡 Knowledge Base: Pinecone Vector Database")
                        print(f"🎯 Mode: RAG (Context-aware generation)")
                    else:
                        print(f"📊 QUESTION SOURCE SUMMARY (FALLBACK MODE)")
                        print(f"{'='*60}")
                        print(f"⚠️  No relevant documents found for {subject}")
                        print(f"✅ Questions generated using LLM INTERNAL KNOWLEDGE")
                        print(f"\n💡 Knowledge Base: GPT-4o-mini Training Data")
                        print(f"🎯 Mode: FALLBACK (General knowledge generation)")
                    print(f"{'='*60}")
                    
                    print(f"{'='*60}\n")
                    return questions
                else:
                    print(f"⚠️  WARNING: Generated {len(questions)} questions but {count} were requested!")
                    
                    # If this is not the last attempt, continue to retry
                    if attempt < max_attempts - 1:
                        print(f"Will retry with a more forceful prompt...")
                        continue
                    else:
                        # Last attempt failed - pad or trim to match count
                        print(f"⚠️  Last attempt - adjusting question count...")
                        
                        if len(questions) < count:
                            # Need more questions - duplicate some
                            print(f"Padding from {len(questions)} to {count} questions...")
                            while len(questions) < count:
                                # Duplicate a random question with modified text
                                import random
                                template = random.choice(questions).copy()
                                template['id'] = str(len(questions))
                                template['text'] = f"[Variation] {template['text']}"
                                questions.append(template)
                        elif len(questions) > count:
                            # Too many questions - trim
                            print(f"Trimming from {len(questions)} to {count} questions...")
                            questions = questions[:count]
                        
                        # Re-assign IDs
                        for i, q in enumerate(questions):
                            q['id'] = str(i)
                        
                        # Add detailed source information summary
                        print(f"\n{'='*60}")
                        if source_files:
                            print(f"📊 QUESTION SOURCE SUMMARY (RAG MODE)")
                            print(f"{'='*60}")
                            print(f"✅ Questions generated from {len(source_files)} UPLOADED PDFs")
                            print(f"\n📁 Source Documents Used:")
                            for sf in source_files:
                                print(f"   • {sf}")
                            
                            # Show detailed page information
                            print(f"\n📖 Detailed Source Breakdown:")
                            for detail in source_details:
                                print(f"   • {detail['file']} (Page {detail['page']}) - Relevance: {detail['score']:.4f}")
                            
                            print(f"\n💡 Knowledge Base: Pinecone Vector Database")
                            print(f"🎯 Mode: RAG (Context-aware generation)")
                        else:
                            print(f"📊 QUESTION SOURCE SUMMARY (FALLBACK MODE)")
                            print(f"{'='*60}")
                            print(f"⚠️  No relevant documents found for {subject}")
                            print(f"✅ Questions generated using LLM INTERNAL KNOWLEDGE")
                            print(f"\n💡 Knowledge Base: GPT-4o-mini Training Data")
                            print(f"🎯 Mode: FALLBACK (General knowledge generation)")
                        print(f"{'='*60}")
                        
                        print(f"{'='*60}\n")
                        return questions

            except json.JSONDecodeError as e:
                print(f"\n❌ JSON Parse Error: {e}")
                print(f"Response content: {content[:500]}...")
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    continue
                else:
                    raise
            except Exception as e:
                print(f"\n❌ ERROR in RAG generation: {e}")
                import traceback
                traceback.print_exc()
                if attempt < max_attempts - 1:
                    print("Retrying...")
                    continue
                else:
                    raise
        
        # If we get here, all attempts failed
        print(f"\n❌ All {max_attempts} attempts failed")
        return [
            {
                "id": "error",
                "text": f"Error generating questions after {max_attempts} attempts. Please try again.",
                "options": ["Error", "Error", "Error", "Error"],
                "correctAnswer": 0,
                "explanation": "An error occurred in the backend."
            }
        ]

    def ingest_document(self, file_path: str, subject: str):
        subject = subject.strip()
        print(f"\n{'='*60}")
        print(f"INGESTING DOCUMENT:")
        print(f"  File: {file_path}")
        print(f"  Subject: {subject}")
        print(f"{'='*60}\n")

        try:
            # 1. Load PDF using PyMuPDF (better extraction)
            print("Loading PDF with PyMuPDF...")
            try:
                loader = PyMuPDFLoader(file_path)
                documents = loader.load()
            except Exception as e:
                print(f"PyMuPDF failed: {e}. Falling back to PyPDFLoader...")
                loader = PyPDFLoader(file_path)
                documents = loader.load()
            
            # 2. Check for scanned PDF and apply OCR if needed
            total_text_len = sum(len(doc.page_content.strip()) for doc in documents)
            if total_text_len < 500:
                print("⚠️  WARNING: Very little text detected. Attempting OCR fallback...")
                try:
                    # Verify Tesseract binary is available
                    pytesseract.get_tesseract_version()
                    # Render each page as image and run OCR
                    pdf_doc = fitz.open(file_path)
                    ocr_texts = []
                    for page_num in range(pdf_doc.page_count):
                        print(f"   OCR processing page {page_num + 1}/{pdf_doc.page_count}...")
                        page = pdf_doc.load_page(page_num)
                        pix = page.get_pixmap()
                        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        text = pytesseract.image_to_string(img)
                        ocr_texts.append(text)
                    # Build Document objects from OCR results
                    from langchain_core.documents import Document as LangDoc
                    documents = [LangDoc(page_content=text, metadata={"page": idx+1}) for idx, text in enumerate(ocr_texts)]
                    print(f"✅ OCR extracted text from {len(documents)} pages.")
                except pytesseract.pytesseract.TesseractNotFoundError as tnfe:
                    print(f"❌ Tesseract OCR engine not found: {tnfe}")
                    print("   Install Tesseract on your system and ensure it's in the PATH.")
                    return False
                except Exception as e:
                    print(f"❌ OCR failed: {e}")
                    print("   Please provide a searchable PDF.")
                    return False
                # Re-check text length after OCR
                total_text_len = sum(len(doc.page_content.strip()) for doc in documents)
                if total_text_len < 100:
                    print("❌ OCR did not extract sufficient text. Skipping document.")
                    return False
            
            # 3. Split documents into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                add_start_index=True,
            )
            chunks = text_splitter.split_documents(documents)
            print(f"Created {len(chunks)} chunks.")

            # 4. Create embeddings and prepare for Pinecone
            print("Creating embeddings and preparing for Pinecone...")
            
            vectors = []
            batch_size = 100
            
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                print(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}...")
                
                # Get texts for embedding
                texts = [chunk.page_content for chunk in batch]
                
                # Create embeddings
                embeddings = self.embeddings.embed_documents(texts)
                
                # Prepare vectors with metadata
                for j, chunk in enumerate(batch):
                    # Create a unique ID for the chunk
                    chunk_id = f"{os.path.basename(file_path)}_{i+j}_{int(time.time())}"
                    
                    # Clean up metadata
                    metadata = {
                        "text": chunk.page_content,
                        "source": os.path.basename(file_path),
                        "subject": subject.lower(),
                        "page": chunk.metadata.get("page", 0) + 1, # 1-based page number
                        "chunk_index": i+j
                    }
                    
                    vectors.append({
                        "id": chunk_id,
                        "values": embeddings[j],
                        "metadata": metadata
                    })

            # 4. Upsert to Pinecone
            print(f"Upserting {len(vectors)} vectors to Pinecone...")
            # Upsert in batches of 100
            for i in range(0, len(vectors), 100):
                batch = vectors[i:i+100]
                self.index.upsert(vectors=batch)
                print(f"  Upserted batch {i//100 + 1}/{(len(vectors)-1)//100 + 1}")
            
            print(f"\n✅ Successfully ingested {os.path.basename(file_path)}")
            print(f"   Subject: {subject}")
            print(f"   Chunks: {len(chunks)}")
            print(f"{'='*60}\n")
            
            return True

        except Exception as e:
            print(f"\n❌ Error ingesting document: {e}")
            import traceback
            traceback.print_exc()
            raise
