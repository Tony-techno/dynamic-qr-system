# app.py - Minimal working version
import streamlit as st
import qrcode
import io

# Initialize session state
if 'qr_content' not in st.session_state:
    st.session_state.qr_content = {
        'title': 'Welcome!', 
        'message': 'Scan this QR code to see dynamic content!'
    }

def generate_qr(url):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

# Main app
st.set_page_config(page_title="Dynamic QR System", page_icon="📱")

# Get current URL
app_url = "https://dynamic-qr-system-akma5nenm2jg5fj3tyhfu9.streamlit.app/"

# Check if we're in mobile view
query_params = st.query_params
if "view" in query_params and query_params["view"] == "content":
    # Mobile view
    st.title(st.session_state.qr_content['title'])
    st.info(st.session_state.qr_content['message'])
    st.caption("Content updates dynamically")
else:
    # Admin view
    st.title("🎯 Dynamic QR Code System")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("QR Code")
        qr_img = generate_qr(app_url + "?view=content")
        st.image(qr_img, width=300)
        
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button(
            "Download QR Code",
            buf.getvalue(),
            "qr_code.png",
            "image/png"
        )
    
    with col2:
        st.subheader("Update Content")
        title = st.text_input("Title", st.session_state.qr_content['title'])
        message = st.text_area("Message", st.session_state.qr_content['message'])
        
        if st.button("Update"):
            st.session_state.qr_content = {'title': title, 'message': message}
            st.success("Content updated!")
        
        if st.button("Preview Mobile View"):
            st.query_params = {"view": "content"}