import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime


def generate_full_pdf_report():
    # ✅ Check all required session states exist
    if "portfolio_data" not in st.session_state or \
       "eda_df" not in st.session_state or \
       "merged_all" not in st.session_state or \
       "conversation" not in st.session_state:
        st.error("Please run Portfolio Manager, EDA, Visualizations, and Chatbot first.")
        return

    # ✅ Set up PDF generation (in-memory buffer)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    normal_style = styles["BodyText"]
    small_style = ParagraphStyle("Small", parent=normal_style, fontSize=9, leading=12)

    # ✅ Title
    story.append(Paragraph("📊 Portfolio Insights Report", title_style))
    story.append(Spacer(1, 20))

    # ✅ Section 1: Portfolio Manager Data
    story.append(Paragraph("Section 1: Portfolio Manager Data", heading_style))
    story.append(Spacer(1, 10))
    for idx, rec in enumerate(st.session_state["portfolio_data"], start=1):
        story.append(Paragraph(f"<b>Record {idx}:</b>", normal_style))
        for k, v in rec.items():
            story.append(Paragraph(f"{k}: {v}", small_style))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # ✅ Section 2: EDA Transformed Data
    story.append(Paragraph("Section 2: EDA Transformed Data (Top 10 Rows)", heading_style))
    df = st.session_state["eda_df"]
    story.append(Spacer(1, 10))
    for i, row in df.head(10).iterrows():
        row_text = ", ".join([f"{col}: {row[col]}" for col in df.columns])
        story.append(Paragraph(row_text, small_style))
        story.append(Spacer(1, 4))
    story.append(PageBreak())

    # ✅ Section 3: Chatbot Conversation Summary
    story.append(Paragraph("Section 3: Chatbot Conversation Summary", heading_style))
    story.append(Spacer(1, 10))
    for msg in st.session_state["conversation"][1:]:
        role = "You" if msg["role"] == "user" else "Assistant"
        story.append(Paragraph(f"<b>{role}:</b>", normal_style))
        story.append(Paragraph(str(msg["content"]), small_style))
        story.append(Spacer(1, 4))

    # ✅ Build PDF into memory
    doc.build(story)
    buffer.seek(0)

    # ✅ Create timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"portfolio_report_{timestamp}.pdf"

    # ✅ Streamlit download button (no local file written)
    st.download_button(
        label="📥 Download Full Portfolio Report (PDF)",
        data=buffer,
        file_name=filename,
        mime="application/pdf"
    )
