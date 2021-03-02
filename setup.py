from setuptools import setup

setup(
    name='spacy_spanish_lemmatizer',
    packages=['spacy_spanish_lemmatizer'],
    include_package_data=True,
    version='0.6',
    license='MIT',
    description='Spanish rule-based lemmatization for spaCy',
    author='Pablo David Muñoz Sánchez',
    author_email='pablodavid.munoz@gmail.com',
    url='https://github.com/pablodms/spacy-spanish-lemmatizer',
    download_url='https://github.com/pablodms/spacy-spanish-lemmatizer/archive/v_0.4.tar.gz',
    keywords=['Lemmatization', 'spaCy', 'Spanish'],
    install_requires=['spacy>=3.0'],
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
