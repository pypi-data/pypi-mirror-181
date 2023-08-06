import setuptools
from setuptools import find_namespace_packages

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ChelsiAI",
    version="2.9",
    author="Yash Kumar Vaibhav & Team",
    author_email="chelsiai2022@gmail.com",
    description="ChelsiAI is python library to build your own AI virtual assistant with natural language processing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://yashkumarvaibhav.github.io/mysite",
    include_package_data=True,
    packages=find_namespace_packages(include=['ChelsiAI.*', 'ChelsiAI']),
    install_requires=['numpy', 'gtts', 'playsound', 'pyscreenshot', "opencv-python",
                      'SpeechRecognition', 'pipwin', 'lxml', 'pyjokes',
                      'beautifulsoup4', 'wikipedia', 'scipy', 'download',
                      "torch", 'lazyme', "requests", "pyttsx3", "googlesearch-python",
                      "spacy", 'textdistance', 'pywhatkit', "googlesearch-python",
                      "youtube-search-python", "shutup", 'Flask', 'speedtest-cli',
                      'pytube', 'pycountry', 'phonetics', 'fuzzywuzzy', 'googletrans', 'wave',
                      'deepspeech', 'halo', 'playsound==1.2.2', 'pyaudio', 'mediapipe==0.8.11',
                      'pycaw'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/',
        'Donate': 'https://www.buymeacoffee.com/',
        'Say Thanks!': 'https://youtube.com/@yashvaibhav9546',
        'Source': 'https://github.com/',
    },
)
