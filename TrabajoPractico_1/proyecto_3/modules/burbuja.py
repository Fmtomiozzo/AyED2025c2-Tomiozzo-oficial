class Burbuja:
    def __init__(self, lista):
        self.__lista=lista

    
    def ordenar_lista(self):
        """ordena una lista de manera ascedente"""
        contador=0
        while contador<len(self.__lista):
            #burbuja= self.__lista[0] 
            tamaño_lista = len(self.__lista)-contador
            for i in range(1,tamaño_lista):
                if self.__lista[i]<self.__lista[i-1]:
                    aux=self.__lista[i]
                    self.__lista[i]=self.__lista[i-1]
                    self.__lista[i-1]=aux

                #     burbuja=self.__lista[i]
                # elif self.__lista[i]==burbuja:
                #     pass
                # else: 
                #     self.__lista[i-1] = self.__lista[i]
                #     self.__lista[i]=burbuja  
            contador+=1                  
        return self.__lista
    
    @property
    def __str__(self):
        return f"{self.__lista}"

