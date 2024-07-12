# Archivo: vlan.py

def verificar_vlan(vlan_id):
    """
    Verifica si el número de VLAN ingresado corresponde a una VLAN del rango normal o extendido.
    
    Args:
    vlan_id (int): Número de VLAN.
    
    Returns:
    str: Mensaje indicando el tipo de VLAN.
    """
    if 1 <= vlan_id <= 1005:
        return "La VLAN {} corresponde a una VLAN del rango normal.".format(vlan_id)
    elif 1006 <= vlan_id <= 4094:
        return "La VLAN {} corresponde a una VLAN del rango extendido.".format(vlan_id)
    else:
        return "El número de VLAN {} no es válido. Debe estar entre 1 y 4094.".format(vlan_id)

def main():
    try:
        vlan_id = int(input("Ingrese el número de VLAN: "))
        mensaje = verificar_vlan(vlan_id)
        print(mensaje)
    except ValueError:
        print("Por favor, ingrese un número entero válido.")

if __name__ == "__main__":
    main()
