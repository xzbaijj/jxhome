@property
    def native_value(self):
        """返回当前的温度数值（应用校准偏移）"""
        # 从 options 中获取用户配置的偏移量，默认为 0
        offset = self._entry.options.get("temp_offset", 0.0)
        base_temp = 25.5 # 假设的原始数据
        return base_temp + offset