import os
import pickle
import pandas as pd
import pprint
from datetime import datetime


def print_summary(content, file_path):
    if 'segments' in content:
        for segment in content['segments']:
            start_time = segment.get('start', 'N/A')
            end_time = segment.get('end', 'N/A')
            text = segment.get('text', 'N/A')
            print(
                f"Segment ID: {segment.get('id', 'N/A')} | "
                f"Start Time: {start_time} | End Time: {end_time}"
            )
            print(f"Text: {text}")
            print(f"Voice File Address: {file_path}\n")
    else:
        print("No segments found in the content.")


def save_full_content(output_directory, filename, content):
    output_path = os.path.join(output_directory, f"{filename}_content.txt")
    with open(output_path, 'w', encoding='utf-8') as file:
        formatted_content = pprint.pformat(content)
        file.write(formatted_content)


def save_text_segments_to_csv(output_directory, all_text_segments):
    df = pd.DataFrame(
        all_text_segments,
        columns=['text', 'voice_file_address', 'start_time', 'end_time', 'language']
    )
    output_path = os.path.join(output_directory, 'all_text_segments.csv')
    df.to_csv(output_path, index=False)


def print_all_pickle_files_content(input_directory):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_directory = os.path.join(os.getcwd(), f'output_{timestamp}')
    os.makedirs(output_directory, exist_ok=True)

    all_text_segments = []

    try:
        for filename in os.listdir(input_directory):
            file_path = os.path.join(input_directory, filename)

            if os.path.isfile(file_path) and filename.endswith('.pkl'):
                with open(file_path, 'rb') as file:
                    content = pickle.load(file)
                    print(f"Summary of {filename}:")
                    print_summary(content, file_path)
                    save_full_content(output_directory, filename, content)

                    if 'segments' in content:
                        for segment in content['segments']:
                            text_segment = {
                                'text': segment.get('text', 'N/A'),
                                'voice_file_address': file_path,
                                'start_time': segment.get('start', 'N/A'),
                                'end_time': segment.get('end', 'N/A'),
                                'language': content.get('language', 'N/A')
                            }
                            all_text_segments.append(text_segment)

                    print(
                        f"Full content of {filename} saved to
                        {output_directory}/{filename}_content.txt"
                    )
                    print("\n" + "=" * 40 + "\n")

        save_text_segments_to_csv(output_directory, all_text_segments)
        print(
            f"All text segments saved to {output_directory}/all_text_segments.csv"
        )

    except Exception as e:
        print(f"An error occurred: {e}")


input_directory_path = (
    'C:/Users/qifanzhang/VR-Police/VR-Police/data/'
    'capture_20240621_015237/voice'
)
print_all_pickle_files_content(input_directory_path)
