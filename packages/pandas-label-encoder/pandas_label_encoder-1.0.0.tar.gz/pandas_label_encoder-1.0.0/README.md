# Pandas-powered LabelEncoder

## Performance benchmark
From the test, compare to sklearn's LabelEncoder.
```
Total rows: 24,123,464
Scikit-learn's LabelEncoder - 13.35 seconds
Pandas-powered LabelEncoder - 2.44 seconds
```

## Usage

### Initiation and fitting
```python
import pandas_label_encoder as ec
from pandas_label_encoder import EncoderCategoryError

categories = ['Cat', 'Dog', 'Bird']  # can be pd.Series, np.array, list

# Fit at inititation
animal_encoder = ec.Encoder(categories)

# Fit later
animal_encoder = ec.Encoder()
animal_encoder.fit(categories)

animal_encoder.categories # ['Cat', 'Dog', 'Bird'], read-only

# Trying to use functions before assign appropiate categories will raise EncoderCategoryError
ec.Encoder().transform() # Raise EncoderCategoryError
ec.Encoder().inverse_transform() # Raise EncoderCategoryError
```

### Transform
- Unknown categories would be parsed as -1
- If you want to raise an error, there are 2 validation options.
  - validation=`all` -- Raise EncoderError if any result is -1
  - validation=`any` -- Raise EncoderError if all of them are -1
```python
from pandas_label_encoder import EncoderValidationError

animal_encoder.transform(['Cat']) # [2]
animal_encoder.transform(['Fish']) # [-1]

animal_encoder.transform(['Fish'], validation='all') # Raise EncoderValidationError
animal_encoder.transform(['Fish'], validation='any') # Raise EncoderValidationError

try:
  animal_encoder.transform(['Fish', 'Cat'], validation='all') # Raise EncoderValidationError
except EncoderError:
  print('There is an unknown animal.')

animal_encoder.transform(['Fish', 'Cat'], validation='any') # [-1, 2]
```

### Inverse transform
- Unknown categories would be parsed as NaN
- If you want to raise an error, there are 2 validation options.
  - validation=`all` -- Raise EncoderError if any result is NaN
  - validation=`any` -- Raise EncoderError if all of them are NaN
```python
from pandas_label_encoder import EncoderValidationError

animal_encoder.inverse_transform([2]) # ['Cat']
animal_encoder.inverse_transform([9]) # [NaN]

animal_encoder.inverse_transform([9], validation='all') # Raise EncoderValidationError
animal_encoder.inverse_transform([9], validation='any') # Raise EncoderValidationError

try:
  animal_encoder.inverse_transform([9, 2], validation='all') # Raise EncoderValidationError
except EncoderError:
  print('There is an unknown animal.')

animal_encoder.inverse_transform([9, 2], validation='any') # [NaN, 'Cat']
```

### Save and load the encoder
The load_encoder and encoder.Encoder.load methods will load the encoder and check for the encoder version.

Different encoder version may have some changes that cause errors.

To check current encoder version, use `encoder.Encoder.__version__`.
```python
from pandas_label_encoder import save_encoder, load_encoder

# Save or load other encoder directly from the encoder itself
animal_encoder.save(path) # save current encoder
animal_encoder.load(path) # load other encoder and assign to current encoder

# Save or load other encoder by using functions
animal_encoder = load_encoder(path)
save_encoder(path)
```
