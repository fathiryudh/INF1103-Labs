FROM python:3.11-slim
WORKDIR /app
COPY product.py physical_product.py digital_product.py can_be_shipped.py supplier.py inventory.py order.py order_line.py inventory_manager.py inventory.json test_inventory.py ./
CMD ["python", "inventory_manager.py"]
