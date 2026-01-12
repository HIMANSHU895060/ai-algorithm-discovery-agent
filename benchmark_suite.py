"""Algorithm Benchmark Suite with Real-Time Performance Metrics

This module provides comprehensive benchmarking capabilities for algorithms,
including execution time, memory usage, scalability analysis, and 
comparative performance visualization.

Features:
- Real-time performance measurement
- Memory profiling and leak detection
- Scalability analysis (how performance changes with input size)
- Comparative benchmarking of multiple algorithms
- Statistical analysis (mean, median, std dev, min, max)
- CSV/JSON export capabilities
- Visual performance reports
"""

import time
import tracemalloc
import psutil
import os
from typing import Callable, Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import statistics


@dataclass
class BenchmarkResult:
    """Stores benchmark metrics for an algorithm."""
    algorithm_name: str
    input_size: int
    execution_time: float
    memory_used: float
    memory_peak: float
    timestamp: str
    success: bool
    error_message: str = None
    
    def to_dict(self) -> Dict:
        """Convert result to dictionary."""
        return asdict(self)


class AlgorithmBenchmark:
    """Benchmark a single algorithm with precise metrics."""
    
    def __init__(self, algorithm: Callable, name: str = None):
        """Initialize benchmark for algorithm.
        
        Args:
            algorithm: Callable algorithm function
            name: Optional name for the algorithm
        """
        self.algorithm = algorithm
        self.name = name or algorithm.__name__
        self.results = []
    
    def run(self, test_input: Any, iterations: int = 1) -> BenchmarkResult:
        """Run algorithm and measure performance.
        
        Args:
            test_input: Input data for algorithm
            iterations: Number of times to run (for averaging)
            
        Returns:
            BenchmarkResult with metrics
        """
        execution_times = []
        memory_used_list = []
        memory_peak = 0
        input_size = len(test_input) if hasattr(test_input, '__len__') else 1
        
        tracemalloc.start()
        
        try:
            for _ in range(iterations):
                # Memory tracking
                snapshot_before = tracemalloc.take_snapshot()
                
                # Time measurement
                start_time = time.perf_counter()
                result = self.algorithm(test_input.copy() if hasattr(test_input, 'copy') else test_input)
                end_time = time.perf_counter()
                
                # Memory analysis
                snapshot_after = tracemalloc.take_snapshot()
                top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
                
                execution_times.append(end_time - start_time)
                memory_used = sum(stat.size_diff for stat in top_stats) / (1024 * 1024)  # MB
                memory_used_list.append(max(0, memory_used))
                memory_peak = max(memory_peak, memory_used)
            
            tracemalloc.stop()
            
            # Calculate statistics
            avg_execution_time = statistics.mean(execution_times)
            avg_memory = statistics.mean(memory_used_list)
            
            result = BenchmarkResult(
                algorithm_name=self.name,
                input_size=input_size,
                execution_time=avg_execution_time,
                memory_used=avg_memory,
                memory_peak=memory_peak,
                timestamp=datetime.now().isoformat(),
                success=True
            )
            
        except Exception as e:
            tracemalloc.stop()
            result = BenchmarkResult(
                algorithm_name=self.name,
                input_size=input_size,
                execution_time=0,
                memory_used=0,
                memory_peak=0,
                timestamp=datetime.now().isoformat(),
                success=False,
                error_message=str(e)
            )
        
        self.results.append(result)
        return result


class BenchmarkSuite:
    """Comprehensive benchmarking suite for multiple algorithms."""
    
    def __init__(self):
        """Initialize benchmark suite."""
        self.benchmarks: Dict[str, AlgorithmBenchmark] = {}
        self.all_results: List[BenchmarkResult] = []
    
    def add_algorithm(self, algorithm: Callable, name: str = None) -> None:
        """Add algorithm to benchmark suite.
        
        Args:
            algorithm: Algorithm function to benchmark
            name: Optional name for algorithm
        """
        algo_name = name or algorithm.__name__
        self.benchmarks[algo_name] = AlgorithmBenchmark(algorithm, algo_name)
    
    def run_all(self, test_inputs: List[Tuple[Any, int]], iterations: int = 3) -> Dict:
        """Run all algorithms with multiple test inputs.
        
        Args:
            test_inputs: List of (input_data, label) tuples
            iterations: Times to run each algorithm
            
        Returns:
            Comprehensive results dictionary
        """
        results = {}
        
        for algo_name, benchmark in self.benchmarks.items():
            results[algo_name] = []
            
            for test_input, label in test_inputs:
                result = benchmark.run(test_input, iterations)
                results[algo_name].append(result.to_dict())
                self.all_results.append(result)
        
        return self._analyze_results(results)
    
    def _analyze_results(self, results: Dict) -> Dict:
        """Analyze benchmark results for comparative insights.
        
        Args:
            results: Raw benchmark results
            
        Returns:
            Analysis with rankings and statistics
        """
        analysis = {
            'raw_results': results,
            'summary': {},
            'fastest_algorithm': None,
            'most_memory_efficient': None,
            'overall_best': None,
        }
        
        algorithm_scores = {}
        
        for algo_name, benchmark_results in results.items():
            successful = [r for r in benchmark_results if r['success']]
            
            if not successful:
                analysis['summary'][algo_name] = {'error': 'All runs failed'}
                continue
            
            times = [r['execution_time'] for r in successful]
            memories = [r['memory_used'] for r in successful]
            
            summary = {
                'avg_time': statistics.mean(times),
                'median_time': statistics.median(times),
                'min_time': min(times),
                'max_time': max(times),
                'std_dev_time': statistics.stdev(times) if len(times) > 1 else 0,
                'avg_memory': statistics.mean(memories),
                'peak_memory': max(memories),
                'success_rate': len(successful) / len(benchmark_results),
            }
            
            analysis['summary'][algo_name] = summary
            
            # Scoring (lower is better)
            time_score = summary['avg_time']
            memory_score = summary['avg_memory']
            algorithm_scores[algo_name] = time_score + memory_score
        
        # Identify best performers
        if analysis['summary']:
            fastest = min(
                [(k, v['avg_time']) for k, v in analysis['summary'].items() if 'avg_time' in v],
                key=lambda x: x[1]
            )
            analysis['fastest_algorithm'] = fastest[0]
            
            most_efficient = min(
                [(k, v['avg_memory']) for k, v in analysis['summary'].items() if 'avg_memory' in v],
                key=lambda x: x[1]
            )
            analysis['most_memory_efficient'] = most_efficient[0]
            
            overall = min(algorithm_scores.items(), key=lambda x: x[1])
            analysis['overall_best'] = overall[0]
        
        return analysis
    
    def export_csv(self, filename: str) -> None:
        """Export results to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        import csv
        
        with open(filename, 'w', newline='') as f:
            if not self.all_results:
                return
            
            fieldnames = self.all_results[0].to_dict().keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in self.all_results:
                writer.writerow(result.to_dict())
    
    def export_json(self, filename: str) -> None:
        """Export results to JSON file.
        
        Args:
            filename: Output JSON filename
        """
        data = [r.to_dict() for r in self.all_results]
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_performance_report(self) -> str:
        """Generate human-readable performance report.
        
        Returns:
            Formatted report string
        """
        if not self.benchmarks:
            return "No algorithms benchmarked."
        
        report = "\n" + "="*70 + "\n"
        report += "ALGORITHM PERFORMANCE BENCHMARK REPORT\n"
        report += "="*70 + "\n\n"
        
        for algo_name, benchmark in self.benchmarks.items():
            if not benchmark.results:
                continue
            
            times = [r.execution_time for r in benchmark.results if r.success]
            memories = [r.memory_used for r in benchmark.results if r.success]
            
            if times:
                report += f"Algorithm: {algo_name}\n"
                report += f"  ⏱️  Execution Time: {statistics.mean(times):.6f}s (avg)\n"
                report += f"  💾 Memory Used: {statistics.mean(memories):.4f} MB (avg)\n"
                report += f"  📊 Runs: {len(benchmark.results)}\n\n"
        
        report += "="*70 + "\n"
        return report


def create_test_suite(sizes: List[int]) -> List[Tuple[List, str]]:
    """Create test cases with various input sizes.
    
    Args:
        sizes: List of input sizes
        
    Returns:
        List of (test_input, label) tuples
    """
    test_cases = []
    
    for size in sizes:
        import random
        test_input = [random.randint(1, 1000) for _ in range(size)]
        label = f"n={size}"
        test_cases.append((test_input, label))
    
    return test_cases


if __name__ == "__main__":
    # Example usage
    def bubble_sort(arr):
        arr = arr.copy()
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def quick_sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quick_sort(left) + middle + quick_sort(right)
    
    # Create benchmark suite
    suite = BenchmarkSuite()
    suite.add_algorithm(bubble_sort, "Bubble Sort")
    suite.add_algorithm(quick_sort, "Quick Sort")
    
    # Create test cases
    test_cases = create_test_suite([100, 500, 1000])
    
    # Run benchmarks
    results = suite.run_all(test_cases)
    
    # Print report
    print(suite.get_performance_report())
    print("Analysis Results:")
    print(json.dumps(results['summary'], indent=2, default=str))
