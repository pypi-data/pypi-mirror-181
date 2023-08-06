import os
import shutil
import logging
from modeldeploy_proxy_controller.processors.nbprocessor import NotebookProcessor, REQUIREMENTS_TAG, PREDICT_TAG, FUNCTIONS_TAG, CVAT_INFO_TAG, CVAT_INVOKE_TAG
from modeldeploy_proxy_controller.rpc.errors import RPCInternalError
import requests

def parse_notebook(request, source_notebook_path):
    request.log.debug("parse_notebook with path({})...".format(source_notebook_path))

    NEW_LINES = '\n\n';
    processor = NotebookProcessor(source_notebook_path)
    blocks = processor.parse_notebook()
    source = ''

    requirements = ''
    request.log.debug("Requirements({})...".format(len(blocks[REQUIREMENTS_TAG])))
    if len(blocks[REQUIREMENTS_TAG]) > 1:
        raise RuntimeError("Requirements tag must be at most 1!")
    elif len(blocks[REQUIREMENTS_TAG]):
        if requirements:
            requirements = '{}{}{}'.format(source, NEW_LINES, blocks[REQUIREMENTS_TAG][0])
        else:
            requirements = '{}'.format(blocks[REQUIREMENTS_TAG][0])

    if len(blocks[PREDICT_TAG]) > 1:
        raise RuntimeError("Predict tag must be at most 1!")
    elif len(blocks[PREDICT_TAG]):
        if source:
            source = '{}{}{}'.format(source, NEW_LINES, blocks[PREDICT_TAG][0])
        else:
            source = '{}'.format(blocks[PREDICT_TAG][0])

    if len(blocks[CVAT_INFO_TAG]) > 1:
        raise RuntimeError("CVAT info tag must be at most 1!")
    elif len(blocks[CVAT_INFO_TAG]):
        if source:
            source = '{}{}{}'.format(source, NEW_LINES, blocks[CVAT_INFO_TAG][0])
        else:
            source = '{}'.format(blocks[CVAT_INFO_TAG][0])

    if len(blocks[CVAT_INVOKE_TAG]) > 1:
        raise RuntimeError("CVAT invoke tag must be at most 1!")
    elif len(blocks[CVAT_INVOKE_TAG]):
        if source:
            source = '{}{}{}'.format(source, NEW_LINES, blocks[CVAT_INVOKE_TAG][0])
        else:
            source = '{}'.format(blocks[CVAT_INVOKE_TAG][0])

    if len(blocks[FUNCTIONS_TAG]):
        for function in blocks[FUNCTIONS_TAG]:
            if source:
                source = '{}{}{}'.format(source, NEW_LINES, function)
            else:
                source = '{}'.format(function)

    request.log.debug("Write contents...")
    request.log.debug(requirements)
    requirements_path = processor.write_requirements_file(requirements);
    transformer_path = processor.write_transformer_python(source);

    request.log.debug("requirements_path({})...".format(requirements_path))
    request.log.debug("transformer_path({})...".format(transformer_path))

    return {
        "requirements_path": requirements_path,
        "transformer_path": transformer_path
    }
