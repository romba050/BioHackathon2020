# OpenProtein Dashboard

A small React app that visualises an OpenProtein training run: the predicted and
actual structure of a validation protein in 3D, training progress, and a
Ramachandran plot of predicted versus actual dihedral angles.

The training process serves the built app together with its data, so for normal
use you only need to build it once from the repository root:

```bash
make dashboard
```

and then start training as usual. The URL is printed when training starts.

## Frontend development

To work on the frontend with hot reloading, start training from the repository
root, then run the dev server here:

```bash
npm start
```

It opens on port 3000 and proxies data requests to the training process on port
5050 (see `proxy` in `package.json`). If training runs on another port, change
that value.

## Origin

Vendored from BioLib's `openprotein-dashboard` (MIT, see `LICENSE`), which is no
longer published under its original GitHub location.
