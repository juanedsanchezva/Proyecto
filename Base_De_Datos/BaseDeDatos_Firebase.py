import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("Base_De_Datos/base-de-datos-proyecto-8b344-firebase-adminsdk-fbsvc-87b7b737f0.json")
firebase_admin.initialize_app(cred, {
    #"databaseURL": "https://testpoo-59c96-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
    "databaseURL": "https://base-de-datos-proyecto-8b344-default-rtdb.firebaseio.com"  # Cambia con tu URL de la base de datos
})

# Referencia al nodo en la base de datos
ref = db.reference("nodo1")  # Cambia "nodo_principal" por tu ruta

# Escribe datos en tiempo real
ref.set({
    "mensaje": "Ya tenemos base de datos team",
    "activo": True
    
})

# Escucha cambios en tiempo real
def escuchar_eventos(event):
    print(f"Cambio detectado: {event.data}")

ref.listen(escuchar_eventos)
