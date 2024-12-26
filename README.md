# Text Processing for PageRank and TrustRank Calculation

[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This Python project is designed for **text processing**, focusing on the computation of PageRank and TrustRank scores from a dataset in JSON format using graph-based techniques. 

**Applications**: Suitable for applications such as text summarization, term importance analysis, and content ranking.

## Table of Contents

- [Quick Start](#quick-start)
- [Requirements and Dependencies](#requirements-and-dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Dataset Structure](#dataset-structure)
- [Usage](#usage)
- [Output](#output)
- [Workflow Overview](#workflow-overview)
- [Project Directory Structure](#project-directory-structure)
- [License](#license)
- [Contributors](#contributors)

## Quick Start

1. Ensure that Python (version 3.6 or later) and pip are installed on your system.

2. Clone the repository and navigate to the directory:
```bash
git clone https://github.com/RJTPP/TextGraphRank.git &&
cd TextGraphRank
```

3. Run the setup script. This will create a virtual environment and install the required dependencies.
```bash
python3 setup.py
```

4. Activate the virtual environment.
 - For Linux/macOS
```bash
source venv/bin/activate
```
- For Windows
```bash
venv\Scripts\activate
```

5. Configure the project by editing `config.json`
   - Set paths for datasets and outputs.
   - Define algorithm parameters and workflow options.
   - For more details, see [Configuration](#configuration) section.

6. Add your dataset to the `dataset/` directory. 
   - Ensure the dataset is in JSON format and contains the structure specified in the [Dataset Structure](#dataset-structure) section.

7. Run the main script. Optional arguments can be provided (optional). See [Options](#options) section for details.
```bash
python3 main.py [OPTIONS]
```

1. View the results in the `output/` directory. See [Output](#output) section for an example.


> [!NOTE]
> For further details, please refer to the [Installation](#installation) and [Usage](#usage) sections.

## Requirements and Dependencies

This project was developed using Python 3.6 and is tested to be compatible with Python 3.6 through 3.12 and should work with newer versions. It requires the following dependencies:
- `networkx`
- `matplotlib`
- `scipy`
- `regex`
- `tqdm`
- `nltk`
- `pathlib`
- `numpy`
- `orjson`

> [!NOTE]
> For a complete list of dependencies, see [`requirements.txt`](requirements.txt)

## Installation

1. Clone the repository.
```bash
git clone https://github.com/RJTPP/TextGraphRank.git &&
cd TextGraphRank
```

2. Run `setup.py`,This will create a virtual environment and install the required dependencies.
```bash
python3 setup.py
```


### Manual Installation (Optional)  
If you prefer to install the dependencies manually, follow these steps:

1. Create a virtual environment.
```bash
python3 -m venv venv
```

2. Activate the virtual environment.
 - For Linux/macOS
```bash
source venv/bin/activate
```
- For Windows
```bash
venv\Scripts\activate
```

3. Upgrade `pip`.
```bash
pip install --upgrade pip
```

4. Install the required dependencies.
```bash
pip install -r requirements.txt
```

## Configuration
The project can be configured through `config.json`, which contains:

### Path Configuration
  - `cached_dir`: Directory for storing cache data.
  - `dataset_dir`: Directory containing input JSON datasets.
  - `output_dir`: Directory where processed results and outputs will be stored.

### Algorithm Parameters
  - `calculation_threshold`: Convergence threshold for iterative calculations like PageRank and TrustRank.
  - `max_calculation_iteration`: Maximum number of iterations for the scoring algorithms.
  - `trustrank_bias_amount`: Number of nodes or elements to bias in TrustRank, chosen from most scored from inverse PageRank. 
  - `max_summarize_length`:  Maximum number of iterations for TrustRank algorithm. This will also be the maximum number of nodes or elements to summarize.

### Workflow Options
  - `use_pagerank_library`: Set to true to use a library-based PageRank implementation (`networkx`) or  false for the custom implementation.
  - `output_graph`: If true, saves the generated graphs as files in the output directory.
  - `show_graph`: If true, displays graphs during execution (requires a GUI).

### Target Data Keys
  - `target_data_key`: Specifies which keys from the JSON dataset to process. See [**Dataset Structure**](#dataset-structure) for details.


### Example Configuration
```json
{
    "path": {
        "cached_dir"  : "caches",
        "dataset_dir" : "dataset",
        "output_dir"  : "output"
    },
    "parameters": {
        "calculation_threshold"     : 1e-5,
        "max_calculation_iteration" : 200,
        "trustrank_bias_amount"     : 1,
        "max_summarize_length"      : 20
    },
    "options": {
        "use_pagerank_library" : false,
        "output_graph"         : true,
        "show_graph"           : false
    },
    "target_data_key": [
        "target_key",
        "nested_target_key"
    ]
}
```

> [!TIP]
> To print the currently configured paths in `config.json`, you can run the `verify_path.py` script.

## Dataset Structure

Input datasets must be JSON files structured as **an array of dictionaries or an array of strings** to ensure compatibility with the workflow. Below is an example of the expected dataset format:

### Example 1: Array of Dictionaries
```json
[
    {
        "id"  : "001",
        "data": {
            "full_text" : "This is a sample text.",
            "author"    : "author_name",
            "date"      : "2024-01-01"
        }
    },
    {
        "id"  : "002",
        "data": {
            "full_text" : "This is another sample text.",
            "author"    : "another_author_name",
            "date"      : "2024-01-02"
        }
    }
]
```

- In this example, the `data.full_text` field contains the text to be processed.
- target_data_key : `["data", "full_text"]`

### Example 2: Array of Strings
```json
[
    "This is a sample text.",
    "This is another sample text."
]
```
- target_data_key: Leave as an empty array `[ ]`.

## Usage

To execute the project, follow these steps:

### 1.	Add Dataset:
- Ensure your dataset files are in the directory specified by the `dataset_dir` field in `config.json`. The default directory is `dataset/`.

### 2. Activate the virtual environment:

 - For Linux/macOS
```bash
source venv/bin/activate
```
- For Windows
```bash
venv\Scripts\activate
```

### 3.	Run the Main Script:

```bash
python3 main.py [OPTIONS]
```

### Options:

- `-f`, `--files`: Specify one or more JSON files to process.

```bash
python3 main.py -f file1.json file2.json
```


- `-e`, `--exclude`: Exclude one or more JSON files from processing.

```bash
python3 main.py -e file1.json
```
> [!NOTE]
> If no options are provided, the script processes all JSON files in the dataset directory by default.

## Output

The project generates the following output files in the `output/` directory or configured output directory.

- `graph_{name}.json`: Represents the generated bigram graph. Each bigram consists of two consecutive words and its associated weight (frequency in the text).

Example:
```json
[
  [
    "word1 word2",
    "word2 word3",
    2 
  ],
]
```

- `inverse_pagerank_{name}.json` and `trust_rank_{name}.json` Contain ranking scores for terms or nodes.

Example:
```json
[
  ["word1 word2", 0.7],
  ["word2 word3", 0.3]
]
```

> [!NOTE]
> Higher scores indicate greater importance or relevance in the dataset.


## Workflow Overview

This project processes textual data in four stages:

### 1. Text Preprocessing

The text preprocessing module applies several cleaning techniques:
  - Converts text to lowercase
  - Expands contractions and replaces slang
  - Removes non-alphabetic characters, punctuation, and URLs
  - Removes stopwords

### 2. Bigram Graph Generation
  - Converts processed text into bigrams
  - Generates weighted bigrams and graphs (library-based or custom implementation depending on the configuration)
  - Optionally visualizes graphs using matplotlib

### 3. Score Calculation
  - Calculates PageRank using either library-based or customized algorithm depending on configuration
  - Calculates TrustRank using customized algorithm based on seeded bias.

### 4. Results Output

  - Processed results are saved to the output directory as defined in the configuration file.
  - Following calculations will be saved:
    - Bigram Graph
    - Inverse PageRank
    - TrustRank

## Project Directory Structure

```
work/
├── caches/
│   └── ... (Cache files)
│   
├── dataset/
│   └── ... (Put your dataset here)
│
├── helper_script/              # Utility scripts
│   ├── __init__.py
│   └── file_reader_helper.py   # File related helper functions
│   ├── json_helper.py          # JSON helper functions
│   ├── func_timer.py           # Timer for monitoring function runtime
│
├── modules_script/             # Core processing modules
│   ├── __init__.py  
│   ├── m_graph_custom.py       # Graph generation for calculating inverse pagerank (custom implementation)
│   ├── m_graph_nx.py           # Graph generation from bigrams (networkx library)
│   └── m_preprocess_text.py    # Text preprocessing logic
│   └── m_process_text.py       # Text to bigrams logic
│
├── config.json                 # Configuration
├── main.py                     # Main script
├── requirements.txt      
├── settings.py                 # Handle settings from config.json 
├── setup.py                    # Setup script
├── verify_path.py              # Verify path settings
└── venv                        # Virtual environment
```

## License

This project is released under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software under the terms of the MIT License. See the LICENSE file for detailed terms and conditions.

## Contributors

Rajata Thamcharoensatit ([@RJTPP](https://github.com/RJTPP))
