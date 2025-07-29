from collections import Counter
import re

class TextAnalyzer:
    def __init__(self, text):
        """
        Initialize with text to analyze
        Args:
            text (str): Text to analyze
        """
        self.original_text = text
        self.text = text.lower() # For case-insensitive analysis

    def get_character_frequency(self, include_spaces=False):
        """
        Get frequency of each character
        Args:
            include_spaces (bool): Whether to include spaces in count
        Returns:
            Counter: Character frequencies
        """
        text_to_count = self.text if include_spaces else self.text.replace(" ", "")
        return Counter(text_to_count)

    def get_word_frequency(self, min_length=1):
        """
        Get frequency of each word (minimum length filter)
        Args:
            min_length (int): Minimum word length to include
        Returns:
            Counter: Word frequencies
        """
        words = re.findall(r'\b\w+\b', self.text)
        filtered_words = filter(lambda x : len(x) >= min_length, words)
        return Counter(filtered_words)


    def get_sentence_length_distribution(self):
        """
        Analyze sentence lengths (in words)
        Returns:
            dict: Contains 'lengths' (Counter), 'average', 'longest', 'shortest'
        """
        # Split sentences using punctuation marks (., !, ?) followed by a space or end of string
        sentences = re.split(r'[.!?]+(?:\s|$)', self.text)

        # Remove empty strings and strip whitespace
        sentences = [s.strip() for s in sentences if s.strip()]

        # Count the number of words in each sentence
        sentence_lengths = [len(re.findall(r'\b\w+\b', sentence)) for sentence in sentences]

        # Use Counter to count how many sentences have each length
        length_count = Counter(sentence_lengths)

        return {
            "lengths" : length_count,
            "average" : sum(sentence_lengths)/len(sentence_lengths) if sentence_lengths else 0,
            "longest" : max(sentence_lengths),
            "shortest" : min(sentence_lengths)
        }

    def find_common_words(self, n=10, exclude_common=True):
        """
        Find most common words, optionally excluding very common English words
        Args:
            n (int): Number of words to return
            exclude_common (bool): Exclude common words like 'the', 'and', etc.
        Returns:
            list: List of tuples (word, count)
        """
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
                        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                        'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
                        'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        words = re.findall(r'\b\w+\b', self.text)
        if exclude_common:
            words = [word for word in words if word not in common_words]
        word_counts = Counter(words)
        return word_counts.most_common(n)

    def get_reading_statistics(self):
        """
        Get comprehensive reading statistics
        Returns:
            dict: Contains character_count, word_count, sentence_count,
                  average_word_length, reading_time_minutes (assume 200 WPM)
        """
        # Characters (excluding spaces)
        character_count = len(self.text.replace(" ", ""))

        # Words
        words = re.findall(r'\b\w+\b', self.text)
        word_count = len(words)

        # Sentences
        sentences = re.split(r'[.!?]+(?:\s|$)', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = len(sentences)

        total_word_length = sum(len(word) for word in words)
        average_word_length = total_word_length / word_count if word_count > 0 else 0

        reading_time_minutes = word_count / 200

        return {
            'character_count': character_count,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': average_word_length,
            'reading_time_minutes': reading_time_minutes
        }


    def compare_with_text(self, other_text):
        """
        Compare this text with another text
        Args:
            other_text (str): Text to compare with
        Returns:
            dict: Contains 'common_words', 'similarity_score', 'unique_to_first', 'unique_to_second'
        """
         # Normalize both texts
        words_self = set(re.findall(r'\b\w+\b', self.text.lower()))
        words_other = set(re.findall(r'\b\w+\b', other_text.lower()))

        # Common and unique words
        common_words = words_self & words_other
        unique_to_first = words_self - words_other
        unique_to_second = words_other - words_self

        # Similarity score: Jaccard similarity
        union = words_self | words_other
        similarity_score = len(common_words) / len(union) if union else 0

        return {
            'common_words': sorted(list(common_words)),
            'similarity_score': similarity_score,
            'unique_to_first': sorted(list(unique_to_first)),
            'unique_to_second': sorted(list(unique_to_second))
        }

# Test your implementation
sample_text = """
Python is a high-level, interpreted programming language with dynamic semantics.
Its high-level built-in data structures, combined with dynamic typing and dynamic binding,
make it very attractive for Rapid Application Development. Python is simple, easy to learn
syntax emphasizes readability and therefore reduces the cost of program maintenance.
Python supports modules and packages, which encourages program modularity and code reuse.
The Python interpreter and the extensive standard library are available in source or binary
form without charge for all major platforms, and can be freely distributed.
"""

analyzer = TextAnalyzer(sample_text)

print("Character frequency (top 5):", analyzer.get_character_frequency().most_common(5))
print("Word frequency (top 5):", analyzer.get_word_frequency().most_common(5))
print("Common words:", analyzer.find_common_words(5))
print("Reading statistics:", analyzer.get_reading_statistics())

# Compare with another text
other_text = "Java is a programming language. Java is object-oriented and platform independent."
comparison = analyzer.compare_with_text(other_text)
print("Comparison results:", comparison)
