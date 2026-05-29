"""
基准测试函数

提供常用的优化测试函数，包括单峰值和多峰值函数。
"""

import math
from src.tidal_algorithm import Vector


def sphere_function(position: Vector) -> float:
    """
    Sphere 函数（单峰值）
    
    全局最优解: f(0, 0, ..., 0) = 0
    搜索空间: [-5.12, 5.12]^n
    
    Args:
        position: 位置向量
    
    Returns:
        适应度值（取负数以转换为最大化问题）
    """
    sum_squares = sum(x ** 2 for x in position.components)
    return -sum_squares


def rastrigin_function(position: Vector) -> float:
    """
    Rastrigin 函数（多峰值）
    
    全局最优解: f(0, 0, ..., 0) = 0
    搜索空间: [-5.12, 5.12]^n
    
    Args:
        position: 位置向量
    
    Returns:
        适应度值（取负数以转换为最大化问题）
    """
    n = position.dimension
    A = 10
    
    sum_term = sum(
        x ** 2 - A * math.cos(2 * math.pi * x)
        for x in position.components
    )
    
    result = A * n + sum_term
    return -result


def ackley_function(position: Vector) -> float:
    """
    Ackley 函数（多峰值）
    
    全局最优解: f(0, 0, ..., 0) = 0
    搜索空间: [-32.768, 32.768]^n
    
    Args:
        position: 位置向量
    
    Returns:
        适应度值（取负数以转换为最大化问题）
    """
    n = position.dimension
    
    sum_squares = sum(x ** 2 for x in position.components)
    sum_cos = sum(math.cos(2 * math.pi * x) for x in position.components)
    
    term1 = -20 * math.exp(-0.2 * math.sqrt(sum_squares / n))
    term2 = -math.exp(sum_cos / n)
    
    result = term1 + term2 + 20 + math.e
    return -result


def rosenbrock_function(position: Vector) -> float:
    """
    Rosenbrock 函数（单峰值但难以优化）
    
    全局最优解: f(1, 1, ..., 1) = 0
    搜索空间: [-5, 10]^n
    
    Args:
        position: 位置向量
    
    Returns:
        适应度值（取负数以转换为最大化问题）
    """
    result = 0.0
    
    for i in range(position.dimension - 1):
        x_i = position[i]
        x_next = position[i + 1]
        result += 100 * (x_next - x_i ** 2) ** 2 + (1 - x_i) ** 2
    
    return -result


def griewank_function(position: Vector) -> float:
    """
    Griewank 函数（多峰值）
    
    全局最优解: f(0, 0, ..., 0) = 0
    搜索空间: [-600, 600]^n
    
    Args:
        position: 位置向量
    
    Returns:
        适应度值（取负数以转换为最大化问题）
    """
    sum_term = sum(x ** 2 for x in position.components) / 4000
    
    prod_term = 1.0
    for i, x in enumerate(position.components):
        prod_term *= math.cos(x / math.sqrt(i + 1))
    
    result = sum_term - prod_term + 1
    return -result
