"""杰效集成的常量"""
DOMAIN = "jxhome"
PLATFORMS = ["sensor", "button"]

# 传感器类型
SENSOR_TYPE_VOLTAGE = "voltage"
SENSOR_TYPE_CURRENT = "current"

# 配置参数步骤
CONFIG_STEP_INIT = "init"
CONFIG_STEP_READ = "read_params"
CONFIG_STEP_SAVE = "save_params"

# 默认参数值
DEFAULT_CURRENT_RATIO = 1.0
DEFAULT_VOLTAGE_RATIO = 1.0