import requests
import os

url = "https://we.tl/t-T75HfKbkjD"  # ← YOUR WeTransfer link here
response = requests.get(url)
with open('my_preschool_ai.h5', 'wb') as f:
    f.write(response.content)
print("Model downloaded!")
