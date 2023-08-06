# voiceinvoiceout


```cmd
pip install voiceinvoiceout
```

Developed by Vedant Barhate (c) 2022

This package is useful when you want to take audio input through mic from user, give audio output, give audio+text output and audio repeating feature (like talking tom).

## Example
```python
from voiceinvoiceout import *

vin = voiceIn("Say something...")    # to take audio input 
print(vin)

vout = voiceOut("Hello world")    # to give audio output

sp = sprint("Welcome")      # to give text+audio output (sprint=speak+print)

speakOut()      # to repeat your words (like talking tom)
```