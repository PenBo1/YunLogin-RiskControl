import configparser
from typing import Optional

class AppConfig:
    """
    读取、修改和保存 INI 配置文件的类
    """

    def __init__(self, config_file: str = 'config.ini'):
        """
        初始化配置管理器
        
        :param config_file: 配置文件路径 (默认: config.ini)
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        
        # 保留键名原始大小写
        self.config.optionxform = str
        
        # 读取配置文件
        self.config.read(self.config_file)

    # 获取 Fingerprint 配置
    @property
    def proxy(self) -> str:
        """获取代理设置"""
        return self.config.get('Fingerprint', 'proxy', fallback='local')

    @property
    def cpu_cores(self) -> int:
        """获取 CPU 核心数"""
        return self.config.getint('Fingerprint', 'cpu', fallback=8)

    @property
    def memory_gb(self) -> int:
        """获取内存大小 (GB)"""
        return self.config.getint('Fingerprint', 'mem', fallback=24)

    @property
    def webgl_enabled(self) -> bool:
        """获取 WebGL 是否启用"""
        return self.config.getboolean('Fingerprint', 'webgl', fallback=0)

    # 获取 OpenUrl 配置
    @property
    def target_url(self) -> str:
        """获取目标 URL"""
        return self.config.get('OpenUrl', 'url', fallback='https://192.168.0.242/gfk4')

    # 获取 Operation 配置
    @property
    def is_delete(self) -> bool:
        """获取是否删除操作"""
        return self.config.getboolean('Operation', 'isdelete', fallback=False)

    @property
    def is_quit(self) -> bool:
        """获取是否退出操作"""
        return self.config.getboolean('Operation', 'isquit', fallback=False)

    def print_current_config(self) -> None:
        """打印当前所有配置"""
        print("[Fingerprint]")
        print(f"  Proxy: {self.proxy}")
        print(f"  CPU Cores: {self.cpu_cores}")
        print(f"  Memory (GB): {self.memory_gb}")
        print(f"  WebGL Enabled: {self.webgl_enabled}")

        print("\n[OpenUrl]")
        print(f"  Target URL: {self.target_url}")

        print("\n[Operation]")
        print(f"  Is Delete: {self.is_delete}")
        print(f"  Is Quit: {self.is_quit}")

    def get_all_config(self) -> dict:
        """
        获取所有配置并返回字典格式
        返回一个字典，包含所有配置项。
        """
        return {
            'Fingerprint': {
                'proxy': self.proxy,
                'cpu': self.cpu_cores,
                'mem': self.memory_gb,
                'webgl': self.webgl_enabled,
            },
            'OpenUrl': {
                'url': self.target_url
            },
            'Operation': {
                'isdelete': self.is_delete,
                'isquit': self.is_quit
            }
        }

    def set_config(self, section: str, option: str, value: Optional[str]) -> None:
        """
        设置配置项，并保存到文件

        :param section: 配置节名
        :param option: 配置项名
        :param value: 配置项的新值
        """
        # 确保配置节存在，如果没有则添加该节
        if not self.config.has_section(section):
            self.config.add_section(section)
        
        # 设置新的值
        self.config.set(section, option, str(value))
        
        # 保存到配置文件
        self.save_config()

    def save_config(self) -> None:
        """保存当前配置到文件"""
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)
        print(f"配置已保存到 {self.config_file}")

    def load_default_config(self):
        """如果没有配置文件，则加载默认配置"""
        self.config.read_dict({
            'Fingerprint': {
                'proxy': 'local',
                'cpu': '8',
                'mem': '24',
                'webgl': '0'
            },
            'OpenUrl': {
                'url': 'https://192.168.0.242/gfk4'
            },
            'Operation': {
                'isdelete': 'False',
                'isquit': 'False'
            }
        })
        self.save_config()


# 使用示例
if __name__ == '__main__':
    # 初始化配置读取类
    config = AppConfig('config.ini')  # 替换为实际文件路径
    
    # 如果配置文件不存在，加载默认配置
    if not config.config.read('config.ini'):
        config.load_default_config()

    # 打印当前配置
    print("\n当前配置：")
    config.print_current_config()

    # 获取所有配置并打印
    all_config = config.get_all_config()
    print("\n所有配置：")
    print(all_config)

