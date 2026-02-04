#!/bin/bash

# Script de Sincronización Core-Web
# Este script prepara todo para que puedas cambiar de computadora sin perder nada.

echo "🚀 Iniciando ritual de sincronización..."

# 1. Añadir todos los cambios (incluyendo STATUS.md)
git add .

# 2. Crear el commit con fecha y hora
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
git commit -m "Sincronización automática: $TIMESTAMP"

# 3. Empujar a la nube (Git)
echo "cloud_upload Subiendo cambios a Repositorio..."
git push origin main

echo "✅ ¡Listo! Todo está en la nube."
echo "🔔 RECUERDA: Espera a que Google Drive termine de sincronizar (check verde) antes de apagar."
