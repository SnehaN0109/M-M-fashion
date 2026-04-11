import time
import requests
import subprocess
import os

print("Starting Flask server...")
server_process = subprocess.Popen(
    ["python", "app.py"],
    cwd=os.path.abspath(os.path.dirname(__file__)),
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

time.sleep(3) # Wait for server to start

try:
    print("Testing Add Product API...")
    url = "http://127.0.0.1:5000/api/admin/add-product"
    data = {
        "name": "Test Floral Kurti",
        "category": "Kurti",
        "variants": [
            {"color": "Blue", "size": "M", "quantity": 100, "price_garba": 999, "price_ttd": 750, "price_maha": 800}
        ]
    }
    res = requests.post(url, json=data)
    try:
        print("Add Product Response:", res.status_code, res.json())
    except:
        print("Add Product Response Failed to Parse JSON. Status:", res.status_code, "Text:", res.text)

    print("Testing Get Products API...")
    res = requests.get("http://127.0.0.1:5000/api/products/")
    try:
        print("Get Products Response:", res.status_code, res.json()[:1]) # Print just first to keep it clean
    except:
        print("Get Products Response Failed to Parse JSON. Status:", res.status_code, "Text:", res.text)

    print("Testing Get Specific Product API by ID (1)...")
    res = requests.get("http://127.0.0.1:5000/api/products/1")
    print("Get Specific Product Response:", res.status_code)

finally:
    print("Terminating server...")
    server_process.terminate()
    server_process.wait()
