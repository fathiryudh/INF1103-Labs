FROM python:3.11-slim

WORKDIR /app

COPY product.py inventory.py inventory_manager.py inventory.json test_inventory.py ./

CMD ["python", "inventory_manager.py"]
