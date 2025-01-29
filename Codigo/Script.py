import requests
import csv
import time
import os

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


def main():
    query = input("Por favor, ingrese los términos de búsqueda separados por comas (ejemplo: 'Cascos LS2, Cascos AGV, Cascos MAC'): ")

    queries = [q.strip() for q in query.split(',')]


    path_to_save_directory = input("Por favor, ingrese la ruta del directorio donde guardar el archivo CSV (ejemplo: 'C:/ruta/cascos/'): ")

    filename = "_".join([q.replace(" ", "_").lower() for q in queries]) + ".csv"
    path_to_save_csv = os.path.join(path_to_save_directory, filename)

    all_items = {}
    for query in queries:
        item_ids = get_items_by_search(query)
        all_items[query] = item_ids

    for query, ids in all_items.items():
        print(f"Se encontraron {len(ids)} productos para {query}")

    all_item_details = []
    
    for query, item_ids in all_items.items():
        print(f"Obteniendo detalles de los productos de {query}...")
        item_details_batch = fetch_item_details_parallel(item_ids)
        all_item_details.extend(item_details_batch)

    if all_item_details:
        save_to_csv(all_item_details, path_to_save_csv)
        print(f"Los detalles de los productos fueron guardados en '{path_to_save_csv}'.")
    else:
        print("No se obtuvieron detalles de los productos.")



if __name__ == "__main__":
    main()
