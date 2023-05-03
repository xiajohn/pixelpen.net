import os
import spacy
import nltk
from nltk.corpus import wordnet
from collections import Counter
from textstat import flesch_reading_ease
nltk.download('punkt')
class BlogReviewer:
    def __init__(self, text):
        self.text = text
        self.nlp = spacy.load("en_core_web_sm")

    def adjust_connectors(self, sentences):
        connectors = ["Moreover", "Additionally", "Furthermore", "However", "On the other hand", "Consequently", "In contrast"]
        modified_sentences = []
        for idx, sent in enumerate(sentences):
            if idx > 0 and idx % 3 == 0:
                modified_sentences.append(f"{connectors[idx % len(connectors)]}, {sent}")
            else:
                modified_sentences.append(sent)
        return modified_sentences

    def adjust_word_usage(self, text):
        words = nltk.word_tokenize(text)
        word_freq = Counter(words)

        for word, count in word_freq.items():
            if count > 5:  # Adjust this threshold as needed
                synonyms = wordnet.synsets(word)
                if synonyms:
                    synonym = synonyms[0].lemmas()[0].name()
                    text = text.replace(word, synonym)

        return text

    def assess_readability(self, text):
        readability_score = flesch_reading_ease(text)
        return readability_score

    def review_blog(self):
        # Adjust connectors
        doc = self.nlp(self.text)
        sentences = [sent.text for sent in doc.sents]
        final_sentences = self.adjust_connectors(sentences)
        final_text = ' '.join(final_sentences)

        # Adjust word usage patterns
        final_text = self.adjust_word_usage(final_text)

        # Assess readability
        readability_score = self.assess_readability(final_text)
        print(f"Readability score: {readability_score}")

        return final_text
