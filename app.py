# app.py - SIMPLE WORKING VERSION
import streamlit as st
import qrcode
import io
import base64

# Initialize session state
if 'qr_content' not in st.session_state:
    st.session_state.qr_content = {
        'title': 'Welcome to Our Service!', 
        'message': 'This content can be updated anytime without changing the QR code. Check back for updates!'
    }

def generate_qr_base64(url):
    """Generate QR code and return as base64 string"""
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to bytes
    buf = io.BytesIO()
    qr_img.save(buf, format="PNG")
    buf.seek(0)
    
    # Convert to base64 for display
    img_str = base64.b64encode(buf.read()).decode()
    return img_str

def main():
    st.set_page_config(
        page_title="Dynamic QR System", 
        page_icon="📱", 
        layout="wide"
    )
    
    # Simple routing based on URL parameter in query string
    try:
        # Check if we're in mobile view by looking at URL
        import os
        current_url = os.environ.get('STREAMLIT_SERVER_BASE_URL_PATH', '')
        if 'view=content' in current_url:
            show_mobile_view()
            return
    except:
        pass
    
    # Default to admin view
    show_admin_view()

def show_admin_view():
    """Admin interface for QR generation and content management"""
    st.title("🎯 Dynamic QR Code System")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔗 Your Permanent QR Code")
        
        # Current app URL
        app_url = "https://dynamic-qr-system-akma5nenm2jg5fj3tyhfu9.streamlit.app/"
        
        st.info(f"**App URL:** {app_url}")
        
        # Generate QR code for mobile view
        qr_url = app_url + "?view=content"
        qr_base64 = generate_qr_base64(qr_url)
        
        # Display QR code using HTML to avoid PIL issues
        st.markdown(f'<img src="data:image/png;base64,{qr_base64}" width="300" alt="QR Code">', 
                   unsafe_allow_html=True)
        st.caption("Scan this QR code - content updates dynamically!")
        
        # Download button
        st.download_button(
            "📥 Download QR Code",
            data=base64.b64decode(qr_base64),
            file_name="dynamic_qr_code.png",
            mime="image/png"
        )
        
        st.success("✅ **QR Code Generated!** Print this once and update content anytime.")
    
    with col2:
        st.subheader("⚙️ Content Management")
        
        with st.form("content_form"):
            title = st.text_input("Title", value=st.session_state.qr_content['title'])
            message = st.text_area("Message", value=st.session_state.qr_content['message'], height=150)
            
            submitted = st.form_submit_button("🔄 Update Content")
            if submitted:
                if title and message:
                    st.session_state.qr_content = {'title': title, 'message': message}
                    st.success("✅ Content updated successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in both title and message")
        
        # Quick preview
        with st.expander("📱 Mobile Preview", expanded=True):
            st.subheader(st.session_state.qr_content['title'])
            st.write(st.session_state.qr_content['message'])
            st.markdown("---")
            st.caption("This is what mobile users will see")
            
        # Direct link to mobile view
        st.markdown("---")
        st.subheader("Test Mobile View")
        mobile_url = "https://dynamic-qr-system-akma5nenm2jg5fj3tyhfu9.streamlit.app/?view=content"
        st.markdown(f'<a href="{mobile_url}" target="_blank">👀 Open Mobile View</a>', 
                   unsafe_allow_html=True)

def show_mobile_view():
    """What mobile users see when scanning QR code"""
    # Hide sidebar for clean mobile view
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
            .main > div {padding: 2rem 1rem;}
            header {display: none;}
        </style>
    """, unsafe_allow_html=True)
    
    # Mobile-optimized display
    st.markdown(f"""
    <div style='
        text-align: center; 
        padding: 30px 20px; 
        font-family: Arial, sans-serif;
        min-height: 100vh;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    '>
        <div style='
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            margin: 20px 0; 
            color: #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        '>
            <h1 style='color: #2E86AB; margin-bottom: 20px; font-size: 24px;'>
                {st.session_state.qr_content['title']}
            </h1>
            <div style='
                background: #f8f9fa; 
                padding: 25px; 
                border-radius: 15px; 
                margin: 20px 0;
                border-left: 5px solid #2E86AB;
            '>
                <p style='font-size: 18px; line-height: 1.6; margin: 0;'>
                    {st.session_state.qr_content['message']}
                </p>
            </div>
            <p style='color: #666; font-size: 14px; margin-top: 30px;'>
                🔄 Content updates dynamically
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()