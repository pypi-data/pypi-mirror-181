import argparse
from argparse import RawTextHelpFormatter
from modeldeploy_proxy_controller.processors.nbprocessor import NotebookProcessor

ARGS_DESC = ""

def main():
    """Entry-point of CLI command."""
    parser = argparse.ArgumentParser(description = ARGS_DESC, formatter_class = RawTextHelpFormatter)
    general_group = parser.add_argument_group('General')
    general_group.add_argument('--nb', type=str, help='Path to source JupyterNotebook.', required=True)
    general_group.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    processor = NotebookProcessor(args.nb, {})
    processor.parse_notebook()

if __name__ == "__main__":
    main()
