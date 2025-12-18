import nltk
from nltk.corpus import wordnet as wn
from langdetect import detect, detect_langs

# only run in first time
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

class SubwordTokenizer:
    def __init__(self):
        # ISO 639-1 to ISO 639-3 mapping
        self.lang_map = {
            'af': 'afr',
            'ar': 'ara',
            'bg': 'bul',
            'bn': 'ben',
            'ca': 'cat',
            'cs': 'ces',
            'cy': 'cym',
            'da': 'dan',
            'de': 'deu',
            'el': 'ell',
            'en': 'eng',
            'es': 'spa',
            'et': 'est',
            'fa': 'fas',
            'fi': 'fin',
            'fr': 'fra',
            'gu': 'guj',
            'he': 'heb',
            'hi': 'hin',
            'hr': 'hrv',
            'hu': 'hun',
            'id': 'ind',
            'it': 'ita',
            'ja': 'jpn',
            'kn': 'kan',
            'ko': 'kor',
            'lt': 'lit',
            'lv': 'lav',
            'mk': 'mkd',
            'ml': 'mal',
            'mr': 'mar',
            'ne': 'nep',
            'nl': 'nld',
            'no': 'nor',
            'pa': 'pan',
            'pl': 'pol',
            'pt': 'por',
            'ro': 'ron',
            'ru': 'rus',
            'sk': 'slk',
            'sl': 'slv',
            'so': 'som',
            'sq': 'sqi',
            'sv': 'swe',
            'sw': 'swa',
            'ta': 'tam',
            'te': 'tel',
            'th': 'tha',
            'tl': 'tgl',
            'tr': 'tur',
            'uk': 'ukr',
            'ur': 'urd',
            'vi': 'vie',
            'zh-cn': 'cmn',
            'zh-tw': 'cmn'
        }

        # Get list of supported languages in WordNet (OMW 1.4)
        self.supported_langs = [
        "tha",
        "als",
        "arb",
        "bul",
        "cow",
        "dan",
        "ell",
        "fin",
        "fra",
        "heb",
        "hrv",
        "isl",
        "ita",
        "iwn",
        "jpn",
        "mcr",
        "msa",
        "nld",
        "nor",
        "pol",
        "por",
        "ron",
        "slk",
        "slv",
        "swe"
    ]
        # Ensure 'eng' is always supported (it's the base)
        self.supported_langs.append('eng')

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
            print(f"Language {lang_code} not supported, falling back to 'eng'")
            lang_code = 'eng'
            
        try:
            return len(wn.synsets(word, lang=lang_code)) > 0
        except Exception as e:
            print(f"WordNet error: {e}")
            return False

    def split_compound(self, compound_word: str, min_len: int = 2) -> list[list[str]]:
        """
        Split compound word into 2 or more meaningful parts based on dictionary.
        min_len: Minimum length of subword (for Thai might need 1)
        """
        lang_code = self.detect_language(compound_word)
        memo = {}

        def _recursive_split(text):
            if text in memo:
                return memo[text]
            
            valid_splits = []
            
            # Check if the text itself is a valid word
            if self.is_in_dict(text, lang_code):
                valid_splits.append([text])
            
            # Try to split into prefix + suffix
            for i in range(min_len, len(text) - min_len + 1):
                prefix = text[:i]
                suffix = text[i:]
                
                if self.is_in_dict(prefix, lang_code):
                    suffix_splits = _recursive_split(suffix)
                    for s_split in suffix_splits:
                        valid_splits.append([prefix] + s_split)
                        
            memo[text] = valid_splits
            return valid_splits

        all_splits = _recursive_split(compound_word)
        # Filter specifically for compound usage (2 or more parts)
        return [s for s in all_splits if len(s) >= 2]

if __name__ == "__main__":
    splitter = SubwordTokenizer()

    # Example 1: English
    # word_list_en = ['Sunflower', 'Firefly', 'Keyboard']
    # for word in word_list_en:
    #     print(f"{word}: {splitter.split_compound(word)}")

    # Example 2: Thai
    word_list_th = [
        "ตู้เย็น", "พัดลม", "เตารีด", "รถเมล์", "ปากกา",
        "น้ำปลา", "ใจดี", "อ่อนน้อม", "บ้านพัก", "ทางม้าลาย",
        "แม่ครัว", "ลูกน้อง", "หนังสือพิมพ์", "ไฟฉาย", "ยาสระผม",
        "รองเท้า", "ผ้าห่ม", "เข็มขัด", "แกงเผ็ด", "กล้วยแขก",
        "ตู้เย็นขนาดเล็ก", "เครื่องปรับอากาศ", "เตาไมโครเวฟ", "รถโดยสารประจำทาง", "พนักงานทำความสะอาด",
        "หนังสือแบบเรียน", "เครื่องซักผ้า", "กล้องถ่ายรูป", "น้ำยาล้างจาน", "รองเท้าผ้าใบ",
        "โทรศัพท์มือถือ", "ทางม้าลายข้ามถนน", "รถไฟความเร็วสูง", "แผ่นพับโฆษณา", "กระดาษชำระ",
        "หม้อหุงข้าวไฟฟ้า", "กระเป๋าสตางค์", "ไม้บรรทัดเหล็ก", "ยาสีฟันสมุนไพร", "ช้อนส้อมพลาสติก"
    ]
    for word in word_list_th:
        print(f"{word}: {splitter.split_compound(word)}")