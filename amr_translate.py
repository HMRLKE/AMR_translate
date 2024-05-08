import argparse
import pandas as pd
import deepl
import os

def translate_sentences_incremental(input_file_path: str, m: int, n: int, deepl_key: str, output_file_path: str) -> None:
    """
    Translates sentences from the specified rows of the DataFrame from English to Hungarian,
    saves the translations incrementally to a CSV file, and does not return any value.
    """
    try:
        df = pd.read_csv(input_file_path)
    except pd.errors.ParserError as e:
        print(f"Error reading the CSV file: {e}")
        return

    translator = deepl.Translator(deepl_key)
    write_header = not os.path.exists(output_file_path) or os.stat(output_file_path).st_size == 0

    for index in range(m, n):
        sentence = df.at[index, 'sentence']
        result = translator.translate_text(sentence, target_lang="HU")
        print(result.text)
        temp_df = pd.DataFrame({'id': [df.at[index, 'id']], 'sentence': [sentence], 'hu_sentence': [result.text]})
        temp_df.to_csv(output_file_path, mode='a', header=write_header, index=False)
        write_header = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate sentences from English to Hungarian using DeepL API.")
    parser.add_argument("--input_file_path", type=str, required=True, help="Path to the input CSV file containing sentences to translate.")
    parser.add_argument("--m", type=int, required=True, help="Starting index (inclusive).")
    parser.add_argument("--n", type=int, required=True, help="Ending index (exclusive).")
    parser.add_argument("--deepl_key", type=str, required=True, help="DeepL API key.")
    parser.add_argument("--output_file_path", type=str, default="translated.csv", help="Path to save the translated output CSV. Default is the current directory.")

    args = parser.parse_args()

    translate_sentences_incremental(args.input_file_path, args.m, args.n, args.deepl_key, args.output_file_path)
