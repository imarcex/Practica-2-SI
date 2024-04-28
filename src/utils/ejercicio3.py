import requests

API = 'https://cve.circl.lu/api/last'

def __obtener_ultimas_vulnerabilidades(num_vulnerabilidades=10):
    url = API
    parametros = {'range': num_vulnerabilidades}
    
    try:
        respuesta = requests.get(url, params=parametros)
        if respuesta.status_code == 200:
            data = respuesta.json()
            return list(data)[:num_vulnerabilidades]
        else:
            print("Error al obtener las vulnerabilidades. Código de estado:", respuesta.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)
        return None

def __ultimas_vulns(vulnerabilidades):
    res = []
    if vulnerabilidades:
        content = {}
        for vuln in vulnerabilidades:
            content["CVE-ID"] = vuln.get("id")
            content["Descripción"] = vuln.get("summary")
            content["Publicado"] = vuln.get("Published")
            res.append(content)
    return res

def get_latest_vulns():
    ultimas_vulnerabilidades = __obtener_ultimas_vulnerabilidades()
    return __ultimas_vulns(ultimas_vulnerabilidades)
