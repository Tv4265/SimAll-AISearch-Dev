import pandas as pd

def extract_and_lookup_pairs(phone_number: str, meaning_df: pd.DataFrame) -> list:
    """แยกคู่เลขจากเบอร์โทรศัพท์และดึงความหมายจาก DataFrame"""
    cleaned_num = phone_number.replace('-', '').strip()
    if len(cleaned_num) != 10 or not cleaned_num.startswith('0'):
        return [{"error": "Invalid phone number format."}]
    
    seven_digits = cleaned_num[1:] # ตัด 0 ออก เหลือ 9 หลัก
    
    analysis_results = []
    # วนลูปเพื่อหาคู่เลข 7 คู่
    for i in range(len(seven_digits) - 1):
        pair = seven_digits[i:i+2]
        
        # ค้นหาความหมายใน DataFrame ที่โหลดมาจาก data/processed/numerology_meaning.csv
        lookup = meaning_df[meaning_df['number_pair'] == pair]
        
        if not lookup.empty:
            meaning = lookup.iloc[0]['meaning_th']
            traits = lookup.iloc[0]['positive_traits']
        else:
            meaning = "ไม่พบข้อมูล/รออัปเดต"
            traits = "N/A"
            
        analysis_results.append({
            'pair': pair,
            'index': i + 1,
            'meaning': meaning,
            'traits': traits
        })
        
    return analysis_results

# ตัวอย่างการใช้งาน (สมมติว่าโหลด DataFrame จาก data/processed/numerology_meaning.csv แล้ว)
# meaning_df = pd.read_csv('data/processed/numerology_meaning.csv')
# results = extract_and_lookup_pairs("0814289639", meaning_df)
# print(json.dumps(results, indent=2, ensure_ascii=False))
