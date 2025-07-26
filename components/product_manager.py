import streamlit as st
import tempfile
import os
import io
import sys
from datetime import datetime
from PIL import Image
import dateparser
from utils.database import get_user_products, get_deleted_products, add_product, update_product, delete_product, restore_product
from utils.ocr_processor import process_image_ocr, process_dual_image_ocr, apply_hitl_feedback
from utils.helpers import get_expiry_status, filter_products

def render_products_tab(products):
    st.markdown("<h2>📋 Products List</h2>", unsafe_allow_html=True)
    search_term = st.text_input("🔍 Search by Product Name", key="search_input").strip().lower()
    filter_option = st.selectbox("📂 Filter by:", ["All Items", "Expiring This Week", "Expired Only"])
    filtered_products = filter_products(products, filter_option, search_term)
    
    if filtered_products:
        render_product_list(filtered_products)
        render_undo_functionality()
    else:
        st.warning("😔 No products match your criteria.")

def render_product_list(products):
    for i, product in enumerate(sorted(products, key=lambda x: x["expiry"])):
        render_product_item(product, i)

def render_product_item(product, index):
    days_left = (product["expiry"] - datetime.now()).days
    status = get_expiry_status(product["expiry"])
    emoji = "❌" if status == "Expired" else ("⚠" if status == "Expiring Soon" else "✅")
    
    col_item, col_edit, col_delete = st.columns([4, 1, 1])
    with col_item:
        st.markdown(f"<div style='font-size:1.1rem;'>{emoji} <b>{product['name']}</b> — Expires in {abs(days_left)} day(s) ({product['expiry'].strftime('%Y-%m-%d')}) [{status}]</div>", unsafe_allow_html=True)
    with col_edit:
        if st.button("🖋️", key=f"edit_{product['_id']}_{index}"):
            st.session_state[f"editing_{product['_id']}"] = True
            st.rerun()
    with col_delete:
        if st.button("🗑️", key=f"delete_{product['_id']}_{index}"):
            st.session_state["last_deleted_item"] = product.copy()
            delete_product(product["_id"])
            st.warning(f"🗑 Deleted {product['name']}.")
            st.rerun()
    
    if st.session_state.get(f"editing_{product['_id']}", False):
        with st.form(f"edit_form_{product['_id']}"):
            new_name = st.text_input("New name:", value=product["name"])
            new_expiry = st.date_input("New expiry:", value=product["expiry"])
            col_save, col_cancel = st.columns([1, 1])
            with col_save:
                if st.form_submit_button("✅ Save"):
                    update_product(product["_id"], new_name, datetime(new_expiry.year, new_expiry.month, new_expiry.day))
                    st.success(f"✅ Updated {new_name}")
                    st.session_state[f"editing_{product['_id']}"] = False
                    st.rerun()
            with col_cancel:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state[f"editing_{product['_id']}"] = False
                    st.rerun()

def render_add_item_tab():
    st.markdown("<h2>➕ Add Item Manually</h2>", unsafe_allow_html=True)
    with st.form("manual_entry_form"):
        name = st.text_input("Product Name")
        expiry_date = st.date_input("Expiry Date")
        if st.form_submit_button("✅ Add Product") and name:
            expiry_dt = datetime(expiry_date.year, expiry_date.month, expiry_date.day)
            add_product(st.session_state["user_email"], name, expiry_dt)
            st.success(f"✅ Added {name}, expiring on {expiry_dt.strftime('%Y-%m-%d')}.")
    
    st.markdown("<h2>📸 Upload Product Images (Tesseract OCR)</h2>", unsafe_allow_html=True)
    render_image_upload_form()

def render_image_upload_form():
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if st.session_state.form_submitted:
        st.session_state.form_submitted = False
        st.rerun()
    
    st.markdown("### 📱 Choose Upload Option:")
    
    # Fixed: Changed the text color to white for dark theme visibility
    st.markdown('<p style="color: white; font-weight: 500; margin-bottom: 10px;">Select how you want to upload images:</p>', unsafe_allow_html=True)
    
    upload_option = st.radio(
        "",  # Empty label since we're using custom text above
        ["📷 Single Photo", "🔄 Both Sides (Front & Back)"],
        key="upload_option",
        label_visibility="collapsed"
    )
    
    upload_counter = st.session_state.get('upload_counter', 0)
    
    if upload_option == "📷 Single Photo":
        render_single_upload(upload_counter)
    else:
        render_dual_upload(upload_counter)

def render_single_upload(upload_counter):
    """Single photo upload"""
    uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'], key=f"single_{upload_counter}")
    
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(uploaded_file.read())
            image_path = temp_file.name
        
        st.image(image_path, caption="Processing with Tesseract OCR", use_container_width=True)
        
        # Capture debug output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        with st.spinner("Extracting text..."):
            pred_product, pred_expiry = process_image_ocr(image_path, st.session_state["user_email"])
        
        debug_output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Show debug info
        if debug_output:
            with st.expander("🔍 Debug: What Tesseract Extracted", expanded=False):
                st.code(debug_output, language="text")
        
        render_ocr_form(pred_product, pred_expiry, [image_path], upload_counter)

def render_dual_upload(upload_counter):
    """Dual photo upload with debug info"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📷 Front Side:**")
        front_file = st.file_uploader("Front image", type=['png', 'jpg', 'jpeg'], key=f"front_{upload_counter}")
    
    with col2:
        st.markdown("**🔄 Back Side:**")
        back_file = st.file_uploader("Back image (optional)", type=['png', 'jpg', 'jpeg'], key=f"back_{upload_counter}")
    
    if front_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(front_file.read())
            front_path = temp_file.name
        
        image_paths = [front_path]
        back_path = None
        
        if back_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(back_file.read())
                back_path = temp_file.name
            image_paths.append(back_path)
        
        # Display images
        if back_path:
            col1, col2 = st.columns(2)
            with col1:
                st.image(front_path, caption="Front Side", use_container_width=True)
            with col2:
                st.image(back_path, caption="Back Side", use_container_width=True)
        else:
            st.image(front_path, caption="Front Side Only", use_container_width=True)
            st.info("💡 Upload back side for better accuracy")
        
        # Capture debug output
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        with st.spinner("Processing images..."):
            if back_path:
                pred_product, pred_expiry = process_dual_image_ocr(front_path, back_path, st.session_state["user_email"])
            else:
                pred_product, pred_expiry = process_image_ocr(front_path, st.session_state["user_email"])
        
        debug_output = buffer.getvalue()
        sys.stdout = old_stdout
        
        # Show debug info
        if debug_output:
            with st.expander("🔍 Debug: What Tesseract Extracted", expanded=False):
                st.code(debug_output, language="text")
        
        render_ocr_form(pred_product, pred_expiry, image_paths, upload_counter)

def render_ocr_form(pred_product, pred_expiry, image_paths, upload_counter):
    """OCR results form"""
    st.markdown("**Review & edit fields before saving:**")
    
    with st.form(f"ocr_form_{upload_counter}"):
        user_prod = st.text_input("Product Name (Auto-detected)", value=pred_product)
        user_expiry = st.text_input("Expiry Date (Auto-detected)", value=pred_expiry)
        
        # Confidence indicator
        if pred_product != "Unknown" and pred_expiry != "Unknown":
            st.success("🎯 Both detected!")
        elif pred_product != "Unknown" or pred_expiry != "Unknown":
            st.warning("⚠️ Partial detection")
        else:
            st.error("❌ No text detected")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            submit = st.form_submit_button("✅ Save")
        with col2:
            edit = st.form_submit_button("✏️ Log Feedback")
        with col3:
            skip = st.form_submit_button("❌ Skip")
        
        if submit and user_prod:
            try:
                parsed_expiry = dateparser.parse(user_expiry) or datetime(2025, 1, 1)
                add_product(st.session_state["user_email"], user_prod, parsed_expiry)
                st.success(f"✅ Product '{user_prod}' saved!")
                _cleanup_and_reset(image_paths)
            except Exception as e:
                st.error(f"Error: {e}")
                _cleanup_and_reset(image_paths)
        
        if edit:
            try:
                apply_hitl_feedback(st.session_state["user_email"], image_paths[0], pred_product, pred_expiry, user_prod, user_expiry)
                st.success("✅ Feedback logged!")
                _cleanup_and_reset(image_paths)
            except Exception as e:
                st.error(f"Error: {e}")
                _cleanup_and_reset(image_paths)
        
        if skip:
            st.warning("⚠️ Images skipped.")
            _cleanup_and_reset(image_paths)

def _cleanup_and_reset(image_paths):
    """Clean up temp files and reset"""
    for path in image_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
        except:
            pass
    
    st.session_state.form_submitted = True
    st.session_state.upload_counter = st.session_state.get('upload_counter', 0) + 1

def render_recycle_bin_tab():
    st.markdown("<h2>♻ Deleted Items</h2>", unsafe_allow_html=True)
    filter_option = st.selectbox("📂 Filter:", ["All Deleted", "Expired This Week", "All Expired"], key="recycle_filter")
    deleted_products = get_deleted_products(st.session_state["user_email"])
    
    if filter_option == "Expired This Week":
        deleted_products = [p for p in deleted_products if 0 <= (datetime.now() - p["expiry"]).days <= 7]
    elif filter_option == "All Expired":
        deleted_products = [p for p in deleted_products if p["expiry"] < datetime.now()]
    
    if deleted_products:
        for i, product in enumerate(deleted_products):
            col_item, col_restore, col_delete = st.columns([3, 1, 1])
            with col_item:
                st.markdown(f"🗑 {product['name']} - {product['expiry'].strftime('%Y-%m-%d')}")
            with col_restore:
                if st.button("↩️", key=f"restore_{i}"):
                    restore_product(product['_id'])
                    st.success(f"✅ Restored {product['name']}")
                    st.rerun()
            with col_delete:
                if st.button("❌", key=f"delete_{i}"):
                    st.warning(f"🗑 Permanently deleted {product['name']}")
                    st.rerun()
    else:
        st.info("📦 Recycle bin is empty")

def render_undo_functionality():
    if st.session_state.get("last_deleted_item"):
        item = st.session_state["last_deleted_item"]
        if st.button(f"↩️ Undo Delete: {item['name']}", key=f"undo_{item['_id']}"):
            restore_product(item['_id'])
            st.success(f"✅ Restored {item['name']}")
            st.session_state["last_deleted_item"] = None
            st.rerun()
