"""
向量类实现

提供向量运算功能，包括加法、减法、标量乘法、点积、模长和归一化。
验证需求: 15.1-15.8
"""

import math
from typing import List, Union


class DimensionMismatchError(Exception):
    """维度不匹配错误"""
    pass


class Vector:
    """
    n维向量类
    
    支持基本的向量运算操作。
    """
    
    def __init__(self, components: Union[List[float], tuple]):
        """
        初始化向量
        
        Args:
            components: 向量的分量列表或元组
        
        Raises:
            ValueError: 如果分量列表为空
        """
        if not components:
            raise ValueError("向量分量不能为空")
        
        self.components = list(components)
        self.dimension = len(self.components)
    
    def __add__(self, other: 'Vector') -> 'Vector':
        """
        向量加法
        
        Args:
            other: 另一个向量
        
        Returns:
            两个向量的和
        
        Raises:
            DimensionMismatchError: 如果维度不匹配
        
        验证需求: 15.1
        """
        if self.dimension != other.dimension:
            raise DimensionMismatchError(
                f"向量维度不匹配: {self.dimension} vs {other.dimension}"
            )
        
        result = [a + b for a, b in zip(self.components, other.components)]
        return Vector(result)
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        """
        向量减法
        
        Args:
            other: 另一个向量
        
        Returns:
            两个向量的差
        
        Raises:
            DimensionMismatchError: 如果维度不匹配
        
        验证需求: 15.2
        """
        if self.dimension != other.dimension:
            raise DimensionMismatchError(
                f"向量维度不匹配: {self.dimension} vs {other.dimension}"
            )
        
        result = [a - b for a, b in zip(self.components, other.components)]
        return Vector(result)
    
    def __mul__(self, scalar: float) -> 'Vector':
        """
        向量标量乘法
        
        Args:
            scalar: 标量值
        
        Returns:
            向量与标量的乘积
        
        验证需求: 15.3
        """
        result = [c * scalar for c in self.components]
        return Vector(result)
    
    def __rmul__(self, scalar: float) -> 'Vector':
        """支持标量在左侧的乘法: scalar * vector"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector':
        """
        向量标量除法
        
        Args:
            scalar: 标量值
        
        Returns:
            向量除以标量的结果
        
        Raises:
            ZeroDivisionError: 如果标量为零
        """
        if scalar == 0:
            raise ZeroDivisionError("不能除以零")
        
        result = [c / scalar for c in self.components]
        return Vector(result)
    
    def dot(self, other: 'Vector') -> float:
        """
        向量点积
        
        Args:
            other: 另一个向量
        
        Returns:
            两个向量的点积
        
        Raises:
            DimensionMismatchError: 如果维度不匹配
        
        验证需求: 15.4
        """
        if self.dimension != other.dimension:
            raise DimensionMismatchError(
                f"向量维度不匹配: {self.dimension} vs {other.dimension}"
            )
        
        return sum(a * b for a, b in zip(self.components, other.components))
    
    def magnitude(self) -> float:
        """
        计算向量模长
        
        Returns:
            向量的模长（欧几里得范数）
        
        验证需求: 15.5
        """
        return math.sqrt(sum(c * c for c in self.components))
    
    def normalize(self) -> 'Vector':
        """
        归一化向量
        
        Returns:
            归一化后的单位向量，如果是零向量则返回零向量
        
        验证需求: 15.6, 15.8
        """
        mag = self.magnitude()
        
        # 零向量返回零向量
        if mag == 0:
            return Vector(self.components)
        
        return self / mag
    
    def __getitem__(self, index: int) -> float:
        """获取指定索引的分量"""
        return self.components[index]
    
    def __setitem__(self, index: int, value: float):
        """设置指定索引的分量"""
        self.components[index] = value
    
    def __len__(self) -> int:
        """返回向量维度"""
        return self.dimension
    
    def __repr__(self) -> str:
        """向量的字符串表示"""
        return f"Vector({self.components})"
    
    def __eq__(self, other: object) -> bool:
        """判断两个向量是否相等"""
        if not isinstance(other, Vector):
            return False
        
        if self.dimension != other.dimension:
            return False
        
        return all(abs(a - b) < 1e-10 for a, b in zip(self.components, other.components))
    
    @staticmethod
    def zero(dimension: int) -> 'Vector':
        """
        创建零向量
        
        Args:
            dimension: 向量维度
        
        Returns:
            指定维度的零向量
        """
        return Vector([0.0] * dimension)
