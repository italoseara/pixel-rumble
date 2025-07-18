import logging
import os
from datetime import datetime

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    data_hoje = datetime.now().strftime("%Y-%m-%d")
    
    existing_logs = [
        f for f in os.listdir("logs")
        if f.startswith(data_hoje) and f.endswith(".log")
    ]

    numeros = [
        int(f.split("_")[-1].split(".")[0])
        for f in existing_logs
        if "_" in f and f.split("_")[-1].split(".")[0].isdigit()
    ]
    proximo_numero = max(numeros) + 1 if numeros else 1

    nome_arquivo = f"logs/{data_hoje}_{proximo_numero}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(nome_arquivo, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
