"""Proyecto Integrador: Máquina de Snacks"""

import os


#
# CLASE SNACK
#
class Snack:
    contador_snack = 0

    def __init__(self, nombre: str, precio: float):
        Snack.contador_snack += 1
        self.id_snack = Snack.contador_snack
        self.nombre = nombre
        self.precio = precio

    def __str__(self):
        return f"ID: {self.id_snack} | Snack: {self.nombre} | Precio: ${self.precio:.2f}"

    def escribir_snack(self):
        return f"{self.id_snack},{self.nombre},{self.precio}"


#
# CLASE SERVICIO DE SNACKS (MANEJO DE ARCHIVOS)
#
class ServicioSnacks:
    NOMBRE_ARCHIVO = "snacks.txt"

    def __init__(self):
        self.snacks = []
        if os.path.isfile(self.NOMBRE_ARCHIVO):
            self.snacks = self.obtener_snacks()
        else:
            self.cargar_snacks_iniciales()

    def obtener_snacks(self):
        snacks = []
        try:
            with open(self.NOMBRE_ARCHIVO, "r", encoding="utf8") as archivo:
                for linea in archivo:
                    id_snack, nombre, precio = linea.strip().split(",")
                    snack = Snack(nombre, float(precio))
                    snacks.append(snack)
        except Exception as e:
            print(f"Error al leer el archivo de snacks: {e}")
        return snacks

    def cargar_snacks_iniciales(self):
        snacks_iniciales = [
            Snack("Papas", 30.0),
            Snack("Refresco", 50.0),
            Snack("Sandwich", 120.0)
        ]
        self.snacks.extend(snacks_iniciales)
        self.guardar_snacks_archivo(snacks_iniciales)

    def guardar_snacks_archivo(self, snacks):
        try:
            with open(self.NOMBRE_ARCHIVO, "a", encoding="utf8") as archivo:
                for snack in snacks:
                    archivo.write(f"{snack.escribir_snack()}\n")
        except Exception as e:
            print(f"Error al guardar en el archivo: {e}")

    def agregar_snack(self, snack: Snack):
        self.snacks.append(snack)
        self.guardar_snacks_archivo([snack])

    def mostrar_snacks(self):
        print("\n--- SNACKS DISPONIBLES EN EL INVENTARIO ---")
        for snack in self.snacks:
            print(snack)

    def get_snacks(self):
        return self.snacks


#
# CLASE MÁQUINA DE SNACKS (CONTROL DE FLUJO Y TICKET)
#
class MaquinaSnacks:
    def __init__(self):
        self.servicio_snacks = ServicioSnacks()
        self.productos_comprados = []

    def ejecutar_maquina(self):
        salir = False
        print("❄️ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ❄️")
        print("      BIENVENIDO A LA MÁQUINA DE SNACKS   ")
        print("❄️ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ❄️")

        while not salir:
            try:
                opcion = self.mostrar_menu()
                salir = self.procesar_opcion(opcion)
            except Exception as e:
                print(f"Ocurrió un error inesperado: {e}")

    def mostrar_menu(self):
        print("""
        Menú Principal:
        1. Comprar Snack
        2. Mostrar Ticket
        3. Agregar Nuevo Snack al Inventario
        4. Listar Inventario
        5. Salir
        """)
        return int(input("Elige una opción (1-5): "))

    def procesar_opcion(self, opcion):
        if opcion == 1:
            self.comprar_snack()
        elif opcion == 2:
            self.mostrar_ticket()
        elif opcion == 3:
            self.agregar_nuevo_snack()
        elif opcion == 4:
            self.servicio_snacks.mostrar_snacks()
        elif opcion == 5:
            print("¡Gracias por tu compra, regresa pronto!")
            return True
        else:
            print("Opción no válida. Introduce un número entre 1 y 5.")
        return False

    def comprar_snack(self):
        self.servicio_snacks.mostrar_snacks()
        id_ingresado = int(input("\nIngresa el ID del snack que deseas comprar: "))
        lista_snacks = self.servicio_snacks.get_snacks()

        # Búsqueda con next() optimizada
        snack_encontrado = next((s for s in lista_snacks if s.id_snack == id_ingresado), None)

        if snack_encontrado:
            self.productos_comprados.append(snack_encontrado)
            print(f"✅ ¡Agregado al carrito!: {snack_encontrado.nombre} (${snack_encontrado.precio:.2f})")
        else:
            print(f"❌ No se encontró un snack con el ID: {id_ingresado}")

    def mostrar_ticket(self):
        if not self.productos_comprados:
            print("\n🛒 El carrito está vacío. No hay compras registradas.")
            return

        total = sum(s.precio for s in self.productos_comprados)
        print("\n" + "~" * 40)
        print("            TICKET DE VENTA             ")
        print("~" * 40)
        for item in self.productos_comprados:
            print(f"  - {item.nombre} ................. ${item.precio:.2f}")
        print("-" * 40)
        print(f"  TOTAL A PAGAR: ................ ${total:.2f}")
        print("~" * 40)

    def agregar_nuevo_snack(self):
        nombre = input("Ingresa el nombre del nuevo snack: ")
        precio = float(input("Ingresa el precio del nuevo snack: $"))
        nuevo_snack = Snack(nombre, precio)
        self.servicio_snacks.agregar_snack(nuevo_snack)
        print(f"✨ ¡Snack '{nombre}' agregado exitosamente al inventario!")


if __name__ == "__main__":
    app_snacks = MaquinaSnacks()
    app_snacks.ejecutar_maquina()