# diag_nulls.py
import os
root = r"c:\Users\Royse\OneDrive\Escritorio\AS\inventario"
found = False
for dirpath, dirs, files in os.walk(root):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(dirpath, f)
            try:
                with open(path, 'rb') as fh:
                    data = fh.read()
            except Exception as e:
                print("ERROR leyendo:", path, "->", e)
                continue
            if b'\x00' in data:
                found = True
                idx = data.find(b'\x00')
                context = data[max(0, idx-40): idx+40]
                print("NUL encontrado en:", path)
                print("   offset:", idx)
                print("   contexto (bytes):", context)
                print()
if not found:
    print("No se encontraron archivos .py con bytes nulos.")