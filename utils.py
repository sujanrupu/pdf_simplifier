import fitz  # PyMuPDF
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

from nltk.corpus import wordnet
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer

def extract_text_from_pdf(pdf_bytes):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def extract_keywords(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    counter = Counter(filtered_words)
    keywords = counter.most_common(10)
    return [keyword for keyword, count in keywords]

def paraphrase_text(text):
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    # Initialize lemmatizer
    lemmatizer = WordNetLemmatizer()

    paraphrased_sentences = []

    # Iterate over each sentence
    for sentence in sentences:
        # Tokenize the sentence
        words = word_tokenize(sentence)

        # Get part-of-speech tags
        pos_tags = pos_tag(words)

        # Initialize an empty list to store paraphrased words
        paraphrased_words = []

        # Iterate over each word and paraphrase it
        for word, pos in pos_tags:
            # Get the word's lemma
            lemma = lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos))
            
            # Find synonyms for the lemma
            synonyms = find_synonyms(lemma)

            # If synonyms are found, choose one randomly
            if synonyms:
                paraphrased_word = synonyms[0]
            else:
                paraphrased_word = word  # If no synonyms are found, keep the original word
            
            paraphrased_words.append(paraphrased_word)

        # Join the paraphrased words to form a paraphrased sentence
        paraphrased_sentence = ' '.join(paraphrased_words)
        paraphrased_sentences.append(paraphrased_sentence)

    # Join the paraphrased sentences to form the paraphrased text
    paraphrased_text = ' '.join(paraphrased_sentences)
    
    return paraphrased_text

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun if the part-of-speech tag is not recognized

def find_synonyms(word):
    synonyms = []
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
    return synonyms
