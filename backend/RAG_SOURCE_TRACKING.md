# RAG Source Tracking - Implementation Summary

## Overview
Enhanced the backend to provide complete transparency about where questions come from - whether they're generated using RAG (Retrieval-Augmented Generation) with your uploaded documents, or pure LLM knowledge.

---

## What's New

### 1. **Detailed Context Retrieval Logging**
Every time questions are generated, you'll see:
- **Source files** that were retrieved from Pinecone
- **Subject metadata** for each document chunk
- **Page numbers** where the content came from
- **Relevance scores** (0-1 scale, higher = more relevant)
- **Text previews** of the retrieved content

### 2. **RAG vs LLM Indicator**
Clear visual indicator showing:
- ✅ **RAG MODE**: Questions use your uploaded documents
- ⚠️ **PURE LLM MODE**: Questions use only LLM's general knowledge

### 3. **Source File Summary**
At the end of each generation, you get a summary showing:
- Total number of source documents used
- List of all PDF files that contributed to the questions
- Knowledge source type (Vector DB + LLM vs LLM only)

---

## Code Changes Made

### File: `rag_service.py`

#### Change 1: Enhanced Context Retrieval (Lines 88-135)
```python
# Now extracts and displays:
- source_files = []  # Track which files were used
- using_rag = False  # Flag to indicate RAG vs pure LLM

# For each Pinecone match:
- Source file name
- Subject metadata
- Page number
- Relevance score
- Text preview
```

#### Change 2: RAG Status Indicator (Lines 122-135)
```python
if not context_str or not using_rag:
    print("⚠️  RAG STATUS: Using PURE LLM KNOWLEDGE")
else:
    print("✅ RAG STATUS: Using RAG CONTEXT")
    print(f"   📁 Source Files Used:")
    for sf in source_files:
        print(f"      • {sf}")
```

#### Change 3: Question Source Summary (Lines 237-252, 286-301)
```python
# Added at the end of successful generation:
print("📊 QUESTION SOURCE SUMMARY:")
if using_rag and source_files:
    print("✅ Questions generated using RAG")
    print(f"   📁 Documents Used ({len(source_files)}):")
    for sf in source_files:
        print(f"      • {sf}")
else:
    print("⚠️  Questions generated using PURE LLM KNOWLEDGE")
```

---

## How to Use

### Step 1: Generate Questions
Use your frontend to request questions:
- Subject: Any subject (Physics, Chemistry, Maths, etc.)
- Difficulty: easy/medium/hard
- Count: Number of questions (1-20)

### Step 2: Check Terminal Output
Open the backend terminal (`py main.py`) and look for:

**Section 1: Retrieved Context**
```
📚 RETRIEVED CONTEXT FROM PINECONE:
────────────────────────────────────
  Match #1:
    📄 Source File: physics_chapter5.pdf
    📊 Subject: physics
    📖 Page: 23
    🎯 Relevance Score: 0.8523
```

**Section 2: RAG Status**
```
✅ RAG STATUS: Using RAG CONTEXT
   📚 Total Context Chunks: 5
   📁 Source Files Used:
      • physics_chapter5.pdf
      • jee_physics_problems.pdf
```

**Section 3: Question Source Summary**
```
📊 QUESTION SOURCE SUMMARY:
────────────────────────────────────
✅ Questions generated using RAG
   Knowledge Source: Vector Database + LLM
   📁 Documents Used (2):
      • physics_chapter5.pdf
      • jee_physics_problems.pdf
```

---

## Benefits

### 1. **Transparency**
You know exactly where each set of questions comes from

### 2. **Quality Assurance**
- RAG questions = Based on your curriculum materials
- Pure LLM = General knowledge (may not match your syllabus)

### 3. **Coverage Tracking**
Quickly identify which subjects need more documents uploaded

### 4. **Debugging**
- See if Pinecone is working correctly
- Verify documents are indexed properly
- Check if subject metadata is correct

### 5. **Traceability**
Can trace questions back to specific PDF files and pages

---

## Example Scenarios

### Scenario A: Good RAG Coverage
```
Subject: Physics
RAG Status: ✅ Using RAG CONTEXT
Source Files: 
  • physics_mechanics.pdf
  • jee_advanced_physics.pdf
  • ncert_physics_class11.pdf
Result: High-quality, curriculum-specific questions
```

### Scenario B: No Documents Available
```
Subject: Biology
RAG Status: ⚠️ Using PURE LLM KNOWLEDGE
Reason: No relevant documents in Pinecone
Action Needed: Upload Biology textbooks/materials
```

### Scenario C: Partial Coverage
```
Subject: Chemistry
RAG Status: ✅ Using RAG CONTEXT
Source Files:
  • organic_chemistry_basics.pdf
Note: Only 1 document - consider uploading more for better coverage
```

---

## Next Steps

1. **Test the new logging**: Generate questions and check the terminal
2. **Upload more documents**: If you see "PURE LLM" for subjects you want RAG coverage
3. **Verify metadata**: Check that source files show correct subject/page info
4. **Monitor quality**: Compare RAG vs Pure LLM question quality

---

## Technical Details

### Metadata Structure
Each Pinecone vector should have metadata:
```python
{
    "text": "Content chunk...",
    "source": "filename.pdf",
    "subject": "physics",  # lowercase
    "page": 42
}
```

### Relevance Score Interpretation
- **0.9 - 1.0**: Highly relevant
- **0.7 - 0.9**: Very relevant
- **0.5 - 0.7**: Moderately relevant
- **< 0.5**: Low relevance (may not be used)

### When RAG is Used
- ✅ Documents uploaded to Pinecone
- ✅ Relevant documents found for the query
- ✅ Subject filter matches (if metadata exists)

### When Pure LLM is Used
- ⚠️ No documents in Pinecone
- ⚠️ No relevant documents for the subject
- ⚠️ Subject filter excludes all documents
