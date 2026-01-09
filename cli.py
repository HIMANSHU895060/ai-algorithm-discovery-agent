#!/usr/bin/env python3
"""Command Line Interface for Offline AI Algorithm Discovery Agent
Easy-to-use terminal commands for offline operation.
"""

import argparse
import json
import sys
from offline_mode import OfflineMode, OfflineDatabase
from agent_core import AIAgentCore


class OfflineAgentCLI:
    """CLI for offline AI agent"""
    
    def __init__(self):
        self.offline = OfflineMode()
        self.agent = AIAgentCore()
    
    def discover(self, problem_type: str, input_size: int = 1000):
        """Discover algorithm for problem"""
        print(f"\n🔍 Discovering algorithm for: {problem_type} (input_size={input_size})")
        discovery = self.agent.discover_algorithm(problem_type, input_size)
        
        if 'error' in discovery:
            print(f"❌ Error: {discovery['error']}")
            return
        
        # Save to offline database
        self.offline.db.save_discovery(discovery)
        
        print(f"✅ Algorithm: {discovery['selected_algorithm']}")
        print(f"   Time Complexity: {discovery['time_complexity']}")
        print(f"   Space Complexity: {discovery['space_complexity']}")
        print(f"   Fitness Score: {discovery['fitness_score']:.4f}")
    
    def save_solution(self, problem_type: str, code: str, language: str = 'python', notes: str = ''):
        """Save problem solution locally"""
        print(f"\n💾 Saving solution for: {problem_type}")
        self.offline.db.save_solution(problem_type, code, language, notes)
        print(f"✅ Solution saved successfully!")
    
    def list_discoveries(self, limit: int = 10):
        """List recent discoveries"""
        print(f"\n📋 Recent Discoveries (last {limit}):")
        discoveries = self.offline.db.get_discoveries(limit)
        
        if not discoveries:
            print("No discoveries yet. Run 'discover' command first!")
            return
        
        for i, disc in enumerate(discoveries, 1):
            print(f"\n{i}. Problem: {disc['problem_type']} | Input Size: {disc['input_size']}")
            print(f"   Algorithm: {disc['algorithm']} | Fitness: {disc['fitness_score']:.4f}")
            print(f"   Timestamp: {disc['timestamp']}")
    
    def list_solutions(self, problem_type: str = None):
        """List saved solutions"""
        print(f"\n📚 Saved Solutions:")
        solutions = self.offline.db.get_solutions(problem_type)
        
        if not solutions:
            print("No solutions saved yet!")
            return
        
        for i, sol in enumerate(solutions, 1):
            print(f"\n{i}. Problem: {sol['problem_type']} | Language: {sol['language']}")
            print(f"   Notes: {sol['notes']}")
            print(f"   Saved: {sol['timestamp']}")
    
    def stats(self):
        """Show offline statistics"""
        print(f"\n📊 Offline Mode Statistics:")
        status = self.offline.get_offline_status()
        
        print(f"\n✓ Offline Mode: {status['offline_mode']}")
        print(f"✓ Database: {status['database']}")
        print(f"✓ Pending Syncs: {status['pending_syncs']}")
        
        stats = status['statistics']
        print(f"\n📈 Performance Stats:")
        print(f"   Avg Success Rate: {stats.get('avg_success_rate', 'N/A')}")
        print(f"   Avg Execution Time: {stats.get('avg_execution_time', 'N/A')}s")
        print(f"   Total Tests: {stats.get('total_tests', 0)}")
    
    def export(self, filepath: str):
        """Export all data"""
        print(f"\n📤 Exporting data to: {filepath}")
        result = self.offline.export_data(filepath)
        if result['status'] == 'success':
            print(f"✅ Data exported successfully!")
        else:
            print(f"❌ Export failed: {result.get('message')}")
    
    def import_data(self, filepath: str):
        """Import data from file"""
        print(f"\n📥 Importing data from: {filepath}")
        result = self.offline.import_data(filepath)
        if result['status'] == 'success':
            print(f"✅ Data imported successfully!")
        else:
            print(f"❌ Import failed: {result.get('message')}")
    
    def status(self):
        """Show system status"""
        print(f"\n🏥 System Status:")
        status = self.offline.get_offline_status()
        
        print(f"\nMode: {'OFFLINE 🔴' if status['offline_mode'] else 'ONLINE 🟢'}")
        print(f"Database: {status['database']}")
        print(f"Cache: {status['cache_file']}")
        print(f"Pending Syncs: {status['pending_syncs']}")
        
        disc_count = len(status['recent_discoveries'])
        print(f"\nRecent Discoveries: {disc_count}")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='AI Algorithm Discovery Agent - Offline Mode CLI'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # discover command
    discover_parser = subparsers.add_parser('discover', help='Discover algorithm')
    discover_parser.add_argument('problem_type', help='Problem type (sorting, searching, dp, graph)')
    discover_parser.add_argument('--size', type=int, default=1000, help='Input size')
    
    # save-solution command
    save_parser = subparsers.add_parser('save', help='Save solution')
    save_parser.add_argument('problem_type', help='Problem type')
    save_parser.add_argument('code_file', help='Python file with solution')
    save_parser.add_argument('--lang', default='python', help='Language')
    save_parser.add_argument('--notes', default='', help='Notes')
    
    # list commands
    subparsers.add_parser('discoveries', help='List all discoveries')
    subparsers.add_parser('solutions', help='List all solutions')
    
    # stats command
    subparsers.add_parser('stats', help='Show statistics')
    subparsers.add_parser('status', help='Show system status')
    
    # export/import
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('filepath', help='Output file path')
    
    import_parser = subparsers.add_parser('import', help='Import data')
    import_parser.add_argument('filepath', help='Input file path')
    
    args = parser.parse_args()
    
    cli = OfflineAgentCLI()
    
    if args.command == 'discover':
        cli.discover(args.problem_type, args.size)
    elif args.command == 'save':
        try:
            with open(args.code_file, 'r') as f:
                code = f.read()
            cli.save_solution(args.problem_type, code, args.lang, args.notes)
        except FileNotFoundError:
            print(f"❌ File not found: {args.code_file}")
    elif args.command == 'discoveries':
        cli.list_discoveries()
    elif args.command == 'solutions':
        cli.list_solutions()
    elif args.command == 'stats':
        cli.stats()
    elif args.command == 'status':
        cli.status()
    elif args.command == 'export':
        cli.export(args.filepath)
    elif args.command == 'import':
        cli.import_data(args.filepath)
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
