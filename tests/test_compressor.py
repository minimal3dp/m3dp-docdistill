import pytest
from doc_distill.compressor import PromptCompressor

@pytest.fixture
def compressor():
    return PromptCompressor()

def test_basic_compression(compressor):
    text = "The quick brown fox jumps over the lazy dog."
    # Stop words: "The", "over", "the"
    # Expected: "quick brown fox jumps lazy dog" (case sensitive unless specified)
    # Actually, "The" might not be in lowercase stopwords list if we don't lower it first, 
    # but NLTK stopwords are usually lowercase.
    # Let's check logic: word.lower() not in stop_words. So "The" -> "the" -> in stop_words -> removed.
    
    expected = "quick brown fox jumps lazy dog"
    # Note: punctuation is removed.
    assert compressor.compress(text) == expected

def test_punctuation_removal(compressor):
    text = "Hello, world! This is a test."
    expected = "Hello world test"
    assert compressor.compress(text) == expected

def test_lowercase_option(compressor):
    text = "The Quick Brown Fox"
    expected = "quick brown fox"
    assert compressor.compress(text, lower_case=True) == expected

def test_empty_input(compressor):
    assert compressor.compress("") == ""

def test_only_stopwords(compressor):
    text = "The a an in on at"
    assert compressor.compress(text) == ""

def test_whitespace_collapse(compressor):
    text = "Word1    Word2\nWord3"
    expected = "Word1 Word2 Word3"
    assert compressor.compress(text) == expected
