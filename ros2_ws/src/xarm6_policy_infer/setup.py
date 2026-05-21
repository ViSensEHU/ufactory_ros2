from setuptools import find_packages, setup

package_name = 'xarm6_policy_infer'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='isaac_sim',
    maintainer_email='isaac_sim@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'test_infer = xarm6_policy_infer.test_node:main',
            'infer = xarm6_policy_infer.real_node:main',
        ],
    },
)
