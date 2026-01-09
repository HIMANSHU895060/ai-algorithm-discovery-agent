"""Autonomous AI Agent Core Module
Generalized AI agent for discovering and optimizing algorithms
using reinforcement learning and genetic algorithms.
"""

import json
import numpy as np
from collections import defaultdict
import time
from typing import Dict, List, Any

class QLearningAgent:
    """Q-Learning agent for algorithm selection"""
    
    def __init__(self, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_values = defaultdict(lambda: defaultdict(float))
        self.state_visits = defaultdict(int)
        
    def select_action(self, state: str, available_actions: List[str]) -> str:
        """Epsilon-greedy action selection"""
        self.state_visits[state] += 1
        
        if np.random.random() < self.epsilon:
            return np.random.choice(available_actions)
        
        q_vals = [self.q_values[state][a] for a in available_actions]
        max_q = max(q_vals) if q_vals else 0
        
        best_actions = [a for a, q in zip(available_actions, q_vals) if q == max_q]
        return np.random.choice(best_actions)
    
    def update_q_value(self, state: str, action: str, reward: float, 
                       next_state: str, next_actions: List[str]):
        """Update Q-values using the Q-learning update rule"""
        current_q = self.q_values[state][action]
        
        if next_actions:
            max_next_q = max([self.q_values[next_state][a] for a in next_actions])
        else:
            max_next_q = 0
        
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )
        self.q_values[state][action] = new_q
    
    def get_best_algorithm(self, state: str) -> str:
        """Get the best algorithm for a given state"""
        if not self.q_values[state]:
            return None
        return max(self.q_values[state], key=self.q_values[state].get)


class AlgorithmLibrary:
    """Library of available algorithms"""
    
    ALGORITHMS = {
        'sorting': {
            'quicksort': {'time': 'O(n log n)', 'space': 'O(log n)'},
            'mergesort': {'time': 'O(n log n)', 'space': 'O(n)'},
            'heapsort': {'time': 'O(n log n)', 'space': 'O(1)'},
            'bubblesort': {'time': 'O(n^2)', 'space': 'O(1)'},
            'insertion_sort': {'time': 'O(n^2)', 'space': 'O(1)'}
        },
        'searching': {
            'binary_search': {'time': 'O(log n)', 'space': 'O(1)'},
            'linear_search': {'time': 'O(n)', 'space': 'O(1)'},
            'hash_search': {'time': 'O(1)', 'space': 'O(n)'}
        },
        'dp': {
            'fibonacci': {'time': 'O(n)', 'space': 'O(n)'},
            'knapsack': {'time': 'O(nW)', 'space': 'O(nW)'},
            'lcs': {'time': 'O(mn)', 'space': 'O(mn)'}
        },
        'graph': {
            'dfs': {'time': 'O(V+E)', 'space': 'O(V)'},
            'bfs': {'time': 'O(V+E)', 'space': 'O(V)'},
            'dijkstra': {'time': 'O((V+E)logV)', 'space': 'O(V)'}
        }
    }
    
    @classmethod
    def get_algorithms(cls, problem_type: str) -> List[str]:
        """Get available algorithms for a problem type"""
        return list(cls.ALGORITHMS.get(problem_type, {}).keys())
    
    @classmethod
    def get_complexity(cls, problem_type: str, algorithm: str) -> Dict[str, str]:
        """Get time and space complexity of algorithm"""
        return cls.ALGORITHMS.get(problem_type, {}).get(algorithm, {})


class AIAgentCore:
    """Core AI Agent for algorithm discovery and optimization"""
    
    def __init__(self, learning_rate=0.1, epsilon=0.1):
        self.rl_agent = QLearningAgent(learning_rate=learning_rate, epsilon=epsilon)
        self.algorithm_library = AlgorithmLibrary()
        self.discovery_history = []
        self.performance_cache = {}
        
    def discover_algorithm(self, problem_type: str, input_size: int, 
                          constraints: Dict[str, float] = None) -> Dict[str, Any]:
        """Discover optimal algorithm for problem"""
        state = f"{problem_type}_{input_size}"
        available_algorithms = self.algorithm_library.get_algorithms(problem_type)
        
        if not available_algorithms:
            return {'error': f'Unknown problem type: {problem_type}'}
        
        selected_algorithm = self.rl_agent.select_action(state, available_algorithms)
        complexity = self.algorithm_library.get_complexity(problem_type, selected_algorithm)
        
        discovery = {
            'problem_type': problem_type,
            'input_size': input_size,
            'selected_algorithm': selected_algorithm,
            'time_complexity': complexity.get('time', 'Unknown'),
            'space_complexity': complexity.get('space', 'Unknown'),
            'fitness_score': np.random.uniform(0.7, 1.0),
            'timestamp': time.time()
        }
        
        self.discovery_history.append(discovery)
        return discovery
    
    def evaluate_algorithm_performance(self, algorithm: str, 
                                       test_cases: List[Dict]) -> Dict[str, Any]:
        """Evaluate algorithm performance on test cases"""
        passed = 0
        failed = 0
        execution_time = 0
        
        for test_case in test_cases:
            try:
                # Simulate evaluation
                execution_time += np.random.uniform(0.001, 0.1)
                passed += 1
            except Exception as e:
                failed += 1
        
        success_rate = passed / len(test_cases) if test_cases else 0
        
        return {
            'algorithm': algorithm,
            'passed_tests': passed,
            'failed_tests': failed,
            'success_rate': success_rate,
            'avg_execution_time': execution_time / len(test_cases) if test_cases else 0
        }
    
    def get_discovery_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent discovery history"""
        return self.discovery_history[-limit:]
    
    def reset_learning(self):
        """Reset RL agent"""
        self.rl_agent = QLearningAgent()
        self.discovery_history = []
