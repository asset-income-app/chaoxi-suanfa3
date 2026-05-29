"""
边界类实现

定义搜索空间的上下界限。
验证需求: 1.2, 1.7, 11.9, 11.10
"""

from .vector import Vector


class InvalidBoundsError(Exception):
    """无效边界错误"""
    pass


class Bounds:
    """
    搜索空间边界
    
    定义每个维度的上下界限。
    """
    
    def __init__(self, lower: Vector, upper: Vector):
        """
        初始化边界
        
        Args:
            lower: 下界向量
            upper: 上界向量
        
        Raises:
            InvalidBoundsError: 如果边界定义无效
        
        验证需求: 1.7, 11.9, 11.10
        """
        # 检查维度是否匹配
        if lower.dimension != upper.dimension:
            raise InvalidBoundsError(
                f"下界和上界维度不匹配: {lower.dimension} vs {upper.dimension}"
            )
        
        # 检查每个维度的下界是否小于上界
        for i in range(lower.dimension):
            if lower[i] >= upper[i]:
                raise InvalidBoundsError(
                    f"维度 {i} 的下界必须小于上界: {lower[i]} >= {upper[i]}"
                )
            
            # 检查是否包含无穷大或 NaN
            if not self._is_finite(lower[i]) or not self._is_finite(upper[i]):
                raise InvalidBoundsError(
                    f"维度 {i} 的边界包含无穷大或 NaN 值"
                )
        
        self.lower = lower
        self.upper = upper
        self.dimension = lower.dimension
    
    @staticmethod
    def _is_finite(value: float) -> bool:
        """检查值是否为有限数（不是无穷大或 NaN）"""
        import math
        return not (math.isnan(value) or math.isinf(value))
    
    def clamp(self, vector: Vector) -> Vector:
        """
        将向量限制在边界内
        
        Args:
            vector: 要限制的向量
        
        Returns:
            限制后的向量
        
        Raises:
            ValueError: 如果向量维度与边界维度不匹配
        
        验证需求: 10.1, 10.2, 10.3
        """
        if vector.dimension != self.dimension:
            raise ValueError(
                f"向量维度与边界维度不匹配: {vector.dimension} vs {self.dimension}"
            )
        
        clamped = []
        for i in range(self.dimension):
            value = vector[i]
            # 限制在下界和上界之间
            if value < self.lower[i]:
                value = self.lower[i]
            elif value > self.upper[i]:
                value = self.upper[i]
            clamped.append(value)
        
        return Vector(clamped)
    
    def is_within(self, vector: Vector) -> bool:
        """
        检查向量是否在边界内
        
        Args:
            vector: 要检查的向量
        
        Returns:
            如果向量在边界内返回 True，否则返回 False
        
        验证需求: 1.2, 4.6
        """
        if vector.dimension != self.dimension:
            return False
        
        for i in range(self.dimension):
            if vector[i] < self.lower[i] or vector[i] > self.upper[i]:
                return False
        
        return True
    
    def get_range(self, dimension: int) -> float:
        """
        获取指定维度的范围（上界 - 下界）
        
        Args:
            dimension: 维度索引
        
        Returns:
            该维度的范围
        """
        if dimension < 0 or dimension >= self.dimension:
            raise IndexError(f"维度索引超出范围: {dimension}")
        
        return self.upper[dimension] - self.lower[dimension]
    
    def __repr__(self) -> str:
        """边界的字符串表示"""
        return f"Bounds(lower={self.lower}, upper={self.upper})"
