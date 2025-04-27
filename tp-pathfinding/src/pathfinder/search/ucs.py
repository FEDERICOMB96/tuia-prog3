from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)
        explored[node.state] = node.cost

        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()       

            if node.state == grid.end:
                return Solution(node, explored)

            successors = grid.get_neighbours(node.state) #{a1:s1, a2:s2,...}
            acciones = successors.keys()
            
            for action in acciones:
                new_state = successors[action]

                cost = node.cost + grid.get_cost(new_state)

                if new_state not in explored or cost < explored[new_state]:
                    new_node = Node("", 
                                    new_state,
                                    cost,
                                    node,
                                    action)
                    
                    explored[new_state] = cost
                    frontier.add(new_node, new_node.cost)