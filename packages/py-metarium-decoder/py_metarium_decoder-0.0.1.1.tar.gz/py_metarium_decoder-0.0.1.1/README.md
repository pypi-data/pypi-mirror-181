# py-metarium-decoder

# Usage


## 1. Virtual environment

### 1.1. Install virtual environment

```
pip3 install virtualenv
```

### 1.2. Create virtual environment for metarium

```
python3 -m venv virtualenv ~/venv-metarium-decoder
```

### 1.3. Activate metarium virtual environment

```
source ~/.venv-py-metarium-decoder/bin/activate
```

## 2. Install

### 2.1. Install metarium-decoder

```
pip install py-metarium-decoder
```

### 2.2. Install metarium

```
pip install py-metarium
```

### 2.3. Install substrate client

```
pip install substrate-interface==1.4.0
```

## 3. Example usage

### 3.1. Create a simple Listener
Create a listener script called `simple-listener.py` with the following code block
```
from py_metarium import (PAST, FUTURE)
from py_metarium_decoder import Decoder


class Listener:

    def __init__(self, url=None) -> None:
        self.__decoder = Decoder(url)
    
    def info(self):
        return self.__decoder.info()

    def listen(self, direction, block_hash=None, block_count=None):
        return self.__decoder.decode(direction, block_hash=block_hash, block_count=block_count)


metarium_node_url = "ws://127.0.0.1:9944"

# listen to past events and print the blocks in reverse order
listener = Listener(metarium_node_url)
print("listening ...")

with open('metarium_blocks.txt', 'w') as f:
    for block, has_metarium_call in listener.listen(PAST, None, None):
        print(f"{block['header']['number']}")
        if has_metarium_call:
            f.write(f"\n{block}")
```
Run the listener script
```
python simple-listener.py
```

## 4. Teardown

Please remember to deactivate the virtual environment after usage

```
deactivate
```