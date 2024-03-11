import pytesseract
from PIL import Image
import re

def extract_information_from_receipt(image_path, start_word, end_word):
    # Load the receipt image
    image = Image.open(image_path)

    # Use Tesseract to perform OCR on the image
    full_text = pytesseract.image_to_string(image)

    # Extract the substring between start_word and end_word
    start_index = full_text.find(start_word)
    end_index = full_text.find(end_word)
    
    if start_index == -1 or end_index == -1 or start_index >= end_index:
        print(f"Error: Unable to find specified boundaries ('{start_word}' to '{end_word}') in the text.")
        return

    text_between_words = full_text[start_index + len(start_word):end_index]

    # Adjusted regular expression for product information
    component_pattern = re.compile(r'(\d+)\s+([\w\s&]+)\s*(?:([\d,]+)\s+)?([\d,]+)')

    # Initialize lists to store components and prices
    units_list = []
    descriptions = []
    unit_prices = []
    total_prices = []

    # Extract information using the adjusted regular expression
    matches = component_pattern.findall(text_between_words)
    for match in matches:
        units_list.append(int(match[0]))
        descriptions.append(match[1].strip())
        unit_prices.append(float(match[2].replace(',', '.')) if match[2] else None)
        total_prices.append(float(match[3].replace(',', '.')) if match[3] else None)

    # Display the extracted information
    for units, description, unit_price, total_price in zip(units_list, descriptions, unit_prices, total_prices):
        print(f"Units: {units}")
        print(f"Description: {description}")
        if unit_price is not None:
            print(f"Unit Price: {unit_price:.2f}")
        if total_price is not None:
            print(f"Total Price: ${total_price:.2f}")
        print()

if __name__ == "__main__":
    # Provide the path to the receipt image
    receipt_image_path = "C:\\proyectos\\repositorios\\receipt-reader\\images\\receipt.jpg"

    # Specify the start and end words to define the search boundaries
    start_word = "Importe"
    end_word = "TOTAL"

    # Call the function to extract information
    extract_information_from_receipt(receipt_image_path, start_word, end_word)
