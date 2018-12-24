# ImageAnalysisProject - web app

Simple web application that recognizes several hand gestures displayed by the user.


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