import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import csv
import time
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_items_by_search(query, limit=50):
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={query}&limit={limit}"
    items = []
    offset = 0

    while True:
        response = requests.get(f"{url}&offset={offset}")
        
        if response.status_code != 200:
            print(f"Error en la solicitud para {query}: {response.status_code}")
            break
        
        data = response.json()

        if 'results' not in data:
            print(f"No se encontraron resultados para {query}.")
            break
        
        items += [item['id'] for item in data['results']]

        if len(data['results']) < limit:
            break

        offset += limit
        time.sleep(1) 

    return items



def get_item_details(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    response = requests.get(url)
    item_data = response.json()

    try:
        item_info = {
            'item_id': item_data.get('id', 'No ID'),
            'title': item_data.get('title', 'No Title'),
            'price': item_data.get('price', 'No Price'),
            'currency_id': item_data.get('currency_id', 'No Currency'),
            'condition': item_data.get('condition', 'No Condition'),
            'available_quantity': item_data.get('initial_quantity', 'No Quantity'),
            'seller_id': item_data.get('seller_id', 'No Seller ID'),
            'seller_reputation': item_data.get('seller', {}).get('reputation', {}).get('level_id', 'No Reputation'),
            'location': item_data.get('seller_address', {"state": {"id", "name"}}).get("state", {"id", "name"}).get("name", 'No location info'),
            'url': item_data.get('permalink', 'No URL')
        }
        return item_info
    except Exception as e:
        print(f"Error al procesar el ítem {item_id}: {e}")
        return None



def save_to_csv(data, filename):
    if not data:
        print("No se encontraron datos para guardar.")
        return


    os.makedirs(os.path.dirname(filename), exist_ok=True)
    

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)



def fetch_item_details_parallel(item_ids):
    all_item_details = []

    with ThreadPoolExecutor(max_workers=10) as executor:  
        futures = {executor.submit(get_item_details, item_id): item_id for item_id in item_ids}
        
        for future in as_completed(futures):
            item_details = future.result()
            if item_details:
                all_item_details.append(item_details)

    return all_item_details



def execute_search():
  
    query = entry_query.get()
    if not query:
        messagebox.showerror("Error", "Por favor, ingrese al menos un término de búsqueda.")
        return


    path_to_save_directory = entry_directory.get()
    if not path_to_save_directory:
        messagebox.showerror("Error", "Por favor, seleccione una ruta de directorio.")
        return

    queries = [q.strip() for q in query.split(',')]
    filename = "_".join([re.sub(r'[^\w\s-]', '', q.replace(" ", "_").lower()) for q in queries]) + ".csv"
    path_to_save_csv = os.path.join(path_to_save_directory, filename)

    all_items = {}
    for query in queries:
        item_ids = get_items_by_search(query)
        all_items[query] = item_ids

    all_item_details = []
    
    for query, item_ids in all_items.items():
        item_details_batch = fetch_item_details_parallel(item_ids)
        all_item_details.extend(item_details_batch)


    if all_item_details:
        save_to_csv(all_item_details, path_to_save_csv)
        messagebox.showinfo("Éxito", f"Los detalles de los productos fueron guardados en '{path_to_save_csv}'.")
    else:
        messagebox.showwarning("Aviso", "No se obtuvieron detalles de los productos.")


def browse_directory():
    directory = filedialog.askdirectory()  
    entry_directory.delete(0, tk.END) 
    entry_directory.insert(0, directory)  



root = tk.Tk()
root.title("Búsqueda de productos en MercadoLibre")
root.geometry("600x300") 

label_query = tk.Label(root, text="Ingrese los términos de búsqueda (separados por comas):")
label_query.pack(pady=10)

entry_query = tk.Entry(root, width=50)
entry_query.pack(pady=5)

label_directory = tk.Label(root, text="Seleccione el directorio para guardar el archivo CSV:")
label_directory.pack(pady=10)

entry_directory = tk.Entry(root, width=50)
entry_directory.pack(pady=5)

browse_button = tk.Button(root, text="Buscar Directorio", command=browse_directory)
browse_button.pack(pady=5)


search_button = tk.Button(root, text="Ejecutar Búsqueda", command=execute_search)
search_button.pack(pady=20)

root.mainloop()
