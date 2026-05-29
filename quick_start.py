"""
潮汐算法 - 5分钟快速入门

这个文件展示了如何用最简单的方式使用潮汐算法。
"""

from src.tidal_algorithm import TidalOptimizer, Vector, Bounds

print("="*60)
print("潮汐算法 - 快速入门示例")
print("="*60)

# ============================================================
# 示例 1: 最简单的使用方式
# ============================================================
print("\n【示例 1】找到函数 f(x, y) = x² + y² 的最小值")
print("-"*60)

# 步骤1: 定义你要优化的函数
# 注意：潮汐算法是最大化问题，所以要找最小值需要加负号
def my_function(position):
    x = position[0]  # 第一个变量
    y = position[1]  # 第二个变量
    return -(x**2 + y**2)  # 加负号转换为最大化问题

# 步骤2: 定义搜索范围
# 我们在 x∈[-10, 10], y∈[-10, 10] 的范围内搜索
lower_bound = Vector([-10, -10])  # 下界
upper_bound = Vector([10, 10])    # 上界
bounds = Bounds(lower_bound, upper_bound)

# 步骤3: 创建优化器
optimizer = TidalOptimizer(
    objective_function=my_function,  # 你的函数
    population_size=30,              # 种群大小（可以理解为同时尝试多少个点）
    dimensions=2,                    # 变量个数（x和y，所以是2）
    bounds=bounds                    # 搜索范围
)

# 步骤4: 运行优化
print("开始优化...")
best_solution = optimizer.optimize(max_iterations=50)  # 运行50次迭代

# 步骤5: 查看结果
print(f"\n找到的最优解:")
print(f"  x = {best_solution.position[0]:.6f}")
print(f"  y = {best_solution.position[1]:.6f}")
print(f"  函数值 = {-best_solution.fitness:.6f}")  # 记得转回来
print(f"  理论最优值 = 0.0 (在 x=0, y=0 处)")


# ============================================================
# 示例 2: 优化一个实际问题
# ============================================================
print("\n\n【示例 2】优化一个实际问题：找到最佳的产品定价")
print("-"*60)
print("假设你有一个产品，需要找到最佳的价格和广告预算")

def profit_function(position):
    """
    利润函数
    position[0] = 价格（元）
    position[1] = 广告预算（千元）
    """
    price = position[0]
    ad_budget = position[1]
    
    # 简化的利润模型（实际中你会用真实的业务模型）
    # 销量 = 基础销量 - 价格敏感度 + 广告效果
    sales = 1000 - 5 * price + 20 * ad_budget - 0.5 * ad_budget**2
    
    # 利润 = 销量 × (价格 - 成本) - 广告预算
    cost = 50  # 成本50元
    profit = sales * (price - cost) - ad_budget * 1000
    
    return profit  # 这次不用加负号，因为我们要最大化利润

# 定义搜索范围
# 价格: 60-200元
# 广告预算: 0-50千元
bounds = Bounds(
    lower=Vector([60, 0]),
    upper=Vector([200, 50])
)

# 创建优化器
optimizer = TidalOptimizer(
    objective_function=profit_function,
    population_size=40,
    dimensions=2,
    bounds=bounds
)

# 运行优化
print("开始寻找最佳定价策略...")
best = optimizer.optimize(max_iterations=50)

# 查看结果
print(f"\n最佳策略:")
print(f"  产品价格: {best.position[0]:.2f} 元")
print(f"  广告预算: {best.position[1]:.2f} 千元")
print(f"  预期利润: {best.fitness:.2f} 元")


# ============================================================
# 示例 3: 多变量优化
# ============================================================
print("\n\n【示例 3】优化多个变量（10个变量）")
print("-"*60)

def multi_variable_function(position):
    """简单的多变量函数：找到所有变量都接近0的点"""
    return -sum(x**2 for x in position.components)

# 10个变量，每个在[-5, 5]范围内
dimensions = 10
bounds = Bounds(
    lower=Vector([-5] * dimensions),
    upper=Vector([5] * dimensions)
)

optimizer = TidalOptimizer(
    objective_function=multi_variable_function,
    population_size=50,
    dimensions=dimensions,
    bounds=bounds
)

print(f"优化{dimensions}个变量...")
best = optimizer.optimize(max_iterations=50)

print(f"\n结果:")
print(f"  函数值: {-best.fitness:.6f}")
print(f"  前3个变量的值: {[f'{best.position[i]:.4f}' for i in range(3)]}")


# ============================================================
# 总结
# ============================================================
print("\n\n" + "="*60)
print("使用总结")
print("="*60)
print("""
使用潮汐算法只需要4步：

1. 定义函数: def my_func(position): ...
   - 如果要找最小值，函数前加负号
   - 如果要找最大值，直接返回

2. 定义范围: bounds = Bounds(lower, upper)
   - lower: 每个变量的最小值
   - upper: 每个变量的最大值

3. 创建优化器: optimizer = TidalOptimizer(...)
   - objective_function: 你的函数
   - population_size: 30-100（越大越准确但越慢）
   - dimensions: 变量个数
   - bounds: 搜索范围

4. 运行优化: best = optimizer.optimize(max_iterations=50)
   - max_iterations: 迭代次数（50-200通常够用）

就这么简单！
""")

print("\n运行完成！你可以修改上面的代码来优化你自己的问题。")
print("="*60)
