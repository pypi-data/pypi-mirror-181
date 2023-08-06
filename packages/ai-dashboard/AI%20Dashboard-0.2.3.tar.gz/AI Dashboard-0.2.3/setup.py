from setuptools import find_packages, setup

from ai_dashboard import __version__

requirements = [
    "marko==1.2.2",
    "requests>=2.0.0",
    "kaleido==0.1.0",
    "plotly==5.3.1",
]


test_requirements = [
    "pytest",
    "pytest-xdist",
    "pytest-cov",
]


setup(
    name="AI Dashboard",
    version=__version__,
    url="https://relevance.ai/",
    author="Relevance AI",
    author_email="dev@relevance.ai",
    packages=find_packages(),
    setup_requires=["wheel"],
    install_requires=requirements,
    package_data={
        "": [
            "*.ini",
        ]
    },
    extras_require=dict(
        tests=test_requirements,
    ),
)
