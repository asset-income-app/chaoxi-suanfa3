"""
解类实现

表示优化问题的一个候选解，包含位置、速度、加速度和质量等物理属性。
验证需求: 1.1-1.4
"""

from .vector import Vector


class Solution:
    """
    候选解
    
    包含解的物理状态（位置、速度、加速度）和质量、适应度等属性。
    """
    
    def __init__(
        self,
        position: Vector,
        velocity: Vector = None,
        acceleration: Vector = None,
        mass: float = 1.0,
        fitness: float = 0.0,
        stagnation_counter: int = 0
    ):
        """
        初始化解
        
        Args:
            position: 解在搜索空间中的位置
            velocity: 解的速度向量（默认为零向量）
            acceleration: 解的加速度向量（默认为零向量）
            mass: 解的质量（默认为 1.0）
            fitness: 解的适应度值（默认为 0.0）
            stagnation_counter: 停滞计数器（默认为 0）
        
        Raises:
            ValueError: 如果质量不为正数或停滞计数器为负数
        
        验证需求: 1.3, 1.4
        """
        if mass <= 0:
            raise ValueError(f"质量必须为正数: {mass}")
        
        if stagnation_counter < 0:
            raise ValueError(f"停滞计数器必须为非负整数: {stagnation_counter}")
        
        self.position = position
        self.dimension = position.dimension
        
        # 如果未提供速度和加速度，初始化为零向量
        self.velocity = velocity if velocity is not None else Vector.zero(self.dimension)
        self.acceleration = acceleration if acceleration is not None else Vector.zero(self.dimension)
        
        # 验证速度和加速度的维度
        if self.velocity.dimension != self.dimension:
            raise ValueError(
                f"速度维度与位置维度不匹配: {self.velocity.dimension} vs {self.dimension}"
            )
        
        if self.acceleration.dimension != self.dimension:
            raise ValueError(
                f"加速度维度与位置维度不匹配: {self.acceleration.dimension} vs {self.dimension}"
            )
        
        self.mass = mass
        self.fitness = fitness
        self.stagnation_counter = stagnation_counter
    
    def clone(self) -> 'Solution':
        """
        创建解的深拷贝
        
        Returns:
            解的副本
        """
        return Solution(
            position=Vector(self.position.components),
            velocity=Vector(self.velocity.components),
            acceleration=Vector(self.acceleration.components),
            mass=self.mass,
            fitness=self.fitness,
            stagnation_counter=self.stagnation_counter
        )
    
    def __repr__(self) -> str:
        """解的字符串表示"""
        return (
            f"Solution(position={self.position}, "
            f"velocity={self.velocity}, "
            f"acceleration={self.acceleration}, "
            f"mass={self.mass:.4f}, "
            f"fitness={self.fitness:.4f}, "
            f"stagnation_counter={self.stagnation_counter})"
        )
