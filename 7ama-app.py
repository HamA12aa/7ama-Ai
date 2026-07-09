import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SRT Translator", page_icon="📝")

st.title("وەرگێڕی دەقی SRT")

st.sidebar.header("رێکخستنەکان")
api_key = st.sidebar.text_input("Google API Key لێرە دابنێ:", type="password")
target_language = st.sidebar.selectbox("وەرگێڕان بۆ زمانی:", ["Kurdish", "Arabic", "English", "Persian"])

def translate_srt(text, target_lang):
    if not api_key:
        st.error("تکایە API Key دابنێ!")
        return None
    
    try:
        genai.configure(api_key=api_key)
        # لێرە ناوی مۆدێلەکەمان بە وردی دیاری کردووە
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        
        prompt = f"Translate this SRT content to {target_lang}. Keep timestamps and format exactly the same: \n\n{text}"
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # ئەمە یارمەتیدەرە بۆ ئەوەی بزانیت کێشەکە چییە ئەگەر دووبارە بووەوە
        st.error(f"Error: {str(e)}")
        return None

tab1, tab2 = st.tabs(["کۆپی و پەیست", "بارکردنی فایل"])
srt_content = ""

with tab1:
    input_text = st.text_area("دەقی SRT لێرە دابنێ:", height=200)
    if input_text: srt_content = input_text

with tab2:
    uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە", type=["srt"])
    if uploaded_file: srt_content = uploaded_file.read().decode("utf-8")

if st.button("دەستپێکردنی وەرگێڕان"):
    if srt_content:
        with st.spinner('چاوەڕێ بە...'):
            translated_result = translate_srt(srt_content, target_language)
            if translated_result:
                st.text_area("ئەنجام:", translated_result, height=200)
                st.download_button("داگرتنی فایلەکە", translated_result, file_name="translated.srt")
    else:
        st.warning("هیچ دەقێک نییە بۆ وەرگێڕان")
