# InsightRAG — Business Analytics & Decision Support

InsightRAG is a small Streamlit web app that retrieves relevant passages from a local knowledge base and displays the source. It currently uses transparent keyword-overlap retrieval, not an external LLM or embedding model.

## Live demo
After deploying on Streamlit Community Cloud, add your public app URL here.

## Features
- Search business analytics notes about revenue, profit margin, customer churn, and RFM segmentation
- View retrieved passages and source labels
- Upload `.txt` or `.md` notes for a session-based knowledge base extension
- Avoids fabricating an answer when no matching source is found

## Tech stack
- Python
- Streamlit
- Regular expressions / keyword matching

## Run locally
```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Limitations
This is a retrieval baseline and does not generate natural-language answers with an LLM, use vector embeddings, or provide semantic search. Uploaded documents are processed for the current app session only. Do not upload confidential or personal information.

## Suggested next improvements
1. Add chunking for longer documents.
2. Add embedding-based retrieval and vector search.
3. Add answer generation with citations and an evaluation set.
