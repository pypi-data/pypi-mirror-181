from distutils.core import setup


setup(
    name="pytorch-model-trainer",
    version="0.1.3",
    license="MIT",
    description="A tool to train pytorch models implementing an interface similar to keras",
    author="Matthias Pijarowski",
    author_email="pijarowski.matthias@gmail.com",
    url="https://gitlab.com/pijarowski.matthias/pytorch_trainer",
    download_url="https://gitlab.com/pijarowski.matthias/pytorch_trainer/-/archive/v0.1/pytorch_trainer-v0.1.3.tar.gz",
    packages=["pytorch_trainer", "pytorch_trainer.metrics", "pytorch_trainer.callbacks"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ]
)
