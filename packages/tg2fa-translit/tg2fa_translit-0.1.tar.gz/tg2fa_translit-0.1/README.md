# tg2fa_translit

A Tajik-to-Persian transliteration model.

## Installation
```pip install tg2fa```

## Dependency
- `numpy`
- `keras`

## API

```py
from tg2fa_translit.conversion import convert

text = 'То ғами фардо нахӯрем'
print(convert('text'))  # can be printed in reverse order; in this case copy-paste the output or write directly to a file
```

## Datasets and Training Details

The model shows a Levenshtein ratio of 0.96.
See the dataset here: https://github.com/stibiumghost/tajik-persian-transliteration

## Acknowledgment

Based on https://github.com/bashartalafha/Arabizi-Transliteration.
