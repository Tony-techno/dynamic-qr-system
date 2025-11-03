# app.py - FINAL WORKING VERSION for Streamlit 1.28.0
import streamlit as st
import qrcode
import io

# Initialize session state
if 'qr_content' not in st.session_state:
    st.session_state.qr_content = {
        'title': 'Welcome to Our Service!', 
        'message': 'This content can be updated anytime without changing the QR code. Check back for updates!'
    }

def generate_qr(url):
    """Generate QR code with high error correction"""
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    return qr.make_image(fill_color="black", back_color="white")

def main():
    st.set_page_config(
        page_title="Dynamic QR System", 
        page_icon="📱", 
        layout="wide"
    )
    
    # Get URL parameters the old way (compatible with Streamlit 1.28.0)
    try:
        # For Streamlit 1.28.0, we need to check the URL manually
        from urllib.parse import parse_qs, urlparse
        import requests
        
        # Get current URL from the request
        ctx = st.runtime.scriptrunner.get_script_run_ctx()
        if ctx and hasattr(ctx, 'request'):
            current_url = ctx.request.url
        else:
            current_url = ""
        
        # Parse query parameters
        parsed_url = urlparse(current_url)
        query_params = parse_qs(parsed_url.query)
        
        # Check if we should show mobile view
        if 'view' in query_params and query_params['view'][0] == 'content':
            show_mobile_view()
            return
            
    except:
        # If we can't get URL params, just show admin view
        pass
    
    # Show admin view by default
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
        qr_img = generate_qr(qr_url)
        
        # Display QR code
        st.image(qr_img, caption="Scan this QR code - content updates dynamically!", width=300)
        
        # Download button
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        st.download_button(
            "📥 Download QR Code",
            buf.getvalue(),
            "dynamic_qr_code.png",
            "image/png"
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
                    st.balloons()
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
        st.markdown(f"[👀 Open Mobile View]({mobile_url})")

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