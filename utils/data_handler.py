import json
import os
from typing import Any, List, Dict

def carregar_dades(arxiu: str) -> List[Dict[str, Any]]:
    try:
        if os.path.exists(arxiu):
            with open(arxiu, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Si el fitxer no existeix, creará el directori necessari
            os.makedirs(os.path.dirname(arxiu), exist_ok=True)
            return []
    except json.JSONDecodeError:
        print(f"Error llegint {arxiu}. Inicialitzant amb dades buides.")
        return []
    except Exception as e:
        print(f"Error inesperat llegint {arxiu}: {e}")
        return []

def guardar_dades(arxiu: str, dades: List[Dict[str, Any]]) -> bool:
    try:
        # Crear directori si no existeix
        os.makedirs(os.path.dirname(arxiu), exist_ok=True)
        
        with open(arxiu, 'w', encoding='utf-8') as f:
            json.dump(dades, f, ensure_ascii=False, indent=2)
        return True
    
    except Exception as e:
        print(f"Error guardant {arxiu}: {e}")
        return False