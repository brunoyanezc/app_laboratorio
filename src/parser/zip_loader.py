from pathlib import Path
from zipfile import ZipFile
import tempfile


def extract_zip(uploaded_file):

    temp_dir = tempfile.mkdtemp()

    zip_path = Path(temp_dir) / uploaded_file.name

    with open(zip_path, "wb") as f:

        f.write(uploaded_file.getbuffer())

    with ZipFile(zip_path, "r") as zip_ref:

        zip_ref.extractall(temp_dir)

    return temp_dir