"""
物理引擎实现

负责计算解之间的引力并更新解的物理状态。
验证需求: 3.1-3.6, 4.1-4.8, 10.1-10.4, 12.1-12.3
"""

import logging
import math

from .vector import Vector
from .solution import Solution
from .bounds import Bounds
from .parameters import PhysicsParameters

logger = logging.getLogger(__name__)


class PhysicsEngine:
    """
    物理引擎
    
    实现牛顿力学模拟，包括引力计算和物理状态更新。
    """
    
    def __init__(self, params: PhysicsParameters):
        """
        初始化物理引擎
        
        Args:
            params: 物理参数
        """
        self.params = params
    
    def compute_gravitational_force(
        self,
        s1: Solution,
        s2: Solution
    ) -> Vector:
        """
        计算两个解之间的引力
        
        使用公式: F = G × m1 × m2 / (r³ + ε)
        
        Args:
            s1: 第一个解
            s2: 第二个解
        
        Returns:
            从 s1 指向 s2 的引力向量
        
        验证需求: 3.1-3.6, 12.1
        """
        # 计算位置差向量
        delta = s2.position - s1.position
        
        # 计算距离
        distance = delta.magnitude()
        
        # 计算引力大小（1/r³ 衰减，使用 epsilon 保护）
        distance_cubed = distance ** 3
        force_magnitude = (
            self.params.gravitational_constant * s1.mass * s2.mass
        ) / (distance_cubed + self.params.distance_epsilon)
        
        # 限制最大引力（数值稳定性保护）
        if force_magnitude > self.params.max_force:
            force_magnitude = self.params.max_force
            logger.debug(f"引力被限制到最大值: {self.params.max_force}")
        
        # 计算引力方向（单位向量）
        if distance > 0:
            direction = delta / distance
        else:
            # 如果两个解在同一位置，引力为零
            direction = Vector.zero(s1.dimension)
        
        # 计算引力向量
        force = direction * force_magnitude
        
        return force
    
    def update_acceleration(
        self,
        solution: Solution,
        total_force: Vector
    ) -> None:
        """
        根据牛顿第二定律更新加速度
        
        F = ma => a = F / m
        
        Args:
            solution: 要更新的解
            total_force: 作用在解上的总受力
        
        验证需求: 4.1, 4.7
        """
        # 牛顿第二定律: a = F / m
        solution.acceleration = total_force / solution.mass
    
    def update_velocity(
        self,
        solution: Solution
    ) -> None:
        """
        根据加速度更新速度
        
        v_new = (v_old + a × Δt) × damping
        
        Args:
            solution: 要更新的解
        
        验证需求: 4.2, 4.3, 4.8, 12.3
        """
        # 更新速度: v = v + a * dt
        new_velocity = solution.velocity + solution.acceleration * self.params.time_step
        
        # 应用阻尼系数
        new_velocity = new_velocity * self.params.velocity_damping
        
        # 限制最大速度（防止速度爆炸）
        velocity_magnitude = new_velocity.magnitude()
        if velocity_magnitude > self.params.max_velocity:
            # 归一化并缩放到最大速度
            new_velocity = new_velocity.normalize() * self.params.max_velocity
            logger.debug(f"速度被限制到最大值: {self.params.max_velocity}")
        
        solution.velocity = new_velocity
    
    def update_position(
        self,
        solution: Solution,
        bounds: Bounds
    ) -> None:
        """
        根据速度更新位置并应用边界约束
        
        p_new = p_old + v × Δt
        
        Args:
            solution: 要更新的解
            bounds: 搜索空间边界
        
        验证需求: 4.4, 4.5, 4.6, 10.1-10.4
        """
        # 更新位置: p = p + v * dt
        new_position = solution.position + solution.velocity * self.params.time_step
        
        # 应用边界约束（限制在边界内）
        new_position = bounds.clamp(new_position)
        
        solution.position = new_position
    
    def update_solution(
        self,
        solution: Solution,
        total_force: Vector,
        bounds: Bounds
    ) -> None:
        """
        更新解的完整物理状态
        
        Args:
            solution: 要更新的解
            total_force: 作用在解上的总受力
            bounds: 搜索空间边界
        
        验证需求: 4.1-4.8
        """
        # 1. 更新加速度
        self.update_acceleration(solution, total_force)
        
        # 2. 更新速度
        self.update_velocity(solution)
        
        # 3. 更新位置
        self.update_position(solution, bounds)
