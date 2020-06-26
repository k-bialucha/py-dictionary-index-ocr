# Indeksowanie Słownika OCR

[EN version](./README.md).

## Instalacja

Wymagania:

- Python >=3.7
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)

Należy utworzyć ([instrukcja](https://www.tutorialspoint.com/python-virtual-environment)) oraz aktywować wirtualne środowisko Pythona:

```sh
# Linux
source ./env/bin/activate
# Windows
env\Scripts\Activate.ps1
```

Instalacja zależności:

```sh
pip install -r requirements.txt
```

## Skrypty

Przed przetwarzaniem należy umieścić pliki wejściowe w katalogu `input`.

Główny skrypt (przetwarzanie):

```sh
python main.py p0089 p0138 -cn my_config_name
```

Skrypt ewaluacyjny:

```sh
python evaluation.py p0089 p0138 -cn my_config_name
```

Pomoc dotycząca skryptów:

```sh
python main.py --help
python evaluation.py --help
```
