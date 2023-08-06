<div align="center">
<h1>create-pyscript-app</h1>

<div>Create PyScript web app project.</div>

<br />

<!-- Badges -->

![License](https://badgen.net/github/license/yeoularu/create-pyscript-app)
![Version](https://badgen.net/pypi/v/create-pyscript-app)
![Python Version](https://badgen.net/badge/python/>=3.6/blue)

<br />
<pre>pip install <a href="https://pypi.org/project/create-pyscript-app">create-pyscript-app</a></pre>

<br />
<img src="sample.gif" width="600" />
</div>

<br />

_you can see the preview site [HERE](https://yeoularu.github.io/pyscript-deploy-test/)_

<br />

## Creating an App

- You'll need to have **Python 3.6 or later version** on local development machine.

- **To run PyScript, Internet connection is required** because it use assets served on [https://pyscript.net](https://pyscript.net). If you want to download the source and build it yourself, follow the instructions in the [PyScript README.md](https://github.com/pyscript/pyscript/blob/main/README.md) file.

To create a new app, first install package with pip:

```sh
pip install create-pyscript-app
```

and run following command with project directory name(in this example, my-app):

```sh
python -m create-pyscript-app my-app
```

It will create a directory called `my-app` inside the current folder.

<br />
Inside that directory, it will generate the initial project structure:

```
my-app
├── index.html
├── index.css
├── app.py
└── favicon.ico
```

## Run the App in local browser

Once the installation is done, you can open your project foler:

```sh
cd my-app
```

and open local http server with run following command:

```sh
python -m http.server
```

check the following message about port (default :8000) and open url "http://localhost:8000/" in browser ([Chrome](https://www.google.com/chrome/) recommended).

---

## What is PyScript

~~**Py**thon + Java**Script**~~

> Python in the browser

PyScript is a framework that allows users to create rich Python applications in the browser using HTML's interface and the power of Pyodide, WASM, and modern web technologies.

## Reference

[PyScript](https://pyscript.net/)

[Create React App](https://create-react-app.dev/)

create-next-app ([Next.js](https://github.com/vercel/next.js))

## License

This project is [Apache-2.0](https://github.com/yeoularu/create-pyscript-app/blob/main/LICENSE) licensed. This software is powered by [PyScript](https://pyscript.net/) software.
