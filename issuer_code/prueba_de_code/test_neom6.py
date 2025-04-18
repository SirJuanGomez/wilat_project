import gps_module 

try:
    gps = gps_module.NE06M()
    try:
        gps.update()
        lat = gps.latitude
        lon = gps.longitude
        print(f"Latitud: {lat}, Longitud: {lon}")
    except Exception as e:
        print(f"Error en la lectura {e}")
except Exception as e:
    print(f"Error al iniciar el modulo {e}")

