import openai
import json
import os
# OpenAI API 키 설정
OPENAI_API_KEY = "YOUR_API_KEY"

# image_base64.json에서 base64로 인코딩된 이미지 데이터를 불러오는 함수
def read_base64_images(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 결과 저장 함수
def save_results_to_file(result_path, file_name, caption):
    # 결과 파일에 저장
    with open(result_path, "a", encoding="utf-8") as result_file:
        result_file.write(f"이미지 '{file_name}' 캡션:\n{caption.strip()}\n\n")


def save_results_to_json(result_path, file_name, caption):
    data = {"gt": file_name, "caption": caption.strip()}
    with open(result_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + ",\n")  # 쉼표도 같이 붙임

# 이미지를 처리하는 함수
def generate_fashion_description(image_base64_data, file_name):
    # image_base64_data에서 해당 이미지의 base64 인코딩된 데이터를 그대로 가져오기
    encoded_image = image_base64_data.get(file_name)

    if not encoded_image:
        raise ValueError(f"No image data found for {file_name}")

    common_prompt = '''
    You are a creative fashion image captioning assistant. Generate a two-sentence description of a fashion outfit based on the image. Do NOT describe or identify the person in the image.

    First sentence:
    If shoes or footwear are clearly visible, describe the only footwear factually using this exact format:
    'The outfit is styled with [type of footwear] featuring [notable characteristics].'
    If footwear is not visible or cannot be identified: Skip the first sentence.
    
    Second sentence:
    Always include this sentence and add a stylized, emotional summary using this exact format: 
    'This [style] look evokes [mood], perfect for [season]’s [setting].'

    To encourage variety and consistency, follow these expression banks:
    Use the [style] to guide the selection of [mood] from its matching group. Do not reuse the same word across multiple generations. Be creative, polished, and fashion-forward.

    [Style → Recommended Mood Group]
    • sexy → Bold & Edgy(bold, fierce, rebellious, confident, daring, sharp)
    • elegant → Chic & Sophisticated(elegant, refined, polished, timeless, understated)
    • casual → Youthful & Playful(playful, spirited, fresh, bubbly, carefree)
    • chic → Chic & Sophisticated / Soft & Serene(dreamy, tranquil, poetic, gentle, graceful, airy)
    • vintage → Romantic & Feminine(romantic, sweet, whimsical, delicate, nostalgic) / Soft & Serene
    • minimalist → Soft & Serene / Chic & Sophisticated
    • street → Bold & Edgy / Youthful & Playful
    • preppy → Youthful & Playful / Romantic & Feminine

    [Setting Bank – time/place/occasion examples]
    daily wear, a casual café outing, a weekend getaway, a beach day, a picnic in the park, a morning run, a mountain hike, a school day, a yoga session, a romantic date, a stroll on campus, a stylish office day, a cozy camping trip, a summer festival, a wedding ceremony, a first date, a casual tennis match, a day at the pool, a confident interview, a formal family gathering
    '''
    
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": common_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "This is the fashion image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ],
        temperature=1.0,
        max_tokens=100
    )

    return response.choices[0].message.content

