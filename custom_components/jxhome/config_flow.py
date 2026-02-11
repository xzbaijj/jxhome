from homeassistant import config_entries
from homeassistant.core import callback, HomeAssistant
from homeassistant.data_entry_flow import FlowResult
import voluptuous as vol
from .const import DOMAIN

class JXHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理初次添加集成时的逻辑"""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name", default="杰效设备"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """关联选项流（点击配置按钮时调用）"""
        return JXHomeOptionsFlowHandler(config_entry)

    @staticmethod
    @callback
    def async_supports_device_config_entry_flow(config_entry):
        """支持设备级别配置"""
        return True


class JXHomeOptionsFlowHandler(config_entries.OptionsFlow):
    """处理集成选项流的逻辑 - 在集成配置中显示参数配置选项"""

    def __init__(self, config_entry):
        self.config_entry = config_entry
        self.read_data = {}

    async def async_step_init(self, user_input=None):
        """选项流的起始步骤 - 选择操作"""
        if user_input is not None:
            action = user_input.get("action")
            if action == "read":
                return await self.async_step_read_params()
            elif action == "save":
                return await self.async_step_save_params()
        
        # 显示操作选择菜单
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("action"): vol.In({
                    "read": " 读取参数",
                    "save": " 修改参数"
                })
            }),
            description_placeholders={
                "description": "请选择要执行的操作"
            }
        )

    async def async_step_read_params(self, user_input=None):
        """读取参数步骤"""
        if user_input is None:
            # 从设备读取参数（通过 MQTT）
            self.read_data = await self._read_from_device()
            
            # 显示读取到的参数
            return self.async_show_form(
                step_id="read_params",
                data_schema=vol.Schema({
                    vol.Required(
                        "current_ratio",
                        default=self.read_data.get("current_ratio", 1.0)
                    ): float,
                    vol.Required(
                        "voltage_ratio",
                        default=self.read_data.get("voltage_ratio", 1.0)
                    ): float,
                }),
                description_placeholders={
                    "info": "以下是从设备读取的参数值（只读）"
                }
            )
        else:
            # 用户查看完参数后，返回主菜单
            return await self.async_step_init()

    async def async_step_save_params(self, user_input=None):
        """保存参数步骤"""
        if user_input is not None:
            # 保存参数到配置条目选项
            config_data = {
                "current_ratio": user_input.get("current_ratio", 1.0),
                "voltage_ratio": user_input.get("voltage_ratio", 1.0),
            }
            
            # 发送参数到设备（通过 MQTT）
            await self._save_to_device(config_data)
            
            # 保存到 Home Assistant 选项
            return self.async_create_entry(title="", data=config_data)
        
        # 获取当前的配置值，作为默认值
        current_current_ratio = self.config_entry.options.get("current_ratio", 1.0)
        current_voltage_ratio = self.config_entry.options.get("voltage_ratio", 1.0)
        
        # 定义保存参数的表单
        return self.async_show_form(
            step_id="save_params",
            data_schema=vol.Schema({
                vol.Required("current_ratio", default=current_current_ratio): float,
                vol.Required("voltage_ratio", default=current_voltage_ratio): float,
            }),
            description_placeholders={
                "current_ratio_help": "电流互感器变比（用于校准电流测量值）",
                "voltage_ratio_help": "电压互感器变比（用于校准电压测量值）",
            }
        )

    async def _read_from_device(self):
        """从设备通过 MQTT 读取参数"""
        # TODO: 实现 MQTT 读取逻辑
        # 这里应该发送 MQTT 消息到设备，请求设备回复当前参数
        # 然后解析设备的回复并返回
        return {
            "current_ratio": self.config_entry.options.get("current_ratio", 1.0),
            "voltage_ratio": self.config_entry.options.get("voltage_ratio", 1.0),
        }

    async def _save_to_device(self, config_data):
        """通过 MQTT 保存参数到设备"""
        # TODO: 实现 MQTT 保存逻辑
        # 这里应该发送 MQTT 消息到设备，包含新的参数值
        pass
