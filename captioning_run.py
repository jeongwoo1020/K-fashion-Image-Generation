from captioning_utils import read_base64_images, generate_fashion_description, save_results_to_json
import openai

openai.api_key = "YOUR_API_KEY"

style_list=['레트로','로맨틱','리조트','매니시','모던','기타','밀리터리','섹시','소피스트케이티드']

for style in style_list:
    # image_base64.json에서 이미 이미지 데이터를 불러오기
    image_base64_data = read_base64_images(f'{style}_image_base64.json') 

    selected_images = list(image_base64_data.keys()) 

    # 이미지 파일명 목록과 처리할 이미지 데이터 목록 설정
    for file_name in selected_images:
        try:
            description = generate_fashion_description(image_base64_data, file_name)
            print(f"\n📌 {file_name}")
            print(description)
            save_results_to_json(f"{style}_image_caption_results.jsonl", file_name, description) 
        except Exception as e:
            print(f"❌ Error processing {file_name}: {e}")