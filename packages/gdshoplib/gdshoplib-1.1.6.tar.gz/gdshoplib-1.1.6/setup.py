# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdshoplib',
 'gdshoplib.apps',
 'gdshoplib.apps.finance',
 'gdshoplib.apps.marketing',
 'gdshoplib.apps.platforms',
 'gdshoplib.apps.platforms.avito',
 'gdshoplib.apps.platforms.instagram',
 'gdshoplib.apps.platforms.ok',
 'gdshoplib.apps.platforms.tg',
 'gdshoplib.apps.platforms.ula',
 'gdshoplib.apps.platforms.vk',
 'gdshoplib.apps.platforms.yandex_market',
 'gdshoplib.apps.products',
 'gdshoplib.core',
 'gdshoplib.core.base',
 'gdshoplib.packages',
 'gdshoplib.packages.files',
 'gdshoplib.services',
 'gdshoplib.services.notion']

package_data = \
{'': ['*'], 'gdshoplib': ['templates/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'Pillow>=9.3.0,<10.0.0',
 'isort>=5.10.1,<6.0.0',
 'lxml>=4.9.1,<5.0.0',
 'orjson>=3.8.3,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'redis>=4.3.5,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'twine>=4.0.1,<5.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['gdshoplib = gdshoplib.core.cli:app']}

setup_kwargs = {
    'name': 'gdshoplib',
    'version': '1.1.6',
    'description': '',
    'long_description': '# Библиотека для управления магазином gdshop\n\nПользовательские объекты для высокоуровневой работы без привязки к слою данных. Предоставляет Python like интерфейс для работы с объектами\n\n- Получить информацию \n- Выполнить сценарий\n- Поддержка совместимости интерфейса между версиями\n\n## Finance\n\n- [ ] Информация о состоянии счетов\n- [ ] Операций с финансами\n- [ ] Статистика по финансам за периоды + Прогнозы\n- [ ] Расчет и контроль бюджетов\n- [ ] Сбор информации с площадок по финансам\n- [ ] Генерация отчетов\n\n## Marketing\n\n- [ ] Статистика рекламных компаний\n- [ ] Управление рекламными компаниями\n- [ ] Статистика воронок\n- [ ] Выгрузка информации с площадок\n- [ ] Генерация отчетов\n\n## Product\n- [ ] Получение информации о продукте\n- [ ] Обновление содержимого продукта\n- [ ] Синхронизация информации о продуктах между платформами\n- [ ] Работа с заказами\n- [ ] Работа с закупками\n- [ ] Выгрузка статистики\n- [ ] Оценка материалов\n- [ ] Работа с media\n- [ ] Работа с description\n\n## Platform\n- [ ] Генерация товарных фидов\n\n\n# Полезные ссылки\n\n## Описание товарного фида\n\nhttps://yandex.ru/support/partnermarket/export/yml.html\nhttps://drive.google.com/file/d/1kkKa0KU7iNOszyC2oQSGmHNwp3sRGKFb/view',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
