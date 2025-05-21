import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Aesthetic Theme Config
st.set_page_config(
    page_title="Sales Dashboard", 
    layout="centered",
    page_icon="📊"
)

# Custom CSS for Aesthetic Dark Theme
st.markdown("""
    <style>
        :root {
            --primary: #8a63ff;
            --secondary: #ff6b9d;
            --bg: #121826;
            --card: #1e2430;
            --text: #e0e8ff;
            --accent: #5ce1ff;
        }
        
        html, body, .stApp {
            background-color: var(--bg);
            color: var(--text);
            font-family: 'Segoe UI', sans-serif;
        }
        .main {
            background-color: var(--card);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        h1, h2, h3 {
            color: var(--accent);
            font-weight: 600;
        }
        .stMarkdown {
            color: var(--text) !important;
        }
        .stDataFrame {
            background-color: var(--card) !important;
        }
        .stButton>button {
            background-color: var(--primary);
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

def get_db_engine():
    """Create PostgreSQL engine with SSL"""
    DB_URL = os.getenv("DATABASE_URL")
    if not DB_URL:
        st.error("❌ Database URL not found")
        st.stop()
    
    return create_engine(
        DB_URL,
        connect_args={
            "options": "-c client_encoding=utf8",
            "sslmode": "require"
        }
    )

@st.cache_data(ttl=300)
def load_data():
    """Load product sales data"""
    try:
        query = text("""
            SELECT "Product", COUNT(*) AS count
            FROM sales_data
            GROUP BY "Product";
        """)
        with engine.connect() as connection:
            result = connection.execute(query)
            return pd.DataFrame(result.mappings().all())
    except Exception as e:
        st.error(f"⚠️ Database error: {e}")
        return pd.DataFrame()

# Main App
with st.container():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    engine = get_db_engine()
    df = load_data()

    st.title("✨ Product Analytics")
    st.subheader("Top Performing Products")

    if not df.empty:
        # Aesthetic color scale (purple-pink gradient)
        fig = px.bar(
            df,
            x="Product",
            y="count",
            title="<b>Sales Distribution</b>",
            color="count",
            color_continuous_scale=px.colors.sequential.Magma,
            text="count",
            height=500
        )
        
        # Refined chart styling
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(
                family="'Segoe UI', sans-serif",
                color='#e0e8ff',
                size=14
            ),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=12, color='#8a63ff'),
                gridcolor='rgba(255,255,255,0.05)',
                linecolor='rgba(255,255,255,0.1)'
            ),
            yaxis=dict(
                gridcolor='rgba(255,255,255,0.05)',
                tickfont=dict(color='#8a63ff'),
                linecolor='rgba(255,255,255,0.1)'
            ),
            coloraxis_colorbar=dict(
                title='Sales Count',
                tickfont=dict(color='white')
            ),
            title_font=dict(
                size=24,
                color='#5ce1ff',
                family="'Segoe UI', sans-serif"
            ),
            hoverlabel=dict(
                bgcolor='#1e2430',
                font=dict(color='white'),
                bordercolor='rgba(255,255,255,0.1)'
            ),
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        # Bar styling
        fig.update_traces(
            texttemplate='<b>%{text}</b>',
            textposition='outside',
            textfont=dict(color='#e0e8ff', size=12),
            marker_line_color='rgba(255,255,255,0.2)',
            marker_line_width=1,
            opacity=0.9
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available", icon="⚠️")

    st.markdown('</div>', unsafe_allow_html=True)