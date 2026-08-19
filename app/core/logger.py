import logging
import os



if not os.path.exists("logs"):
    os.mkdir("logs")



logger=logging.getLogger("AL_AI")


logger.setLevel(logging.INFO)



file_handler=logging.FileHandler("logs/app.log",encoding="utf-8")


formatter=logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


console_handler=logging.StreamHandler()

console_handler.setFormatter(formatter)

logger.addHandler(console_handler)