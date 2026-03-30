# Task 1 - File Read & Write Basics

# Part A - Write
file = open("python_notes.txt", "w", encoding="utf-8")
file.write("Topic 1: Variables store data. Python is dynamically typed.\n")
file.write("Topic 2: Lists are ordered and mutable.\n")
file.write("Topic 3: Dictionaries store key-value pairs.\n")
file.write("Topic 4: Loops automate repetitive tasks.\n")
file.write("Topic 5: Exception handling prevents crashes.\n")
file.close()
print("File written successfully.")

# Append two more lines
file = open("python_notes.txt", "a", encoding="utf-8")
file.write("Topic 6: Functions help us reuse code.\n")
file.write("Topic 7: Python is beginner friendly.\n")
file.close()
print("Lines appended.")

# Part B - Read
file  = open("python_notes.txt", "r", encoding="utf-8")
lines = file.readlines()
file.close()

# print numbered lines
for i in range(len(lines)):
    line = lines[i].strip()
    print(i + 1, ".", line)

# total lines
print("Total lines :", len(lines))

# keyword search
keyword = input("Enter a keyword to search: ")
found   = False

for line in lines:
    if keyword.lower() in line.lower():
        print(line.strip())
        found = True

if found == False:
    print("No lines found with that keyword!")

#---------------------------------------------------------------------------------------------------

# Task 2 - API Integration
import requests

# Step 1 - fetch 20 products
response = requests.get("https://dummyjson.com/products?limit=20", timeout=5)
data     = response.json()
products = data["products"]

# print table
print("ID  | Title                          | Category      | Price    | Rating")
print("----|--------------------------------|---------------|----------|-------")

for product in products:
    print(
        str(product["id"]).ljust(4), "|",
        str(product["title"]).ljust(30), "|",
        str(product["category"]).ljust(13), "|",
        "$" + str(product["price"]).ljust(8), "|",
        product["rating"]
    )

print("")

# Step 2 - filter rating >= 4.5 and sort by price
filtered = []

for product in products:
    if product["rating"] >= 4.5:
        filtered.append(product)

# sort by price highest first
for i in range(len(filtered)):
    for j in range(i + 1, len(filtered)):
        if filtered[j]["price"] > filtered[i]["price"]:
            temp        = filtered[i]
            filtered[i] = filtered[j]
            filtered[j] = temp

print("Filtered products (rating >= 4.5) sorted by price :")
for product in filtered:
    print(product["title"], "- $" + str(product["price"]), "- Rating:", product["rating"])

print("")

# Step 3 - laptops category
response2 = requests.get("https://dummyjson.com/products/category/laptops", timeout=5)
data2     = response2.json()
laptops   = data2["products"]

print("Laptops :")
for laptop in laptops:
    print(laptop["title"], "- $" + str(laptop["price"]))

print("")

# Step 4 - POST request
new_product = {
    "title":       "My Custom Product",
    "price":       999,
    "category":    "electronics",
    "description": "A product I created via API"
}

response3 = requests.post("https://dummyjson.com/products/add", json=new_product, timeout=5)
print("POST response :")
print(response3.json())

#---------------------------------------------------------------------------------------------------

# Task 3 - Exception Handling

import requests

# Part A - safe divide
def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print(safe_divide(10, 2))
print(safe_divide(10, 0))
print(safe_divide("ten", 2))
print("")

# Part B - safe file reader
def read_file_safe(filename):
    try:
        file    = open(filename, "r", encoding="utf-8")
        content = file.read()
        file.close()
        return content
    except FileNotFoundError:
        print("Error: File '" + filename + "' not found.")
    finally:
        print("File operation attempt complete.")

print(read_file_safe("python_notes.txt"))
print(read_file_safe("ghost_file.txt"))
print("")

# Part C - robust API calls
try:
    response = requests.get("https://dummyjson.com/products?limit=20", timeout=5)
    data     = response.json()
    print("Products fetched successfully!")
except requests.exceptions.ConnectionError:
    print("Connection failed. Please check your internet.")
except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except Exception as e:
    print("Unexpected error:", e)

print("")

# Part D - input validation loop
while True:
    user_input = input("Enter a product ID (1-100) or 'quit' to exit: ")

    if user_input == "quit":
        break

    if not user_input.isdigit():
        print("Warning: Please enter a valid number!")
        continue

    product_id = int(user_input)

    if product_id < 1 or product_id > 100:
        print("Warning: Number must be between 1 and 100!")
        continue

    try:
        response = requests.get("https://dummyjson.com/products/" + str(product_id), timeout=5)

        if response.status_code == 404:
            print("Product not found.")
        elif response.status_code == 200:
            product = response.json()
            print("Title :", product["title"])
            print("Price : $" + str(product["price"]))

    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
    except Exception as e:
        print("Unexpected error:", e)

#---------------------------------------------------------------------------------------------------

# Task 4 - Logging to File

from datetime import datetime
import requests

# logger function
def log_error(location, error_message):
    now       = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = "[" + timestamp + "] ERROR in " + location + ": " + error_message + "\n"

    file = open("error_log.txt", "a", encoding="utf-8")
    file.write(log_entry)
    file.close()

    print("Logged:", log_entry)

# trigger ConnectionError
print("Triggering ConnectionError...")
try:
    response = requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError:
    log_error("fetch_products", "ConnectionError - No connection could be made")
except requests.exceptions.Timeout:
    log_error("fetch_products", "Timeout - Request timed out")

print("")

# trigger 404 error
print("Triggering 404 error...")
try:
    response = requests.get("https://dummyjson.com/products/999", timeout=5)

    if response.status_code != 200:
        log_error("lookup_product", "HTTPError - 404 Not Found for product ID 999")
    else:
        print("Product found!")

except requests.exceptions.ConnectionError:
    log_error("lookup_product", "ConnectionError - No connection could be made")
except requests.exceptions.Timeout:
    log_error("lookup_product", "Timeout - Request timed out")

print("")

# print error log
print("Contents of error_log.txt :")
file    = open("error_log.txt", "r", encoding="utf-8")
content = file.read()
file.close()
print(content)