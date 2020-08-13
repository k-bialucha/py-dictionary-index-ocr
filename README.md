# Dictionary index with OCR

[Wersja PL](./README_PL.md).

## Installation

Requirements:

- Python >=3.7
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

Create ([instruction](https://www.tutorialspoint.com/python-virtual-environment)) and activate Python's virtualenv:

```sh
# Linux
source ./env/bin/activate
# Windows
env\Scripts\Activate.ps1
```

Install dependencies:

```sh
pip install -r requirements.txt
```

## Scripts

Before processing make sure to place input files in the `input` directory.

Run the main script (processing):

```sh
python main.py p0089 p0138 -cn my_config_name
```

Run the evaluation script:

```sh
python evaluation.py p0089 p0138 -cn my_config_name
```

For available script parameters type:

```sh
python main.py --help
python evaluation.py --help
```
