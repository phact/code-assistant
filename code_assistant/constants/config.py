import os

GENERATED_APPS_DIR = os.getcwd() + "/" + os.getenv('CA_GENERATED_APPS_DIR', 'generated_apps')
MODEL = os.getenv('CA_MODEL', 'gpt-4o-2024-08-06')
#MODEL = os.getenv('CA_MODEL', 'claude-3-5-sonnet-20240620')