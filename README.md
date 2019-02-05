# ImageAnalysisProject - web app

Simple web application that recognizes 10 hand gestures displayed by the user.

https://mindreaders.ml/

Web application designed to create a photo database needed to train the model of the neural network.

https://mindreaders.ml/learn

Documentation.

https://mindreaders.ml/docs

## Installation

```bash
sudo apt-get install python3-venv
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Usage
```python3
from img_processing import process_dir
process_dir('../imgs/in', '../imgs/out', True)
```

## Deploy

```bash
pip install ansible
ansible-playbook iac/site.yml 
```
