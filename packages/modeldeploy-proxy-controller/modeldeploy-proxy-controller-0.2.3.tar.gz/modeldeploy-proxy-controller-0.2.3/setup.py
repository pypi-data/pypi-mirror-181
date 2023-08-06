from setuptools import setup

setup(
    name = 'modeldeploy-proxy-controller',
    version = '0.2.3',
    description = 'The JupyterLab backend component for modeldeploy-proxy.',
    author = 'ever cheng',
    author_email = 'ever_cheng@asus.com',
    license = 'Apache License Version 2.0',
    packages = [
        'modeldeploy_proxy_controller',
        'modeldeploy_proxy_controller.res',
        'modeldeploy_proxy_controller.common',
        'modeldeploy_proxy_controller.rpc',
        'modeldeploy_proxy_controller.processors'
    ],
    install_requires = [
        'IPython >= 7.6.0',
        'jupyter-client >=5.3.4, <7.0.0',
        'jupyter-core >= 4.6.0',
        'nbformat',
        'ipykernel >= 5.1.4',
        'notebook >= 6.0.0',
        'packaging > 20',
        'Flask >= 2.0.0',
        'prometheus-client >= 0.15.0'
    ],
    extras_require = {
        'dev': [
            'pytest',
            'pytest-clarity',
            'testfixtures',
            'pytest-cov',
        ]
    },
    entry_points = {
        'console_scripts': [
            'modeldeploy_proxy_controller=src.cli:main'
        ]
    },
    python_requires = '>=3.7.0',
    include_package_data = True,
    zip_safe = False
)
