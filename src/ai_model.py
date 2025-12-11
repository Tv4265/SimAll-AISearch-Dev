import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# --- 1. การเตรียมโมเดล Intent Classifier (I.C.) ---

# Dataset จำลอง: คำถามและเจตนา
IC_data = {
    'query': [
        "เช็คเบอร์ 081xxxxxxx", "ทำนายเบอร์มือถือ", "ดูผลรวมทะเบียนรถ", 
        "ความหมายเลข 42", "เลข 28 ดีไหม", "ดวงความรักปี 69", "ฤกษ์ดีเดือนธันวา",
        "เลขเด็ดงวดนี้", "วิธีแก้ปีชง"
    ],
    'intent': [
        'TOOL_CHECK_NUMBER', 'TOOL_CHECK_NUMBER', 'TOOL_CAR_PLATE_CHECK', 
        'INFO_NUM_MEANING', 'INFO_NUM_MEANING', 'INFO_TIMING_HORO', 'INFO_TIMING_HORO',
        'INFO_LUCKY_NUMBER', 'INFO_TIMING_HORO'
    ]
}
IC_df = pd.DataFrame(IC_data)

# ฝึกโมเดล I.C.
ic_vectorizer = TfidfVectorizer()
X_vectorized = ic_vectorizer.fit_transform(IC_df['query'])
ic_model = LogisticRegression()
ic_model.fit(X_vectorized, IC_df['intent'])

def predict_intent(user_query: str) -> str:
    """ทำนายเจตนาของผู้ใช้: TOOL_CHECK_NUMBER, INFO_NUM_MEANING, ฯลฯ"""
    query_vec = ic_vectorizer.transform([user_query])
    prediction = ic_model.predict(query_vec)[0]
    return prediction

# --- 2. การค้นหาเชิงความหมาย (Semantic Retrieval) ---

# Dataset จำลอง: บทความ (สำหรับค้นหาความหมาย)
SR_data = {
    'doc_id': [1, 2, 3, 4],
    'title': ["คู่เลข 24 เสน่ห์และเงิน", "เลข 78 กับการลงทุน", "ดวงปี 2569", "ฤกษ์ขึ้นบ้านใหม่"],
    'content': [
        "เลข 24 คือคู่แห่งเสน่ห์ เมตตามหานิยม เหมาะกับอาชีพที่ใช้การเจรจาและการค้าขาย",
        "เลข 78 คือเลขเจ้าพ่อ มีอำนาจ เหมาะกับการลงทุนระยะยาวและการบริหารกิจการใหญ่",
        "ปี 2569 เป็นปีม้าไฟ ชง 100% คือปีชวด ส่วนปีวัวเป็นปีทอง การงานดีมาก",
        "ฤกษ์ที่ดีที่สุดสำหรับขึ้นบ้านใหม่ในเดือนธันวาคมคือวันที่ 6, 10, และ 24"
    ]
}
SR_df = pd.DataFrame(SR_data)

# สร้าง Vector Embeddings สำหรับบทความทั้งหมด (จำลองด้วย TF-IDF)
sr_vectorizer = TfidfVectorizer()
content_vectors = sr_vectorizer.fit_transform(SR_df['content'])

def semantic_search(user_query: str, top_k: int = 2) -> pd.DataFrame:
    """ค้นหาบทความที่ใกล้เคียงที่สุดตามความหมาย (Cosine Similarity)"""
    query_vector = sr_vectorizer.transform([user_query])
    
    # คำนวณความใกล้เคียง (Similarity Score)
    similarity_scores = cosine_similarity(query_vector, content_vectors).flatten()
    
    # ดึงดัชนีของบทความที่มีคะแนนสูงสุด
    top_indices = np.argsort(similarity_scores)[::-1][:top_k]
    
    results = SR_df.iloc[top_indices].copy()
    results['similarity_score'] = similarity_scores[top_indices]
    
    return results

# --- 3. ฟังก์ชัน AI Search Engine หลัก ---

def ai_search_engine(user_query: str):
    """ฟังก์ชันหลักของ AI Search ที่รวม Intent และ Semantic Search"""
    intent = predict_intent(user_query)
    print(f"-> Detected Intent: {intent}")
    
    if intent.startswith('TOOL_'):
        # หากเป็นเจตนาต้องการเครื่องมือ 
        return f"ACTION: Redirect user to the relevant tool page based on {intent}."
    
    elif intent.startswith('INFO_'):
        # หากเป็นเจตนาต้องการข้อมูล ให้ค้นหาเชิงความหมาย
        results = semantic_search(user_query, top_k=2)
        
        # นำผลลัพธ์ไปสังเคราะห์คำตอบ (AI Synthesis)
        synthesized_answer = (
            f"Based on your query '{user_query}' (Intent: {intent}), "
            f"the most relevant information found is:\n"
            f"1. Title: {results.iloc[0]['title']} (Score: {results.iloc[0]['similarity_score']:.3f})\n"
            f"   Snippet: {results.iloc[0]['content'][:100]}...\n"
            f"2. Title: {results.iloc[1]['title']} (Score: {results.iloc[1]['similarity_score']:.3f})"
        )
        return synthesized_answer

# --- ตัวอย่างการรัน ---
print("--- TEST CASE 1: TOOL INTENT ---")
query_1 = "ฉันต้องการเช็คเบอร์ 099xxxxxxx"
print(ai_search_engine(query_1))

print("\n--- TEST CASE 2: INFO INTENT (Semantic) ---")
query_2 = "เลขอะไรที่เหมาะกับการค้าขายและดึงดูดลูกค้า?"
print(ai_search_engine(query_2))
