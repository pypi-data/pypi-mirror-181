[![Datalayer](https://assets.datalayer.design/datalayer-25.svg)](https://datalayer.io)

# 🪐 📖 Jupyter Mardown

> Create code-interactive websites from your Jupyter and ObservableHQ notebooks.

```bash
pip install -e .[test]
jupyter labextension develop . --overwrite
jupyter labextension list
jupyter server extension list
# open http://localhost:8686/api/jupyter/lab?token=60c1661cc408f978c309d04157af55c9588ff9557c9380e4fb50785750703da6
yarn jupyterlab
```

## See

- https://github.com/rafgraph/spa-github-pages
- https://github.com/fastai/fastpages

## Documentation

- Jupyter Mardown https://jupyter-react/...

## 🚧 Static Example

You can build a static example website that will be available under the `example/.out` folder.

```bash
# This will open example/.out/index.html in your browser.
make example-example && \
  open example/.out/index.html
```

You can deploy the example in your [Vercel](https://vercel.com) (former Now.js) account. Ccnfigure a vercel `datalayer-jupyter-react-example` project with:

- Build command: `yarn build:vercel`
- Output directory: `storybook/.out`.

Then run the following command to deploy in you vercel.

```bash 
# Deploy the example (if you have karma for).
# open https://api/jupyter.datalayer.io
make example-deploy
```
