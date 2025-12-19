import os
import json
from typing import List, Dict, Any, Optional
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import random
import asyncio
from model_service import ModelService

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
        
        # Initialize Embeddings (using OpenAI by default)
        print("Initializing Embeddings...")
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
        except Exception as e:
            print(f"Error initializing Embeddings: {e}")
        
        # Model Service for multi-model support
        self.model_service = ModelService()
        print("RAGAgent initialization complete.")

    async def generate_questions(
        self, 
        subject: str, 
        difficulty: str, 
        count: int, 
        exam_type: Optional[str] = None,
        model_provider: Optional[str] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        subject = subject.strip()
        
        # Get default config if not specified
        if model_provider is None or model_name is None:
            default_config = ModelService.get_default_config()
            model_provider = model_provider or default_config["provider"]
            model_name = model_name or default_config["model_name"]
            temperature = temperature if temperature is not None else default_config["temperature"]
        
        print(f"\n{'='*60}")
        print(f"QUESTION GENERATION REQUEST:")
        print(f"  Exam Type: {exam_type or 'General'}")
        print(f"  Subject: {subject}")
        print(f"  Difficulty: {difficulty}")
        print(f"  Count: {count}")
        print(f"  Model: {model_provider}/{model_name}")
        print(f"  Temperature: {temperature}")
        print(f"  Mode: RAG-FIRST with LLM Fallback")
        print(f"{'='*60}\n")
        
        # Perform retrieval once to get context for all batches
        try:
            # 1. Retrieve Context from Pinecone
            try:
                # Enhanced query that includes difficulty level for better semantic matching
                # Add negative context to push away other subjects
                other_subjects = "Physics Chemistry" if subject.lower() == "maths" else \
                               "Maths Chemistry" if subject.lower() == "physics" else \
                               "Maths Physics" if subject.lower() == "chemistry" else "other subjects"
                               
                query_text = f"{difficulty} level {subject} concepts, problems, and theory. NOT {other_subjects}."
                print(f"Querying Pinecone with: '{query_text}'")
                
                # Create embedding for the query
                query_embedding = self.embeddings.embed_query(query_text)
                
                # Dynamic top_k based on requested count
                dynamic_top_k = max(60, count * 5)
                
                # Query Pinecone
                results = self.index.query(
                    vector=query_embedding,
                    top_k=dynamic_top_k,
                    include_metadata=True,
                    filter={"subject": {"$in": [subject.lower(), "mixed"]}}
                )
                
                # Randomization
                import time
                random_seed = int(time.time() * 1000) + random.randint(1, 10000)
                random.seed(random_seed)
                
                all_matches = results['matches']
                if all_matches:
                    valid_matches = [m for m in all_matches if 'text' in m['metadata']]
                    target_context_count = max(20, count * 2)
                    
                    if len(valid_matches) > target_context_count:
                        # Use random.sample to pick unique elements
                        selected_matches = random.sample(valid_matches, target_context_count)
                    else:
                        selected_matches = valid_matches
                        
                    random.shuffle(selected_matches)
                    results['matches'] = selected_matches
                
            except Exception as rag_error:
                print(f"⚠️ RAG RETRIEVAL FAILED: {rag_error}")
                results = {'matches': []}
            
            # Extract context
            contexts = []
            source_files = []
            
            for match in results['matches']:
                if 'text' in match['metadata']:
                    contexts.append(match['metadata']['text'])
                    source = match['metadata'].get('source', 'Unknown')
                    if source not in source_files:
                        source_files.append(source)
            
            context_str = "\n\n".join(contexts)
            
            # Determine generation mode
            using_rag = bool(context_str)
            if not using_rag:
                print("⚠️ RAG STATUS: NO CONTEXT AVAILABLE - SWITCHING TO LLM FALLBACK")
            else:
                print(f"✅ RAG STATUS: Using RAG CONTEXT ONLY ({len(contexts)} chunks)")

            # Batch Processing
            BATCH_SIZE = 5
            num_batches = (count + BATCH_SIZE - 1) // BATCH_SIZE
            print(f"🚀 Starting parallel generation: {count} questions in {num_batches} batches...")
            
            tasks = []
            for i in range(num_batches):
                batch_count = min(BATCH_SIZE, count - i * BATCH_SIZE)
                task = self._generate_batch_async(
                    subject, difficulty, batch_count, context_str, exam_type, 
                    using_rag, i + 1, num_batches, model_provider, model_name, temperature
                )
                tasks.append(task)
            
            # Use asyncio.gather to run in parallel
            batch_results = await asyncio.gather(*tasks)
            
            # Flatten results
            all_questions = []
            for batch in batch_results:
                all_questions.extend(batch)
            
            # Final validation and cleanup
            # Filter out dependent questions
            all_questions = self._filter_independent_questions(all_questions)
            
            # Trim or pad if necessary (though batching should prevent this)
            if len(all_questions) > count:
                all_questions = all_questions[:count]
            
            # Re-index IDs sequentially
            for i, q in enumerate(all_questions):
                q['id'] = str(i + 1)
                q['subject'] = subject
                q['difficulty'] = difficulty
                
            print(f"✅ FINAL COMPLETE: Generated {len(all_questions)} questions in total")
            return all_questions

        except Exception as e:
            print(f"❌ GLOBAL ERROR in generate_questions: {e}")
            import traceback
            traceback.print_exc()
            return [{
                "id": "error",
                "text": "Error generating questions. Please try again.",
                "options": ["Error", "Error", "Error", "Error"],
                "correctAnswer": 0,
                "explanation": str(e)
            }]

    def _filter_independent_questions(self, questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out questions that are dependent on other questions.
        Returns only independent, standalone questions.
        """
        # Patterns that indicate question dependency
        dependency_patterns = [
            # Direct references to other questions
            r'\b(?:previous|above|earlier|prior|preceding)\s+(?:question|problem|example)\b',
            r'\b(?:question|problem|Q)\s*(?:#|number|no\.?)\s*\d+\b',
            r'\bfrom\s+(?:the\s+)?(?:previous|above|earlier)\b',
            r'\bas\s+(?:shown|given|stated|mentioned)\s+(?:in|above|earlier|previously)\b',
            
            # References to "the question" or "this question" in dependent context
            r'\busing\s+(?:the\s+)?(?:result|answer|value)\s+from\b',
            r'\bbased\s+on\s+(?:the\s+)?(?:previous|above|earlier)\b',
            r'\brefer(?:ring)?\s+to\s+(?:the\s+)?(?:previous|above|earlier)\b',
            
            # Continuation phrases
            r'\bcontinuing\s+from\b',
            r'\bin\s+continuation\b',
            r'\bfollowing\s+from\s+(?:the\s+)?(?:previous|above)\b',
            
            # Part references
            r'\bpart\s+\(?\s*[a-z]\s*\)?\s*of\s+(?:the\s+)?(?:question|problem)\b',
            r'\b(?:sub)?part\s+\d+\b',
        ]
        
        import re
        independent_questions = []
        filtered_count = 0
        
        for q in questions:
            question_text = q.get('text', '').lower()
            is_dependent = False
            
            # Check against all dependency patterns
            for pattern in dependency_patterns:
                if re.search(pattern, question_text, re.IGNORECASE):
                    is_dependent = True
                    filtered_count += 1
                    print(f"  🚫 Filtered dependent question: '{q.get('text', '')[:60]}...'")
                    break
            
            if not is_dependent:
                independent_questions.append(q)
        
        if filtered_count > 0:
            print(f"  ✅ Filtered out {filtered_count} dependent questions, {len(independent_questions)} independent questions remain")
        
        return independent_questions

    async def _generate_batch_async(
        self, subject: str, difficulty: str, count: int, 
        context_str: str, exam_type: str, using_rag: bool, 
        batch_num: int, total_batches: int,
        model_provider: str, model_name: str, temperature: float
    ) -> List[Dict[str, Any]]:
        """
        Helper method to generate a batch of questions asynchronously.
        Handles its own retries.
        """
        # Get LLM instance for this batch
        llm = self.model_service.get_model(
            provider=model_provider,
            model_name=model_name,
            temperature=temperature
        )
        print(f"  ⚡ Starting Batch {batch_num}/{total_batches} ({count} questions)...")
        max_attempts = 2
        
        for attempt in range(max_attempts):
            try:
                random_seed = random.randint(1, 10000)
                
                # Construct Prompt
                if not using_rag:
                    # FALLBACK PROMPT
                    exam_context = ""
                    if exam_type:
                        exam_context = f"\nExam Type: {exam_type}"
                    
                    prompt = f"""You are an expert exam setter.
{exam_context}
Generate EXACTLY {count} UNIQUE questions about {subject}.
Difficulty: {difficulty}
Random Seed: {random_seed}

IMPORTANT: Each question MUST be completely INDEPENDENT. Do NOT reference other questions.

Return a JSON array with EXACTLY {count} objects:
[
  {{
    "text": "Question text?",
    "options": ["A", "B", "C", "D"],
    "correctAnswer": 0,
    "explanation": "Exp"
  }}
]
"""
                else:
                    # RAG PROMPT
                    prompt = f"""Generate EXACTLY {count} questions about {subject} using the context below.
Difficulty: {difficulty}
Random Seed: {random_seed}

CONTEXT:
{context_str[:15000]} 

CRITICAL RULES:
1. ONLY use the context.
2. Each question MUST be completely INDEPENDENT - do NOT reference other questions.
3. NO phrases like "previous question", "above question", "question X", "based on earlier".
4. Each question must be answerable standalone.
5. Clean the data (no "Q1" prefixes).
6. Return VALID JSON array.

Return a JSON array with EXACTLY {count} objects:
[
  {{
    "text": "Question text?",
    "options": ["A", "B", "C", "D"],
    "correctAnswer": 0,
    "explanation": "Exp"
  }}
]
"""
                # Call LLM Async
                response = await llm.ainvoke(prompt)
                content = response.content.strip()
                
                # Clean markdown
                if content.startswith("```json"): content = content[7:]
                if content.startswith("```"): content = content[3:]
                if content.endswith("```"): content = content[:-3]
                content = content.strip()
                
                questions = json.loads(content)
                
                if len(questions) == count:
                    print(f"  ✅ Batch {batch_num} success: {len(questions)} questions")
                    return questions
                
                # If count mismatch, retry or simple fix
                print(f"  ⚠️ Batch {batch_num} count mismatch: got {len(questions)}, wanted {count}")
                if len(questions) > count:
                    return questions[:count]
                
                # If too few, retry if attempts left
                if attempt < max_attempts - 1:
                    continue
                    
                # Last attempt, return what we have (outer logic handle padding if strictly needed, 
                # but for now we just return what we got to avoid infinite loops)
                return questions
                
            except Exception as e:
                print(f"  ❌ Batch {batch_num} error (attempt {attempt+1}): {e}")
                if attempt < max_attempts - 1:
                    continue
        
        # Determine failure fallback
        print(f"  ❌ Batch {batch_num} failed all attempts.")
        # Return fallback error questions to avoid crashing the whole generation
        return [{
            "text": f"Error generating question in batch {batch_num}",
            "options": ["Error", "Error", "Error", "Error"],
            "correctAnswer": 0,
            "explanation": "Generation failed"
        }] * count

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
