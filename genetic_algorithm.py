"""Genetic Algorithm for Algorithm Optimization
Evolves algorithm parameters through multiple generations.
"""

import random
import numpy as np
from typing import List, Dict, Any, Callable
import copy


class Individual:
    """Represents a candidate solution (algorithm with parameters)"""
    
    def __init__(self, genes: Dict[str, Any], fitness: float = 0):
        self.genes = genes  # Algorithm parameters
        self.fitness = fitness
    
    def __repr__(self):
        return f"Individual(fitness={self.fitness:.4f})"


class GeneticAlgorithm:
    """Genetic Algorithm for parameter optimization"""
    
    def __init__(self, population_size: int = 50, generations: int = 100, 
                 mutation_rate: float = 0.1, crossover_rate: float = 0.8):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.best_fitness_history = []
        self.avg_fitness_history = []
    
    def create_population(self, gene_templates: List[Dict[str, Any]]) -> List[Individual]:
        """Create initial population from templates"""
        population = []
        for _ in range(self.population_size):
            template = random.choice(gene_templates)
            genes = copy.deepcopy(template)
            # Add random variation
            individual = Individual(genes)
            population.append(individual)
        return population
    
    def evaluate_fitness(self, individual: Individual, 
                        fitness_function: Callable) -> float:
        """Evaluate fitness of an individual"""
        individual.fitness = fitness_function(individual.genes)
        return individual.fitness
    
    def selection(self, population: List[Individual], 
                 tournament_size: int = 3) -> Individual:
        """Tournament selection"""
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=lambda ind: ind.fitness)
    
    def crossover(self, parent1: Individual, parent2: Individual) -> Individual:
        """Create offspring via crossover"""
        child_genes = {}
        for key in parent1.genes:
            if key in parent2.genes:
                # Randomly select from either parent
                child_genes[key] = random.choice(
                    [parent1.genes[key], parent2.genes[key]]
                )
        return Individual(child_genes)
    
    def mutate(self, individual: Individual, mutation_params: Dict) -> Individual:
        """Apply mutation to individual"""
        if random.random() < self.mutation_rate:
            for key in individual.genes:
                if key in mutation_params:
                    # Add Gaussian noise
                    current_val = individual.genes[key]
                    if isinstance(current_val, (int, float)):
                        noise = np.random.normal(
                            0, mutation_params[key].get('std', 0.1)
                        )
                        individual.genes[key] = max(
                            mutation_params[key].get('min', 0),
                            min(
                                mutation_params[key].get('max', 100),
                                current_val + noise
                            )
                        )
        return individual
    
    def evolve(self, gene_templates: List[Dict[str, Any]], 
              fitness_function: Callable,
              mutation_params: Dict = None) -> Individual:
        """Run genetic algorithm evolution"""
        if mutation_params is None:
            mutation_params = {}
        
        # Initialize population
        population = self.create_population(gene_templates)
        
        # Evaluate initial population
        for individual in population:
            self.evaluate_fitness(individual, fitness_function)
        
        # Evolution loop
        for generation in range(self.generations):
            # Record statistics
            fitnesses = [ind.fitness for ind in population]
            self.best_fitness_history.append(max(fitnesses))
            self.avg_fitness_history.append(np.mean(fitnesses))
            
            # Create new population
            new_population = []
            
            # Elitism: keep best individual
            best_individual = max(population, key=lambda ind: ind.fitness)
            new_population.append(copy.deepcopy(best_individual))
            
            # Generate offspring
            while len(new_population) < self.population_size:
                if random.random() < self.crossover_rate:
                    parent1 = self.selection(population)
                    parent2 = self.selection(population)
                    child = self.crossover(parent1, parent2)
                else:
                    child = copy.deepcopy(self.selection(population))
                
                child = self.mutate(child, mutation_params)
                self.evaluate_fitness(child, fitness_function)
                new_population.append(child)
            
            population = new_population[:self.population_size]
        
        # Return best individual from final population
        return max(population, key=lambda ind: ind.fitness)
    
    def get_statistics(self) -> Dict[str, List]:
        """Get evolution statistics"""
        return {
            'best_fitness': self.best_fitness_history,
            'avg_fitness': self.avg_fitness_history
        }


class AlgorithmOptimizer:
    """Uses GA to optimize algorithm parameters"""
    
    def __init__(self, algorithm_name: str, initial_params: Dict[str, Any]):
        self.algorithm_name = algorithm_name
        self.initial_params = initial_params
        self.ga = GeneticAlgorithm(population_size=50, generations=100)
    
    def optimize(self, fitness_function: Callable, 
                mutation_params: Dict = None) -> Dict[str, Any]:
        """Optimize algorithm parameters"""
        best_individual = self.ga.evolve(
            [self.initial_params],
            fitness_function,
            mutation_params
        )
        
        return {
            'algorithm': self.algorithm_name,
            'optimized_parameters': best_individual.genes,
            'fitness': best_individual.fitness,
            'statistics': self.ga.get_statistics()
        }
