from setuptools import setup

package_name = 'drone_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
   data_files=[
    ('share/ament_index/resource_index/packages',
        ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),

    # ADD THESE ↓↓↓
    ('share/' + package_name + '/launch', ['launch/vision.launch.py']),
    ('share/' + package_name + '/config', ['config/color_params.yaml']),
],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Vision node for drone tracking',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'vision_node = drone_vision.vision_node:main',
        ],
    },
)
