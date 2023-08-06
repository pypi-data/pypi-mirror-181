# py-metarium-listener

# Usage


## 1. Virtual environment

### 1.1. Install virtual environment

```
pip3 install virtualenv
```

### 1.2. Create virtual environment for metarium

```
python3 -m venv virtualenv ~/venv-metarium-listener
```

### 1.3. Activate metarium virtual environment

```
source ~/.venv-py-metarium-listener/bin/activate
```

## 2. Install

### 2.1. Install metarium-listener

```
pip install py-metarium-listener
```

### 2.2. Install metarium-decoder

```
pip install py-metarium-decoder
```

### 2.3. Install metarium

```
pip install py-metarium
```

### 2.4. Install substrate client

```
pip install substrate-interface==1.4.0
```

## 3. Example usage

### 3.1. Create a simple Storage
Create a listener script called `simple-storage.py` with the following code block
```
from py_metarium import (PAST, FUTURE)

from py_metarium_listener import (
    KuriListener,
    QueryParameter
)

metarium_node_url = "ws://127.0.0.1:9944"

# create a query to get all kuris beginnig with `|>ipfs|` registered by an account
query = [
    QueryParameter("caller", "^ACCOUNT_ADDRESS_HERE$"),
    QueryParameter("kuri", "^\|\>ipfs\|.*")
]

# set filename
file_suffix = "all"
if len(query):
    file_suffix = ""
    for param in query:
        if len(file_suffix):
            file_suffix += "&"
        file_suffix += f"{param.field}={param.value}"
file_suffix += ".py"
filename = f"kuris-{file_suffix}"

# listen
kuri_listener = KuriListener(metarium_node_url)
print("listening ...")

# store
with open(f"{filename}", "w") as f:
    print("storing ...")
    for block in kuri_listener.listen(
                FUTURE,
                None,
                None,
                query=query
            ):
        f.write(f"\n{block}")
```
Run the storage script
```
python simple-storage.py
```

## 4. Teardown

Please remember to deactivate the virtual environment after usage

```
deactivate
```