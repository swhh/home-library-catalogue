import vertexai
from vertexai.generative_models import GenerativeModel, Part, Image

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}
PROMPT_TEXT = 'List the titles and authors and of all books in this image. Provide response in plain text with a new line for each book. Separate author and title on each row by the "#" sign. The title should always be first on each row.'
PROJECT = "dulcet-name-441515-v3"


def generate_texts(images):
    vertexai.init(project=PROJECT, location="us-central1")
    model = GenerativeModel(
        "gemini-1.5-flash-002",
    )
    texts = []
    for image_bytes in images:
        response = model.generate_content([
        Part.from_image(Image.from_bytes(image_bytes)),
        PROMPT_TEXT,], generation_config=generation_config)
        texts.append(response.text)
    return texts
