# app.py - ULTRA SIMPLE WORKING VERSION
import streamlit as st
import qrcode
import io

# Initialize session state
if 'qr_content' not in st.session_state:
    st.session_state.qr_content = {
        'title': 'Welcome!', 
        'message': 'Scan this QR code to see dynamic content!'
    }

# Simple app - no complex routing
st.set_page_config(page_title="Dynamic QR System", page_icon="📱")

st.title("🎯 Dynamic QR Code System")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Your Permanent QR Code")
    
    # Generate QR code
    app_url = "https://dynamic-qr-system-akma5nenm2jg5fj3tyhfu9.streamlit.app/"
    qr_url = app_url + "?view=content"
    
    qr = qrcode.QRCode(version=5, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to bytes and display
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    
    st.image(buf, caption="Scan this QR code - content updates dynamically!", width=300)
    
    # Download button
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
    
    if st.button("Update Content"):
        st.session_state.qr_content = {'title': title, 'message': message}
        st.success("Content updated!")
    
    st.markdown("---")
    st.subheader("Current Content")
    st.write(f"**{st.session_state.qr_content['title']}**")
    st.write(st.session_state.qr_content['message'])

st.markdown("---")
st.info("💡 **Mobile users**: Visit the URL with `?view=content` to see the mobile-optimized view")