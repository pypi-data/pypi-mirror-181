## dataClay common

- protos: common grpc protocol buffers for dataclay

#### Protos

- Compile in javaclay

```
mvn protobuf:compile-custom -Pprotogen
```
to create just grpc-stubs or
```
mvn clean compile -Pprotogen
```
to compile all javaclay including new protos
- Compile in pyclay

```
pip install grpcio-tools protobufferize
python setup.py protobufferize
```

**NOTE**: if protbufferize cannot be installed via pip, please clone
it from https://github.com/bsc-dom/protobufferize and run `python setup.py install`

# Packaging Python

It's strongly recommended to use a virtual environment.

```bash
# Make sure you have the latest build and twine versions installed
python3 -m pip install --upgrade build twine

# Remove dist folder if exists
rm -rf dist/

# Build release distribution with date tag
python3 -m build -C--global-option=egg_info -C--global-option=--tag-build=$(date +%s)


# Publish package to PyPI
python3 -m twine upload dist/*
```

<!-- For testing -->
<!-- python3 -m twine upload --repository testpypi dist/* -->
