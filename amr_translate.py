import argparse
import pandas as pd
import deepl
import os


def translate_sentences_incremental(input_file_path: str, m: int, n: int, deepl_key: str,
                                    output_file_path: str) -> None:
    """
    Translates sentences from the specified rows of the DataFrame from English to Hungarian,
    saves the translations incrementally to a CSV file, and does not return any value.
    """
    # Load data from CSV
    df = pd.read_csv(input_file_path)

    # Initialize the DeepL translator with the authentication key
    translator = deepl.Translator(deepl_key)

    # Determine if the header should be written (only if the file does not exist or is empty)
    write_header = not os.path.exists(output_file_path) or os.stat(output_file_path).st_size == 0

    # Translate each sentence in the specified range and write to CSV incrementally
    for index in range(m, n):
        sentence = df.at[index, 'sentence']
        # Translate the sentence to Hungarian
        result = translator.translate_text(sentence, target_lang="HU")

        # Print the translated text
        print(result.text)

        # Create a temporary DataFrame for this translation
        temp_df = pd.DataFrame({'id': [df.at[index, 'id']], 'sentence': [sentence], 'hu_sentence': [result.text]})

        # Append to CSV, write headers only if it's the first write
        temp_df.to_csv(output_file_path, mode='a', header=write_header, index=False)

        # Ensure headers are not written again
        write_header = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate sentences from English to Hungarian using DeepL API.")
    parser.add_argument("input_file_path", type=str,
                        help="Path to the input CSV file containing sentences to translate.")
    parser.add_argument("m", type=int, help="Starting index (inclusive).")
    parser.add_argument("n", type=int, help="Ending index (exclusive).")
    parser.add_argument("deepl_key", type=str, help="DeepL API key.")
    parser.add_argument("--output_file_path", type=str, default="translated.csv",
                        help="Path to save the translated output CSV. Default is the current directory.")

    args = parser.parse_args()

    # Set the output file path to include the working directory if not specified
    if os.path.dirname(args.output_file_path) == '':
        args.output_file_path = os.path.join(os.getcwd(), args.output_file_path)

    translate_sentences_incremental(args.input_file_path, args.m, args.n, args.deepl_key, args.output_file_path)
