class Radix_sort:
    def __init__(self, lista):
        # Inicializa la clase con una lista de números.
        # La lista es almacenada como un atributo privado.
        self.__lista = lista

    def ordenar(self):
        # Determina la cantidad máxima de dígitos en los números de la lista.
        # Esto se hace buscando el número máximo de dígitos en cada número convertido a cadena.
        cantidad_de_digitos = 0
        for elemento in self.__lista:
            digitos = len(str(elemento))
            if digitos > cantidad_de_digitos:
                cantidad_de_digitos = digitos


        # Normaliza la lista de números convirtiéndolos a cadenas y rellenándolos con ceros a la izquierda
        # para que todos tengan la misma longitud en términos de dígitos.
        # Por ejemplo, el número 5 en una lista con 3 dígitos se convertirá en '005'.
        lista_normalizada = [str(elemento).zfill(cantidad_de_digitos) for elemento in self.__lista]

        # Itera desde el dígito menos significativo hasta el más significativo.
        # Esto se hace en orden inverso (de derecha a izquierda) para asegurar que el ordenamiento
        # por cada dígito se base en el ordenamiento por el dígito menos significativo primero.
        # El rango (cantidad_de_digitos - 1, -1, -1) se usa para recorrer las posiciones de los dígitos
        # comenzando desde el último (menos significativo) hasta el primero (más significativo).
        # - El primer argumento (cantidad_de_digitos - 1) es la posición inicial (último dígito).
        # - El segundo argumento (-1) indica que el bucle se detendrá antes de llegar a la posición -1, es decir, terminará en la posición 0 (primer dígito).
        # - El tercer argumento (-1) significa que estamos retrocediendo de un dígito a la vez.
        
        for posicion in range(cantidad_de_digitos - 1, -1, -1):
            # Crea una lista auxiliar con 10 sublistas (una para cada dígito de 0 a 9).
            lista_auxiliar = [[] for _ in range(10)]

            # Distribuye los números en las sublistas basándose en el dígito actual (en la posición `posicion`).
            for elemento in lista_normalizada:
                # Extrae el dígito en la posición actual (de derecha a izquierda) de la cadena 'elemento'.
                # 'posicion' indica qué dígito estamos considerando (por ejemplo, las unidades, decenas, centenas, etc.).
                digito = int(elemento[posicion])

                # Añade el número (en formato de cadena) a la sublista correspondiente en 'lista_auxiliar'.
                # La sublista seleccionada es la que corresponde al valor del 'digito'.
                lista_auxiliar[digito].append(elemento)


            # Después de haber agrupado todos los números por el dígito actual, 
            # combinamos todas las sublistas en una sola lista ordenada.
            # Aquí utilizamos una comprensión de listas anidada:
            # - El bucle exterior (for sublista in lista_auxiliar) recorre cada sublista dentro de lista_auxiliar.
            # - El bucle interior (for elemento in sublista) recorre cada número dentro de la sublista actual.
            # - Cada número (elemento) se añade a la lista final.
            # Esto nos permite "aplanar" la lista auxiliar (lista_auxiliar) en una sola lista (lista_normalizada).
            lista_normalizada = [elemento for sublista in lista_auxiliar for elemento in sublista]

        # Convierte las cadenas normalizadas de vuelta a números enteros.
        # El resultado final es la lista ordenada.
        self.__lista = [int(elemento) for elemento in lista_normalizada]

        return self.__lista

