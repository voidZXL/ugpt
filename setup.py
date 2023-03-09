from setuptools import setup, find_packages
from ugpt import __version__

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()


setup(
    name='uGPT',
    version=__version__,
    description='An easy to use API and CLI wrapper for chatGPT and other AIGC API base on utype',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='周煦林 (XuLin Zhou)',
    author_email='zxl@utilmeta.com',
    keywords="ugpt gpt chatgpt openai utype api",
    python_requires='>=3.7',
    install_requires=['utype'],
    license="https://opensource.org/license/mit/",
    url="https://github.com/voidZXL/ugpt",
    project_urls={
        "Project Home": "https://github.com/voidZXL/ugpt",
        "Documentation": "https://github.com/voidZXL/ugpt",
        "Source Code": "https://github.com/voidZXL/ugpt",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
    ],
    packages=find_packages(exclude=["tests.*", "tests"]),
    entry_points={
        'console_scripts': ['meta=ugpt.bin:main'],
    },
)
