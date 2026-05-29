# 潮汐算法 (Tidal Algorithm)

基于物理引力模型的优化算法，专门用于解决无梯度、不连续、多峰值的优化问题。

## 核心理念

潮汐算法将每个候选解视为具有质量的物理粒子，粒子之间通过牛顿引力定律相互作用：

- **引力计算**: F = G × m₁ × m₂ / (r³ + ε)
- **质量机制**: 质量越大的解（适应度高）产生更强的引力
- **物理演化**: 力 → 加速度 → 速度 → 位置
- **涨潮机制**: 在高密度区域自动生成新解
- **退潮机制**: 淘汰长期停滞的解

## 特性

- ✅ 无需梯度信息
- ✅ 处理不连续函数
- ✅ 有效探索多峰值空间
- ✅ 自适应种群大小
- ✅ 动态平衡探索与开发
- ✅ 数值稳定性保护
- ✅ 资源限制管理

## 安装

```bash
# 克隆仓库
git clone <repository-url>
cd tidal-algorithm

# 安装依赖（如果有）
pip install -r requirements.txt
```

## 快速开始

```python
from src.tidal_algorithm import TidalOptimizer, Vector, Bounds

# 定义目标函数
def objective_function(position: Vector) -> float:
    # 例如：Sphere 函数
    return -sum(x ** 2 for x in position.components)

# 定义搜索空间
dimensions = 10
bounds = Bounds(
    lower=Vector([-5.12] * dimensions),
    upper=Vector([5.12] * dimensions)
)

# 创建优化器
optimizer = TidalOptimizer(
    objective_function=objective_function,
    population_size=50,
    dimensions=dimensions,
    bounds=bounds
)

# 运行优化
best_solution = optimizer.optimize(max_iterations=100)

# 查看结果
print(f"最优解: {best_solution.position}")
print(f"最优适应度: {best_solution.fitness}")
```

## 参数说明

### 物理参数 (PhysicsParameters)

```python
from src.tidal_algorithm import PhysicsParameters

physics_params = PhysicsParameters(
    gravitational_constant=1.0,    # 引力常数 G
    time_step=0.1,                 # 时间步长 Δt
    velocity_damping=0.95,         # 速度阻尼系数 [0, 1]
    distance_epsilon=1e-10,        # 距离最小值（避免除零）
    max_velocity=10.0,             # 最大速度限制
    max_force=100.0                # 最大引力限制
)
```

### 潮汐参数 (TidalParameters)

```python
from src.tidal_algorithm import TidalParameters

tidal_params = TidalParameters(
    density_threshold=5.0,         # 高密度阈值
    flood_rate=0.1,                # 涨潮生成率 (0, 1]
    stagnation_threshold=20,       # 停滞阈值（迭代次数）
    ebb_rate=0.2,                  # 退潮淘汰率 (0, 1]
    mass_decay_rate=0.05,          # 质量衰减率 (0, 1]
    min_mass=1e-6,                 # 最小质量阈值
    movement_threshold=1e-4,       # 移动阈值（停滞检测）
    detection_radius=1.0           # 高密度区域检测半径
)
```

## 示例

### 示例 1: 单峰值函数（Sphere）

```python
from examples.benchmark_functions import sphere_function

optimizer = TidalOptimizer(
    objective_function=sphere_function,
    population_size=50,
    dimensions=10,
    bounds=Bounds(Vector([-5.12]*10), Vector([5.12]*10))
)

best = optimizer.optimize(max_iterations=100)
```

### 示例 2: 多峰值函数（Rastrigin）

```python
from examples.benchmark_functions import rastrigin_function

optimizer = TidalOptimizer(
    objective_function=rastrigin_function,
    population_size=100,
    dimensions=10,
    bounds=Bounds(Vector([-5.12]*10), Vector([5.12]*10)),
    physics_params=PhysicsParameters(gravitational_constant=2.0),
    tidal_params=TidalParameters(flood_rate=0.15, ebb_rate=0.25)
)

best = optimizer.optimize(max_iterations=200)
```

### 运行完整示例

```bash
cd examples
python basic_usage.py
```

## 参数调优建议

### 引力常数 (G)
- **过大**: 解快速聚集，可能陷入局部最优
- **过小**: 解移动缓慢，收敛速度慢
- **建议范围**: [0.1, 5.0]

### 时间步长 (Δt)
- **过大**: 数值不稳定，解可能越界
- **过小**: 收敛速度慢
- **建议范围**: [0.01, 0.5]

### 速度阻尼
- **过大**: 解快速停止，探索不足
- **过小**: 解持续振荡，难以收敛
- **建议范围**: [0.9, 0.99]

### 涨潮率
- **过大**: 种群爆炸，计算开销高
- **过小**: 多样性不足
- **建议范围**: [0.05, 0.2]

### 退潮率
- **过大**: 种群快速减少，可能丢失好解
- **过小**: 劣质解长期存在
- **建议范围**: [0.1, 0.3]

## 项目结构

```
tidal-algorithm/
├── src/
│   └── tidal_algorithm/
│       ├── __init__.py
│       ├── vector.py              # 向量运算
│       ├── bounds.py              # 边界定义
│       ├── solution.py            # 解的数据结构
│       ├── parameters.py          # 参数类
│       ├── physics_engine.py      # 物理引擎
│       ├── tidal_mechanism.py     # 潮汐机制
│       ├── fitness_evaluator.py   # 适应度评估器
│       └── tidal_optimizer.py     # 主优化器
├── examples/
│   ├── benchmark_functions.py     # 基准测试函数
│   └── basic_usage.py             # 基本使用示例
├── tests/
│   └── test_vector.py             # 单元测试
├── .kiro/
│   └── specs/
│       └── tidal-algorithm/
│           ├── design.md          # 设计文档
│           ├── requirements.md    # 需求文档
│           └── tasks.md           # 任务列表
└── README.md
```

## 算法流程

1. **初始化**: 在搜索空间中随机生成解群
2. **适应度评估**: 计算每个解的适应度并转换为质量
3. **引力计算**: 计算所有解对之间的引力
4. **物理更新**: 更新加速度、速度和位置
5. **涨潮**: 在高密度区域生成新解
6. **退潮**: 淘汰停滞的解
7. **重复**: 直到达到最大迭代次数或其他终止条件

## 性能考虑

- **时间复杂度**: O(T × N² × D)
  - T: 迭代次数
  - N: 种群大小
  - D: 搜索空间维度

- **空间复杂度**: O(N × D)

- **优化建议**:
  - 对于大规模问题，考虑减少种群大小
  - 使用空间分割优化邻近搜索
  - 并行化引力计算

## 适用场景

✅ **适合**:
- 无梯度信息的黑盒优化
- 不连续或非光滑函数
- 多峰值优化问题
- 组合优化问题
- 参数调优

❌ **不适合**:
- 有梯度信息且函数光滑（使用梯度下降更高效）
- 超高维问题（D > 1000）
- 需要精确解的问题

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 参考文献

本算法基于物理引力模型和群体智能算法的理念设计。

## 联系方式

如有问题或建议，请通过 Issue 联系。
