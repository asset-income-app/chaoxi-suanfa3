"""
潮汐算法 (Tidal Algorithm)

基于物理引力模型的优化算法，用于解决无梯度、不连续、多峰值的优化问题。
"""

from .vector import Vector, DimensionMismatchError
from .bounds import Bounds, InvalidBoundsError
from .solution import Solution
from .parameters import (
    PhysicsParameters,
    TidalParameters,
    InvalidParameterError
)
from .physics_engine import PhysicsEngine
from .tidal_mechanism import TidalMechanism, Region
from .fitness_evaluator import FitnessEvaluator
from .tidal_optimizer import TidalOptimizer

__version__ = "1.0.0"

__all__ = [
    # 核心类
    "TidalOptimizer",
    
    # 数据结构
    "Vector",
    "Bounds",
    "Solution",
    "Region",
    
    # 参数
    "PhysicsParameters",
    "TidalParameters",
    
    # 组件
    "PhysicsEngine",
    "TidalMechanism",
    "FitnessEvaluator",
    
    # 异常
    "DimensionMismatchError",
    "InvalidBoundsError",
    "InvalidParameterError",
]
