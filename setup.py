import setuptools

with open("requirements.txt") as f:
    reqs = f.read().split("\n")

setuptools.setup(
    name="flask_quill",
    version='0.1',
    author="Drew Dru",
    description="",
    url="https://github.com/drewdru/flask-quill",
    packages=setuptools.find_packages(),
    # install_requires=reqs,
    # templates=['flask_quill/templates/dependencies.html'],
    package_data={'flask_quill': [
        'static/editor/editor.js',
        'static/tabs/tabs.css',
        'static/tabs/tabs.js',
        'templates/dependencies.html',
    ]},
    license='LICENSE',
    # description='wtforms widget for quill.js editor',
    long_description=open('README.md').read(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3.0 (GPL v3.0)",
        "Operating System :: OS Independent",
    ]
)
