"""
Vector 类的单元测试

验证需求: 15.1-15.8
"""

import pytest
import math
from src.tidal_algorithm.vector import Vector, DimensionMismatchError


class TestVectorBasicOperations:
    """测试向量基本操作"""
    
    def test_vector_creation(self):
        """测试向量创建"""
        v = Vector([1.0, 2.0, 3.0])
        assert v.dimension == 3
        assert v[0] == 1.0
        assert v[1] == 2.0
        assert v[2] == 3.0
    
    def test_vector_empty_components(self):
        """测试空分量列表"""
        with pytest.raises(ValueError):
            Vector([])
    
    def test_vector_addition(self):
        """测试向量加法 - 需求 15.1"""
        v1 = Vector([1.0, 2.0, 3.0])
        v2 = Vector([4.0, 5.0, 6.0])
        result = v1 + v2
        
        assert result[0] == 5.0
        assert result[1] == 7.0
        assert result[2] == 9.0
    
    def test_vector_subtraction(self):
        """测试向量减法 - 需求 15.2"""
        v1 = Vector([4.0, 5.0, 6.0])
        v2 = Vector([1.0, 2.0, 3.0])
        result = v1 - v2
        
        assert result[0] == 3.0
        assert result[1] == 3.0
        assert result[2] == 3.0
    
    def test_vector_scalar_multiplication(self):
        """测试向量标量乘法 - 需求 15.3"""
        v = Vector([1.0, 2.0, 3.0])
        result = v * 2.0
        
        assert result[0] == 2.0
        assert result[1] == 4.0
        assert result[2] == 6.0
        
        # 测试左乘
        result2 = 2.0 * v
        assert result2[0] == 2.0
        assert result2[1] == 4.0
        assert result2[2] == 6.0
    
    def test_vector_scalar_division(self):
        """测试向量标量除法"""
        v = Vector([2.0, 4.0, 6.0])
        result = v / 2.0
        
        assert result[0] == 1.0
        assert result[1] == 2.0
        assert result[2] == 3.0
    
    def test_vector_division_by_zero(self):
        """测试除以零"""
        v = Vector([1.0, 2.0, 3.0])
        with pytest.raises(ZeroDivisionError):
            v / 0.0
    
    def test_vector_dot_product(self):
        """测试向量点积 - 需求 15.4"""
        v1 = Vector([1.0, 2.0, 3.0])
        v2 = Vector([4.0, 5.0, 6.0])
        result = v1.dot(v2)
        
        # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
        assert result == 32.0
    
    def test_vector_magnitude(self):
        """测试向量模长 - 需求 15.5"""
        v = Vector([3.0, 4.0])
        mag = v.magnitude()
        
        # sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5
        assert abs(mag - 5.0) < 1e-10
    
    def test_vector_normalize(self):
        """测试向量归一化 - 需求 15.6"""
        v = Vector([3.0, 4.0])
        normalized = v.normalize()
        
        # 归一化后模长应为 1
        assert abs(normalized.magnitude() - 1.0) < 1e-10
        
        # 方向应保持不变
        assert abs(normalized[0] - 0.6) < 1e-10
        assert abs(normalized[1] - 0.8) < 1e-10
    
    def test_vector_normalize_zero_vector(self):
        """测试零向量归一化 - 需求 15.8"""
        v = Vector([0.0, 0.0, 0.0])
        normalized = v.normalize()
        
        # 零向量归一化应返回零向量
        assert normalized[0] == 0.0
        assert normalized[1] == 0.0
        assert normalized[2] == 0.0


class TestVectorDimensionMismatch:
    """测试维度不匹配错误 - 需求 15.7"""
    
    def test_addition_dimension_mismatch(self):
        """测试加法维度不匹配"""
        v1 = Vector([1.0, 2.0])
        v2 = Vector([1.0, 2.0, 3.0])
        
        with pytest.raises(DimensionMismatchError):
            v1 + v2
    
    def test_subtraction_dimension_mismatch(self):
        """测试减法维度不匹配"""
        v1 = Vector([1.0, 2.0])
        v2 = Vector([1.0, 2.0, 3.0])
        
        with pytest.raises(DimensionMismatchError):
            v1 - v2
    
    def test_dot_product_dimension_mismatch(self):
        """测试点积维度不匹配"""
        v1 = Vector([1.0, 2.0])
        v2 = Vector([1.0, 2.0, 3.0])
        
        with pytest.raises(DimensionMismatchError):
            v1.dot(v2)


class TestVectorUtilities:
    """测试向量工具方法"""
    
    def test_vector_zero(self):
        """测试零向量创建"""
        v = Vector.zero(3)
        
        assert v.dimension == 3
        assert v[0] == 0.0
        assert v[1] == 0.0
        assert v[2] == 0.0
    
    def test_vector_equality(self):
        """测试向量相等性"""
        v1 = Vector([1.0, 2.0, 3.0])
        v2 = Vector([1.0, 2.0, 3.0])
        v3 = Vector([1.0, 2.0, 3.1])
        
        assert v1 == v2
        assert not (v1 == v3)
    
    def test_vector_repr(self):
        """测试向量字符串表示"""
        v = Vector([1.0, 2.0, 3.0])
        repr_str = repr(v)
        
        assert "Vector" in repr_str
        assert "1.0" in repr_str
