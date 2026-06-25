import streamlit as st
from billbot_core import BillBotCore

# Page Configuration
st.set_page_config(
    page_title="BillBot - AI Billing Agent",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 BillBot - Smart Retail Billing Agent")

# Initialize the bot
if "bot" not in st.session_state:
    st.session_state.bot = BillBotCore()

# Layout: Two Columns
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💬 Talk to BillBot")
    user_input = st.text_input("Type your command here (e.g. add 2 parle g)", key="user_input")

    if st.button("Send", type="primary"):
        if user_input.strip():
            response = ""
            lower_input = user_input.lower()

            if "add" in lower_input:
                response = st.session_state.bot.add_item(user_input)
            elif any(word in lower_input for word in ["cart", "total", "show"]):
                response = st.session_state.bot.get_cart()
            elif any(word in lower_input for word in ["receipt", "bill", "print"]):
                response = st.session_state.bot.generate_receipt()
            elif "inventory" in lower_input:
                response = st.session_state.bot.get_inventory()
            else:
                response = "✅ Try commands like:\n• `add 2 parle g`\n• `show cart`\n• `print receipt`\n• `inventory`"

            st.success(response)

with col2:
    st.subheader("🛒 Current Cart")
    st.markdown(st.session_state.bot.get_cart())

# Sidebar
st.sidebar.subheader("📦 Inventory Status")
st.sidebar.markdown(st.session_state.bot.get_inventory())

if st.sidebar.button("🗑️ Clear Cart"):
    st.session_state.bot.cart = []
    st.rerun()
