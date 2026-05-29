"""
适应度评估器实现

评估解的适应度并将其转换为质量。
验证需求: 2.1-2.6, 3.1-3.6
"""

import logging
import math
from typing import Callable, List

from .solution import Solution

logger = logging.getLogger(__name__)


class FitnessEvaluator:
    """
    适应度评估器
    
    负责计算解的适应度值并将其转换为质量。
    """
    
    def __init__(self, objective_function: Callable):
        """
        初始化适应度评估器
        
        Args:
            objective_function: 目标函数，接受位置向量返回适应度值
        """
        self.objective_function = objective_function
        self.min_fitness = float('inf')
        self.max_fitness = float('-inf')
    
    def evaluate_fitness(self, solution: Solution) -> float:
        """
        评估解的适应度
        
        Args:
            solution: 要评估的解
        
        Returns:
            适应度值
        
        验证需求: 2.1, 2.3, 2.4
        """
        try:
            # 调用目标函数计算适应度
            fitness = self.objective_function(solution.position)
            
            # 检查是否为 NaN 或无穷大
            if math.isnan(fitness) or math.isinf(fitness):
                logger.warning(
                    f"目标函数返回无效值 (NaN 或无穷大)，位置: {solution.position}"
                )
                fitness = float('-inf')
            
            # 更新适应度并返回
            solution.fitness = fitness
            return fitness
            
        except Exception as e:
            # 捕获目标函数抛出的异常
            logger.warning(
                f"目标函数计算失败，位置: {solution.position}, 错误: {e}"
            )
            solution.fitness = float('-inf')
            return float('-inf')
    
    def fitness_to_mass(
        self,
        fitness: float,
        min_fitness: float = None,
        max_fitness: float = None
    ) -> float:
        """
        将适应度转换为质量
        
        Args:
            fitness: 适应度值
            min_fitness: 最小适应度（用于归一化）
            max_fitness: 最大适应度（用于归一化）
        
        Returns:
            质量值（始终为正数）
        
        验证需求: 2.5, 2.6, 3.1-3.6
        """
        # 使用提供的或记录的最小/最大适应度
        if min_fitness is None:
            min_fitness = self.min_fitness
        if max_fitness is None:
            max_fitness = self.max_fitness
        
        # 如果适应度范围未知或无效，返回默认质量
        if math.isinf(min_fitness) or math.isinf(max_fitness):
            return 1.0
        
        # 如果所有解的适应度相同
        if abs(max_fitness - min_fitness) < 1e-10:
            return 1.0
        
        # 归一化适应度到 [0, 1] 范围
        normalized = (fitness - min_fitness) / (max_fitness - min_fitness)
        
        # 转换为质量，确保质量始终为正数
        # 使用 exp 函数使质量差异更明显
        # 最小质量为 0.1，最大质量为 10.0
        mass = 0.1 + 9.9 * normalized
        
        # 确保质量为正数
        if mass <= 0:
            mass = 1e-6
        
        return mass
    
    def evaluate_population(self, solutions: List[Solution]) -> None:
        """
        评估整个种群的适应度并更新质量
        
        Args:
            solutions: 解的列表
        
        验证需求: 2.1-2.6
        """
        if not solutions:
            return
        
        # 评估所有解的适应度
        for solution in solutions:
            self.evaluate_fitness(solution)
        
        # 更新最小和最大适应度
        valid_fitnesses = [
            s.fitness for s in solutions 
            if not math.isinf(s.fitness)
        ]
        
        if valid_fitnesses:
            self.min_fitness = min(valid_fitnesses)
            self.max_fitness = max(valid_fitnesses)
        
        # 转换适应度为质量
        for solution in solutions:
            solution.mass = self.fitness_to_mass(
                solution.fitness,
                self.min_fitness,
                self.max_fitness
            )
