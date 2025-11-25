# 🔍 Quick Reference: Reading Terminal Output

## When You Generate Questions, Look For:

### 1️⃣ **RETRIEVED CONTEXT Section**
```
📚 RETRIEVED CONTEXT FROM PINECONE:
────────────────────────────────────
  Match #1:
    📄 Source File: [filename.pdf]
    📊 Subject: [subject]
    📖 Page: [page number]
    🎯 Relevance Score: [0.0 - 1.0]
    📝 Text Preview: [first 100 chars...]
```

**What to check:**
- ✅ Are the source files relevant to your subject?
- ✅ Are the relevance scores high (> 0.7)?
- ✅ Does the text preview look relevant?

---

### 2️⃣ **RAG STATUS Section**
```
✅ RAG STATUS: Using RAG CONTEXT
   📚 Total Context Chunks: [number]
   📁 Source Files Used:
      • [file1.pdf]
      • [file2.pdf]
```

**OR**

```
⚠️  RAG STATUS: Using PURE LLM KNOWLEDGE
   Reason: No relevant documents found in Pinecone
```

**What it means:**
- ✅ **RAG CONTEXT** = Questions based on YOUR documents
- ⚠️ **PURE LLM** = Questions based on general knowledge

---

### 3️⃣ **GENERATION RESULT Section**
```
GENERATION RESULT:
  Requested: [count] [subject] questions
  Generated: [count] questions
  Q1: [question preview...]
  Q2: [question preview...]
  ...
✅ SUCCESS: Generated exactly [count] questions!
```

**What to check:**
- ✅ Does "Generated" match "Requested"?
- ✅ Do the question previews look relevant to the subject?

---

### 4️⃣ **QUESTION SOURCE SUMMARY Section**
```
📊 QUESTION SOURCE SUMMARY:
────────────────────────────────────
✅ Questions generated using RAG
   Knowledge Source: Vector Database + LLM
   📁 Documents Used (2):
      • physics_chapter5.pdf
      • jee_problems.pdf
────────────────────────────────────
```

**What it tells you:**
- 📚 How many documents were used
- 📄 Which specific files contributed
- 🎯 Whether RAG or pure LLM was used

---

## 🚦 Quick Status Guide

| Symbol | Meaning | Action Needed |
|--------|---------|---------------|
| ✅ | Success / RAG Active | None - working as expected |
| ⚠️ | Warning / Pure LLM | Consider uploading documents |
| 🔄 | Retry in progress | Wait for completion |
| ❌ | Error occurred | Check error message |

---

## 📊 Relevance Score Guide

| Score Range | Interpretation | Quality |
|-------------|----------------|---------|
| 0.9 - 1.0 | Highly relevant | Excellent |
| 0.7 - 0.9 | Very relevant | Good |
| 0.5 - 0.7 | Moderately relevant | Fair |
| < 0.5 | Low relevance | Poor |

---

## 🎯 What You Want to See

**IDEAL OUTPUT:**
```
✅ RAG STATUS: Using RAG CONTEXT
   📚 Total Context Chunks: 5-10
   📁 Source Files Used:
      • [relevant_file1.pdf]
      • [relevant_file2.pdf]
      • [relevant_file3.pdf]

✅ SUCCESS: Generated exactly 10 questions!

📊 QUESTION SOURCE SUMMARY:
✅ Questions generated using RAG
   📁 Documents Used (3):
      • [relevant files listed]
```

**This means:**
- ✅ Questions are based on YOUR curriculum
- ✅ Multiple documents provide diverse context
- ✅ Correct number of questions generated
- ✅ High-quality, specific questions

---

## ⚠️ What to Watch For

**NEEDS ATTENTION:**
```
⚠️  RAG STATUS: Using PURE LLM KNOWLEDGE
   Reason: No relevant documents found

⚠️  Questions generated using PURE LLM KNOWLEDGE
   Knowledge Source: LLM's pre-trained knowledge only
```

**This means:**
- ⚠️ No documents uploaded for this subject
- ⚠️ Questions are generic, not curriculum-specific
- ⚠️ You should upload relevant PDFs

**ACTION:** Upload textbooks/materials for this subject to Pinecone

---

## 📝 Example: Good vs Needs Work

### ✅ GOOD - Physics with RAG
```
Subject: Physics
RAG Status: ✅ Using RAG CONTEXT
Source Files: 
  • ncert_physics_class11.pdf
  • jee_advanced_mechanics.pdf
  • physics_problems_solved.pdf
Relevance Scores: 0.85, 0.82, 0.79
Result: 10 curriculum-specific questions
```

### ⚠️ NEEDS WORK - Chemistry without RAG
```
Subject: Chemistry
RAG Status: ⚠️ Using PURE LLM KNOWLEDGE
Source Files: None
Result: 10 generic chemistry questions
Action: Upload chemistry textbooks
```

---

## 🔧 Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Always shows "PURE LLM" | No documents uploaded | Upload PDFs via admin panel |
| Wrong subject in source | Metadata incorrect | Re-upload with correct metadata |
| Low relevance scores | Documents not relevant | Upload more specific materials |
| No matches found | Subject filter too strict | Check subject naming consistency |

---

## 💡 Pro Tips

1. **Check source files first** - Verify they match your subject
2. **Monitor relevance scores** - Higher is better (aim for > 0.7)
3. **Track document usage** - Ensure all subjects have RAG coverage
4. **Compare question quality** - RAG questions should be more specific
5. **Keep terminal visible** - Watch the logs during generation

---

## 📞 Need Help?

If you see unexpected output:
1. Check the full terminal output
2. Verify documents are uploaded to Pinecone
3. Ensure subject metadata matches your request
4. Check relevance scores
5. Review the source files listed
