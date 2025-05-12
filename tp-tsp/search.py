"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo. Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from time import time
from problem import OptProblem


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Buscamos la acción que genera el sucesor con mayor valor objetivo
            act, succ_val = problem.max_action(actual)

            # Retornar si estamos en un maximo local:
            # el valor objetivo del sucesor es menor o igual al del estado actual
            if succ_val <= value:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            actual = problem.result(actual, act)
            value = succ_val
            self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    # A partir de 30 iteraciones, el algoritmo da el mismo resultado (-86585)
    # Con menos iteraciones, el resultado algunas veces da otros valores.
    def __init__(self, cantInteraciones: int = 30):
        super().__init__()    
        self.cantInteraciones = cantInteraciones

    def solve(self, problem: OptProblem):
        # Inicio del reloj
        start = time()
        
        actual = problem.init
        value = problem.obj_val(problem.init)

        mejorRecorrido = actual
        mejorValor = value 

        for _ in range(self.cantInteraciones):
            while True:
                act, succ_val = problem.max_action(actual)
                
                if succ_val <= value:
                    break
            
                actual = problem.result(actual, act)
                value = succ_val
                self.niters += 1
            
            if mejorValor < value:
                mejorValor = value
                mejorRecorrido = actual
            else:
                actual = problem.random_reset()
                value = problem.obj_val(actual)

        self.tour = mejorRecorrido
        self.value = mejorValor
        end = time()
        self.time = end-start


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def __init__(self, cantInteraciones: int = 2000, cantTabu: int = 20):
        super().__init__()
        self.cantInteraciones = cantInteraciones
        self.cantTabu = cantTabu

    def solve(self, problem: OptProblem):
        start = time()

        current = problem.init

        best = current
        best_value = problem.obj_val(current)

        tabu_list = []

        self.niters = 0
        no_mejora = 0

        while no_mejora < self.cantInteraciones:
            act, succ_val = problem.max_action(current, tabu_list)

            successor = problem.result(current, act)

            self.niters += 1

            if succ_val > best_value:
                best = successor
                best_value = succ_val

                no_mejora = 0
            else:
                no_mejora += 1

            tabu_list.append(act)
            
            if len(tabu_list) > self.cantTabu:
                tabu_list.pop(0)
            
            current = successor

        self.tour = best
        self.value = best_value
        end = time()
        self.time = end - start