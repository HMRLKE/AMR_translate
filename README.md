# Sentence Translator

This script allows you to translate sentences from English to Hungarian using the DeepL API. It reads sentences from a specified CSV file, translates them incrementally, and saves the output to another CSV file.

## Installation

To run this script, you need Python installed on your system along with some additional packages. Follow these steps:

1. Clone or download this repository to your local machine.
2. Ensure you have Anaconda or Miniconda installed, or install it from [here](https://www.anaconda.com/products/individual).

### Create a Conda Environment

Create a Conda environment with Python 3.10 and install the required packages using the following commands:

```bash
conda create --name myenv python=3.10
conda activate myenv
pip install -r requirements.txt


## Requirements

This script requires the following Python packages:

- `pandas`: For handling data in DataFrame format.
- `deepl`: For accessing the DeepL translation API.

Install the necessary packages using the following command:

```
pip install -r requirements.txt
```

## Usage

The script can be run from the command line with the following arguments:

- `input_file_path`: The path to the CSV file containing the sentences to be translated.
- `m`: The starting index of the rows to be translated (inclusive).
- `n`: The ending index of the rows to be translated (exclusive).
- `deepl_key`: Your DeepL API key.
- `--output_file_path` (optional): The path to save the translated output CSV. Defaults to `translated.csv` in the current directory.

### Example Command
```
python sentence_translator.py "path/to/your/input.csv" 0 10 "your_deepl_api_key" --output_file_path "path/to/your/output.csv"
```


This command will translate rows 0 to 9 from the input CSV file using the provided DeepL API key and save the results to the specified output CSV file.

## Output

The output CSV file will contain the following columns:

- `id`: The ID of the sentence.
- `sentence`: The original English sentence.
- `hu_sentence`: The translated Hungarian sentence.

The script will also print the translated sentences to the console as they are processed.

## Notes

- Ensure that your CSV file has a column named `sentence` containing the English sentences.
- The script handles indexing based on pandas DataFrame indexing, so ensure the indices provided are within the range of the DataFrame.
