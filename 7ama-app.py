import streamlit as st

st.title("سڵاو، ئەمە یەکەم پڕۆژەی منە!")
st.write("بەخێر بێیت بۆ بەرنامەکەم کە بە Streamlit دروستکراوە.")

name = st.text_input("ناوت چییە؟")
if name:
    st.write(f"سڵاو {name}!")
