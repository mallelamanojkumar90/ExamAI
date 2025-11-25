# Enhanced RAG Logging - Terminal Output Guide

## What You'll See in the Terminal

When you generate questions, the backend terminal will now show comprehensive information about:
1. **Whether questions come from RAG or pure LLM knowledge**
2. **Which source files were used**
3. **Detailed metadata about each retrieved document**

---

## Example Terminal Output

### Scenario 1: Questions Generated Using RAG Context

```
============================================================
QUESTION GENERATION REQUEST:
  Subject: Physics
  Difficulty: medium
  Count: 10
============================================================

Querying Pinecone with: 'medium level concepts and problems in Physics'
Generated embedding with 384 dimensions
Pinecone query with filter returned 8 matches

────────────────────────────────────────────────────────────
📚 RETRIEVED CONTEXT FROM PINECONE:
────────────────────────────────────────────────────────────

  Match #1:
    📄 Source File: physics_mechanics_chapter3.pdf
    📊 Subject: physics
    📖 Page: 42
    🎯 Relevance Score: 0.8523
    📝 Text Preview: Newton's laws of motion describe the relationship between forces and motion...

  Match #2:
    📄 Source File: physics_mechanics_chapter3.pdf
    📊 Subject: physics
    📖 Page: 45
    🎯 Relevance Score: 0.8201
    📝 Text Preview: The concept of momentum is fundamental in understanding collisions...

  Match #3:
    📄 Source File: jee_physics_problems.pdf
    📊 Subject: physics
    📖 Page: 12
    🎯 Relevance Score: 0.7956
    📝 Text Preview: A block of mass 5kg slides down an inclined plane...

────────────────────────────────────────────────────────────
✅ RAG STATUS: Using RAG CONTEXT
   📚 Total Context Chunks: 3
   📁 Source Files Used:
      • physics_mechanics_chapter3.pdf
      • jee_physics_problems.pdf
────────────────────────────────────────────────────────────

Sending prompt to LLM (requesting 10 Physics questions)...
LLM Response length: 3542 characters

============================================================
GENERATION RESULT:
  Requested: 10 Physics questions
  Generated: 10 questions
  Q1: A block of mass 10 kg is placed on a frictionless surface...
  Q2: Calculate the momentum of a particle moving with velocity...
  Q3: Two objects collide elastically. If the first object has...
  Q4: A force of 50 N is applied to an object at an angle of...
  Q5: Determine the acceleration of a system where a 5 kg mass...
  Q6: A car moving at 20 m/s comes to rest in 5 seconds. What...
  Q7: An object is thrown vertically upward with an initial...
  Q8: Calculate the kinetic energy of a 2 kg object moving at...
  Q9: A spring with spring constant k = 200 N/m is compressed...
  Q10: Two blocks of masses 3 kg and 5 kg are connected by a...
✅ SUCCESS: Generated exactly 10 questions!

────────────────────────────────────────────────────────────
📊 QUESTION SOURCE SUMMARY:
────────────────────────────────────────────────────────────
✅ Questions generated using RAG (Retrieval-Augmented Generation)
   Knowledge Source: Vector Database + LLM
   📁 Documents Used (2):
      • physics_mechanics_chapter3.pdf
      • jee_physics_problems.pdf
────────────────────────────────────────────────────────────
============================================================
```

---

### Scenario 2: Questions Generated Using Pure LLM Knowledge

```
============================================================
QUESTION GENERATION REQUEST:
  Subject: Chemistry
  Difficulty: easy
  Count: 5
============================================================

Querying Pinecone with: 'easy level concepts and problems in Chemistry'
Generated embedding with 384 dimensions
Filter query failed (metadata might not exist): ...
Pinecone query without filter returned 0 matches

────────────────────────────────────────────────────────────
📚 RETRIEVED CONTEXT FROM PINECONE:
────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────
⚠️  RAG STATUS: Using PURE LLM KNOWLEDGE (No RAG context)
   Reason: No relevant documents found in Pinecone
────────────────────────────────────────────────────────────

Sending prompt to LLM (requesting 5 Chemistry questions)...
LLM Response length: 1823 characters

============================================================
GENERATION RESULT:
  Requested: 5 Chemistry questions
  Generated: 5 questions
  Q1: What is the atomic number of Carbon?...
  Q2: Which of the following is a noble gas?...
  Q3: The pH of a neutral solution at 25°C is:...
  Q4: What type of bond is formed when electrons are shared?...
  Q5: Which element has the symbol 'Na'?...
✅ SUCCESS: Generated exactly 5 questions!

────────────────────────────────────────────────────────────
📊 QUESTION SOURCE SUMMARY:
────────────────────────────────────────────────────────────
⚠️  Questions generated using PURE LLM KNOWLEDGE
   Knowledge Source: LLM's pre-trained knowledge only
   Reason: No relevant documents in Pinecone for this query
────────────────────────────────────────────────────────────
============================================================
```

---

## Key Indicators

### ✅ RAG Context Used
- You'll see: "✅ RAG STATUS: Using RAG CONTEXT"
- Source files will be listed
- Questions are based on your uploaded documents + LLM knowledge

### ⚠️ Pure LLM Knowledge
- You'll see: "⚠️ RAG STATUS: Using PURE LLM KNOWLEDGE"
- No source files listed
- Questions are based only on the LLM's pre-trained knowledge
- This happens when:
  - No documents uploaded to Pinecone
  - No relevant documents found for the subject
  - Subject filter doesn't match any documents

---

## What This Tells You

1. **Quality Indicator**: RAG-based questions are typically more specific to your curriculum
2. **Coverage Check**: If you see "PURE LLM" for a subject, you may need to upload more documents for that subject
3. **Traceability**: You can see exactly which PDF files contributed to the questions
4. **Debugging**: Helps identify if Pinecone indexing is working correctly
