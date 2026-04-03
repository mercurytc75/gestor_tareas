#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resumen del proyecto en consola. Ejecutar: python info.py"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent

print("""
╔══════════════════════════════════════════════════════════════╗
║              Gestor de Tareas · estructura local             ║
╚══════════════════════════════════════════════════════════════╝
""")

counts = {'py': 0, 'html': 0, 'css': 0, 'js': 0}
for p in ROOT.rglob('*'):
    if p.is_file() and 'venv' not in p.parts and '__pycache__' not in p.parts:
        suf = p.suffix.lower()
        if suf == '.py':
            counts['py'] += 1
        elif suf == '.html':
            counts['html'] += 1
        elif suf == '.css':
            counts['css'] += 1
        elif suf == '.js':
            counts['js'] += 1

print('Archivos:', ', '.join(f'{k}: {v}' for k, v in counts.items() if v))
print('\nInicio rápido:')
print('  pip install -r requirements.txt')
print('  python run.py')
print('  http://localhost:5000\n')
