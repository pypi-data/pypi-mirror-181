# 🛰 Satlink

> Let me introduce Satlink. Satlink is a light web framework, that aims to be _**easy to get started with**_, _**easy to build in**_ and _**easy to grow in**_, by focusing on core design principles, such as _"Low Barrier to Entry"_ and _"Self-documenting code"_. This framework was part of a project in Frameworks at HiØ, written with love in Python <3

All seriousness aside, this is a highly unstable and experimental framework, where the API might change without a moment's notice. It's simply a playground for trying out stuff. Use at your own risk.

## Getting started

### Dependencies

* There are almost none! 
* Satlink uses only bits from the Python Standard Library. 
* All you need is Python 3.11 or greater.
   * Not tested with earlier versions.

### Installation

Step 1: Start by installing the package from pip.
```bash
pip install satlink
```

Step 2: Let's create a file called `sat.py`.
```bash
touch sat.py
```

Step 4: Now, populate the sat.py file with the following code:
```python
from satlink import Satellite

sat = Satellite()

@sat.get("/")
def index(uplink, downlink):
  return downlink.text("Hello, World!")

sat.transmit()
# Alternatively: sat.transmit(3000, "localhost")
```

Step 5: Lastly, let's boot up our satellite.
```bash
python3 app.py
```
When you visit [http://localhost:3000/](http://localhost:3000/) you should see the text "Hello, World!".

To learn more, take a look at the [API documentation](https://github.com/olejorga/satlink/wiki).
