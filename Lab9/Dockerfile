FROM python:3.11-slim
WORKDIR /app
COPY *.py inventory.json ./
COPY tests/ tests/
CMD ["python", "inventory_manager.py"]
