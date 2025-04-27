from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {} 
        
        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)
        
        frontier = StackFrontier()
        frontier.add(node)

        while True:
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.remove()

            if node.state in explored:
                continue

            explored[node.state] = True

            successors = grid.get_neighbours(node.state) #{a1:s1, a2:s2,...}
            acciones = successors.keys()
            
            for action in acciones:
                new_state = successors[action]

                if new_state not in explored:
                    new_node = Node("", 
                                    new_state,
                                    node.cost + grid.get_cost(new_state),
                                    node,
                                    action)
                    
                    if new_state == grid.end:
                        return Solution(new_node, explored)
                    
                    frontier.add(new_node)
    




