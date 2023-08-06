from setuptools import setup

setup(
    name='shap_on_image',
    version='0.1.1',    
    description='Display shap values on an image to simplify visualisation',
    url='https://github.com/philipperbd/shap_on_image',
    author='Philippe RAMBAUD',
    author_email='p.rambaud@outlook.fr',
    license='BSD 2-clause',
    packages=['shap_on_image'],
    install_requires=['matplotlib'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.8'
    ]
)
