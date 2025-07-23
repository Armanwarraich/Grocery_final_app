import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helpers import get_expiry_status

def render_insights_tab(products):
    st.markdown("<h2>📊 Insights</h2>", unsafe_allow_html=True)
    
    if products:
        render_status_pie_chart(products)
        render_timeline_chart(products)
    else:
        st.info("No products available for insights.")

def render_status_pie_chart(products):
    status_counts = {"Fresh": 0, "Expiring Soon": 0, "Expired": 0}
    for product in products:
        status = get_expiry_status(product["expiry"])
        if status in status_counts:
            status_counts[status] += 1
    
    status_df = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
    fig_pie = px.pie(
        status_df, values="Count", names="Status", 
        title="Product Status Distribution",
        color_discrete_map={"Fresh": "#00C851", "Expiring Soon": "#ffbb33", "Expired": "#ff4444"}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

def render_timeline_chart(products):
    timeline_data = [
        {"Product": p["name"], "Expiry Date": p["expiry"], "Status": get_expiry_status(p["expiry"])}
        for p in products if p.get("expiry")
    ]
    
    if timeline_data:
        timeline_df = pd.DataFrame(timeline_data).sort_values(by="Expiry Date")
        fig_timeline = px.scatter(
            timeline_df, x="Expiry Date", y="Product", color="Status",
            title="Product Expiry Timeline",
            color_discrete_map={"Fresh": "#00C851", "Expiring Soon": "#ffbb33", "Expired": "#ff4444"}
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

def render_alerts_tab(products):
    st.markdown("<h2>⚡ Alerts</h2>", unsafe_allow_html=True)
    
    expired_products = [p for p in products if get_expiry_status(p["expiry"]) == "Expired"]
    soon_products = [p for p in products if get_expiry_status(p["expiry"]) == "Expiring Soon"]
    
    if expired_products:
        st.error("❌ **Expired Products:**")
        for p in expired_products:
            st.error(f"• {p['name']} expired on {p['expiry'].strftime('%Y-%m-%d')}")
    
    if soon_products:
        st.warning("⚠️ **Expiring Soon:**")
        for p in soon_products:
            st.warning(f"• {p['name']} expires on {p['expiry'].strftime('%Y-%m-%d')}")
    
    if not expired_products and not soon_products:
        st.success("✅ No alerts! All products are fresh.")
