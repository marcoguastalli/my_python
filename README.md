# my_python
My Python

### dependencies to install
requirements.txt

### editable install (development mode)
`pip install -e .`

Installs the package as editable: instead of copying files to site-packages,
it creates a link to the source directory so any code change is immediately
active without reinstalling. Requires setup.py or pyproject.toml.
As a side effect it generates the `my_python.egg-info/` metadata folder.

### just a simple http server
`python3 -m http.server 81`

Test it with:
`curl http://localhost:81`

##### mac
```sh
python3 --version
pip3 --version
exit()
```
##### unix
```sh
python3 --version
pip3 --version
```
