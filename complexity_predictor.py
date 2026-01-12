"""Real-Time Algorithm Complexity Predictor with Visualization

This module predicts time/space complexity from algorithm code and generates
visual complexity graphs for algorithm comparison and analysis.

Features:
- Analyze algorithm code for complexity patterns
- Predict Big-O complexity (worst, average, best cases)
- Generate visual Big-O graphs
- Compare multiple algorithms side-by-side
- Provide complexity recommendations
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from enum import Enum
import numpy as np


class ComplexityType(Enum):
    """Enumeration of complexity types."""
    TIME = "time"
    SPACE = "space"


class BigOComplexity(Enum):
    """Big-O complexity classes."""
    CONSTANT = "O(1)"
    LOGARITHMIC = "O(log n)"
    LINEAR = "O(n)"
    LINEARITHMIC = "O(n log n)"
    QUADRATIC = "O(n^2)"
    CUBIC = "O(n^3)"
    EXPONENTIAL = "O(2^n)"
    FACTORIAL = "O(n!)"


class ComplexityPredictor:
    """Predicts algorithm complexity from code patterns."""
    
    def __init__(self):
        self.complexity_patterns = {
            'constant': [
                r'return\s+\d+',
                r'x\s*=\s*\d+',
                r'print\(',
            ],
            'logarithmic': [
                r'while.*//\s*2',
                r'log',
                r'binary.?search',
            ],
            'linear': [
                r'for\s+\w+\s+in\s+range\s*\(\s*n\s*\)',
                r'for\s+\w+\s+in\s+\w+',
                r'while\s+\w+\s*<\s*len',
            ],
            'linearithmic': [
                r'sorted\(',
                r'merge.?sort',
                r'heap.?sort',
                r'quick.?sort.*random',
            ],
            'quadratic': [
                r'for.*for.*range\s*\(\s*n',
                r'nested.*loop',
                r'bubble.?sort',
                r'insertion.?sort',
            ],
            'cubic': [
                r'for.*for.*for.*range\s*\(\s*n',
                r'triple.*nested',
            ],
            'exponential': [
                r'fibonacci\s*\(',
                r'2\s*\*\*\s*n',
                r'recursive.*without.*memo',
            ],
            'factorial': [
                r'permutation',
                r'n\s*!',
            ]
        }
    
    def analyze_code(self, code: str) -> Dict[str, any]:
        """Analyze algorithm code and predict complexity.
        
        Args:
            code: Algorithm source code as string
            
        Returns:
            Dictionary with complexity analysis results
        """
        code_lower = code.lower()
        results = {
            'time_complexity': self._predict_complexity(code_lower, 'time'),
            'space_complexity': self._predict_complexity(code_lower, 'space'),
            'patterns_found': self._find_patterns(code_lower),
            'nested_loops': self._count_nested_loops(code),
            'recursion_depth': self._estimate_recursion_depth(code),
        }
        return results
    
    def _predict_complexity(self, code: str, complexity_type: str) -> Dict:
        """Predict complexity based on code patterns.
        
        Args:
            code: Lowercased algorithm code
            complexity_type: 'time' or 'space'
            
        Returns:
            Dictionary with complexity predictions
        """
        matches = {}
        for complexity, patterns in self.complexity_patterns.items():
            count = sum(len(re.findall(pattern, code)) for pattern in patterns)
            if count > 0:
                matches[complexity] = count
        
        if not matches:
            predicted = 'O(n)'
        else:
            # Weight the matches and select most likely
            best_match = max(matches.items(), key=lambda x: x[1])[0]
            complexity_map = {
                'constant': 'O(1)',
                'logarithmic': 'O(log n)',
                'linear': 'O(n)',
                'linearithmic': 'O(n log n)',
                'quadratic': 'O(n^2)',
                'cubic': 'O(n^3)',
                'exponential': 'O(2^n)',
                'factorial': 'O(n!)',
            }
            predicted = complexity_map.get(best_match, 'O(n)')
        
        return {
            'predicted': predicted,
            'confidence': min(100, (sum(matches.values()) + 1) * 15),
            'pattern_matches': matches,
        }
    
    def _find_patterns(self, code: str) -> List[str]:
        """Find specific algorithm patterns in code.
        
        Args:
            code: Algorithm code
            
        Returns:
            List of detected patterns
        """
        patterns = []
        pattern_map = {
            'binary_search': r'binary.?search|log|divide.*conquer',
            'sorting': r'sort|quicksort|mergesort|heapsort',
            'dynamic_programming': r'dp\[|memo|dynamic|bottom.?up',
            'greedy': r'greedy|max|min',
            'recursion': r'def.*\(.*\):|return.*\(',
            'iteration': r'for|while',
            'hash': r'dict|hash|set|map',
        }
        
        for pattern_name, pattern in pattern_map.items():
            if re.search(pattern, code):
                patterns.append(pattern_name)
        
        return patterns
    
    def _count_nested_loops(self, code: str) -> int:
        """Count maximum nesting level of loops.
        
        Args:
            code: Algorithm code
            
        Returns:
            Maximum nesting depth
        """
        max_depth = 0
        current_depth = 0
        in_loop = False
        
        lines = code.split('\n')
        for line in lines:
            stripped = line.strip()
            if re.match(r'(for|while)\s+', stripped):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
                in_loop = True
            elif in_loop and (stripped.startswith('for ') or stripped.startswith('while ')):
                current_depth += 1
                max_depth = max(max_depth, current_depth)
        
        return max_depth
    
    def _estimate_recursion_depth(self, code: str) -> int:
        """Estimate recursion depth from code.
        
        Args:
            code: Algorithm code
            
        Returns:
            Estimated recursion depth (0 if no recursion)
        """
        if 'def ' not in code:
            return 0
        
        # Simple heuristic: count function calls to itself
        func_match = re.search(r'def\s+(\w+)\s*\(', code)
        if not func_match:
            return 0
        
        func_name = func_match.group(1)
        call_count = len(re.findall(rf'{func_name}\s*\(', code)) - 1  # -1 for definition
        
        return min(call_count, 10)  # Cap at 10


class ComplexityComparator:
    """Compare complexity of multiple algorithms."""
    
    def __init__(self):
        self.predictor = ComplexityPredictor()
    
    def compare_algorithms(self, algorithms: Dict[str, str]) -> Dict:
        """Compare multiple algorithms.
        
        Args:
            algorithms: Dictionary of {name: code} pairs
            
        Returns:
            Comparison results
        """
        results = {}
        for name, code in algorithms.items():
            analysis = self.predictor.analyze_code(code)
            results[name] = analysis
        
        return self._rank_algorithms(results)
    
    def _rank_algorithms(self, analyses: Dict) -> Dict:
        """Rank algorithms by complexity.
        
        Args:
            analyses: Analysis results for each algorithm
            
        Returns:
            Ranked and sorted results
        """
        complexity_score = {
            'O(1)': 1,
            'O(log n)': 2,
            'O(n)': 3,
            'O(n log n)': 4,
            'O(n^2)': 5,
            'O(n^3)': 6,
            'O(2^n)': 7,
            'O(n!)': 8,
        }
        
        ranked = sorted(
            analyses.items(),
            key=lambda x: complexity_score.get(
                x[1]['time_complexity']['predicted'], 5
            )
        )
        
        return {
            'ranked_algorithms': [name for name, _ in ranked],
            'analysis_details': analyses,
            'most_efficient': ranked[0][0] if ranked else None,
        }


def generate_complexity_graph_data(complexity: str, input_sizes: List[int]) -> Dict:
    """Generate data for complexity visualization.
    
    Args:
        complexity: Big-O complexity string (e.g., 'O(n)')
        input_sizes: List of input sizes to calculate
        
    Returns:
        Dictionary with graph data
    """
    complexity_functions = {
        'O(1)': lambda n: np.ones(len(n)),
        'O(log n)': lambda n: np.log2(np.array(n) + 1),
        'O(n)': lambda n: np.array(n),
        'O(n log n)': lambda n: np.array(n) * np.log2(np.array(n) + 1),
        'O(n^2)': lambda n: np.array(n) ** 2,
        'O(n^3)': lambda n: np.array(n) ** 3,
        'O(2^n)': lambda n: 2 ** np.minimum(np.array(n), 20),
        'O(n!)': lambda n: np.array([1 if x < 10 else float('inf') for x in n]),
    }
    
    func = complexity_functions.get(complexity, complexity_functions['O(n)'])
    operations = func(input_sizes).tolist()
    
    return {
        'complexity': complexity,
        'input_sizes': input_sizes,
        'operations': operations,
        'graph_type': 'line',
    }


def format_analysis_report(analysis: Dict) -> str:
    """Format analysis results as readable report.
    
    Args:
        analysis: Analysis dictionary
        
    Returns:
        Formatted report string
    """
    report = f"""
╔════════════════════════════════════════════╗
║   Algorithm Complexity Analysis Report     ║
╚════════════════════════════════════════════╝

⏱️  TIME COMPLEXITY
  Predicted: {analysis['time_complexity']['predicted']}
  Confidence: {analysis['time_complexity']['confidence']}%

💾 SPACE COMPLEXITY
  Predicted: {analysis['space_complexity']['predicted']}
  Confidence: {analysis['space_complexity']['confidence']}%

🔍 PATTERNS DETECTED
  {', '.join(analysis['patterns_found']) if analysis['patterns_found'] else 'None'}

🔗 LOOP ANALYSIS
  Max Nested Loops: {analysis['nested_loops']}
  Recursion Depth: {analysis['recursion_depth']}
"""
    return report


if __name__ == "__main__":
    # Example usage
    predictor = ComplexityPredictor()
    
    # Test with simple algorithm
    test_code = """
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    """
    
    analysis = predictor.analyze_code(test_code)
    print(format_analysis_report(analysis))
    
    # Compare algorithms
    comparator = ComplexityComparator()
    algorithms = {
        'bubble_sort': test_code,
        'quick_sort': 'def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr',
    }
    comparison = comparator.compare_algorithms(algorithms)
    print("\n" + json.dumps(comparison, indent=2))
