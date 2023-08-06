import os
import requests
from modeldeploy_proxy_controller.rpc.nb import parse_notebook
import importlib.resources as resources
from modeldeploy_proxy_controller import res

API_HOST_URL = os.environ.get("API_HOST_URL", "")
API_VERSION = os.environ.get("API_VERSION", "v1")
PROXY_API_PREFIX = "{}/api/{}/".format(API_HOST_URL, API_VERSION)
TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)

def revise_proxy_api_url(request, proxy_url):
    request.log.debug("revise_proxy_api_url")

    if not proxy_url:
        raise RuntimeError("Proxy URL should not be empty!")

    global PROXY_API_PREFIX
    global TRANSFORMER_UPLOAD_URL
    global REQUIREMENTS_UPLOAD_URL
    global STATUS_URL

    PROXY_API_PREFIX = "{}/api/{}/".format(proxy_url, API_VERSION)
    TRANSFORMER_UPLOAD_URL = "{}/transformer/upload".format(PROXY_API_PREFIX)
    REQUIREMENTS_UPLOAD_URL = "{}/requirements/upload".format(PROXY_API_PREFIX)
    STATUS_URL = "{}/proxy/health/status".format(PROXY_API_PREFIX)

def apply(request, proxy_url, source_notebook_path):
    request.log.debug("apply transformer({}) content to proxy({})...".format(source_notebook_path, proxy_url))

    if proxy_url:
        revise_proxy_api_url(request, proxy_url)

    paths = parse_notebook(request, source_notebook_path)

    if paths.get('requirements_path', None):
        files = {'file': open(paths.get('requirements_path'), 'rb')}
        request.log.debug("POST {} with files...".format(REQUIREMENTS_UPLOAD_URL))
        response = requests.post(REQUIREMENTS_UPLOAD_URL, files = files)
        request.log.debug(response.json())

    if paths.get('transformer_path', None):
        files = {'file': open(paths.get('transformer_path'), 'rb')}
        request.log.debug("POST {} with files...".format(TRANSFORMER_UPLOAD_URL))
        response = requests.post(TRANSFORMER_UPLOAD_URL, files = files)
        request.log.debug(response.json())

def reset(request, proxy_url, source_notebook_path):
    request.log.debug("reset transformer({}) content to proxy({})...".format(source_notebook_path, proxy_url))
    text = resources.read_text(res, 'transformer.ipynb', encoding = 'utf8', errors = 'strict')
    request.log.debug(text)
    nb_file = open(source_notebook_path, "w")
    nb_file.write(text)
    nb_file.close()

def info(request):
    request.log.debug("info")
    cwd = os.getcwd()
    proxy_url = ""
    nb_paths = []
    PROXY_URL_FILE_NAME = ".proxy"
    TRANSFORMER_NB_FILE_NAME = "transformer.ipynb"
    try:
        for root, dirs, files in os.walk(cwd):
            if PROXY_URL_FILE_NAME in files:
                path = os.path.join(root, PROXY_URL_FILE_NAME)
                proxy_url = open(path).readline().strip()
                break
    except Exception:
        pass

    request.log.debug("proxy_url: {}".format(proxy_url))
    try:
        for root, dirs, files in os.walk(cwd):
            if TRANSFORMER_NB_FILE_NAME in files:
                nb_paths.append(os.path.join(root, TRANSFORMER_NB_FILE_NAME))
    except Exception:
        pass
    request.log.debug("nb_paths: {}".format(nb_paths))

    UNAVAILABLE = "Unavailable"
    info = {
        "nb_paths": nb_paths,
        "proxy_url": proxy_url,
        "proxy_status": UNAVAILABLE
    }
    if proxy_url:
        revise_proxy_api_url(request, proxy_url)

        try:
            response = requests.get(STATUS_URL)
            if response.status_code == 200:
                info['proxy_status'] = response.json().get("status", UNAVAILABLE)
        except requests.exceptions.RequestException as e:
            request.log.warn(str(e))
    return info
