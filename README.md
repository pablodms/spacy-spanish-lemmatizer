# spacy-spanish-lemmatizer
Spanish rule-based lemmatization for spaCy

## Steps to use lemmatizer
* Ensure you have installed spaCy following the instructions given at https://spacy.io/usage.
* Ensure you have installed spaCy Spanish model following the instructions given at https://spacy.io/usage/models.
* Install package via pip
```pip install spacy_spanish_lemmatizer```
* Generate lemmatization rules (it may take several minutes):
__NOTE__: currently, only lemmatization based on Wiktionary dump files is implemented. Due to licensing restrictions, the following command will download Wiktionary dump files and generate lemmatization rules based on them. By executing it, you are agreeing Wikimedia [License](https://dumps.wikimedia.org/legal.html).
```python -m spacy_spanish_lemmatizer download wiki```

* Use it in Python:
```
import spacy
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer
# Change "es" to the Spanish model installed in step 2
nlp = spacy.load("es")
lemmatizer = SpacyCustomLemmatizer()
nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")
for token in nlp(
    """Con estos fines, la Dirección de Gestión y Control Financiero monitorea
       la posición de capital del Banco y utiliza los mecanismos para hacer un
       eficiente manejo del capital."""
):
    print(token.text, token.lemma_)
```

```
Con con
estos este
fines fin
, ,
la el
Dirección dirección
de de
Gestión gestión
y y
Control control
Financiero financiero
monitorea monitorea

la el
posición posición
de de
capital capital
del del
Banco banco
y y
utiliza utilizar
los el
mecanismos mecanismo
para para
hacer hacer
un un

eficiente eficiente
manejo manejo
del del
capital capital
. .
```
