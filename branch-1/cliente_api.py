"""
Cliente HTTP para consumir la API de Ticketing
Demuestra la relación 1:N entre Ticket e Incidentes
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def print_response(title: str, response: requests.Response):
    """Imprime la respuesta de forma legible."""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def crear_ticket_con_incidentes():
    """Ejemplo 1: Crear un ticket con múltiples incidentes."""
    print("\nTEST 1: Crear ticket con múltiples incidentes (1:N)")
    
    data = {
        "cliente_id": 1,
        "servicio_id": 1,
        "equipo_id": 1,
        "empleado_id": 1,
        "incidentes": [
            {
                "descripcion": "Mouse no responde",
                "categoria": "Hardware",
                "prioridad": "Media"
            },
            {
                "descripcion": "Disco duro hace ruido",
                "categoria": "Hardware",
                "prioridad": "Alta"
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/tickets", json=data)
    print_response("POST /tickets - Crear ticket con incidentes", response)
    
    return response.json().get("id")


def obtener_ticket_con_incidentes(ticket_id: int):
    """Ejemplo 2: Obtener un ticket con sus incidentes."""
    print("\nTEST 2: Obtener ticket con sus incidentes")
    
    response = requests.get(f"{BASE_URL}/tickets/{ticket_id}?incluir_incidentes=true")
    print_response(f"GET /tickets/{ticket_id}?incluir_incidentes=true", response)


def agregar_incidente_a_ticket(ticket_id: int):
    """Ejemplo 3: Agregar un nuevo incidente a un ticket existente."""
    print("\nTEST 3: Agregar incidente a ticket existente")
    
    data = {
        "descripcion": "Ventilador hace ruido excesivo",
        "categoria": "Hardware",
        "prioridad": "Baja"
    }
    
    response = requests.post(f"{BASE_URL}/tickets/{ticket_id}/incidentes", json=data)
    print_response(f"POST /tickets/{ticket_id}/incidentes", response)


def listar_todos_los_tickets():
    """Ejemplo 4: Listar todos los tickets."""
    print("\TEST 4: Listar todos los tickets")
    
    response = requests.get(f"{BASE_URL}/tickets")
    print_response("GET /tickets", response)


def listar_tickets_con_incidentes():
    """Ejemplo 5: Listar tickets incluyendo sus incidentes."""
    print("\nTEST 5: Listar tickets con incidentes incluidos")
    
    response = requests.get(f"{BASE_URL}/tickets?incluir_incidentes=true")
    print_response("GET /tickets?incluir_incidentes=true", response)


def crear_incidente_directo():
    """Ejemplo 6: Crear un incidente directamente asociado a un ticket."""
    print("\nTEST 6: Crear incidente directamente")
    
    data = {
        "descripcion": "Cable de red dañado",
        "categoria": "Red",
        "prioridad": "Media",
        "ticket_id": 1
    }
    
    response = requests.post(f"{BASE_URL}/incidentes", json=data)
    print_response("POST /incidentes", response)


def listar_incidentes_por_ticket(ticket_id: int):
    """Ejemplo 7: Listar incidentes de un ticket específico."""
    print("\nTEST 7: Listar incidentes de un ticket")
    
    response = requests.get(f"{BASE_URL}/incidentes/ticket/{ticket_id}")
    print_response(f"GET /incidentes/ticket/{ticket_id}", response)


def filtrar_incidentes_por_categoria():
    """Ejemplo 8: Filtrar incidentes por categoría."""
    print("\nTEST 8: Filtrar incidentes por categoría")
    
    response = requests.get(f"{BASE_URL}/incidentes/filtrar/categoria?categoria=Hardware")
    print_response("GET /incidentes/filtrar/categoria?categoria=Hardware", response)


def cerrar_ticket(ticket_id: int):
    """Ejemplo 9: Cerrar un ticket."""
    print("\nTEST 9: Cerrar ticket")
    
    response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/cerrar")
    print_response(f"PUT /tickets/{ticket_id}/cerrar", response)


def reabrir_ticket(ticket_id: int):
    """Ejemplo 10: Reabrir un ticket."""
    print("\nTEST 10: Reabrir ticket")
    
    response = requests.put(f"{BASE_URL}/tickets/{ticket_id}/reabrir")
    print_response(f"PUT /tickets/{ticket_id}/reabrir", response)


def filtrar_tickets_por_estado():
    """Ejemplo 11: Filtrar tickets por estado."""
    print("\nTEST 11: Filtrar tickets por estado")
    
    response = requests.get(f"{BASE_URL}/tickets/filtrar/estado?estado=Abierto")
    print_response("GET /tickets/filtrar/estado?estado=Abierto", response)


def health_check():
    """Verifica que la API esté funcionando."""
    print("\nTEST 0: Health Check")
    
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", response)


def main():
    """Ejecuta todos los tests del cliente."""
    print("=" * 60)
    print("Cliente HTTP - Probando API de Ticketing")
    print("=" * 60)
    print(f"Base URL: {BASE_URL}")
    
    try:
        # Test 0: Verificar que la API esté funcionando
        health_check()
        
        # Test 1: Crear ticket con múltiples incidentes
        ticket_id = crear_ticket_con_incidentes()
        
        if not ticket_id:
            print("\nError: No se pudo crear el ticket")
            return
        
        # Test 2: Obtener ticket con incidentes
        obtener_ticket_con_incidentes(ticket_id)
        
        # Test 3: Agregar incidente al ticket
        agregar_incidente_a_ticket(ticket_id)
        
        # Test 4: Listar todos los tickets
        listar_todos_los_tickets()
        
        # Test 5: Listar tickets con incidentes
        listar_tickets_con_incidentes()
        
        # Test 6: Crear incidente directamente
        crear_incidente_directo()
        
        # Test 7: Listar incidentes de un ticket
        listar_incidentes_por_ticket(ticket_id)
        
        # Test 8: Filtrar incidentes por categoría
        filtrar_incidentes_por_categoria()
        
        # Test 9: Cerrar ticket
        cerrar_ticket(ticket_id)
        
        # Test 10: Reabrir ticket
        reabrir_ticket(ticket_id)
        
        # Test 11: Filtrar tickets por estado
        filtrar_tickets_por_estado()
        
        print("\n" + "=" * 60)
        print("Todos los tests completados exitosamente")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\nError: No se pudo conectar a la API")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python app.py")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()