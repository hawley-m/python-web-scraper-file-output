import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def clean_name(name):
    """Remove invalid characters from file or folder names."""
    invalid_chars = '/\\:*?"<>|'
    for char in invalid_chars:
        name = name.replace(char, "")
    return name.strip()


# ---------------------------
# User Input
# ---------------------------

url = input("Enter the website URL (include https://): ").strip()

print("\nWhat data would you like to extract?")
print("1 - Page title")
print("2 - Headings (h1, h2, h3)")
print("3 - Links")
print("4 - Paragraph text")

choice = input("Enter one or more choices (example: 1,3): ")
choices = [c.strip() for c in choice.split(",")]

valid_choices = {"1", "2", "3", "4"}
if not any(c in valid_choices for c in choices):
    print("\nError: Invalid selection. Choose from 1, 2, 3, or 4.")
    exit()

folder_name = clean_name(input("\nEnter a folder name to save the results: "))
file_name = clean_name(input("Enter an output file name (example: results.txt): "))
use_timestamp = input("Add timestamp to filename? (y/n): ").lower()

# Defaults
if not folder_name:
    folder_name = "scraped_data"

if not file_name:
    file_name = "results.txt"

if not file_name.endswith(".txt"):
    file_name += ".txt"

if use_timestamp == "y":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}_{file_name}"


# ---------------------------
# Request Website (Error Handling)
# ---------------------------

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException:
    print("\nError: Unable to connect to the website.")
    print("Please check the URL and your internet connection.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")


# ---------------------------
# Create Folder and File
# ---------------------------

os.makedirs(folder_name, exist_ok=True)
file_path = os.path.join(folder_name, file_name)

try:
    file = open(file_path, "w", encoding="utf-8")
except OSError:
    print("\nError: Could not create the output file.")
    exit()


# ---------------------------
# Extract Data
# ---------------------------

if "1" in choices:
    file.write("PAGE TITLE:\n")
    title = soup.title.string if soup.title else "No title found"
    file.write(title + "\n\n")

if "2" in choices:
    file.write("HEADINGS:\n")
    for heading in soup.find_all(["h1", "h2", "h3"]):
        file.write(heading.get_text() + "\n")
    file.write("\n")

if "3" in choices:
    file.write("LINKS:\n")
    for link in soup.find_all("a"):
        file.write(link.get("href", "") + "\n")
    file.write("\n")

if "4" in choices:
    file.write("PARAGRAPHS:\n")
    for paragraph in soup.find_all("p"):
        file.write(paragraph.get_text() + "\n")


# ---------------------------
# Finish
# ---------------------------

file.close()
print(f"\nDone! Your data is saved at:\n{file_path}")
