import json
import sys

try:
    with open('webServerApiSettings.json', 'r') as f:
        data = json.load(f)
        print(data['webServerPort'])
except Exception as e:
    print(f"Erro ao ler arquivo: {e}", file=sys.stderr)
    print(8080)