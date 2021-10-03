## Setup

```
git clone https://github.com/collinsuzebu/merchants.git
pip install -r merchants/requirements.txt
```

**[hotreload]**
_hupper -m waitress --port=8000 merchants.app:app_

**[waitress-server]**
_python -m waitress --port=8000 merchants.app:app_

**[pytest]**
_pytest merchants_
