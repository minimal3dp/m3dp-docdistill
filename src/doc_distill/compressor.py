import nltk
from nltk.corpus import stopwords
import string
import re

class PromptCompressor:
    """
    Compresses text for LLM usage by removing low-semantic-value tokens.
    
    This class implements a semantic compression algorithm that reduces token count
    by removing stop words, punctuation, and excessive whitespace, while maintaining
    the core meaning of the text for Large Language Model (LLM) processing.
    """
    
    def __init__(self):
        """
        Initialize the PromptCompressor.
        
        Ensures that necessary NLTK resources (stopwords, punkt) are downloaded.
        """
        self._ensure_resources()
        self.stop_words = set(stopwords.words('english'))

    def _ensure_resources(self):
        """
        Check and download NLTK resources if missing.
        
        Downloads 'stopwords' and 'punkt' tokenizers if they are not already present.
        """
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

    def compress(self, text: str, lower_case: bool = False) -> str:
        """
        Compresses the input text by removing non-essential tokens.
        
        The compression process involves:
        1. Converting to lowercase (optional).
        2. Removing punctuation.
        3. Tokenizing the text.
        4. Filtering out standard English stop words.
        5. Rejoining the remaining tokens with single spaces.
        
        Args:
            text (str): The raw input text to be compressed.
            lower_case (bool): If True, converts all text to lowercase before processing.
                               This can help save tokens with some tokenizers. Defaults to False.
        
        Returns:
            str: The compressed string with reduced token count.
        """
        if lower_case:
            text = text.lower()

        # 1. Basic cleaning: Remove punctuation
        # We replace punctuation with spaces to prevent words joining (e.g., "hello.world" -> "hello world")
        translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        cleaned_text = text.translate(translator)

        # 2. Tokenize (split by whitespace)
        words = cleaned_text.split()

        # 3. Filter Stop Words
        filtered_words = [word for word in words if word.lower() not in self.stop_words]

        # 4. Join back together (automatically collapses whitespace)
        return " ".join(filtered_words)