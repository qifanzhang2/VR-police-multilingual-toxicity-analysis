import json
import re
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

# Function to clean and extract JSON part from mixed content
def clean_and_fix_json(response_text):
    # Remove non-ASCII characters
    response_text = re.sub(r'[^\x00-\x7F]+', '', response_text)
    # Collapse multiple spaces/newlines into a single space
    response_text = re.sub(r'\s+', ' ', response_text)
    # Add commas between adjacent JSON objects/arrays if missing
    response_text = re.sub(r'([}\]])\s*([{\[]])', r'\1,\2', response_text)
    # Wrap cleaned content in an array
    wrapped_json = f'[{response_text}]'
    return wrapped_json

# Function to parse JSON from the cleaned and extracted string
def parse_json(json_str):
    try:
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None

# Visualization function for relative frequency
def visualize_relative_frequency(data, top_n=5):
    languages = []
    relative_word_counts = defaultdict(list)

    for entry in data:
        language = entry["Language"]
        languages.append(language)

        total_toxic_words = sum(word["Frequency"] for word in entry["Top_Toxic_Words"])
        print(f"Total toxic words for {language}: {total_toxic_words}")

        word_frequencies = sorted(
            entry["Top_Toxic_Words"],
            key=lambda x: -x["Frequency"]
        )[:top_n]

        for word_entry in word_frequencies:
            word = word_entry["Word"]
            frequency = word_entry["Frequency"]
            if total_toxic_words > 0:
                relative_frequency = (frequency / total_toxic_words) * 100
            else:
                relative_frequency = 0
            print(f"Relative frequency of '{word}' in {language}: {relative_frequency}%")
            relative_word_counts[(language, word)].append(relative_frequency)

    print("\nFinal relative frequencies by language (before plotting):")
    for (language, word), frequencies in relative_word_counts.items():
        print(f"Language: {language}, Word: {word}, Frequencies: {frequencies}")

    # Unique list of languages
    languages = list(set(lang for lang, _ in relative_word_counts.keys()))

    # Create the color palette based on the number of unique words
    num_colors = len(relative_word_counts)
    color_palette = plt.get_cmap('tab20', num_colors)  # Use 'tab20' to get distinct colors

    fig, ax = plt.subplots(figsize=(16, 10))

    bar_width = 0.4   # Bar thickness
    language_gap = 3  # Gap between language groups
    word_gap = 0.6    # Gap between words within the same language
    language_positions = np.arange(len(languages)) * language_gap * (top_n + 1)

    # Store the positions for the Y-ticks to correctly label languages
    language_tick_positions = []

    # Loop through words and plot each word as a horizontal bar
    for language_index, language in enumerate(languages):
        words_in_language = [
            (lang, word)
            for (lang, word) in relative_word_counts
            if lang == language
        ]

        bar_positions = (
            np.arange(len(words_in_language)) * (bar_width + word_gap)
            + language_positions[language_index]
        )

        # Central position for this language group
        central_position = np.mean(bar_positions)
        language_tick_positions.append(central_position)

        for idx, (lang, word) in enumerate(words_in_language):
            frequencies = relative_word_counts[(lang, word)]
            # Usually one value; if multiple, sum them
            value = sum(frequencies)

            ax.barh(
                bar_positions[idx],
                value,
                height=bar_width,
                label=word,
                color=color_palette(idx)
            )

            # Add data labels for visibility
            if value > 0:
                ax.text(
                    value + 1,
                    bar_positions[idx],
                    f'{word} ({value:.1f}%)',
                    va='center',
                    fontsize=10,
                    color='black'
                )

    # Set labels and title
    ax.set_xlabel('Relative Frequency (%) of Toxic Words', fontsize=14)
    ax.set_ylabel('Languages', fontsize=14)
    ax.set_title(f'Top {top_n} Toxic Words by Language (Relative Frequency)', fontsize=18)

    # Set ticks and labels for languages
    ax.set_yticks(language_tick_positions)
    ax.set_yticklabels(languages, fontsize=12)

    # Add grid for clarity
    ax.grid(True, which='both', axis='x', linestyle='--', alpha=0.6)

    # Optimize layout
    plt.tight_layout()
    plt.show()

def main():
    print("Please input the response including structured JSON data. Type 'END' when done:")

    input_lines = []
    while True:
        line = input()
        if line.strip().lower() == 'end':
            break
        input_lines.append(line)

    full_input_text = "\n".join(input_lines)

    cleaned_json_str = clean_and_fix_json(full_input_text)
    json_data = parse_json(cleaned_json_str)

    if json_data:
        visualize_relative_frequency(json_data, top_n=5)
    else:
        print("Unable to parse the JSON.")

if __name__ == "__main__":
    main()
