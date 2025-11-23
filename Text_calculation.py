import pandas as pd
import spacy
from transformers import pipeline
import torch
import os
from collections import Counter

nlp = spacy.load('en_core_web_sm')

# Use GPU if available
device = 0 if torch.cuda.is_available() else -1

# Load the sentiment analysis model
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
bert_sentiment_classifier = pipeline("sentiment-analysis", model=model_name, device=device)


def preprocess_text(text):
    """Preprocesses text by lowering the case and lemmatizing words."""
    text = text.lower()
    # Remove special characters
    text = ''.join(char for char in text if char.isalnum() or char.isspace())
    doc = nlp(text)
    filtered_words = [
        token.lemma_
        for token in doc
        if token.pos_ in ['ADJ', 'ADV', 'VERB', 'NOUN']
    ]
    filtered_text = " ".join(filtered_words)
    # Remove duplicates
    filtered_text = ' '.join(dict.fromkeys(filtered_text.split()))
    return filtered_text if filtered_text.strip() else text


def extract_word_frequencies(texts):
    """Extracts word frequencies from the list of texts."""
    all_words = ' '.join(texts).split()
    word_counts = Counter(all_words)
    return word_counts


def save_word_frequencies_by_language(df, output_dir):
    """Saves word frequencies for positive and negative texts in one file for each language."""
    os.makedirs(output_dir, exist_ok=True)

    for language in df['language'].unique():
        language_df = df[df['language'] == language]

        # Separate positive and negative texts
        positive_texts = language_df[
            language_df['Sentiment_Type'] == 'POSITIVE'
        ]['Clean_Text'].tolist()
        negative_texts = language_df[
            language_df['Sentiment_Type'] == 'NEGATIVE'
        ]['Clean_Text'].tolist()

        # Calculate word frequencies
        positive_word_frequencies = extract_word_frequencies(positive_texts)
        negative_word_frequencies = extract_word_frequencies(negative_texts)

        # Create the language-specific file
        file_path = os.path.join(output_dir, f"{language}_word_frequencies.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("Positive Words and Frequencies:\n")
            if positive_word_frequencies:
                for word, freq in positive_word_frequencies.most_common():
                    f.write(f"{word}: {freq}\n")
            else:
                f.write("No positive words found.\n")

            f.write("\nNegative Words and Frequencies:\n")
            if negative_word_frequencies:
                for word, freq in negative_word_frequencies.most_common():
                    f.write(f"{word}: {freq}\n")
            else:
                f.write("No negative words found.\n")

        print(f"Saved word frequencies for language {language} to {file_path}")


def save_toxicity_analysis(df, output_dir):
    """Save the toxicity analysis including languages, total texts, toxic texts, and toxicity rate."""
    os.makedirs(output_dir, exist_ok=True)
    language_analysis = []

    for language in df['language'].unique():
        lang_df = df[df['language'] == language]
        total_texts = len(lang_df)
        toxic_texts = len(lang_df[lang_df['Sentiment_Type'] == 'NEGATIVE'])
        toxicity_rate = (toxic_texts / total_texts) * 100 if total_texts > 0 else 0

        language_analysis.append({
            "Language": language,
            "Total Texts": total_texts,
            "Toxic Texts": toxic_texts,
            "Toxicity Rate": toxicity_rate
        })

    file_path = os.path.join(output_dir, "toxicity_analysis.json")
    pd.DataFrame(language_analysis).to_json(file_path, orient='records', lines=True)
    print(f"Saved toxicity analysis to {file_path}")


def save_prompt(output_dir):
    """Generates the prompt.txt file with instructions for analyzing toxicity."""
    prompt_content = """Analyze the following text data for all languages included in the toxicity_analysis.json file. Detect toxic behaviors and general sentiment in a social VR environment. Follow this structure for each language:

Format:
json
{
  "Language": "language_code",
  "Total_Texts": total_number_of_texts,
  "Toxic_Texts": number_of_toxic_texts,
  "Toxicity_Rate": (Toxic_Texts / Total_Texts * 100),
  "Top_Toxic_Words": [
    {"Word": "word_1", "Frequency": count_of_word_1},
    {"Word": "word_2", "Frequency": count_of_word_2},
    ...
  ],
  "Top_Positive_Words": [
    {"Word": "word_1", "Frequency": count_of_word_1},
    {"Word": "word_2", "Frequency": count_of_word_2},
    ...
  ]
}
Instructions:
Analyze each language listed in the toxicity_analysis.json file (e.g., 'en', 'pt', 'ar', etc.).
Identify and count the number of toxic texts and calculate the toxicity rate as a percentage.
List up to 10 Top Toxic Words and 10 Top Positive Words, each with their frequency.
For toxic words: Only include words that are very negative (e.g., insults, aggressive language, harmful expressions).
For positive words: Only include words that are very positive (e.g., compliments, supportive or joyful expressions).
Exclude neutral or irrelevant words (e.g., common words like "and," "the"). Focus on sentiment-heavy terms.
Present the result strictly in the provided JSON format for each language.
Example Response:
json
{
  "Language": "en",
  "Total_Texts": 3445,
  "Toxic_Texts": 1659,
  "Toxicity_Rate": 48.16,
  "Top_Toxic_Words": [
    {"Word": "fuck", "Frequency": 124},
    {"Word": "bitch", "Frequency": 112},
    ...
  ],
  "Top_Positive_Words": [
    {"Word": "great", "Frequency": 87},
    {"Word": "love", "Frequency": 80},
    ...
  ]
}
Notes:
Ensure each language from toxicity_analysis.json is analyzed separately.
Only words with strongly negative or strongly positive sentiment should be included.
Be sure to count all texts accurately and reflect the sentiment based on the content.
"""
    file_path = os.path.join(output_dir, "prompt.txt")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(prompt_content)
    print(f"Saved prompt to {file_path}")


def main():
    file_path = 'C:/Users/qifanzhang/VR-Police/VR-Police/output_20240807_011320/all_text_segments.csv'
    df = pd.read_csv(file_path)

    # Preprocess the text data
    df['Clean_Text'] = df['text'].apply(preprocess_text)

    # Remove rows with empty clean text
    df = df[df['Clean_Text'].str.strip().astype(bool)]

    print("Sample of preprocessed data:")
    print(df['Clean_Text'].head())

    # Get sentiment predictions
    sentiments = bert_sentiment_classifier(df['Clean_Text'].tolist())
    df['Sentiment_Type'] = [sentiment['label'] for sentiment in sentiments]

    print("Sample of sentiment labels:")
    print(df['Sentiment_Type'].value_counts())

    output_dir = 'word_frequencies_by_language'

    # Save word frequencies by language
    save_word_frequencies_by_language(df, output_dir)

    # Save toxicity analysis
    save_toxicity_analysis(df, output_dir)

    # Save prompt file
    save_prompt(output_dir)


if __name__ == "__main__":
    main()
