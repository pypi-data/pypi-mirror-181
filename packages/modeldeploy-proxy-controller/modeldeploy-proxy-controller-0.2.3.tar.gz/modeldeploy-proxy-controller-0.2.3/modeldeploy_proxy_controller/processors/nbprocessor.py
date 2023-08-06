import os
import re
import warnings
from typing import Any, Dict
import nbformat as nb
from modeldeploy_proxy_controller.common import utils

TRANSFORMER_NB_METADATA_KEY = 'transformer'

REQUIREMENTS_TAG = 'requirements'
PREDICT_TAG = 'predict'
FUNCTIONS_TAG = 'functions'
CVAT_INFO_TAG = 'cvat-info'
CVAT_INVOKE_TAG = 'cvat-invoke'

SUPPORTED_TAGS = [
    REQUIREMENTS_TAG,
    PREDICT_TAG,
    FUNCTIONS_TAG,
    CVAT_INFO_TAG,
    CVAT_INVOKE_TAG
]

class NotebookProcessor():
    id = "nb"

    def __init__(self, nb_path: str, **kwargs):
        """Instantiate a new NotebookProcessor.

        Args:
            nb_path: Path to source notebook
        """
        self.nb_path = os.path.expanduser(nb_path)
        self.notebook = self._read_notebook()

    def _read_notebook(self):
        if not os.path.exists(self.nb_path):
            raise ValueError("NotebookProcessor could not find a notebook at path %s" % self.nb_path)
        return nb.read(self.nb_path, as_version=nb.NO_CONVERT)

    def parse_notebook(self):
        requirements_block = list()
        predict_block = list()
        functions_block = list()
        cvat_info_block = list()
        cvat_invoke_block = list()

        for c in self.notebook.cells:
            tag = self.get_cell_transformer_tag(c.metadata)
            if not tag:
                continue

            if REQUIREMENTS_TAG == tag:
                requirements_block.append(c.source);
                continue
            elif PREDICT_TAG == tag:
                predict_block.append(c.source)
                continue
            elif FUNCTIONS_TAG == tag:
                functions_block.append(c.source)
                continue
            elif CVAT_INFO_TAG == tag:
                cvat_info_block.append(c.source)
                continue
            elif CVAT_INVOKE_TAG == tag:
                cvat_invoke_block.append(c.source)
                continue
            else:
                continue
        return {
            REQUIREMENTS_TAG: requirements_block,
            PREDICT_TAG: predict_block,
            FUNCTIONS_TAG: functions_block,
            CVAT_INFO_TAG: cvat_info_block,
            CVAT_INVOKE_TAG: cvat_invoke_block
        }

    def get_cell_transformer_tag(self, metadata):
        """Parse a notebook's cell's metadata field.

        The UI widget writes the 'transformer' key-value in metadata filed as a 
        tag. Supported tags are defined by SUPPORTED_TAGS.

        Args:
            metadata (dict): a dict containing a notebook's cell's metadata

        Returns (str): parsed tag

        """
        if TRANSFORMER_NB_METADATA_KEY not in metadata or len(metadata[TRANSFORMER_NB_METADATA_KEY]) == 0:
            return None

        if not isinstance(metadata[TRANSFORMER_NB_METADATA_KEY], str):
            raise ValueError("Tag must be string. Found tag %s of type %s" % (metadata[TRANSFORMER_NB_METADATA_KEY], type(metadata[TRANSFORMER_NB_METADATA_KEY])))

        if metadata[TRANSFORMER_NB_METADATA_KEY] not in SUPPORTED_TAGS:
            raise ValueError("Unrecognized tag: {}".format(metadata[TRANSFORMER_NB_METADATA_KEY]))

        return metadata[TRANSFORMER_NB_METADATA_KEY]

    def write_transformer_python(self, source):
        python_file_path = os.path.dirname(self.nb_path) + '/transformer.py'
        python_file = open(python_file_path, "w+")
        python_file.write(source)
        return python_file_path

    def write_requirements_file(self, requirements):
        python_file_path = os.path.dirname(self.nb_path) + '/proxy_requirements.txt'
        python_file = open(python_file_path, "w+")
        python_file.write(requirements)
        return python_file_path
