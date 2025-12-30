import pandas as pd
from pathlib import Path

file = Path("WORTHY OF IT ALL.txt")

print(file.read_text(encoding='utf-8'))


