# OpenProtein Dashboard

A small React app that visualises an OpenProtein training run: the predicted and
actual structure of a validation protein in 3D, training progress, and a
Ramachandran plot of predicted versus actual dihedral angles.

It polls the JSON endpoint that the training process serves (see `dashboard.py`
in the repository root), by default `http://localhost:5000/graph`.

## Running

```
$ cd dashboard
$ npm install
$ npm start
```

Then start training from the repository root without `--hide-ui` and open
`http://localhost:3000/`.

If the training process is serving on a different port, point the dashboard at
it with `REACT_APP_BACKEND_URL`:

```
$ REACT_APP_BACKEND_URL=http://localhost:5050/graph npm start
```

## Origin

Vendored from BioLib's `openprotein-dashboard` (MIT, see `LICENSE`), which is no
longer published under its original GitHub location.
