import os
import logging
import zipfile
from datetime import datetime


def setup_logger() -> None:
    os.makedirs("logs", exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    
    existing_logs = [
        f for f in os.listdir("logs")
        if f.startswith(today) and f.endswith(".log")
    ]

    nums = [
        int(f.split("_")[-1].split(".")[0])
        for f in existing_logs
        if "_" in f and f.split("_")[-1].split(".")[0].isdigit()
    ]
    next_number = max(nums) + 1 if nums else 1

    file_name = f"logs/{today}_{next_number}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(message)s",
        handlers=[
            logging.FileHandler(file_name, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

def compress_logs() -> None:
    """Compresses the log files into a zip archive."""

    today = datetime.now().strftime("%Y-%m-%d")
    zip_filename = f"logs/{today}.zip"

    mode = 'a' if os.path.exists(zip_filename) else 'w'
    with zipfile.ZipFile(zip_filename, mode, zipfile.ZIP_DEFLATED) as zipf:
        for log_file in os.listdir("logs"):
            if log_file.startswith(today) and log_file.endswith(".log"):
                zipf.write(os.path.join("logs", log_file), log_file)
                os.remove(os.path.join("logs", log_file))
