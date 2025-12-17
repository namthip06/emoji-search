import nltk
from nltk.corpus import wordnet as wn
from langdetect import detect, detect_langs

try:
    from .iso_mapping import iso_mapping
except ImportError:
    try:
        from iso_mapping import iso_mapping
    except ImportError:
        # Fallback if running from outside and utils not in path (?) - though app.py adds it
        from utils.iso_mapping import iso_mapping 

# only run in first time
# try:
#     nltk.data.find('corpora/wordnet')
# except LookupError:
#     nltk.download('wordnet')

# try:
#     nltk.data.find('corpora/omw-1.4')
# except LookupError:
#     nltk.download('omw-1.4')

class SubwordTokenizer:
    def __init__(self):
        # ISO 639-1 to ISO 639-3 mapping
        self.lang_map = iso_mapping
        
        # Get list of supported languages in WordNet (OMW 1.4)
        self.supported_langs = set(wn.langs())
        # Ensure 'eng' is always supported (it's the base)
        self.supported_langs.add('eng')

    def iso_1_to_3(self, lang_code: str) -> str:
        """Convert ISO 639-1 code to ISO 639-3 code."""
        return self.lang_map.get(lang_code.lower(), 'eng')

    def detect_language(self, text: str) -> str:
        # print(f"Detecting language of {text}")
        """Detect language of the text and return ISO 639-3 code."""
        try:
            # Detect language
            lang = detect(text)
            # Convert to 3-letter code
            return self.iso_1_to_3(lang)
        except Exception as e:
            print(f"Error detecting language: {e}")
            return 'eng'

    def is_in_dict(self, word: str, lang_code: str = 'eng') -> bool:
        """Check if word exists in WordNet for the specified language."""
        # If language is not supported by WordNet, fallback to English
        # or return False. Here we fallback to 'eng' to handle cases
        # where English words are misidentified (e.g. Firefly -> cym)
        if lang_code not in self.supported_langs:
            # print(f"Language {lang_code} not supported, falling back to 'eng'")
            lang_code = 'eng'
            
        # print(f"Checking {word} in {lang_code}")
        try:
            return len(wn.synsets(word, lang=lang_code)) > 0
        except Exception as e:
            # print(f"WordNet error: {e}")
            return False

    def split_compound(self, compound_word: str, min_len: int = 2) -> list[tuple[str, str]]:
        """
        Split compound word into 2 meaningful parts based on dictionary.
        min_len: Minimum length of subword (for Thai might need 1)
        """
        results = []
        lang_code = self.detect_language(compound_word)
        word_len = len(compound_word)
        
        # Loop to find all possible split points
        for i in range(min_len, word_len - min_len + 1):
            prefix = compound_word[:i]
            suffix = compound_word[i:]

            if self.is_in_dict(prefix, lang_code) and self.is_in_dict(suffix, lang_code):
                results.append((prefix, suffix))
        
        return results

if __name__ == "__main__":
    splitter = SubwordTokenizer()

    # Example 1: English
    # word_list_en = ['Sunflower', 'Firefly', 'Keyboard']
    # for word in word_list_en:
    #     print(f"{word}: {splitter.split_compound(word)}")

    # Example 2: Thai
    word_list_th = ['เสื้อกันฝน', 'เครื่องดูดฝุ่น', 'ที่เปิดกระป๋อง']
    for word in word_list_th:
        print(f"{word}: {splitter.split_compound(word)}")