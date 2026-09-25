# OpenProtein

A PyTorch framework for tertiary protein structure prediction.

![Demo](demo.gif)


## Getting started

You need [uv](https://docs.astral.sh/uv/) for the Python side and Node.js for the dashboard frontend.

```bash
git clone https://github.com/romba050/BioHackathon2020.git
cd BioHackathon2020
make setup      # uv sync: installs Python 3.11/3.12 if needed and the pinned dependencies
make dashboard  # builds the live dashboard frontend, only needed once
make run        # trains the sample experiment
```

Training prints the dashboard URL as it starts. Open it in a browser to watch the model learn:

```
$ make run
------------------------
--- OpenProtein v0.1 ---
------------------------
2026-09-25 18:02:10: Live dashboard available at http://localhost:5050/
2026-09-25 18:02:10: Starting pre-processing of raw data...
...
2026-09-25 18:02:11: Train loss: 1.8581191301345825
2026-09-25 18:02:11: Validation loss: 42.28535 Train loss: 1.8581191301345825
...
2026-09-25 18:02:14: Training finished. The dashboard stays available at http://localhost:5050/ until you press Ctrl-C.
```

`make run` is just `uv run python __main__.py`. Useful flags:

- `--hide-ui` runs without the dashboard, for scripts and CI.
- `--dashboard-port 8000` serves the dashboard on another port. If the port is taken, a free one is chosen automatically and printed.
- `--help` lists all options, including those of the selected experiment.

## Live dashboard

![Alt text](examplemodelrun.png?raw=true "OpenProtein")

The dashboard is a small React app in the [`dashboard/`](dashboard/) folder. It renders the predicted and actual structure of a validation protein in 3D, plots training progress, and draws a Ramachandran plot of predicted versus actual dihedral angles.

The training process serves the built app and its data from the same port (see `dashboard.py`), so nothing needs to be configured. Training still works if the frontend has not been built; the URL then shows the build command instead, and the raw data stays available at `/graph`.

To work on the frontend itself, see [`dashboard/README.md`](dashboard/README.md).

The dashboard was originally published by BioLib as `openprotein-dashboard` under the MIT license and is vendored here because the original repository is no longer online.

## Developing a Predictive Model

See `models.py` for examples of how to create your own model.

To run the linter and tests locally:

```bash
git ls-files '*.py' | xargs uv run pylint --rcfile=.pylintrc
uv run python -m pytest
```

To run pylint on every commit, run `git config core.hooksPath git-hooks`.

## Using a Predictive Model

See `prediction.py` for examples of how to use pre-trained models.

## Memory Usage

OpenProtein includes a preprocessing tool (`preprocessing.py`) which will transform the standard ProteinNet format into a hdf5 file and save it in `data/preprocessed/`. This is done in a memory-efficient way (line-by-line).

The OpenProtein PyTorch data loader is memory optimized too - when reading the hdf5 file it will only load the samples needed for each minibatch into memory.

## Creating Demo image

```bash
# converting demo.mpg -> demo.gif
ffmpeg -i demo.mpg -vf "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" demo.gif

# same but slowed down * 8:
ffmpeg -i demo.mpg -vf "setpts=8.0*PTS,fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -y demo.gif
```

## License

Please see the LICENSE file in the root directory.
