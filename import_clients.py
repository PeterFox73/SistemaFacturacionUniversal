import sqlite3
from bs4 import BeautifulSoup
import os

# Connect to database
db_path = "inventario.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create Clients Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        empresa TEXT,
        telefono TEXT,
        email TEXT,
        notas TEXT
    )
""")

# Parse HTML
html_path = r"C:\Users\Pedro\Desktop\escritorio\conta 2.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
        
    # Python list in the script tag contains the data
    # Let's extract it from the script tag content
    scripts = soup.find_all("script")
    for script in scripts:
        if "const contactsData =" in script.text:
            # Dangerous eval but effective for this specific task ensuring we only get the list
            # We need to clean the string to make it valid python
            js_content = script.text
            start_index = js_content.find("[")
            end_index = js_content.rfind("]") + 1
            json_str = js_content[start_index:end_index]
            
            # JS object keys aren't quoted, need to fix for Python/JSON
            # Simple regex replacement or just manual parsing might be safer given the format
            import re
            
            # Simple manual extraction since the format is consistent
            # name: "Value",
            clients = []
            # We'll rely on the structure being list of dicts
            
            # Let's try flexible parsing or just run a regex for each field
            # The file structure is very regular
            
            # Alternative: use regex to find all matches
            # name: "(.*?)",
            
            names = re.findall(r'name:\s*"(.*?)",', json_str)
            companies = re.findall(r'company:\s*"(.*?)",', json_str)
            titles = re.findall(r'title:\s*"(.*?)",', json_str) # capture but maybe append to notes or company
            phones = re.findall(r'phone:\s*"(.*?)",', json_str)
            emails = re.findall(r'email:\s*"(.*?)",', json_str)
            notes = re.findall(r'notes:\s*"(.*?)"', json_str)
            
            # Zip and insert
            count = 0
            for i in range(len(names)):
                try:
                    name = names[i]
                    company = companies[i]
                    # title = titles[i] # keeping simple for now
                    phone = phones[i]
                    email = emails[i]
                    note = notes[i]
                    
                    cursor.execute("INSERT INTO clientes (nombre, empresa, telefono, email, notas) VALUES (?, ?, ?, ?, ?)",
                                   (name, company, phone, email, note))
                    count += 1
                except IndexError:
                    pass
            
            conn.commit()
            print(f"Imported {count} clients successfully.")
else:
    print("HTML file not found.")

conn.close()
