import nltk
from nltk.corpus import wordnet as wn

# only run in first time
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class SubwordTokenizer:
    def __init__(self):
        pass

    def is_in_dict(self, word: str, lang_code: str = 'eng') -> bool:
        """Check if word exists in WordNet for the specified language."""
        return len(wn.synsets(word, lang=lang_code)) > 0

    def split_compound(self, compound_word: str, min_len: int = 2, lang_code: str = 'eng') -> list[tuple[str, str]]:
        """
        Split compound word into 2 meaningful parts based on dictionary.
        min_len: Minimum length of subword (for Thai might need 1)
        """
        results = []
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

    word_list = ['Sunflower', 'Firefly', 'Keyboard']

    for word in word_list:
        print(f"{word}: {splitter.split_compound(word, lang_code='eng')}")