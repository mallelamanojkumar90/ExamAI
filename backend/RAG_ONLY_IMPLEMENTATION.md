# RAG-Only Question Generation - Implementation Plan

## 🎯 **Objective**
Modify the system to generate questions **ONLY** from uploaded documents (RAG), not from LLM's general knowledge.

## ❌ **Current Behavior**
- If no documents found in Pinecone → Falls back to LLM general knowledge
- Prompt says: "use if relevant" (allows LLM to use its own knowledge)
- Warning message but still generates questions

## ✅ **New Behavior**
- If no documents found in Pinecone → Return ERROR message
- Prompt says: "ONLY use provided context" (strict enforcement)
- No fallback to LLM knowledge

---

## 🔧 **Changes Required**

### **1. Check for Context Availability**
```python
if not context_str or not using_rag:
    # OLD: context_str = "No specific context available. Generate questions based on your knowledge."
    # NEW: Return error immediately
    return [{
        "id": "error",
        "text": f"No documents found for {subject}. Please upload relevant study materials.",
        "options": [...],
        "correctAnswer": 0,
        "explanation": f"The system requires uploaded documents. No {subject} content found."
    }]
```

### **2. Update LLM Prompt**
```python
# OLD PROMPT:
"""
Context from knowledge base (use if relevant to {subject}):
{context_str}
"""

# NEW PROMPT:
"""
**CRITICAL**: Generate questions ONLY from the context below.
DO NOT use your general knowledge.
If context is insufficient, create variations from what's available.

Context from knowledge base (USE ONLY THIS):
{context_str}

STRICT REQUIREMENT: Base ALL questions on the context above.
"""
```

### **3. Update Status Messages**
```python
# Change from:
print("⚠️  RAG STATUS: Using PURE LLM KNOWLEDGE")

# To:
print("❌ RAG STATUS: NO CONTEXT AVAILABLE - RETURNING ERROR")
```

---

## 📋 **Implementation Steps**

1. ✅ **Backup current file** (`rag_service.py.backup`)
2. ⏳ **Modify context check logic** (lines 123-135)
3. ⏳ **Update first attempt prompt** (lines 138-176)
4. ⏳ **Update retry prompt** (lines 177-203)
5. ⏳ **Test with subject that has no documents**
6. ⏳ **Test with subject that has documents**

---

## 🧪 **Testing Plan**

### **Test Case 1: No Documents Available**
- Request: Physics, Medium, 5 questions
- Expected: Error message saying "No documents found for Physics"
- Frontend should show: "Please upload study materials"

### **Test Case 2: Documents Available**
- Request: Subject with uploaded PDFs, Medium, 5 questions
- Expected: Questions generated from PDF content only
- Terminal should show: Source files used

---

## 📝 **User-Facing Error Message**

When no documents are found:
```
"No documents found for [Subject]. 

Please upload relevant study materials to the knowledge base before generating questions.

Options:
A. Upload PDF documents for this subject
B. Check if documents are properly indexed  
C. Verify subject name matches uploaded content
D. Contact administrator for help"
```

---

## 🎯 **Benefits**

1. **Accuracy**: Questions based only on uploaded content
2. **Transparency**: Clear when documents are missing
3. **Quality Control**: Forces proper document management
4. **No Hallucinations**: LLM can't make up content
5. **Traceability**: All questions traceable to source documents

---

## ⚠️ **Important Notes**

- This is a **breaking change** - requires documents for ALL subjects
- Users must upload PDFs before generating questions
- Admin panel document upload becomes **mandatory**
- Consider adding a "test mode" that allows LLM knowledge for demo purposes

---

## 🔄 **Rollback Plan**

If issues arise:
```bash
cp rag_service.py.backup rag_service.py
```

The backup file contains the original logic with LLM fallback.
