"""
基本使用示例

演示如何使用潮汐算法优化简单的测试函数。
"""

import logging
import sys
sys.path.insert(0, '..')

from src.tidal_algorithm import (
    TidalOptimizer,
    Vector,
    Bounds,
    PhysicsParameters,
    TidalParameters
)
from benchmark_functions import sphere_function, rastrigin_function, ackley_function


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def optimize_sphere():
    """优化 Sphere 函数（单峰值）"""
    print("\n" + "="*60)
    print("优化 Sphere 函数")
    print("="*60)
    
    # 定义搜索空间
    dimensions = 10
    lower = Vector([-5.12] * dimensions)
    upper = Vector([5.12] * dimensions)
    bounds = Bounds(lower, upper)
    
    # 创建优化器
    optimizer = TidalOptimizer(
        objective_function=sphere_function,
        population_size=50,
        dimensions=dimensions,
        bounds=bounds,
        physics_params=PhysicsParameters(
            gravitational_constant=1.0,
            time_step=0.1,
            velocity_damping=0.95
        ),
        tidal_params=TidalParameters(
            density_threshold=5.0,
            flood_rate=0.1,
            stagnation_threshold=20,
            ebb_rate=0.2,
            mass_decay_rate=0.05
        )
    )
    
    # 运行优化
    best_solution = optimizer.optimize(max_iterations=100)
    
    # 输出结果
    print(f"\n最优解位置: {best_solution.position}")
    print(f"最优适应度: {best_solution.fitness:.6f}")
    print(f"理论最优值: 0.0")
    print(f"误差: {abs(best_solution.fitness):.6f}")


def optimize_rastrigin():
    """优化 Rastrigin 函数（多峰值）"""
    print("\n" + "="*60)
    print("优化 Rastrigin 函数")
    print("="*60)
    
    # 定义搜索空间
    dimensions = 10
    lower = Vector([-5.12] * dimensions)
    upper = Vector([5.12] * dimensions)
    bounds = Bounds(lower, upper)
    
    # 创建优化器
    optimizer = TidalOptimizer(
        objective_function=rastrigin_function,
        population_size=100,
        dimensions=dimensions,
        bounds=bounds,
        physics_params=PhysicsParameters(
            gravitational_constant=2.0,
            time_step=0.1,
            velocity_damping=0.95
        ),
        tidal_params=TidalParameters(
            density_threshold=8.0,
            flood_rate=0.15,
            stagnation_threshold=15,
            ebb_rate=0.25,
            mass_decay_rate=0.08
        )
    )
    
    # 运行优化
    best_solution = optimizer.optimize(max_iterations=200)
    
    # 输出结果
    print(f"\n最优解位置: {best_solution.position}")
    print(f"最优适应度: {best_solution.fitness:.6f}")
    print(f"理论最优值: 0.0")
    print(f"误差: {abs(best_solution.fitness):.6f}")


def optimize_ackley():
    """优化 Ackley 函数（多峰值）"""
    print("\n" + "="*60)
    print("优化 Ackley 函数")
    print("="*60)
    
    # 定义搜索空间
    dimensions = 10
    lower = Vector([-32.768] * dimensions)
    upper = Vector([32.768] * dimensions)
    bounds = Bounds(lower, upper)
    
    # 创建优化器
    optimizer = TidalOptimizer(
        objective_function=ackley_function,
        population_size=80,
        dimensions=dimensions,
        bounds=bounds,
        physics_params=PhysicsParameters(
            gravitational_constant=1.5,
            time_step=0.1,
            velocity_damping=0.95
        ),
        tidal_params=TidalParameters(
            density_threshold=6.0,
            flood_rate=0.12,
            stagnation_threshold=18,
            ebb_rate=0.22,
            mass_decay_rate=0.06
        )
    )
    
    # 运行优化
    best_solution = optimizer.optimize(max_iterations=150)
    
    # 输出结果
    print(f"\n最优解位置: {best_solution.position}")
    print(f"最优适应度: {best_solution.fitness:.6f}")
    print(f"理论最优值: 0.0")
    print(f"误差: {abs(best_solution.fitness):.6f}")


if __name__ == "__main__":
    print("潮汐算法 - 基本使用示例")
    print("="*60)
    
    # 运行示例
    optimize_sphere()
    optimize_rastrigin()
    optimize_ackley()
    
    print("\n" + "="*60)
    print("所有示例运行完成！")
    print("="*60)
