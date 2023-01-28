from setuptools import setup
#'happy_face=happy_face.happy_face:main'

package_name = 'happy_face'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Ahmad',
    maintainer_email='a.alghooneh@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['CLC_node=happy_face.closed_loop_controller:main',
        ],
    },
)
