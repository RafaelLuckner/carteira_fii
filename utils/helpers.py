import logging
import os

# Criar diretório de logs se não existir
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar logging
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,  # Níveis: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Criar um logger
logger = logging.getLogger(__name__)
