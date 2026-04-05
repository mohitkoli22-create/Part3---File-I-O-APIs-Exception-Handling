# Task 1 - File read and write basics.
# Write to file
f = open("python_notes.txt", "w", encoding="utf-8") # create or overwrite file with utf-8 encoding and write mode "w"
f.write("Topic 1: Variables store data.\n")
f.write("Topic 2: Lists are ordered.\n")
f.write("Topic 3: Dictionaries store key-value pairs.\n")
f.write("Topic 4: Loops automate tasks.\n")
f.write("Topic 5: Exception handling prevents crashes.\n")
f.close() # saves and closes the file
print("File written successfully.")

# Append to file
f = open("python_notes.txt", "a", encoding="utf-8") # open file in append mode "a" to add new content without overwriting
f.write("Topic 6: Functions are used to reuse code.\n")
f.write("Topic 7: API allows communication between systems.\n")
f.close()

print("Lines appended.")

# Read file
f = open("python_notes.txt", "r", encoding="utf-8")
lines = f.readlines() #gives list of lines
f.close()

# Print with numbering
for i in range(len(lines)):
    print(i+1, ".", lines[i].strip()) # i+1 to start numbering from1 , .strip() to remove extra blank spaces

print("Total lines:", len(lines))

# Search keyword
keyword = input("Enter keyword: ").lower() # converts input to lowecase
found = False

for line in lines:
    if keyword in line.lower(): # make search lowercase for case-insensitive search 

        print(line.strip())
        found = True

if not found:
    print("No match found.")





# Task 2 — API Integration
import requests # import requests library to make HTTP requests

# Base URL
BASE_URL = "https://dummyjson.com/products"

# Step 1 — Fetch and Display Products
response = requests.get(f"{BASE_URL}?limit=20") #send request to API to get 20 products
data = response.json() # convert API response to python dictionary

products = data["products"] # extract list of products from the response

# Print table header
print("ID  | Title                          | Category      | Price    | Rating")
print("----|--------------------------------|---------------|----------|-------")

# Print each product
for p in products:
    print(f"{p['id']:<4}| {p['title']:<30}| {p['category']:<13}| ${p['price']:<8}| {p['rating']}")

# Step 2 — Filter and Sort
filtered = [p for p in products if p["rating"] >= 4.5] # filter products with rating 4.5 or higher using list comprehension

# Sort by price (descending)
sorted_products = sorted(filtered, key=lambda x: x["price"], reverse=True)

print("\nFiltered (rating ≥ 4.5) and Sorted by Price:\n") # print header for filtered and sorted products

for p in sorted_products:
    print(f"{p['title']} - ${p['price']} - Rating: {p['rating']}") # print title, price, and rating of each filtered and sorted product

# Step 3 — Search by Category
laptop_response = requests.get(f"{BASE_URL}/category/laptops") # send request to API to get products in the "laptops" category
laptops = laptop_response.json()["products"] # extract list of laptop products from the response

print("\nLaptops Category:\n")

for l in laptops:
    print(f"{l['title']} - ${l['price']}")

# Step 4 — POST Request
new_product = {
    "title": "iPHONE16",
    "price": 900,
    "category": "SMARTPHONES",
    "description": "A product I created via API"
}

post_response = requests.post(f"{BASE_URL}/add", json=new_product) # send POST request to API to add new product, json parameter automatically converts the dictionary to JSON format

print("\nPOST Response:\n")
print(post_response.json())



#Task 3 — Exception Handling

 # PART A - GUARDED CALCULATOR

def safe_divide(a, b): # function to perform division with exception handling
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

# Testing
print(safe_divide(10, 2))     # Normal case
print(safe_divide(10, 0))     # Divide by zero
print(safe_divide("ten", 2))  # Wrong type


# PART B - GUARDED FILE READER 

def read_file_safe(filename): # function to read file content with exception handling
    try:
        file = open(filename, "r")
        content = file.read()
        file.close()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    finally:
        print("File operation attempt complete.")

# Testing
print(read_file_safe("python_notes.txt"))   # should work
print(read_file_safe("ghost_file.txt"))     # should show error

# PART C - ROBUST API CALL

import requests

url = "https://dummyjson.com/products" # API TO FETCH DATA

try:
    response = requests.get(url, timeout=5) # send GET request to API with a timeout of 5 seconds to prevent hanging indefinitely
    print("Status Code:", response.status_code)

except requests.exceptions.ConnectionError: # handle connection errors such as no internet or server issues
    print("Connection failed. Please check your internet.")

except requests.exceptions.Timeout: # handle timeout errors when the API takes too long to respond
    print("Request timed out. Try again later.")

except Exception as e:
    print("Error:", e)

# PART D - INPUT VALIDATION LOOP

import requests

while True:
    user_input = input("Enter product ID (1–100) or 'quit': ") # prompt user for input to enter product ID or quit the program

    if user_input.lower() == "quit": # check if user wants to quit the program
        print("Goodbye!")
        break

    # Check if input is a number
    if not user_input.isdigit(): # check if the input is not a valid number
        print("Please enter a valid number.")
        continue

    product_id = int(user_input) # convert the input to an integer for further processing.

    # Check range
    if product_id < 1 or product_id > 100: # check if the product ID is within the valid range of 1 to 100
        print("Please enter a number between 1 and 100.")
        continue

    # API call
    try:
        url = f"https://dummyjson.com/products/{product_id}" # cONNECT the API URL using the user-provided product ID to fetch specific product details
        response = requests.get(url, timeout=5)

        if response.status_code == 200: # check if the API response is successful (status code 200) 
            data = response.json()
            print("Title:", data["title"])
            print("Price:", data["price"])

        elif response.status_code == 404: # check if the product is not found (status code 404) 
            print("Product not found.")

    except requests.exceptions.ConnectionError: # handle connection errors such as no internet or server issues
        print("No internet connection.")

    except requests.exceptions.Timeout: # handle timeout errors when the API takes too long to respond
        print("Request timed out.")

    except Exception as e:
        print("Error:", e)



# TASK 4 — LOGGING TO FILE

import requests
from datetime import datetime # import datetime module to get current date and time for logging purposes

# Step 1: Function to log errors
def log_error(function_name, error_type, message): # function to log error details to a file, takes function name, error type, and message as parameters
    time_now = datetime.now()
    
    log_message = f"[{time_now}] ERROR in {function_name}: {error_type} — {message}\n" # format the log message to include time, function name, error type, and message.
    
    # Open file in append mode
    with open("error_log.txt", "a") as file: # open the log file in append mode to add new log entries without overwriting existing logs
        file.write(log_message)

# Step 2: Trigger Connection Error
try:
    response = requests.get("https://this-host-does-not-exist-xyz.com/api") # attempt to connect to a  host to trigger a connection error
except requests.exceptions.ConnectionError:
    log_error("fetch_products", "ConnectionError", "No connection could be made") # log the connection error details to log_error function.

# Step 3: Trigger HTTP Error (404)
response = requests.get("https://dummyjson.com/products/999") # attempt to fetch a product with an ID that does not exist to trigger a 404 error.

if response.status_code != 200:
    log_error("lookup_product", "HTTPError", "404 Not Found for product ID 999") # log the HTTP error details to log_error function if the response status code is not 200.

# Step 4: Read and print log file
print("\n--- Error Log ---")
with open("error_log.txt", "r") as file: # open the log file in read mode to read and display the logged errors
    print(file.read())
