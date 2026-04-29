import os
from glob import glob
from setuptools import setup

package_name = 'project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Tell colcon to copy all .sdf files to the share directory
        (os.path.join('share', package_name), glob('*.sdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sam',
    maintainer_email='sam@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # This makes your autonomy script executable via ros2 run
            'autonomy_eval = project.autonomy_eval:main'
        ],
    },
)