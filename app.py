import re
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="InsightRAG", page_icon="🔎", layout="wide")

DEFAULT_DOCS = [
    {
        "title": "Revenue trend",
        "source": "Business Analytics Notes",
        "text": "Revenue is total sales before expenses. Compare month-on-month revenue using consistent date ranges. Check for seasonality and one-off events before interpreting changes."
    },
    {
        "title": "Profit margin",
        "source": "Business Analytics Notes",
        "text": "Profit margin equals profit divided by revenue, multiplied by 100. A higher margin may indicate better cost control or pricing. Always confirm that revenue and profit use the same period and currency."
    },
    {
        "title": "Customer churn",
        "source": "Business Analytics Notes",
        "text": "Churn rate is customers lost during a period divided by customers at the start of the period, multiplied by 100. Define the customer, time period, and churn event before comparing rates."
    },
    {
        "title": "RFM segmentation",
        "source": "Business Analytics Notes",
        "text": "RFM uses recency, frequency, and monetary value to group customers for retention analysis. Recency measures how recently a customer purchased, frequency counts purchases, and monetary value measures spend."
    },
]

def tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", s.lower()))

def retrieve(query: str, docs: list[dict], k: int = 3) -> list[tuple[int, dict]]:
    q = tokens(query)
    scored = []
    for doc in docs:
        content = f"{doc.get('title','')} {doc.get('text','')}"
        overlap = len(q & tokens(content))
        if overlap:
            scored.append((overlap, doc))
    return sorted(scored, key=lambda x: x[0], reverse=True)[:k]

st.title("🔎 InsightRAG")
st.subheader("Business Analytics & Decision Support")
st.caption("A transparent, source-grounded retrieval demo. This version uses local keyword matching; it does not call an external AI model.")

with st.sidebar:
    st.header("Knowledge base")
    st.write("Ask questions about the built-in business analytics notes, or upload a `.txt` or `.md` file to add your own notes.")
    uploads = st.file_uploader("Add source documents", type=["txt", "md"], accept_multiple_files=True)
    top_k = st.slider("Number of source notes", min_value=1, max_value=4, value=3)
    st.divider()
    st.caption("Demo data only. Do not upload confidential or personal information.")

docs = list(DEFAULT_DOCS)
if uploads:
    for uploaded in uploads:
        try:
            content = uploaded.getvalue().decode("utf-8", errors="replace").strip()
            if content:
                docs.append({
                    "title": Path(uploaded.name).stem.replace("_", " "),
                    "source": uploaded.name,
                    "text": content[:20000],
                })
        except Exception:
            st.warning(f"Could not read {uploaded.name}.")

left, right = st.columns([2, 1])
with left:
    question = st.text_input(
        "Ask a business analytics question",
        placeholder="e.g. How is churn rate calculated?",
    )
    search_clicked = st.button("Search knowledge base", type="primary", use_container_width=True)

with right:
    st.markdown("#### Try a sample question")
    sample = st.selectbox("Example questions", [
        "How do I calculate profit margin?",
        "What is customer churn rate?",
        "Explain RFM segmentation",
        "How should I compare monthly revenue?",
    ])
    if st.button("Use example", use_container_width=True):
        st.session_state["sample_question"] = sample
        st.rerun()

if "sample_question" in st.session_state and not question:
    question = st.session_state.pop("sample_question")

if search_clicked or (question and st.session_state.get("auto_search", False)):
    pass

if question:
    hits = retrieve(question, docs, top_k)
    st.markdown("### Retrieved evidence")
    if not hits:
        st.warning("No relevant source note was found. Add a relevant document or try different wording. InsightRAG will not invent an answer.")
    else:
        st.info("This demo returns relevant source passages rather than generating unsupported claims.")
        for i, (score, doc) in enumerate(hits, start=1):
            with st.expander(f"{i}. {doc['title']} · relevance overlap: {score}", expanded=(i == 1)):
                st.write(doc["text"])
                st.caption(f"Source: {doc.get('source', 'Business Analytics Notes')}")
else:
    st.markdown("### How it works")
    st.markdown(
        "1. Enter a question.  \n"
        "2. InsightRAG searches the knowledge base for matching terms.  \n"
        "3. Review the retrieved evidence and its source before using it."
    )

st.divider()
st.caption("Portfolio project by Rishabh Gupta · Educational prototype · Keyword retrieval baseline, not a full generative RAG system.")
