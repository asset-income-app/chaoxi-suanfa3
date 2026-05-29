"""
潮汐优化器实现

主控制器，协调所有组件完成优化过程。
验证需求: 1.1-1.7, 9.1-9.9, 13.1-13.5, 14.1-14.5
"""

import logging
import random
import time
from typing import Callable, List, Optional

from .vector import Vector
from .bounds import Bounds
from .solution import Solution
from .parameters import PhysicsParameters, TidalParameters
from .physics_engine import PhysicsEngine
from .tidal_mechanism import TidalMechanism
from .fitness_evaluator import FitnessEvaluator

logger = logging.getLogger(__name__)


class TidalOptimizer:
    """
    潮汐优化器
    
    基于物理引力模型的优化算法，通过涨潮和退潮机制动态调整解的分布。
    """
    
    def __init__(
        self,
        objective_function: Callable,
        population_size: int,
        dimensions: int,
        bounds: Bounds,
        physics_params: PhysicsParameters = None,
        tidal_params: TidalParameters = None,
        max_population: int = 10000,
        max_time: float = 3600.0,
        diversity_threshold: float = 1e-6
    ):
        """
        初始化潮汐优化器
        
        Args:
            objective_function: 目标函数
            population_size: 种群大小
            dimensions: 搜索空间维度
            bounds: 搜索空间边界
            physics_params: 物理参数（可选）
            tidal_params: 潮汐参数（可选）
            max_population: 最大种群大小（默认 10000）
            max_time: 最大执行时间（秒，默认 3600）
            diversity_threshold: 多样性阈值（默认 1e-6）
        
        Raises:
            ValueError: 如果参数无效
        
        验证需求: 1.1-1.7, 11.1-11.3, 13.4, 13.5
        """
        # 验证参数
        if population_size <= 0:
            raise ValueError(f"种群大小必须为正整数: {population_size}")
        
        if dimensions <= 0:
            raise ValueError(f"维度必须为正整数: {dimensions}")
        
        if bounds.dimension != dimensions:
            raise ValueError(
                f"边界维度与搜索空间维度不匹配: {bounds.dimension} vs {dimensions}"
            )
        
        self.objective_function = objective_function
        self.population_size = population_size
        self.dimensions = dimensions
        self.bounds = bounds
        self.max_population = max_population
        self.max_time = max_time
        self.diversity_threshold = diversity_threshold
        
        # 初始化参数
        self.physics_params = physics_params or PhysicsParameters()
        self.tidal_params = tidal_params or TidalParameters()
        
        # 初始化组件
        self.physics_engine = PhysicsEngine(self.physics_params)
        self.tidal_mechanism = TidalMechanism(self.tidal_params)
        self.fitness_evaluator = FitnessEvaluator(objective_function)
        
        # 初始化状态
        self.solutions: List[Solution] = []
        self.best_solution: Optional[Solution] = None
        self.iteration = 0
        self.start_time = 0.0
    
    def initialize(self) -> None:
        """
        初始化解群
        
        验证需求: 1.1-1.7, 9.1
        """
        logger.info(f"初始化种群，大小: {self.population_size}, 维度: {self.dimensions}")
        
        self.solutions = []
        
        for _ in range(self.population_size):
            # 在边界内随机生成位置
            position_components = [
                random.uniform(self.bounds.lower[i], self.bounds.upper[i])
                for i in range(self.dimensions)
            ]
            position = Vector(position_components)
            
            # 创建解
            solution = Solution(
                position=position,
                velocity=Vector.zero(self.dimensions),
                acceleration=Vector.zero(self.dimensions),
                mass=1.0,
                fitness=0.0,
                stagnation_counter=0
            )
            
            self.solutions.append(solution)
        
        # 评估初始适应度
        self.fitness_evaluator.evaluate_population(self.solutions)
        
        # 初始化最优解
        self.best_solution = max(self.solutions, key=lambda s: s.fitness).clone()
        
        logger.info(f"初始化完成，最优适应度: {self.best_solution.fitness:.6f}")
    
    def _perform_one_iteration(self) -> None:
        """
        执行一次优化迭代
        
        验证需求: 9.2, 9.3, 9.4, 9.5, 9.6
        """
        # 1. 计算引力和更新物理状态
        for i, solution_i in enumerate(self.solutions):
            total_force = Vector.zero(self.dimensions)
            
            # 计算所有其他解对当前解的引力
            for j, solution_j in enumerate(self.solutions):
                if i != j:
                    force = self.physics_engine.compute_gravitational_force(
                        solution_i,
                        solution_j
                    )
                    total_force = total_force + force
            
            # 更新物理状态
            self.physics_engine.update_solution(
                solution_i,
                total_force,
                self.bounds
            )
        
        # 2. 重新评估适应度和质量
        self.fitness_evaluator.evaluate_population(self.solutions)
        
        # 3. 涨潮机制
        high_density_regions = self.tidal_mechanism.detect_high_density_regions(
            self.solutions
        )
        
        for region in high_density_regions:
            new_solutions = self.tidal_mechanism.flood_tide(
                region,
                self.solutions,
                self.bounds
            )
            self.solutions.extend(new_solutions)
            
            if len(new_solutions) > 0:
                logger.debug(f"涨潮：在区域 {region} 生成 {len(new_solutions)} 个新解")
        
        # 评估新解的适应度
        if high_density_regions:
            self.fitness_evaluator.evaluate_population(self.solutions)
        
        # 4. 退潮机制
        for solution in self.solutions:
            self.tidal_mechanism.detect_stagnation(solution)
        
        original_size = len(self.solutions)
        self.solutions = self.tidal_mechanism.ebb_tide(self.solutions)
        
        if len(self.solutions) < original_size:
            logger.debug(f"退潮：移除 {original_size - len(self.solutions)} 个解")
        
        # 5. 更新最优解
        current_best = max(self.solutions, key=lambda s: s.fitness)
        if current_best.fitness > self.best_solution.fitness:
            self.best_solution = current_best.clone()
            logger.info(
                f"迭代 {self.iteration}: 发现更好的解，适应度: {self.best_solution.fitness:.6f}"
            )
    
    def _check_resource_limits(self) -> bool:
        """
        检查资源限制
        
        Returns:
            如果应该继续优化返回 True，否则返回 False
        
        验证需求: 13.1, 13.2, 13.4, 13.5
        """
        # 检查种群大小限制
        if len(self.solutions) > self.max_population:
            logger.warning(f"种群大小超过限制 ({len(self.solutions)} > {self.max_population})，执行强制退潮")
            # 强制退潮到最大种群的 70%
            target_size = int(self.max_population * 0.7)
            sorted_solutions = sorted(self.solutions, key=lambda s: s.mass, reverse=True)
            self.solutions = sorted_solutions[:target_size]
        
        # 检查时间限制
        elapsed_time = time.time() - self.start_time
        if elapsed_time > self.max_time:
            logger.warning(f"达到时间限制 ({elapsed_time:.2f}s > {self.max_time}s)，提前终止")
            return False
        
        return True
    
    def _check_diversity(self) -> None:
        """
        检查种群多样性并在必要时触发强制涨潮
        
        验证需求: 18.1-18.4
        """
        if len(self.solutions) < 2:
            return
        
        # 计算种群多样性（平均距离）
        total_distance = 0.0
        count = 0
        
        for i in range(len(self.solutions)):
            for j in range(i + 1, len(self.solutions)):
                distance = (self.solutions[i].position - self.solutions[j].position).magnitude()
                total_distance += distance
                count += 1
        
        diversity = total_distance / count if count > 0 else 0.0
        
        # 如果多样性过低，触发强制涨潮
        if diversity < self.diversity_threshold:
            logger.warning(f"种群多样性过低 ({diversity:.6f})，触发强制涨潮")
            
            # 生成额外的随机解
            num_new = int(self.population_size * 0.3)
            for _ in range(num_new):
                position_components = [
                    random.uniform(self.bounds.lower[i], self.bounds.upper[i])
                    for i in range(self.dimensions)
                ]
                position = Vector(position_components)
                
                solution = Solution(
                    position=position,
                    velocity=Vector.zero(self.dimensions),
                    acceleration=Vector.zero(self.dimensions),
                    mass=1.0,
                    fitness=0.0,
                    stagnation_counter=0
                )
                
                self.solutions.append(solution)
            
            # 评估新解的适应度
            self.fitness_evaluator.evaluate_population(self.solutions)
    
    def optimize(self, max_iterations: int) -> Solution:
        """
        执行优化
        
        Args:
            max_iterations: 最大迭代次数
        
        Returns:
            最优解
        
        Raises:
            ValueError: 如果最大迭代次数无效
        
        验证需求: 9.8, 14.1-14.5
        """
        if max_iterations <= 0:
            raise ValueError(f"最大迭代次数必须为正整数: {max_iterations}")
        
        logger.info(f"开始优化，最大迭代次数: {max_iterations}")
        
        # 初始化
        self.initialize()
        self.start_time = time.time()
        
        # 主迭代循环
        for self.iteration in range(1, max_iterations + 1):
            # 执行一次迭代
            self._perform_one_iteration()
            
            # 检查资源限制
            if not self._check_resource_limits():
                break
            
            # 检查种群多样性
            if self.iteration % 10 == 0:
                self._check_diversity()
            
            # 定期输出进度
            if self.iteration % 10 == 0:
                elapsed_time = time.time() - self.start_time
                logger.info(
                    f"迭代 {self.iteration}/{max_iterations}: "
                    f"最优适应度 = {self.best_solution.fitness:.6f}, "
                    f"种群大小 = {len(self.solutions)}, "
                    f"时间 = {elapsed_time:.2f}s"
                )
        
        # 优化完成
        total_time = time.time() - self.start_time
        logger.info(
            f"优化完成，总迭代次数: {self.iteration}, "
            f"总时间: {total_time:.2f}s, "
            f"最优适应度: {self.best_solution.fitness:.6f}"
        )
        
        return self.best_solution
    
    def get_best_solution(self) -> Optional[Solution]:
        """
        获取当前最优解
        
        Returns:
            最优解，如果尚未初始化则返回 None
        
        验证需求: 14.1-14.5
        """
        return self.best_solution
