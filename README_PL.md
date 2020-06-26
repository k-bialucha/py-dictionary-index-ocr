# Indeksowanie Słownika OCR

[EN version](./README.md).

## Instalacja

Należy aktywować wirtualne środowisko Pythona:

```sh
source ./env/bin/activate
```

Instalacja zależności:

```sh
pip install requirements.txt
```

## Skrypty

Przed przetwarzaniem należy umieścić pliki wejściowe w katalogu `input`.

Główny skrypt (przetwarzanie):

```sh
python main.py p0089 p0110 -cn my_config_name
```

Skrypt ewaluacyjny:

```sh
python evaluation.py p0089 p0110 -cn my_config_name
```

Pomoc dotycząca skryptów:

```sh
python main.py --help
python evaluation.py --help
```
