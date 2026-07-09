import streamlit as st
import google.generativeai as genai

# رێکخستنی لاپەڕە
st.set_page_config(page_title="SRT Translator", page_icon="📝")

st.title("وەرگێڕی دەقی SRT")
st.write("دەقەکانت لێرە دابنێ یان فایلەکە باربکە بۆ وەرگێڕان بە Gemini 1.5 Flash")

# ڕێکخستنی Sidebar بۆ API Key و زمان
st.sidebar.header("رێکخستنەکان")
api_key = st.sidebar.text_input("Google API Key لێرە دابنێ:", type="password")
target_language = st.sidebar.selectbox("وەرگێڕان بۆ زمانی:", ["Kurdish", "Arabic", "English", "Persian"])

# فەرمانی وەرگێڕان
def translate_srt(text, target_lang):
    if not api_key:
        st.error("تکایە API Key دابنێ لە لای چەپ!")
        return None
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert subtitle translator. 
    Translate the following SRT content into {target_lang}.
    Rules:
    1. Keep the SRT index numbers and timestamps EXACTLY as they are.
    2. Only translate the spoken text.
    3. Maintain the SRT format structure.
    4. Provide only the translated SRT text as output.

    Content:
    {text}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"هەڵەیەک ڕوویدا: {str(e)}")
        return None

# دروستکردنی دوو تابی جیاواز (یەک بۆ کۆپی-پەیست، یەک بۆ فایل)
tab1, tab2 = st.tabs(["کۆپی و پەیست (Paste Text)", "بارکردنی فایل (Upload File)"])

srt_content = ""

with tab1:
    input_text = st.text_area("دەقی فایلی SRT لێرە دابنێ (Paste):", height=300)
    if input_text:
        srt_content = input_text

with tab2:
    uploaded_file = st.file_uploader("فایلی SRT هەڵبژێرە", type=["srt"])
    if uploaded_file is not None:
        srt_content = uploaded_file.read().decode("utf-8")
        st.success("فایلەکە بەسەرکەوتوویی خوێنرایەوە!")

# دوگمەی دەستپێکردنی وەرگێڕان
if st.button("دەستپێکردنی وەرگێڕان ✨"):
    if srt_content:
        with st.spinner('خەریکی وەرگێڕانە... تکایە چاوەڕێ بە'):
            translated_result = translate_srt(srt_content, target_language)
            
            if translated_result:
                st.subheader("ئەنجامی وەرگێڕان:")
                st.text_area("دەقی وەرگێڕدراو:", translated_result, height=300)
                
                # دوگمەی دابەزاندن
                st.download_button(
                    label="داگرتنی فایلی وەرگێڕدراو (.srt)",
                    data=translated_result,
                    file_name=f"translated_{target_language}.srt",
                    mime="text/plain"
                )
    else:
        st.warning("تکایە سەرەتا دەقێک دابنێ یان فایلێک باربکە.")
