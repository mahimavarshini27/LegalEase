import requests
import streamlit as st
from io import BytesIO
from docx import Document
from fpdf import FPDF


# -------------------------
# PAGE CONFIGURATION
# -------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -------------------------
# SESSION STATE
# -------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "edited_document" not in st.session_state:
    st.session_state.edited_document = ""


# -------------------------
# CUSTOM UI
# -------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 20px;
        margin-top: 0px;
    }

    .description {
        font-size: 16px;
        margin-bottom: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------
# HEADER
# -------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'Create professional legal document drafts quickly '
    'using AI.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# -------------------------
# DOCUMENT DETAILS
# -------------------------

st.subheader("📋 Document Details")


document_type = st.selectbox(
    "Select Document Type",
    [
        "Employment Contract",
        "Lease Agreement",
        "Non-Disclosure Agreement (NDA)"
    ]
)


parties = st.text_area(
    "Parties Involved",
    placeholder="Example: Company name and Employee name"
)


effective_date = st.date_input(
    "Effective Date"
)


key_terms = st.text_area(
    "Key Terms",
    placeholder="Enter the important terms and conditions..."
)


# -------------------------
# GENERATE DOCUMENT
# -------------------------

if st.button(
    "✨ Generate Document",
    use_container_width=True
):

    with st.spinner(
        "🤖 AI is generating your document..."
    ):

        data = {
            "document_type": document_type,
            "parties": parties,
            "effective_date": str(effective_date),
            "key_terms": key_terms
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/generate",
                json=data,
                timeout=120
            )

            if response.status_code == 200:

                result = response.json()

                generated_document = result["document"]

                # Save generated document
                st.session_state.generated_document = (
                    generated_document
                )

                # Save editable copy
                st.session_state.edited_document = (
                    generated_document
                )

                st.success(
                    "✅ Document generated successfully!"
                )

            else:

                st.error(
                    "❌ Backend returned an error."
                )

                st.code(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Backend server is not running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "❌ The request took too long. "
                "Please try again."
            )

        except Exception as e:

            st.error(
                "❌ Something went wrong."
            )

            st.code(str(e))


# -------------------------
# EDIT & PREVIEW
# -------------------------

if st.session_state.generated_document:

    st.subheader("✏️ Edit & Preview")

    edited_document = st.text_area(
        "Edit Your Document",
        value=st.session_state.edited_document,
        height=500,
        key="document_editor"
    )

    # Keep edited text saved
    st.session_state.edited_document = edited_document


    # =========================
    # DOCX DOWNLOAD
    # =========================

    document = Document()

    for line in edited_document.split("\n"):
        document.add_paragraph(line)

    docx_file = BytesIO()

    document.save(docx_file)

    docx_file.seek(0)


    st.download_button(
        label="📄 Download DOCX",
        data=docx_file.getvalue(),
        file_name="LegalEase_Document.docx",
        mime=(
            "application/vnd.openxmlformats-"
            "officedocument.wordprocessingml.document"
        ),
        use_container_width=True
    )


    # =========================
    # PDF DOWNLOAD
    # =========================

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        size=12
    )


    # Make Unicode text PDF-safe

    safe_text = (
        edited_document
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
        .replace("…", "...")
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


    for line in safe_text.split("\n"):

        pdf.multi_cell(
            0,
            8,
            line
        )


    pdf_bytes = pdf.output(
        dest="S"
    ).encode("latin-1")


    pdf_file = BytesIO(
        pdf_bytes
    )

    pdf_file.seek(0)


    st.download_button(
        label="📕 Download PDF",
        data=pdf_file.getvalue(),
        file_name="LegalEase_Document.pdf",
        mime="application/pdf",
        use_container_width=True
    )


    # -------------------------
    # DISCLAIMER
    # -------------------------

    st.warning(
        "⚠️ This AI-generated document is a draft "
        "for informational purposes only. "
        "Please have it reviewed by a qualified "
        "legal professional before using it."
    )


# -------------------------
# FOOTER
# -------------------------

st.divider()

st.caption(
    "LegalEase © 2026 — AI-Powered Legal Document Generator"
)