# Dictionary index with OCR

[Wersja PL](./README_PL.md).

## Installation

Activate env:

```sh
source ./env/bin/activate
```

Install dependencies:

```sh
pip install requirements.txt
```

## Scripts

Before processing make sure to place input files in the `input` directory.

Run the main script (processing):

```sh
python main.py p0089 p0110 -cn my_config_name
```

Run the evaluation script:

```sh
python evaluation.py p0089 p0110 -cn my_config_name
```

For available script parameters type:

```sh
python main.py --help
python evaluation.py --help
```
