from extras.plugins import PluginConfig

class ReportsConfig(PluginConfig):
    name = 'netbox_reports_plugin'
    verbose_name = 'netbox_reports_plugin'
    description = 'netbox_reports_plugin'
    version = '0.1'
    author = 'Ilya Gulin'
    author_email = 'i.gulin@di-di.ru'
    base_url = 'netbox_reports_plugin'
    required_settings = []
    default_settings = {}


config = ReportsConfig
