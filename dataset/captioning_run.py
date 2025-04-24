from captioning_utils import read_base64_images, generate_fashion_description, save_results_to_file
import openai

openai.api_key = "YOUR_API_KEY"

# image_base64.json에서 이미 이미지 데이터를 불러오기만 합니다.
image_base64_data = read_base64_images('retro_image_base64.json')  # 여기서 'image_base64.json' 파일 경로를 설정하세요

# 첫 10개 이미지만 선택
selected_images = list(image_base64_data.keys()) 

# 이미지 파일명 목록과 처리할 이미지 데이터 목록 설정
for file_name in selected_images:
    try:
        description = generate_fashion_description(image_base64_data, file_name)
        print(f"\n📌 {file_name}")
        print(description)
        save_results_to_file("retro_image_caption_results.jsonl", file_name, description)  # 여기에 캡션을 저장
    except Exception as e:
        print(f"❌ Error processing {file_name}: {e}")