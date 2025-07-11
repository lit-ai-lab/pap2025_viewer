import pandas as pd
import os
from uuid import uuid4


EXPORT_DIR = "static/downloads"
os.makedirs(EXPORT_DIR, exist_ok=True)


def generate_excel_file(viewers):
    df = pd.DataFrame([v.__dict__ for v in viewers])
    filename = f"viewer_export_{uuid4().hex}.xlsx"
    file_path = os.path.join(EXPORT_DIR, filename)
    df.to_excel(file_path, index=False)
    return file_path
