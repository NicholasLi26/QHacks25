# chatgpt lmfao

import requests

def send_to_google_gemini(api_url, api_key, images, prompt):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    responses = []
    
    for i, image_path in enumerate(images):
        with open(image_path, "rb") as img_file:
            # Convert image to base64 if needed by the API
            image_data = img_file.read()
            # You may need to base64 encode this based on API documentation
            # import base64
            # image_data = base64.b64encode(img_file.read()).decode("utf-8")
            
            payload = {
                "prompt": prompt,
                "image": image_data,
            }

            try:
                response = requests.post(api_url, headers=headers, json=payload)
                response.raise_for_status()  # Raise HTTPError for bad responses
                responses.append(response.json())
            except requests.exceptions.RequestException as e:
                print(f"Error sending request for image {i + 1}: {e}")
    
    return responses

# Example Usage
if __name__ == "__main__":
    # Replace these placeholders with actual values
    GOOGLE_GEMINI_API_URL = "https://api.google.com/gemini/v1/your-endpoint"
    API_KEY = "your_api_key_here"

    images = [
        "images/mon.png",
        "images/tue.png",
        "images/wed.png",
        "images/thu.png",
        "images/fri.png",
    ]
    prompt = "What day of the week is this, what classes do I have, and what are the start and end times of each class? Thank you!"

    responses = send_to_google_gemini(GOOGLE_GEMINI_API_URL, API_KEY, images, prompt)

    for i, response in enumerate(responses):
        print(f"Response for Image {i + 1}: {response}")