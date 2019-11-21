from setuptools import setup, find_packages
from glob import glob
from os.path import basename
from os.path import splitext
setup(
    name='spacy_spanish_lemmatizer',
    packages=find_packages('spacy_spanish_lemmatizer'),
    package_dir={'': 'spacy_spanish_lemmatizer'},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0]
                for path in glob('spacy_spanish_lemmatizer/*.py')],
    version='0.2',
    license='MIT',
    description='Spanish rule-based lemmatization for spaCy',
    author='Pablo David Muñoz Sánchez',
    author_email='pablodavid.munoz@gmail.com',
    url='https://github.com/pablodms/spacy-spanish-lemmatizer',
    download_url='https://github.com/pablodms/spacy-spanish-lemmatizer/archive/v_0.2.tar.gz',
    keywords=['Lemmatization', 'spaCy', 'Spanish'],
    install_requires=['spacy>=2.0'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

)
