"""
参数类实现

定义物理参数和潮汐参数。
验证需求: 11.1-11.10
"""


class InvalidParameterError(Exception):
    """无效参数错误"""
    pass


class PhysicsParameters:
    """
    物理参数
    
    包含引力常数、时间步长、速度阻尼等物理模拟参数。
    """
    
    def __init__(
        self,
        gravitational_constant: float = 1.0,
        time_step: float = 0.1,
        velocity_damping: float = 0.95,
        distance_epsilon: float = 1e-10,
        max_velocity: float = 10.0,
        max_force: float = 100.0
    ):
        """
        初始化物理参数
        
        Args:
            gravitational_constant: 引力常数 G（默认 1.0）
            time_step: 时间步长 Δt（默认 0.1）
            velocity_damping: 速度阻尼系数（默认 0.95，范围 [0, 1]）
            distance_epsilon: 距离最小值，避免除零（默认 1e-10）
            max_velocity: 最大速度限制（默认 10.0）
            max_force: 最大引力限制（默认 100.0）
        
        Raises:
            InvalidParameterError: 如果参数值无效
        
        验证需求: 11.4, 11.5, 11.6
        """
        # 验证引力常数
        if gravitational_constant <= 0:
            raise InvalidParameterError(
                f"引力常数必须为正数: {gravitational_constant}"
            )
        
        # 验证时间步长
        if time_step <= 0:
            raise InvalidParameterError(
                f"时间步长必须为正数: {time_step}"
            )
        
        # 验证速度阻尼
        if not (0 <= velocity_damping <= 1):
            raise InvalidParameterError(
                f"速度阻尼必须在 [0, 1] 范围内: {velocity_damping}"
            )
        
        # 验证距离 epsilon
        if distance_epsilon <= 0:
            raise InvalidParameterError(
                f"距离 epsilon 必须为正数: {distance_epsilon}"
            )
        
        # 验证最大速度
        if max_velocity <= 0:
            raise InvalidParameterError(
                f"最大速度必须为正数: {max_velocity}"
            )
        
        # 验证最大引力
        if max_force <= 0:
            raise InvalidParameterError(
                f"最大引力必须为正数: {max_force}"
            )
        
        self.gravitational_constant = gravitational_constant
        self.time_step = time_step
        self.velocity_damping = velocity_damping
        self.distance_epsilon = distance_epsilon
        self.max_velocity = max_velocity
        self.max_force = max_force
    
    def __repr__(self) -> str:
        """参数的字符串表示"""
        return (
            f"PhysicsParameters("
            f"G={self.gravitational_constant}, "
            f"dt={self.time_step}, "
            f"damping={self.velocity_damping}, "
            f"epsilon={self.distance_epsilon}, "
            f"max_velocity={self.max_velocity}, "
            f"max_force={self.max_force})"
        )


class TidalParameters:
    """
    潮汐参数
    
    包含涨潮和退潮机制的参数。
    """
    
    def __init__(
        self,
        density_threshold: float = 5.0,
        flood_rate: float = 0.1,
        stagnation_threshold: int = 20,
        ebb_rate: float = 0.2,
        mass_decay_rate: float = 0.05,
        min_mass: float = 1e-6,
        movement_threshold: float = 1e-4,
        detection_radius: float = 1.0
    ):
        """
        初始化潮汐参数
        
        Args:
            density_threshold: 高密度阈值（默认 5.0）
            flood_rate: 涨潮生成率（默认 0.1，范围 (0, 1]）
            stagnation_threshold: 停滞阈值（默认 20 次迭代）
            ebb_rate: 退潮淘汰率（默认 0.2，范围 (0, 1]）
            mass_decay_rate: 质量衰减率（默认 0.05，范围 (0, 1]）
            min_mass: 最小质量阈值（默认 1e-6）
            movement_threshold: 移动阈值，用于停滞检测（默认 1e-4）
            detection_radius: 高密度区域检测半径（默认 1.0）
        
        Raises:
            InvalidParameterError: 如果参数值无效
        
        验证需求: 11.7, 11.8
        """
        # 验证密度阈值
        if density_threshold <= 0:
            raise InvalidParameterError(
                f"密度阈值必须为正数: {density_threshold}"
            )
        
        # 验证涨潮率
        if not (0 < flood_rate <= 1):
            raise InvalidParameterError(
                f"涨潮率必须在 (0, 1] 范围内: {flood_rate}"
            )
        
        # 验证停滞阈值
        if stagnation_threshold <= 0:
            raise InvalidParameterError(
                f"停滞阈值必须为正整数: {stagnation_threshold}"
            )
        
        # 验证退潮率
        if not (0 < ebb_rate <= 1):
            raise InvalidParameterError(
                f"退潮率必须在 (0, 1] 范围内: {ebb_rate}"
            )
        
        # 验证质量衰减率
        if not (0 < mass_decay_rate <= 1):
            raise InvalidParameterError(
                f"质量衰减率必须在 (0, 1] 范围内: {mass_decay_rate}"
            )
        
        # 验证最小质量
        if min_mass <= 0:
            raise InvalidParameterError(
                f"最小质量必须为正数: {min_mass}"
            )
        
        # 验证移动阈值
        if movement_threshold <= 0:
            raise InvalidParameterError(
                f"移动阈值必须为正数: {movement_threshold}"
            )
        
        # 验证检测半径
        if detection_radius <= 0:
            raise InvalidParameterError(
                f"检测半径必须为正数: {detection_radius}"
            )
        
        self.density_threshold = density_threshold
        self.flood_rate = flood_rate
        self.stagnation_threshold = stagnation_threshold
        self.ebb_rate = ebb_rate
        self.mass_decay_rate = mass_decay_rate
        self.min_mass = min_mass
        self.movement_threshold = movement_threshold
        self.detection_radius = detection_radius
    
    def __repr__(self) -> str:
        """参数的字符串表示"""
        return (
            f"TidalParameters("
            f"density_threshold={self.density_threshold}, "
            f"flood_rate={self.flood_rate}, "
            f"stagnation_threshold={self.stagnation_threshold}, "
            f"ebb_rate={self.ebb_rate}, "
            f"mass_decay_rate={self.mass_decay_rate}, "
            f"min_mass={self.min_mass}, "
            f"movement_threshold={self.movement_threshold}, "
            f"detection_radius={self.detection_radius})"
        )
