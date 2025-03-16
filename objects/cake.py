from collections import Counter

class Cake:
    def __init__(self, numbers):
        self.numbers = numbers  # The numbers inside the cake
        self.main=[]            # The numbers it will accept from outside cakes
        self.empty= 0           # Number of empty spaces
        self.check_main()
        self.check_empty()
                   

    # Assign a main number to a cake    
    def check_main(self):
                # Filtrar los números que no son 0
        numeros_filtrados = [num for num in self.numbers if num != 0]

        # Contar las ocurrencias de cada número
        contador = Counter(numeros_filtrados)
        try:
            # Obtener el máximo número de repeticiones
            max_repeticiones = max(contador.values())
            # Obtener todos los números con el máximo conteo
            numeros = [num for num, rep in contador.items() if rep == max_repeticiones]
        except:
            numeros=[0]
        self.main=numeros


    def check_empty(self):
        count=0
        for i in range(6):
            if self.numbers[i]==0: count+=1
        self.empty=count
