import logging
import os

from modeldeploy_proxy_controller.common import logutils

LOG_DIR = os.getenv("HOME", ".")
LOG_BASENAME = "modeldeploy-proxy-controller.log"
LOG_FILE = os.path.join(LOG_DIR, LOG_BASENAME)

FMT_PREFIX = "%(asctime)s %(module)s:%(lineno)d [%(levelname)s] "
RPC_FMT_EXTRAS = "[TID=%(trans_id)s] [%(nb_path)s] "


def create_adapter(logger, trans_id = None, nb_path = None):
    """Create log Adapter."""
    extras = {
        "trans_id": trans_id or "",
        "nb_path": os.path.realpath(nb_path) if nb_path else ""
    }
    return logging.LoggerAdapter(logger, extras)


def setup_logging(request):
    """Configure logging."""
    # Set up root logger
    fmt = FMT_PREFIX + "%(message)s"
    _root_log = logutils.get_or_create_logger("", fmt = fmt, file_level = logging.INFO, log_path = LOG_FILE)
    _root_log.setLevel(logging.INFO)

    fmt = FMT_PREFIX + RPC_FMT_EXTRAS + "%(message)s"
    logutils.get_or_create_logger("modeldeploy_proxy_controller.rpc", fmt = fmt, log_path = LOG_FILE)

    # mute other loggers
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3').setLevel(logging.INFO)
