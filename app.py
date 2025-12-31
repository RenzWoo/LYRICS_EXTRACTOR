import pandas as pd
from pathlib import Path

folder = Path(r'C:\Users\User\Documents\Lyrics')

records = []

for idx, file in enumerate(folder.glob("*.txt")):
    records.append({'id':idx,'song':file.name, 'lyrics':file.read_text(encoding='utf-8')})

print(pd.DataFrame(records))

