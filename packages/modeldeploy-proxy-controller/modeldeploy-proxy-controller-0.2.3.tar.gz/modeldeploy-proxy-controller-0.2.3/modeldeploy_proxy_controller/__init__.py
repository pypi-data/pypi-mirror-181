from .processors import NotebookProcessor
from modeldeploy_proxy_controller.common import logutils

logutils.get_or_create_logger(module=__name__, name="controller")
del logutils
