from setuptools import setup, find_packages

setup(
    name='devops-auto-tools',
    version='1.0.0',    
    description='A Python project for eks,ssh manager',
    author='Baristi Trieu',
    author_email='ltqtrieu.0204@gmail.com',
    packages=find_packages(),
    license ='MIT',
    install_requires=[
        'simple_term_menu==1.4.1'
    ],
    
    entry_points={
        'console_scripts': [
            'eksm = tools.main:eksm',
            'sshm = tools.main:sshm',
        ]
    },
    
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)
