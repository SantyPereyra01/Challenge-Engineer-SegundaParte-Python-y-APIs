# Challenge-Engineer-SegundaParte-Python-y-APIs
Challenge Engineer - Segunda Parte - Python y APIs
# Análisis de la Oferta de Cascos para Motos en MercadoLibre

## Objetivo del Proyecto
El objetivo de este proyecto es realizar un análisis sobre la oferta de productos relacionados con cascos para motos en MercadoLibre Argentina. Para ello, se hace uso de la API pública de MercadoLibre para recolectar información sobre precios, condiciones de los productos (nuevo vs usado), reputación de los vendedores, y más. Posteriormente, se realiza un análisis exploratorio de los datos obtenidos, generando visualizaciones útiles que pueden ser utilizadas para tomar decisiones informadas.

**Herramientas y Tecnologías Utilizadas**:
- **Lenguaje de Programación**: Python
- **Librerías**:
  - `requests`: Para realizar solicitudes HTTP a la API de MercadoLibre.
  - `pandas`: Para el procesamiento y análisis de datos.
  - `matplotlib`, `seaborn`: Para la creación de visualizaciones.
  - `tkinter`: Para la creación de la interfaz gráfica del usuario (GUI).
  - `csv`: Para guardar los resultados en formato CSV.
- **API**: API pública de MercadoLibre (consulta de productos y detalles)
- **Formato de Salida**: CSV (archivo con los detalles de los productos).

---

## Flujo de Datos

1. **Entrada del Usuario**:
   - El usuario ingresa los **términos de búsqueda** (por ejemplo: "Cascos LS2", "Cascos AGV") a través de una **interfaz gráfica** o línea de comandos.
   - El usuario selecciona la **ubicación del archivo CSV** donde desea guardar los resultados.

2. **Consulta a la API de MercadoLibre**:
   - El sistema realiza una consulta **GET** a la API de MercadoLibre para obtener los **ID** de los productos correspondientes a los términos de búsqueda.

3. **Obtención de Detalles de los Productos**:
   - Una vez que se obtienen los IDs, el sistema realiza solicitudes **GET** a la API de MercadoLibre para obtener detalles adicionales de los productos como el **precio**, **cantidad disponible**, **reputación del vendedor**, **condición**, etc.

4. **Desnormalización y Guardado de Datos**:
   - Los datos obtenidos se procesan y se desnormalizan. El sistema guarda los resultados en un archivo **CSV** con las siguientes columnas:
     - `item_id`: ID del producto.
     - `title`: Nombre del producto.
     - `price`: Precio del producto.
     - `currency_id`: Moneda en la que se encuentra el precio.
     - `condition`: Condición del producto (nuevo/usado).
     - `available_quantity`: Cantidad disponible.
     - `seller_id`: ID del vendedor.
     - `seller_reputation`: Reputación del vendedor.
     - `location`: Ubicación del producto (estado).
     - `url`: Enlace al producto.

5. **Análisis Exploratorio de Datos**:
   - Se realiza un análisis exploratorio de los datos, que incluye la **distribución de precios**, **condiciones de los productos**, **distribución de la cantidad disponible**, y **reputación de los vendedores**. Se utilizan gráficos como histogramas, boxplots y gráficos de dispersión.

6. **Salida al Usuario**:
   - El archivo **CSV** con los resultados es guardado en el directorio seleccionado por el usuario.
   - Los gráficos y resultados del análisis también se presentan al usuario a través de la interfaz gráfica o la consola.

---

## Diagrama de Arquitectura

El flujo del sistema se visualiza a través de un diagrama de alto nivel, que muestra los pasos clave de la solución desde la **entrada del usuario** hasta la **salida con el archivo CSV** y los resultados del análisis.

- **Entrada del Usuario**: El usuario ingresa los términos de búsqueda y la ubicación para guardar el archivo CSV.
- **Consulta a la API de MercadoLibre**: Se realiza una consulta a la API para obtener los IDs de los productos.
- **Obtención de Detalles del Producto**: Usando los IDs de los productos, se obtiene información detallada de cada uno.
- **Procesamiento y Guardado de Datos**: Los datos obtenidos se procesan y se guardan en un archivo CSV.
- **Análisis Exploratorio**: Se realizan gráficos y análisis estadísticos de los datos.
- **Salida al Usuario**: El archivo CSV se guarda y los resultados son presentados.

**Nota**: El diagrama de flujo fue creado utilizando [Draw.io](https://app.diagrams.net/), una herramienta gratuita y fácil de usar para crear diagramas visuales.

---

## Pasos Detallados

### 1. Entrada del Usuario
   - El usuario ingresa los términos de búsqueda (por ejemplo: "Cascos LS2", "Cascos AGV") en la interfaz gráfica o línea de comandos.
   - El sistema también solicita la **ruta donde guardar el archivo CSV**.

### 2. Consulta a la API de MercadoLibre
   - El sistema realiza una consulta **GET** a la API pública de MercadoLibre (`https://api.mercadolibre.com/sites/MLA/search?q={query}&limit=50`) para obtener los IDs de los productos.

### 3. Obtención de Detalles de los Productos
   - Después de obtener los IDs de los productos, el sistema realiza solicitudes **GET** a `https://api.mercadolibre.com/items/{Item_Id}` para obtener detalles de cada producto, como:
     - **Precio**: Precio en ARS.
     - **Condición**: Producto nuevo o usado.
     - **Cantidad Disponible**: Cantidad de unidades disponibles en stock.
     - **Reputación del Vendedor**: Reputación del vendedor en MercadoLibre.
     - **Ubicación**: Estado de la ubicación del producto.

### 4. Desnormalización y Guardado de Datos
   - Los datos obtenidos se desnormalizan y se almacenan en un archivo CSV con las columnas mencionadas previamente.

### 5. Análisis Exploratorio
   - Se realiza un análisis exploratorio utilizando **pandas**, **matplotlib** y **seaborn**:
     - **Distribución de precios**.
     - **Distribución de condiciones** (nuevo vs usado).
     - **Distribución de reputación de vendedores**.
     - **Relación entre el precio y la cantidad disponible**.

### 6. Salida al Usuario
   - El archivo CSV con los resultados es guardado en la ruta especificada por el usuario.
   - Los gráficos y análisis también son mostrados al usuario a través de la interfaz gráfica o la consola.

---

## Análisis Exploratorio

### Distribución de Precios
Se realizó un análisis de la **distribución de precios** utilizando un histograma con `seaborn`. Se mostró cómo los precios están distribuidos entre los cascos para motos.

### Distribución de Condiciones (Nuevo vs Usado)
Se utilizó un **`countplot`** para visualizar cuántos cascos son **nuevos** y cuántos son **usados**.

### Reputación de los Vendedores
Un análisis con **`countplot`** también se utilizó para visualizar la **distribución de la reputación de los vendedores**. La mayoría de los vendedores tienen **alta** o **media** reputación.

### Relación entre Precio y Cantidad Disponible
Se generó un **scatter plot** para visualizar la **relación entre precio y cantidad disponible** de los cascos para moto.

---

## Conclusión

Este proyecto permite analizar de manera eficiente la oferta de cascos para motos en MercadoLibre, comparando diferentes marcas, condiciones de los productos, y otras variables importantes. Las herramientas de visualización utilizadas brindan un análisis claro y detallado de la información obtenida, lo que puede ser útil para tomar decisiones sobre compras o entender la dinámica de precios en el mercado de cascos para motos.
