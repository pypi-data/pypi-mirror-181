import asyncio
import aiohttp
import requests
import base64
from PIL import Image
from io import BytesIO
import time


async def async_stablediffusion(hsp_apikey, submit_dict=None, prompt=None, n=None, width=None, height=None, steps=None, cfg_scale=None, seed=None):
    if submit_dict is None:
        submit_dict = {}
        if prompt is not None:
            submit_dict["prompt"] = prompt
        else:
            return "Error: No se ha recibido ningún prompt."
        if n is not None:
            submit_dict["n"] = n
        if width is not None:
            submit_dict["width"] = width
        if height is not None:
            submit_dict["height"] = height
        if steps is not None:
            submit_dict["steps"] = steps
        if cfg_scale is not None:
            submit_dict["cfg_scale"] = cfg_scale
        if seed is not None:
            submit_dict["seed"] = seed
        
        submit_dict["params"] = {}
        if n is not None:
            submit_dict["params"]["n"] = n
        if width is not None:
            submit_dict["params"]["width"] = width
        if height is not None:
            submit_dict["params"]["height"] = height
        if steps is not None:
            submit_dict["params"]["steps"] = steps
        if cfg_scale is not None:
            submit_dict["params"]["cfg_scale"] = cfg_scale
        if seed is not None:
            submit_dict["params"]["seed"] = seed

    tiempo_inicial = time.time()
    url_base = 'https://stablehorde.net/api/v2/generate'
    url_generate = f'{url_base}/async'
    url_check = f'{url_base}/check'
    url_status = f'{url_base}/status'
    headers = {"apikey": hsp_apikey}
    async with aiohttp.ClientSession() as session:
        print("Se está procesando la petición, por favor, espera...")
        submit_resp = await session.post(url_generate, json=submit_dict, headers=headers)
        submit_req = await submit_resp.json()
        # Salir si el ID no está en el diccionario
        if 'id' not in submit_req:
            return "Error: No se obtiene un ID válido, comprueba tu clave API."

        req_id = submit_req['id']
        while True:
            chk_resp = await session.get(f'{url_check}/{req_id}')
            chk_req = await chk_resp.json()

            # Salir si el campo 'done' no está en el diccionario
            if 'done' not in chk_req:
                return "Error: No se obtiene respuesta válida, comprueba tu clave API."

            is_done = chk_req['done']
            if is_done:
                break
            await asyncio.sleep(4)

        status_resp = await session.get(f'{url_status}/{req_id}')
        status_req = await status_resp.json()

        # Salir si el campo 'faulted' no está en el diccionario 
        if 'faulted' not in status_req:
            return "Error: No se puede obtener el estado del trabajo, comprueba tu clave API."

        if status_req['faulted']: # Si el campo 'faulted' es True, el trabajo ha fallado
            return "Error: El trabajo ha fallado, comprueba tu clave API."

        results = status_req['generations']
        generated_images = []
        tiempo_final = time.time()
        for result in results:
            image = result['img']
            image = image.split(',')[0]
            # Usa Pillow para cargar la imagen directamente desde la cadena codificada en base64 (se reciben codificadas en base64 en formato webp)
            image = Image.open(BytesIO(base64.b64decode(image)))
            generated_images.append(image)
        if len(results) == 1:
            print(f"Se ha generado 1 imagen en {int(tiempo_final - tiempo_inicial)} segundos.")
        else:
            print(f"Se han generado {len(results)} imágenes en {int(tiempo_final - tiempo_inicial)} segundos.")
        return generated_images


def stablediffusion(hsp_apikey,submit_dict=None, prompt=None, n=None, width=None, height=None, steps=None, cfg_scale=None, seed=None):
    if submit_dict is None:
        submit_dict = {}
        if prompt is not None:
            submit_dict["prompt"] = prompt
        else:
            return "Error: No se ha recibido ningún prompt."
        if n is not None:
            submit_dict["n"] = n
        if width is not None:
            submit_dict["width"] = width
        if height is not None:
            submit_dict["height"] = height
        if steps is not None:
            submit_dict["steps"] = steps
        if cfg_scale is not None:
            submit_dict["cfg_scale"] = cfg_scale
        if seed is not None:
            submit_dict["seed"] = seed

        submit_dict["params"] = {}
        if n is not None:
            submit_dict["params"]["n"] = n
        if width is not None:
            submit_dict["params"]["width"] = width
        if height is not None:
            submit_dict["params"]["height"] = height
        if steps is not None:
            submit_dict["params"]["steps"] = steps
        if cfg_scale is not None:
            submit_dict["params"]["cfg_scale"] = cfg_scale
        if seed is not None:
            submit_dict["params"]["seed"] = seed

    tiempo_inicial = time.time()
    url_base = 'https://stablehorde.net/api/v2/generate'
    url_generate = f'{url_base}/async'
    url_check = f'{url_base}/check'
    url_status = f'{url_base}/status'
    headers = {"apikey": hsp_apikey}
    with requests.Session() as session:
        print("Se está procesando la petición, por favor, espera...")
        submit_resp = session.post(url_generate, json=submit_dict, headers=headers)
        submit_req = submit_resp.json()
        # Salir si el ID no está en el diccionario
        if 'id' not in submit_req:
            return "Error: No se obtiene un ID válido, comprueba tu clave API."

        req_id = submit_req['id']
        while True:
            chk_resp = session.get(f'{url_check}/{req_id}')
            chk_req = chk_resp.json()

            # Salir si el campo 'done' no está en el diccionario
            if 'done' not in chk_req:
                return "Error: No se obtiene respuesta válida, comprueba tu clave API."

            is_done = chk_req['done']
            if is_done:
                break
            time.sleep(4)

        status_resp = session.get(f'{url_status}/{req_id}')
        status_req = status_resp.json()

        # Salir si el campo 'faulted' no está en el diccionario 
        if 'faulted' not in status_req:
            return "Error: No se puede obtener el estado del trabajo, comprueba tu clave API."

        if status_req['faulted']: # Si el campo 'faulted' es True, el trabajo ha fallado
            return "Error: El trabajo ha fallado, comprueba tu clave API."

        results = status_req['generations']
        generated_images = []
        tiempo_final = time.time()
        for result in results:
            image = result['img']
            image = image.split(',')[0]
            # Usa Pillow para cargar la imagen directamente desde la cadena codificada en base64 (se reciben codificadas en base64 en formato webp)
            image = Image.open(BytesIO(base64.b64decode(image)))
            generated_images.append(image)
        if len(results) == 1:
            print(f"Se ha generado 1 imagen en {int(tiempo_final - tiempo_inicial)} segundos.")
        else:
            print(f"Se han generado {len(results)} imágenes en {int(tiempo_final - tiempo_inicial)} segundos.")
        return generated_images