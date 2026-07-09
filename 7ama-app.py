import streamlit as st
import google.generativeai as genai

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="SRT Translator", page_icon="🌍", layout="wide")

# ستایلی کوردی (ڕاست بۆ چەپ)
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_警示=True)

st.title("وەرگێڕی فایلی ژێرنووس (SRT) 📝")
st.write("بە بەکارهێنانی مۆدێلی Gemini 1.5 Flash - خێرا و بێبەرامبەر")

# Sidebar بۆ ڕێکخستنەکان
st.sidebar.header("⚙️ ڕێکخستنەکان")
api_key = st.sidebar.text_input("Google API Key لێرە دابنێ:", type="password")
target_language = st.sidebar.selectbox("وەرگێڕان بۆ زمانی:", 
    ["Kurdish (Soranî)", "Arabic", "English", "Persian", "Turkish", "German", "French"])

st.sidebar.markdown("---")
st.sidebar.info("تێبینی: ئەگەر هەڵەی 404ت بۆ هات، دڵنیابە کە API Key-ەکەت ڕاستە.")

# فەنکشنی سەرەکی وەرگێڕان
def translate_srt(text, target_lang):
    if not api_key:
        st.error("تکایە سەرەتا API Key داخڵ بکە!")
        return None
    
    try:
        # ڕێکخستنی API
        genai.configure(api_key=api_key)
        
        # تاقیکردنەوەی مۆدێلەکە بە فۆرماتی جیاواز بۆ دوورکەوتنەوە لە 404
        # زۆربەی کات 'gemini-1.5-flash' کار دەکات لە وەشانی نوێدا
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional subtitle translator.
        Translate the following SRT content into {target_lang}.
        
        Strict Rules:
        1. Keep all SRT index numbers and timestamps (e.g., 00:00:01,000 --> 00:00:04,000) EXACTLY as they are.
        2. Only translate the dialogue text.
        3. Do not add any explanations or extra text, only provide the translated SRT format.
        4. If it's Kurdish, use the Sorani dialect with Arabic script.

        Content to translate:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        st.error(f"هەڵەیەک ڕوویدا: {str(e)}")
        return None

# دروستکردنی تابەکان
tab1, tab2 = st.tabs(["📥 بارکردنی فایل", "✍️ کۆپی و پەیست"])

srt_input = ""

with tab1:
    uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە", type=["srt"])
    if uploaded_file is not None:
        srt_input = uploaded_file.read().decode("utf-8")
        st.success("فایلەکە بەسەرکەوتوویی بارکرا")

with tab2:
    text_input = st.text_area("دەقی فایلی SRT لێرە دابنێ:", height=300, placeholder="1\n00:00:01,000 --> 00:00:04,000\nHello world!")
    if text_input:
        srt_input = text_input

# دوگمەی وەرگێڕان
if st.button("دەستپێکردنی وەرگێڕان ✨"):
    if srt_input:
        with st.spinner('خەریکی وەرگێڕانە... تکایە چاوەڕێ بە (ئەمە چەند چرکەیەکی کەم دەخایەنێت)'):
            translated_text = translate_srt(srt_input, target_language)
            
            if translated_text:
                st.markdown("### ✅ وەرگێڕان تەواو بوو")
                
                # پیشاندانی ئەنجام لە سندوقێکدا
                st.text_area("ئەنجامی کۆتایی:", translated_text, height=300)
                
                # دروستکردنی دوگمەی داگرتن
                st.download_button(
                    label="📥 داگرتنی فایلی وەرگێڕدراو",
                    data=translated_text,
                    file_name=f"translated_{target_language}.srt",
                    mime="text/plain"
                )
    else:
        st.warning("تکایە دەقێک دابنێ یان فایلێک باربکە!")
