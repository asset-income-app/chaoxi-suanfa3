"""
潮汐机制实现

实现涨潮和退潮机制，动态调整解的分布。
验证需求: 5.1-5.6, 6.1-6.7, 7.1-7.5, 8.1-8.6
"""

import logging
import math
import random
from typing import List, Tuple

from .vector import Vector
from .solution import Solution
from .bounds import Bounds
from .parameters import TidalParameters

logger = logging.getLogger(__name__)


class Region:
    """
    高密度区域
    
    表示解密度较高的区域。
    """
    
    def __init__(self, center: Vector, radius: float, density: float):
        """
        初始化区域
        
        Args:
            center: 区域中心
            radius: 区域半径
            density: 区域密度
        """
        self.center = center
        self.radius = radius
        self.density = density
    
    def __repr__(self) -> str:
        return f"Region(center={self.center}, radius={self.radius:.2f}, density={self.density:.2f})"


class TidalMechanism:
    """
    潮汐机制
    
    实现涨潮（在高密度区域生成新解）和退潮（淘汰停滞解）机制。
    """
    
    def __init__(self, params: TidalParameters):
        """
        初始化潮汐机制
        
        Args:
            params: 潮汐参数
        """
        self.params = params
    
    def detect_high_density_regions(
        self,
        solutions: List[Solution]
    ) -> List[Region]:
        """
        检测高密度区域
        
        Args:
            solutions: 解的列表
        
        Returns:
            高密度区域列表
        
        验证需求: 5.1-5.6
        """
        if not solutions:
            return []
        
        regions = []
        processed = set()
        
        for i, solution in enumerate(solutions):
            if i in processed:
                continue
            
            # 计算以当前解为中心的区域内的解数量
            neighbors = []
            neighbor_indices = []
            
            for j, other in enumerate(solutions):
                distance = (solution.position - other.position).magnitude()
                if distance <= self.params.detection_radius:
                    neighbors.append(other)
                    neighbor_indices.append(j)
            
            # 计算密度
            volume = self._sphere_volume(
                self.params.detection_radius,
                solution.dimension
            )
            density = len(neighbors) / volume if volume > 0 else 0
            
            # 如果密度超过阈值，创建区域
            if density > self.params.density_threshold:
                center = self._compute_center_of_mass(neighbors)
                region = Region(center, self.params.detection_radius, density)
                regions.append(region)
                
                # 标记所有邻居为已处理
                for idx in neighbor_indices:
                    processed.add(idx)
            else:
                processed.add(i)
        
        return regions
    
    def flood_tide(
        self,
        region: Region,
        existing_solutions: List[Solution],
        bounds: Bounds
    ) -> List[Solution]:
        """
        涨潮机制：在高密度区域生成新解
        
        Args:
            region: 高密度区域
            existing_solutions: 现有解列表
            bounds: 搜索空间边界
        
        Returns:
            新生成的解列表
        
        验证需求: 6.1-6.7
        """
        # 计算要生成的新解数量
        num_new_solutions = int(len(existing_solutions) * self.params.flood_rate)
        
        if num_new_solutions == 0:
            return []
        
        new_solutions = []
        
        for _ in range(num_new_solutions):
            # 在区域中心附近随机生成位置
            offset = self._random_vector_in_sphere(
                region.radius * 0.5,
                region.center.dimension
            )
            new_position = region.center + offset
            
            # 确保新位置在边界内
            new_position = bounds.clamp(new_position)
            
            # 创建新解
            new_solution = Solution(
                position=new_position,
                velocity=Vector.zero(region.center.dimension),
                acceleration=Vector.zero(region.center.dimension),
                mass=1.0,  # 初始质量
                fitness=0.0,
                stagnation_counter=0
            )
            
            new_solutions.append(new_solution)
        
        return new_solutions
    
    def detect_stagnation(
        self,
        solution: Solution
    ) -> bool:
        """
        检测解是否停滞
        
        Args:
            solution: 要检查的解
        
        Returns:
            如果解停滞返回 True，否则返回 False
        
        验证需求: 7.1-7.5
        """
        # 计算速度大小
        velocity_magnitude = solution.velocity.magnitude()
        
        # 检查速度是否接近零
        if velocity_magnitude < self.params.movement_threshold:
            solution.stagnation_counter += 1
        else:
            solution.stagnation_counter = 0
        
        # 判断是否停滞
        return solution.stagnation_counter >= self.params.stagnation_threshold
    
    def ebb_tide(
        self,
        solutions: List[Solution]
    ) -> List[Solution]:
        """
        退潮机制：淘汰停滞的解
        
        Args:
            solutions: 解的列表
        
        Returns:
            过滤后的解列表
        
        验证需求: 8.1-8.6
        """
        if not solutions:
            return []
        
        # 对停滞的解应用质量衰减
        for solution in solutions:
            if solution.stagnation_counter > 0:
                solution.mass *= (1 - self.params.mass_decay_rate)
        
        # 按质量降序排序
        sorted_solutions = sorted(solutions, key=lambda s: s.mass, reverse=True)
        
        # 计算最小种群大小
        min_population_size = max(
            int(len(solutions) * (1 - self.params.ebb_rate)),
            1
        )
        
        # 移除质量过低的解，但保留最小种群数量
        filtered_solutions = []
        for solution in sorted_solutions:
            if solution.mass >= self.params.min_mass or len(filtered_solutions) < min_population_size:
                filtered_solutions.append(solution)
            
            if len(filtered_solutions) >= len(solutions):
                break
        
        # 确保至少保留最小数量的解
        if len(filtered_solutions) < min_population_size:
            filtered_solutions = sorted_solutions[:min_population_size]
        
        return filtered_solutions
    
    @staticmethod
    def _sphere_volume(radius: float, dimension: int) -> float:
        """
        计算 n 维球体的体积
        
        Args:
            radius: 半径
            dimension: 维度
        
        Returns:
            体积
        """
        if dimension == 1:
            return 2 * radius
        elif dimension == 2:
            return math.pi * radius ** 2
        elif dimension == 3:
            return (4.0 / 3.0) * math.pi * radius ** 3
        else:
            # 使用通用公式: V = π^(n/2) * r^n / Γ(n/2 + 1)
            # 简化计算，使用近似
            return (math.pi ** (dimension / 2)) * (radius ** dimension) / math.gamma(dimension / 2 + 1)
    
    @staticmethod
    def _compute_center_of_mass(solutions: List[Solution]) -> Vector:
        """
        计算解群的质心
        
        Args:
            solutions: 解的列表
        
        Returns:
            质心位置
        """
        if not solutions:
            raise ValueError("解列表不能为空")
        
        dimension = solutions[0].dimension
        center = Vector.zero(dimension)
        
        for solution in solutions:
            center = center + solution.position
        
        center = center / len(solutions)
        
        return center
    
    @staticmethod
    def _random_vector_in_sphere(radius: float, dimension: int) -> Vector:
        """
        在 n 维球体内生成随机向量
        
        Args:
            radius: 球体半径
            dimension: 维度
        
        Returns:
            随机向量
        """
        # 生成随机方向
        components = [random.gauss(0, 1) for _ in range(dimension)]
        direction = Vector(components).normalize()
        
        # 生成随机半径（均匀分布在球体内）
        r = random.random() ** (1.0 / dimension) * radius
        
        return direction * r
