# personal.soda480.devops.test-pypi

## `devops-intc`

### Build Docker Image
```
docker image build -t pypi-test:latest .
```

### Run Docker Container
```
docker container run --rm -it -v $PWD:/code pypi-test:latest bash
```

### Build Package
```
python setup.py sdist bdist_wheel
```

### Publish Package

Publish to TestPyPi
```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=TOKEN
python -m twine upload --repository testpypi dist/*
```

Publish to PyPi
```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=TOKEN
python -m twine upload dist/*
```

### Install Package

Install from TestPyPi
```
pip install -i https://test.pypi.org/simple/ devops-intc
```

Install from PyPi
```
pip install devops-intc
```

### Test Package
```
say-hello
```