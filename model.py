import warnings, random
warnings.filterwarnings("ignore")

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
captions = []

def get_captions(image_path, limit):
    image = Image.open(image_path)
    inputs = processor(image, return_tensors="pt")

    for _ in range(limit):
        outputs = model.generate(**inputs, do_sample=True, temperature=0.7)
        caption = processor.tokenizer.decode(outputs[0], skip_special_tokens=True)
        captions.append(caption)

    return captions

    