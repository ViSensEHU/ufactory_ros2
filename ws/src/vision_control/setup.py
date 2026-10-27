from setuptools import find_packages, setup

package_name = 'vision_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
                    ['launch/green_follower.launch.py']
                ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='javier.arambarri@ehu.eus',
    description='vision_control package',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'green_filter_node = vision_control.green_filter_node:main',
            'center_vs_node = vision_control.center_visual_servoing_node:main',
            'xarm_visual_servo_controller = vision_control.xarm_visual_servo_controller:main',
        ],
    },
)
