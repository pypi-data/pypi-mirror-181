# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_label_encoder']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.23.2', 'pandas==1.5.2']

setup_kwargs = {
    'name': 'pandas-label-encoder',
    'version': '0.0.1',
    'description': '',
    'long_description': "# Pandas-powered LabelEncoder\n\n## Performance benchmark\nFrom the test, compare to sklearn's LabelEncoder.\n```\nTotal rows: 24,123,464\nScikit-learn's LabelEncoder - 13.35 seconds\nPandas-powered LabelEncoder - 2.44 seconds\n```\n\n## Usage\n\n### Initiation and fitting\n```python\nimport pandas_label_encoder as ec\nfrom pandas_label_encoder import EncoderCategoryError\n\ncategories = ['Cat', 'Dog', 'Bird']  # can be pd.Series, np.array, list\n\n# Fit at inititation\nanimal_encoder = ec.Encoder(categories)\n\n# Fit later\nanimal_encoder = ec.Encoder()\nanimal_encoder.fit(categories)\n\nanimal_encoder.categories # ['Cat', 'Dog', 'Bird'], read-only\n\n# Trying to use functions before assign appropiate categories will raise EncoderCategoryError\nec.Encoder().transform() # Raise EncoderCategoryError\nec.Encoder().inverse_transform() # Raise EncoderCategoryError\n```\n\n### Transform\n- Unknown categories would be parsed as -1\n- If you want to raise an error, there are 2 validation options.\n  - validation=`all` -- Raise EncoderError if any result is -1\n  - validation=`any` -- Raise EncoderError if all of them are -1\n```python\nfrom pandas_label_encoder import EncoderValidationError\n\nanimal_encoder.transform(['Cat']) # [2]\nanimal_encoder.transform(['Fish']) # [-1]\n\nanimal_encoder.transform(['Fish'], validation='all') # Raise EncoderValidationError\nanimal_encoder.transform(['Fish'], validation='any') # Raise EncoderValidationError\n\ntry:\n  animal_encoder.transform(['Fish', 'Cat'], validation='all') # Raise EncoderValidationError\nexcept EncoderError:\n  print('There is an unknown animal.')\n\nanimal_encoder.transform(['Fish', 'Cat'], validation='any') # [-1, 2]\n```\n\n### Inverse transform\n- Unknown categories would be parsed as NaN\n- If you want to raise an error, there are 2 validation options.\n  - validation=`all` -- Raise EncoderError if any result is NaN\n  - validation=`any` -- Raise EncoderError if all of them are NaN\n```python\nfrom pandas_label_encoder import EncoderValidationError\n\nanimal_encoder.inverse_transform([2]) # ['Cat']\nanimal_encoder.inverse_transform([9]) # [NaN]\n\nanimal_encoder.inverse_transform([9], validation='all') # Raise EncoderValidationError\nanimal_encoder.inverse_transform([9], validation='any') # Raise EncoderValidationError\n\ntry:\n  animal_encoder.inverse_transform([9, 2], validation='all') # Raise EncoderValidationError\nexcept EncoderError:\n  print('There is an unknown animal.')\n\nanimal_encoder.inverse_transform([9, 2], validation='any') # [NaN, 'Cat']\n```\n\n### Save and load the encoder\nThe load_encoder and encoder.Encoder.load methods will load the encoder and check for the encoder version.\n\nDifferent encoder version may have some changes that cause errors.\n\nTo check current encoder version, use `encoder.Encoder.__version__`.\n```python\nfrom pandas_label_encoder import save_encoder, load_encoder\n\n# Save or load other encoder directly from the encoder itself\nanimal_encoder.save(path) # save current encoder\nanimal_encoder.load(path) # load other encoder and assign to current encoder\n\n# Save or load other encoder by using functions\nanimal_encoder = load_encoder(path)\nsave_encoder(path)\n```\n",
    'author': 'NOPDANAI DEJVORAKUL',
    'author_email': 'b.intm@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
