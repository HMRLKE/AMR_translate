import argparse
import pandas as pd
import deepl
import os

def parse_amr_data(file_path: str):
    """
    Parses a text file where every odd line is an identifier and every even line is the corresponding sentence.
    Returns a DataFrame with columns 'id' and 'sentence'.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    i = 0
    while i < len(lines):
        if i + 1 < len(lines):
            current_id = lines[i].strip()
            current_sentence = lines[i + 1].strip()
            data.append({'id': current_id, 'sentence': current_sentence})
        i += 2

    return pd.DataFrame(data)

def translate_sentences_incremental(df: pd.DataFrame, m: int, n: int, deepl_key: str, output_file_path: str) -> None:
    """
    Translates sentences from the specified rows of the DataFrame from English to Hungarian,
    saves the translations incrementally to a CSV file, and prints them.
    """
    translator = deepl.Translator(deepl_key)
    write_header = not os.path.exists(output_file_path) or os.stat(output_file_path).st_size == 0

    for index in range(m, n):
        if index >= len(df):
            break
        sentence = df.at[index, 'sentence']
        result = translator.translate_text(sentence, target_lang="HU")
        print(f"{df.at[index, 'id']}: {result.text}")

        temp_df = pd.DataFrame({
            'id': [df.at[index, 'id']],
            'sentence': [sentence],
            'hu_sentence': [result.text]
        })
        temp_df.to_csv(output_file_path, mode='a', header=write_header, index=False)
        write_header = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate sentences from English to Hungarian using DeepL API.")
    parser.add_argument("--input_file_path", type=str, required=True, help="Path to the input TXT file containing sentences to translate.")
    parser.add_argument("--m", type=int, required=True, help="Starting index (inclusive).")
    parser.add_argument("--n", type=int, required=True, help="Ending index (exclusive).")
    parser.add_argument("--deepl_key", type=str, required=True, help="DeepL API key.")
    parser.add_argument("--output_file_path", type=str, default="translated.csv", help="Path to save the translated output CSV. Default is the current directory.")

    args = parser.parse_args()

    # Parse the data from the specified text file
    df = parse_amr_data(args.input_file_path)
    # Translate the specified range of sentences
    translate_sentences_incremental(df, args.m, args.n, args.deepl_key, args.output_file_path)
