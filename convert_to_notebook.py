"""
Script mejorado para convertir 3_v3.py a formato .ipynb para Google Colab
"""
import json
import re

def py_to_notebook(py_file, ipynb_file):
    """Convierte un archivo .py a .ipynb respetando la estructura"""
    
    with open(py_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cells = []
    current_cell = []
    current_type = "code"
    in_markdown = False
    
    for line in lines:
        # Detectar inicio/fin de markdown con """
        if line.strip().startswith('"""'):
            if not in_markdown:
                # Guardar celda de código anterior si existe
                if current_cell:
                    cells.append({
                        "cell_type": "code",
                        "execution_count": None,
                        "metadata": {},
                        "outputs": [],
                        "source": current_cell
                    })
                    current_cell = []
                in_markdown = True
                # Capturar el texto del markdown (sin las comillas)
                markdown_text = line.strip()[3:].strip()
                if markdown_text:
                    current_cell.append(markdown_text + "\n")
            else:
                # Fin del markdown
                if current_cell:
                    cells.append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": current_cell
                    })
                    current_cell = []
                in_markdown = False
            continue
        
        # Si estamos en markdown, agregar la línea
        if in_markdown:
            current_cell.append(line)
        else:
            # Es código
            # Ignorar líneas que empiezan con # -*- coding
            if line.strip().startswith('# -*- coding'):
                continue
            
            # Si encontramos una línea en blanco y ya hay contenido, crear nueva celda
            if line.strip() == '' and current_cell and len(current_cell) > 3:
                # Crear celda de código
                cells.append({
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {},
                    "outputs": [],
                    "source": current_cell
                })
                current_cell = []
            elif line.strip() != '' or current_cell:  # Agregar línea si no está vacía o ya hay contenido
                current_cell.append(line)
    
    # Agregar última celda si existe
    if current_cell:
        cell_type = "markdown" if in_markdown else "code"
        cells.append({
            "cell_type": cell_type,
            "execution_count": None if cell_type == "code" else None,
            "metadata": {},
            "outputs": [] if cell_type == "code" else None,
            "source": current_cell
        })
    
    # Agregar celda inicial para crear carpeta models
    cells.insert(0, {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Configuración para Google Colab\n",
            "import os\n",
            "os.makedirs('models', exist_ok=True)\n",
            "print('✅ Carpeta models/ creada')\n"
        ]
    })
    
    # Crear la estructura del notebook
    notebook = {
        "cells": cells,
        "metadata": {
            "colab": {
                "name": "3_v3.ipynb",
                "provenance": []
            },
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.10.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 0
    }
    
    # Guardar el notebook
    with open(ipynb_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Convertido: {py_file} -> {ipynb_file}")
    print(f"   Total de celdas: {len(cells)}")

if __name__ == "__main__":
    py_to_notebook("3_v3.py", "3_v3.ipynb")
