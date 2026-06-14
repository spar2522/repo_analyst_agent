# tools module for repo_analyst
# Contains utility functions and classes for repository analysis tasks

from .config import ConfigLoader
from .data import RepoDataProcessor
from .analysis import CodeQualityAnalyzer
from .visualization import RepoVisualizer

__version__ = '0.1.0'
__author__ = 'Arpit Ratan'

def load_config(config_path: str) -> ConfigLoader:
    """Factory function to create config loader instance"""
    return ConfigLoader(config_path)

def analyze_repo(config: ConfigLoader) -> dict:
    """Entry point for repository analysis workflow"""
    processor = RepoDataProcessor(config)
    analyzer = CodeQualityAnalyzer(processor)
    visualizer = RepoVisualizer(config)
    
    results = analyzer.run_analysis()
    visualizer.generate_report(results)
    
    return results

# Public API exports
__all__ = [
    'ConfigLoader',
    'RepoDataProcessor',
    'CodeQualityAnalyzer',
    'RepoVisualizer',
    'load_config',
    'analyze_repo'
]