def translate_srt(text, target_lang):
    if not api_key:
        st.error("تکایە API Key دابنێ!")
        return None
    
    try:
        genai.configure(api_key=api_key)
        
        # تاقیکردنەوەی چەند ناوێکی جیاوازی مۆدێلەکە بۆ دڵنیایی
        model_name = 'gemini-1.5-flash-latest' # یان 'gemini-1.5-flash'
        
        model = genai.GenerativeModel(model_name=model_name)
        
        prompt = f"""
        Translate this SRT subtitle to {target_lang}. 
        Keep the SRT format and timestamps exactly the same.
        Text:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # ئەگەر کێشەی هەبوو، لێرە لیستێک لەو مۆدێلانە دەبینین کە کاردەکەن بۆت
        st.error(f"هەڵە: {str(e)}")
        return None
