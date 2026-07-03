import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'tfm_martin'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='martinalangua',
    maintainer_email='martinalangua@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'prueba       = tfm_martin.prueba:main',
        'run = tfm_martin.prueba_motor_lineal:main',
        'coordinador = tfm_martin.coordinador_xarm_motorlin_850:main',
        'coordinador_celda_colaborativa = tfm_martin.coordinador_celda_colaborativa:main',
    ],
},
)
