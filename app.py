# app.py - ULTRA SIMPLE TEXT-ONLY VERSION
import streamlit as st

# Initialize session state
if 'qr_content' not in st.session_state:
    st.session_state.qr_content = {
        'title': 'Welcome!', 
        'message': 'Scan the QR code to see this content.'
    }

st.set_page_config(page_title="Dynamic QR System", page_icon="📱")

st.title("🎯 Dynamic QR Code System")
st.markdown("Create a permanent QR code with dynamic content")

# Your app URL for QR generation
app_url = "https://dynamic-qr-system-akma5nenm2jg5fj3tyhfu9.streamlit.app/"
mobile_url = app_url + "?view=content"

st.subheader("Step 1: Generate QR Code")
st.info(f"**Use this URL in any QR code generator:**")
st.code(mobile_url)
st.markdown("💡 **Tip:** Use free online QR generators like QRCode Monkey, QRickit, or similar")

st.subheader("Step 2: Update Content")
col1, col2 = st.columns(2)

with col1:
    title = st.text_input("Title", st.session_state.qr_content['title'])
    message = st.text_area("Message", st.session_state.qr_content['message'])

with col2:
    st.subheader("Preview")
    st.write(f"**{st.session_state.qr_content['title']}**")
    st.write(st.session_state.qr_content['message'])

if st.button("Update Content", type="primary"):
    st.session_state.qr_content = {'title': title, 'message': message}
    st.success("Content updated! Existing QR codes will show the new content.")

st.markdown("---")
st.info("**How it works:**\n1. Generate QR code once with the URL above\n2. Update content anytime using this panel\n3. Scanning the QR code shows updated content")