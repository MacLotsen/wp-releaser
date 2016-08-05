from setuptools import setup

if __name__ == '__main__':
    setup(
        name='wp-releaser',
        version='1.0.0',
        license='GNU LGPLv3',
        author='Erik Nijenhuis',
        author_email='erik@xerdi.com',
        scripts=['wp_releaser.py'],
        entry_points={
            'console_scripts':['wp-releaser = wp_releaser:main']
        }
    )