# netbox_reports_plugin
## Обзор
Плагин NetBox для инвентаризации 
## Установка плагина
Активируйте виртуальное окружение:
```
source /opt/netbox/venv/bin/activate
```
Установите плагин:
```
pip install netbox-reports-plugin
```
Перейдите в каталог с manage.py (/opt/netbox/netbox) и выполните миграции:
```
python3 manage.py migrate
```
Включите плагин в файле `configuration.py` (обычно он находится в `/opt/netbox/netbox/netbox/`), добавьте его имя в список `PLUGINS`:
```
PLUGINS = [
    'netbox_reports_plugin'
]
```
Перезапустите NetBox:
```
sudo systemctl restart netbox
```

## Процесс обновления пакета с заливанием на pypi
Изменяем setup.py в корне и по необходимости __init__ внутри функциональной директории из корня проекта билдим:
```
python setup.py sdist
```
Отправляем на pypi
```
twine upload dist/*
```

