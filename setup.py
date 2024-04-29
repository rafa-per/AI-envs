import setuptools

setuptools.setup(
    name="AI-envs",
    version="0.1.4",
    author="Rafael Pereira",
    author_email="ranobrega@gmail.com",
    description="Ambientes do gym",
    url="https://github.com/rafa-per/AI-envs.git",
    project_urls={
        'Source': 'https://github.com/rafa-per/AI-envs.git',
        'Tracker': 'https://github.com/rafa-per/AI-envs.git/issues',
    },
    license="MIT",
    packages=['AI_envs', 'AI_envs.agente'],
    install_requires=['pygame', 'gym==0.17.2'],  # Exigindo a versão 0.17.2 do gym
    extras_require={
        'agente': ['tensorflow', 'numpy', 'pandas_datareader', 'yfinance'],  # Dependências adicionais para o módulo 'agente'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
