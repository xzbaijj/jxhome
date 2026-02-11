# 杰效设备参数配置说明

## 设备级参数配置

### 访问方式
1. 进入 Home Assistant **设置** → **设备与服务** → **设备**
2. 找到 **杰效主控板** 设备
3. 点击设备卡片右上角的**三点菜单**（⋯）
4. 选择 **参数配置** 选项

### 功能说明

#### 读取参数
- 点击"读取参数"按钮
- 系统会从设备通过 MQTT 读取当前的电流和电压变比系数
- 显示设备上的当前参数值（只读）

#### 保存参数
- 点击"保存参数"按钮
- 输入新的电流变比系数和电压变比系数
- 点击提交后，系统会通过 MQTT 将参数发送到设备
- 参数也会保存到 Home Assistant 配置中

## 参数说明

### 电流变比系数 (current_ratio)
- 用于校准电流测量值
- 默认值：1.0
- 范围：建议 0.1-10.0

### 电压变比系数 (voltage_ratio)
- 用于校准电压测量值  
- 默认值：1.0
- 范围：建议 0.1-10.0

## MQTT 集成

目前 MQTT 读写函数位于 `config_flow.py` 中：
- `_read_from_device()` - 读取参数
- `_save_to_device()` - 保存参数

需要根据实际的设备协议进行实现。

### 实现 MQTT 读取
```python
async def _read_from_device(self):
    """从设备通过 MQTT 读取参数"""
    # TODO: 发送 MQTT 消息到设备
    # 订阅设备回复的 MQTT 主题
    # 解析并返回参数
    return {
        "current_ratio": 1.0,
        "voltage_ratio": 1.0,
    }
```

### 实现 MQTT 保存
```python
async def _save_to_device(self, config_data):
    """通过 MQTT 保存参数到设备"""
    # TODO: 发送 MQTT 消息到设备
    # 包含新的参数值
    pass
```
