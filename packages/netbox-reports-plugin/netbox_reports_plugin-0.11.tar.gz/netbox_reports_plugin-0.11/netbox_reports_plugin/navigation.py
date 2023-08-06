from extras.plugins import PluginMenuItem

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_reports_plugin:reports_device_list",
        link_text="Инвентаризация",
        permissions=['netbox_reports_plugin.reports_device_list'],
    ),
)
