from googletrans import Translator

def translate_text(text, target_language='en'):
    translator = Translator()
    try:
        translated_text = translator.translate(text, dest=target_language)
        return translated_text.text
    except Exception as e:
        print("Translation Error:", e)
        return None

# Original title
original_title = "Hello, World!"

# Translate to French
translated_title = translate_text(original_title, target_language='fr')

if translated_title:
    print("Original Title:", original_title)
    print("Translated Title:", translated_title)
else:
    print("Translation failed.")
