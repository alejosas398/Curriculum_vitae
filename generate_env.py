#!/usr/bin/env python
"""
Script para generar variables de entorno para Render Deploy
Uso: python generate_env.py
"""

import secrets
import os
from pathlib import Path

def generate_secret_key():
    """Genera una SECRET_KEY segura para Django"""
    return 'django-' + secrets.token_urlsafe(50)

def main():
    print("\n" + "="*70)
    print("GENERADOR DE VARIABLES DE ENTORNO - RENDER DEPLOY")
    print("="*70 + "\n")
    
    # Generar SECRET_KEY
    secret_key = generate_secret_key()
    print("1. SECRET_KEY (Generada automáticamente):")
    print(f"   {secret_key}\n")
    
    # Pedir dominio
    print("2. ALLOWED_HOSTS:")
    domain = input("   Ingresa tu dominio Render (ej: hoja-de-vida.onrender.com): ").strip()
    if not domain:
        domain = "hoja-de-vida.onrender.com"
    print(f"   Valor: {domain}\n")
    
    # Pedir Azure Storage
    print("3. AZURE_STORAGE_CONNECTION_STRING:")
    azure_conn = input("   Pega tu connection string de Azure: ").strip()
    if not azure_conn:
        print("   ⚠️  IMPORTANTE: Necesitas agregar esto manualmente en Render\n")
    
    # Container
    print("4. AZURE_CONTAINER_NAME:")
    container = input("   Nombre del container Azure (por defecto: cursos): ").strip()
    if not container:
        container = "cursos"
    print(f"   Valor: {container}\n")
    
    # Crear archivo .env.render
    env_content = f"""# Variables para Render Deploy
SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS={domain}

AZURE_STORAGE_CONNECTION_STRING={azure_conn}
AZURE_CONTAINER_NAME={container}

# Esto se genera automáticamente en Render si creas PostgreSQL
# DATABASE_URL=postgresql://usuario:contraseña@host:5432/nombre_db
"""
    
    env_file = Path(".env.render")
    env_file.write_text(env_content)
    
    print("\n" + "="*70)
    print("✅ Archivo creado: .env.render")
    print("="*70)
    print("\nCopia estas variables en Render Dashboard → Environment:")
    print(f"""
SECRET_KEY={secret_key}
DEBUG=False
ALLOWED_HOSTS={domain}
AZURE_STORAGE_CONNECTION_STRING={azure_conn}
AZURE_CONTAINER_NAME={container}
    """)
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
