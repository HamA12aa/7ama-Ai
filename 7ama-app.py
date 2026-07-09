import streamlit as st
import google.generativeai as genai
import time

# رێکخستنی لاپەڕە
st.set_page_config(page_title="SRT Translator (Gemini Flash)", layout="centered")

st.title("وەرگێڕی فایلە ژێرنووسەکان (SRT)")
st.write("بە بەکارهێنانی Google Gemini 1.5 Flash")

# وەرگرتنی API Key لە بەکارهێنەر
api_key = st.sidebar.text_input("Google API Key لێرە دابنێ:", type="password")
target_language = st.selectbox("وەرگێڕان بۆ زمانی:", ["Kurdish", "Arabic", "English", "Persian"])

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.warning("تکایە سەرەتا API Key فۆرمات بکە لە لای چەپەوە.")

# فەرمانی وەرگێڕان بە Gemini
def translate_text(text, target_lang):
    prompt = f"""
    You are a professional subtitle translator. 
    Translate the following SRT subtitle content into {target_lang}.
    Rules:
    1. Keep the SRT index numbers and timestamps exactly as they are.
    2. Only translate the text content.
    3. Maintain the formatting.
    
    Content:
    {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# بارکردنی فایل
uploaded_file = st.file_uploader("فایلی SRT باربکە", type=["srt"])

if uploaded_file is not None and api_key:
    # خوێندنەوەی ناوەڕۆکی فایلەکە
    content = uploaded_file.read().decode("utf-8")
    
    if st.button("دەستپێکردنی وەرگێڕان"):
        with st.spinner('خەریکی وەرگێڕانە... کەمێک چاوەڕێ بە'):
            # تێبینی: بۆ فایلە زۆر گەورەکان باشترە فایلەکە پارچە پارچە بکرێت، 
            # بەڵام Gemini Flash توانای وەرگرتنی دەقی زۆری هەیە.
            translated_content = translate_text(content, target_language)
            
            if translated_content:
                st.success("وەرگێڕان بەسەرکەوتوویی تەواو بوو!")
                
                # پیشاندانی بەشێکی کەم لە وەرگێڕانەکە
                st.text_area("نموونەیەک لە وەرگێڕانەکە:", translated_content[:500], height=200)
                
                # دوگمەی دابەزاندن (Download)
                st.download_button(
                    label="داگرتنی فایلی وەرگێڕدراو",
                    data=translated_content,
                    file_name=f"translated_{target_language}.srt",
                    mime="text/plain"
                )
