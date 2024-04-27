from setuptools import setup, find_packages

setup(
    name="wcg",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "python-dotenv",
        "selenium",
        "webdriver-manager",
        "numpy",
        "pandas",
        "scipy",
        "openai",
        "llama-index",
        "transformers",
        "llama-index-llms-ollama",
        "install llama-index-llms-together",
        "scipy",
    ],
    python_requires=">=3.9",
)
