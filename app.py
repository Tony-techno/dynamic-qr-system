# app.py
import streamlit as st
import qrcode
import io
import sqlite3
from PIL import Image
import base64
import time

# Initialize database
def init_db():
    """Initialize SQLite database for storing dynamic content"""
    conn = sqlite3.connect('qr_content.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS content
                 (id INTEGER PRIMARY KEY, 
                  title TEXT, 
                  message TEXT,
                  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Insert default content if not exists
    c.execute("INSERT OR IGNORE INTO content (id, title, message) VALUES (1, 'Welcome!', 'This content updates dynamically without changing the QR code.')")
    conn.commit()
    conn.close()

def get_content():
    """Retrieve current content from database"""
    conn = sqlite3.connect('qr_content.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT title, message FROM content WHERE id=1")
    result = c.fetchone()
    conn.close()
    
    if result:
        return {"title": result[0], "message": result[1]}
    else:
        return {"title": "Welcome!", "message": "Default content"}

def update_content(title, message):
    """Update content in database"""
    conn = sqlite3.connect('qr_content.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO content (id, title, message) VALUES (1, ?, ?)", 
              (title, message))
    conn.commit()
    conn.close()

def generate_qr(url):
    """Generate QR code with high error correction for better mobile scanning"""
    qr = qrcode.QRCode(
        version=5,  # Larger version for more data
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% error correction
        box_size=12,  # Larger boxes for better mobile scanning
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code with high contrast
    qr_img = qr.make_image(fill_color="black", back_color="white")
    return qr_img

def get_base64_encoded_image(image):
    """Convert image to base64 for display"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def main_admin():
    """Main admin interface for QR generation and content management"""
    st.set_page_config(
        page_title="Dynamic QR Admin",
        page_icon="📱",
        layout="wide"
    )
    
    st.title("🎯 Dynamic QR Code System")
    st.markdown("---")
    
    # Get current app URL (you'll need to update this after deployment)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🔗 Your Permanent QR Code")
        
        # Instructions for URL
        st.info("💡 **After deployment, update the URL below with your actual app URL**")
        
        # Input for app URL (you'll update this after deployment)
        app_url = st.text_input(
            "Your App URL:",
            value="https://your-username-streamlit-app.streamlit.app/",
            help="Change this to your actual deployed URL"
        )
        
        # Generate QR code
        if app_url:
            qr_image = generate_qr(app_url)
            
            # Convert to base64 for better display
            img_str = get_base64_encoded_image(qr_image)
            
            # Display QR code with download option
            st.image(f"data:image/png;base64,{img_str}", 
                    caption="Scan this QR Code - Content updates dynamically!",
                    width=300)
            
            # Download button
            buf = io.BytesIO()
            qr_image.save(buf, format="PNG")
            st.download_button(
                "📥 Download QR Code",
                buf.getvalue(),
                "permanent_dynamic_qr.png",
                "image/png",
                key="download_qr"
            )
    
    with col2:
        st.subheader("⚙️ Content Management")
        
        # Get current content
        current_content = get_content()
        
        # Update form
        with st.form("update_content"):
            new_title = st.text_input("Title", value=current_content["title"])
            new_message = st.text_area("Message", value=current_content["message"], height=150)
            
            if st.form_submit_button("🔄 Update Content"):
                if new_title and new_message:
                    update_content(new_title, new_message)
                    st.success("✅ Content updated successfully!")
                    st.balloons()
                    
                    # Show preview
                    st.subheader("📱 Mobile Preview:")
                    st.markdown(f"**{new_title}**")
                    st.markdown(new_message)
                    st.markdown("---")
                    st.caption("This is what users will see when they scan the QR code")
                else:
                    st.error("Please fill in both title and message")

def main_content():
    """Content page that mobile users see when scanning QR code"""
    st.set_page_config(
        page_title="QR Content",
        page_icon="📱",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Hide sidebar for mobile users
    st.markdown("""
        <style>
            .css-1d391kg {display: none}
        </style>
    """, unsafe_allow_html=True)
    
    # Get current content
    content = get_content()
    
    # Mobile-friendly display
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='color: #2E86AB;'>{content['title']}</h1>
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
                <p style='font-size: 18px; line-height: 1.6;'>{content['message']}</p>
            </div>
            <p style='color: #666; font-size: 14px;'>
                🔄 Content updates dynamically • Last updated: {time.strftime('%Y-%m-%d %H:%M')}
            </p>
        </div>
    """, unsafe_allow_html=True)

# Initialize database
init_db()

# Simple routing - if URL has no parameters, show admin; if it has specific param, show content
query_params = st.experimental_get_query_params()

if query_params.get("view", [""])[0] == "content":
    main_content()
else:
    main_admin()

# Add instructions in sidebar for admin
if not query_params.get("view", [""])[0] == "content":
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Generate QR Code** using your app URL
        2. **Download & print** the QR code
        3. **Update content** anytime using the form
        4. **Scan with mobile** - content updates instantly!
        
        **Mobile URL:** `your-app-url.streamlit.app/?view=content`
        """)
        
        # Quick preview link
        st.markdown("---")
        st.subheader("Quick Preview")
        if st.button("👀 Preview Mobile View"):
            st.experimental_set_query_params(view="content")
            st.experimental_rerun()
            