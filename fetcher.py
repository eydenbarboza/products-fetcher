import csv
import requests
import json
import argparse

class DataFetcher:
    def __init__(self, url: str):
        self.url = url

    def fetch(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.json()

class ProductParser:
    @staticmethod
    def parse(data, lang):
        variants = data.get("allVariants", [])
        parsed_data = []

        for variant in variants:
            attributes = ProductParser.parse_attributes(variant, lang)
            parsed_data.append(attributes)
        
        return parsed_data

    @staticmethod
    def parse_attributes(variant, lang):
        # Extracts the "custom_attributes" field and parses in the selected language
        attributes = {}
        
        for attribute in variant.get("attributesRaw", []):
            if attribute.get("name") == "custom_attributes":
                custom_attributes = attribute.get("value")
                
                # Parses the selected language
                parsed = ProductParser.parse_product_info(custom_attributes, lang)
                attributes.update(parsed)  # Use update to combine attributes into a single dictionary

        return attributes

    @staticmethod
    def parse_product_info(custom_attributes, lang):
        # Processes product information in the specified language
        product_info = json.loads(custom_attributes.get(lang, "{}"))
        
        return {
            "allergens": [allergen.get("name") for allergen in product_info.get("allergens", {}).get("value", [])],
            "sku": product_info.get("sku", {}).get("value"),
            "vegan": product_info.get("vegan", {}).get("value"),
            "kosher": product_info.get("kosher", {}).get("value"),
            "organic": product_info.get("organic", {}).get("value"),
            "vegetarian": product_info.get("vegetarian", {}).get("value"),
            "gluten_free": product_info.get("gluten_free", {}).get("value"),
            "lactose_free": product_info.get("lactose_free", {}).get("value"),
            "package_quantity": product_info.get("package_quantity", {}).get("value"),
            "unit_size": float(product_info.get("unit_size", {}).get("value", 0)),
            "net_weight": float(product_info.get("net_weight", {}).get("value", 0))
        }

class CSVWriter:
    @staticmethod
    def write_to_csv(data, filename="output-product.csv"):
        headers = [
            "allergens", "sku", "vegan", "kosher", "organic", 
            "vegetarian", "gluten_free", "lactose_free", 
            "package_quantity", "unit_size", "net_weight"
        ]
        
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

def main():
    parser = argparse.ArgumentParser(description="Fetch product data and parse it into CSV.")
    parser.add_argument('--lang', type=str, choices=['es-CR', 'en-CR'], default='es-CR',
                        help="Select the language for the product information (default: 'es-CR')")
    args = parser.parse_args()

    url = "https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json"
    fetcher = DataFetcher(url)
    data = fetcher.fetch()

    product_parser = ProductParser()
    parsed_data = product_parser.parse(data, args.lang)

    # Save to CSV
    CSVWriter.write_to_csv(parsed_data)
    print(f"Data saved in output-product.csv in language: {args.lang}")

if __name__ == "__main__":
    main()
