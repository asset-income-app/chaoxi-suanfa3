"""
最简单的演示 - 只有10行代码！
"""

from src.tidal_algorithm import TidalOptimizer, Vector, Bounds

# 定义函数：找 x² + y² 的最小值
def my_func(pos):
    return -(pos[0]**2 + pos[1]**2)

# 创建优化器并运行
opt = TidalOptimizer(my_func, 30, 2, Bounds(Vector([-5,-5]), Vector([5,5])))
best = opt.optimize(30)

# 输出结果
print(f"最优解: x={best.position[0]:.4f}, y={best.position[1]:.4f}")
print(f"最小值: {-best.fitness:.4f} (理论值是0)")
