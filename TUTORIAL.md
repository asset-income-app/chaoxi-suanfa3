# 潮汐算法 - 零基础教程

## 什么是潮汐算法？

潮汐算法是一个**自动寻找最优解**的工具。

想象你在一个山谷里找最低点（或山顶找最高点），但你看不见整个地形。潮汐算法会：
1. 派出一群"探险者"（解）到处探索
2. 好的位置会吸引更多探险者（引力机制）
3. 在有希望的区域增加探险者（涨潮）
4. 淘汰长期没进展的探险者（退潮）

## 适合用在哪里？

✅ **适合的场景**：
- 你有一个函数，想找到让它最大或最小的输入值
- 你不知道函数的公式，只能计算结果（黑盒优化）
- 函数可能有很多局部最优点
- 例如：参数调优、资源分配、路径规划等

❌ **不适合的场景**：
- 简单的数学问题（用公式直接算更快）
- 需要极高精度的问题
- 变量超过1000个的超大规模问题

---

## 快速开始（3步）

### 第1步：定义你的函数

```python
def my_function(position):
    x = position[0]  # 第一个变量
    y = position[1]  # 第二个变量
    
    # 你的计算逻辑
    result = x**2 + y**2
    
    # 如果要找最小值，加负号
    return -result
```

**重要**：
- `position` 是一个向量，用 `position[0]`, `position[1]` 访问各个变量
- 潮汐算法是**最大化**问题，找最小值要加负号

### 第2步：定义搜索范围

```python
from src.tidal_algorithm import Vector, Bounds

# 定义每个变量的范围
lower = Vector([-10, -10])  # x和y的最小值
upper = Vector([10, 10])    # x和y的最大值
bounds = Bounds(lower, upper)
```

### 第3步：运行优化

```python
from src.tidal_algorithm import TidalOptimizer

# 创建优化器
optimizer = TidalOptimizer(
    objective_function=my_function,
    population_size=30,      # 种群大小
    dimensions=2,            # 变量个数
    bounds=bounds
)

# 运行
best = optimizer.optimize(max_iterations=50)

# 查看结果
print(f"最优解: x={best.position[0]}, y={best.position[1]}")
print(f"函数值: {best.fitness}")
```

---

## 完整示例

### 示例1：找函数最小值

```python
from src.tidal_algorithm import TidalOptimizer, Vector, Bounds

# 问题：找到 f(x,y) = x² + y² 的最小值
def objective(position):
    x, y = position[0], position[1]
    return -(x**2 + y**2)  # 加负号因为要找最小值

# 在 [-5, 5] × [-5, 5] 范围内搜索
bounds = Bounds(Vector([-5, -5]), Vector([5, 5]))

# 创建优化器
optimizer = TidalOptimizer(
    objective_function=objective,
    population_size=30,
    dimensions=2,
    bounds=bounds
)

# 运行优化
best = optimizer.optimize(max_iterations=50)

print(f"最优解: ({best.position[0]:.4f}, {best.position[1]:.4f})")
print(f"最小值: {-best.fitness:.4f}")  # 转回来
```

### 示例2：实际业务问题

```python
# 问题：优化产品定价和广告预算以最大化利润

def profit(position):
    price = position[0]        # 价格
    ad_budget = position[1]    # 广告预算（千元）
    
    # 销量模型
    sales = 1000 - 5*price + 20*ad_budget - 0.5*ad_budget**2
    
    # 利润 = 销量 × (价格 - 成本) - 广告费
    cost = 50
    return sales * (price - cost) - ad_budget * 1000

# 价格范围: 60-200元，广告预算: 0-50千元
bounds = Bounds(Vector([60, 0]), Vector([200, 50]))

optimizer = TidalOptimizer(
    objective_function=profit,
    population_size=40,
    dimensions=2,
    bounds=bounds
)

best = optimizer.optimize(max_iterations=50)

print(f"最佳价格: {best.position[0]:.2f} 元")
print(f"最佳广告预算: {best.position[1]:.2f} 千元")
print(f"最大利润: {best.fitness:.2f} 元")
```

---

## 参数说明

### 必需参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `objective_function` | 你要优化的函数 | `my_function` |
| `population_size` | 种群大小（同时尝试多少个点） | `30-100` |
| `dimensions` | 变量个数 | `2` |
| `bounds` | 搜索范围 | `Bounds(lower, upper)` |

### 可选参数

| 参数 | 说明 | 默认值 | 建议 |
|------|------|--------|------|
| `max_iterations` | 迭代次数 | - | 50-200 |
| `physics_params` | 物理参数 | 默认 | 通常不用改 |
| `tidal_params` | 潮汐参数 | 默认 | 通常不用改 |

---

## 常见问题

### Q1: 结果不够准确怎么办？

**方法1**: 增加迭代次数
```python
best = optimizer.optimize(max_iterations=200)  # 从50改到200
```

**方法2**: 增加种群大小
```python
optimizer = TidalOptimizer(
    ...,
    population_size=100  # 从30改到100
)
```

**方法3**: 多运行几次取最好的
```python
best_ever = None
for i in range(5):
    best = optimizer.optimize(max_iterations=50)
    if best_ever is None or best.fitness > best_ever.fitness:
        best_ever = best
```

### Q2: 运行太慢怎么办？

**方法1**: 减少种群大小
```python
population_size=20  # 从50改到20
```

**方法2**: 减少迭代次数
```python
max_iterations=30  # 从100改到30
```

**方法3**: 减少变量个数（如果可能）

### Q3: 如何优化多个变量？

```python
# 假设有5个变量
dimensions = 5

# 定义范围（每个变量可以不同）
lower = Vector([0, -10, 5, -100, 0])
upper = Vector([100, 10, 50, 100, 1])
bounds = Bounds(lower, upper)

def objective(position):
    # 访问各个变量
    var1 = position[0]
    var2 = position[1]
    var3 = position[2]
    var4 = position[3]
    var5 = position[4]
    
    # 你的计算
    return ...
```

### Q4: 如何知道优化是否成功？

```python
best = optimizer.optimize(max_iterations=100)

# 检查结果
print(f"最优适应度: {best.fitness}")
print(f"最优位置: {best.position}")

# 如果知道理论最优值，可以比较
theoretical_best = 0.0
error = abs(best.fitness - theoretical_best)
print(f"误差: {error}")
```

---

## 运行示例

### 方式1：运行快速入门
```bash
python quick_start.py
```

### 方式2：运行完整示例
```bash
cd examples
python basic_usage.py
```

### 方式3：自己写代码
创建一个新文件 `my_optimization.py`：
```python
from src.tidal_algorithm import TidalOptimizer, Vector, Bounds

# 你的函数
def my_func(position):
    # 你的逻辑
    return ...

# 你的范围
bounds = Bounds(...)

# 运行
optimizer = TidalOptimizer(...)
best = optimizer.optimize(max_iterations=50)
print(best.position)
```

---

## 进阶技巧

### 1. 调整参数以获得更好的结果

```python
from src.tidal_algorithm import PhysicsParameters, TidalParameters

# 自定义物理参数
physics = PhysicsParameters(
    gravitational_constant=2.0,  # 增大引力（加快收敛）
    velocity_damping=0.95        # 速度阻尼
)

# 自定义潮汐参数
tidal = TidalParameters(
    flood_rate=0.15,    # 涨潮率（增加探索）
    ebb_rate=0.25       # 退潮率（加快淘汰）
)

optimizer = TidalOptimizer(
    ...,
    physics_params=physics,
    tidal_params=tidal
)
```

### 2. 添加日志查看详细过程

```python
import logging

# 开启详细日志
logging.basicConfig(level=logging.INFO)

optimizer = TidalOptimizer(...)
best = optimizer.optimize(max_iterations=50)
```

### 3. 处理约束条件

如果你的问题有约束（比如 x + y ≤ 10），可以在函数中处理：

```python
def objective_with_constraint(position):
    x, y = position[0], position[1]
    
    # 检查约束
    if x + y > 10:
        return float('-inf')  # 不满足约束，返回极差值
    
    # 正常计算
    return -(x**2 + y**2)
```

---

## 总结

使用潮汐算法就这么简单：

1. **定义函数** - 告诉算法你要优化什么
2. **定义范围** - 告诉算法在哪里搜索
3. **运行优化** - 让算法自动寻找最优解

现在就试试 `python quick_start.py` 吧！

有问题随时查看 `README.md` 或示例代码。
