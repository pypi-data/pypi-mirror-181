<a href="https://semantha.de"><img src="https://www.semantha.de/wp-content/uploads/semantha.svg" width="380" height="95" align="right" /></a>

# semantha-streamlit-compare: semantha building blocks for Streamlit apps

This project gives you an idea of how to use our component for building applications with streamlit. And all of this using semantha's native capabilities to process semantics in text.

tl;dr: using Streamlit, you can employ semantha's semantic comparison with just three lines of code (see below).

## Which Components Are Involved?
Streamlit.io offers easy GUI implementations. semantha.ai is a semantic processing platform which provides a REST/API for many use cases, end systems, etc.

![alt text](https://user-images.githubusercontent.com/117350133/200347538-367e9478-26cb-4f4a-8e9a-21669cf1695f.jpg  "Streamlit Component Example")

## 🚀 Quickstart

You can install `semantha-streamlit-compare` from pip:

```bash
pip install semantha-streamlit-compare
```


Then put the following example code in a file.

```python
from semantha_streamlit_compare.components.compare import SemanticCompare

compare = SemanticCompare()
compare.build_input(sentences=("First sentence", "Second sentence"))
```

## 🎛 Setup, Secret, and API Key
To use the component, you need to request a secrets.toml file. You can request that at support@thingsthinking.atlassian.net<br />
The file is structured as follows:
```
[semantha]
server_url="URL_TO_SERVER"
api_key="YOUR_API_KEY_ISSUED"
domain="USAGE_DOMAIN_PROVIDED_TO_YOU"
documenttype="document_with_contradiction_enabled"
```
