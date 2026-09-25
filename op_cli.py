"""
This file is part of the OpenProtein project.

For license information, please see the LICENSE file in the root directory.
"""

import argparse
import importlib
import sys
import time
import webbrowser
import torch
import dashboard

from util import write_out, set_verbose

def main():
    parser = argparse.ArgumentParser(
        description="OpenProtein version 0.1",
        conflict_handler='resolve')
    parser.add_argument('--silent', dest='silent', action='store_true',
                        help='Hide per-minibatch timing output (it is still written to the '
                             'experiment log in output/).')
    parser.add_argument('--no-browser', dest='no_browser', action='store_true',
                        default=False, help='Do not open the live dashboard in a browser.')
    parser.add_argument('--hide-ui', dest='hide_ui', action='store_true',
                        default=False, help='Hide loss graph and '
                                            'visualization UI while training goes on.')
    parser.add_argument('--evaluate-on-test', dest='evaluate_on_test', action='store_true',
                        default=False, help='Run model of test data.')
    parser.add_argument('--use-gpu', dest='use_gpu', action='store_true',
                        default=False, help='Use GPU.')
    parser.add_argument('--eval-interval', dest='eval_interval', type=int,
                        default=10, help='Evaluate model on validation set every n minibatches.')
    parser.add_argument('--min-updates', dest='minimum_updates', type=int,
                        default=100, help='Minimum number of minibatch iterations.')
    parser.add_argument('--minibatch-size', dest='minibatch_size', type=int,
                        default=8, help='Size of each minibatch.')
    parser.add_argument('--experiment-id', dest='experiment_id', type=str,
                        default="example", help='Which experiment to run.')
    parser.add_argument('--dashboard-port', dest='dashboard_port', type=int,
                        default=dashboard.DEFAULT_PORT,
                        help='Port for the live dashboard. If it is taken, a free '
                             'port is chosen automatically.')
    args, _ = parser.parse_known_args()

    set_verbose(not args.silent)

    if args.hide_ui:
        write_out("Live plot deactivated, see output folder for plot.")

    use_gpu = args.use_gpu

    if use_gpu and not torch.cuda.is_available():
        write_out("Error: --use-gpu was set, but no GPU is available.")
        sys.exit(1)

    dashboard_url = None
    if not args.hide_ui:
        dashboard_url = dashboard.start_dashboard_server(args.dashboard_port)
        banner = "  Live dashboard: " + dashboard_url + "  "
        print("=" * len(banner))
        print(banner)
        print("=" * len(banner))
        if not dashboard.dashboard_is_built():
            write_out("Dashboard frontend is not built yet. To build it, run:",
                      dashboard.BUILD_INSTRUCTIONS)
        elif not args.no_browser:
            webbrowser.open(dashboard_url)

    experiment = importlib.import_module("experiments." + args.experiment_id)
    experiment.run_experiment(parser, use_gpu)

    if dashboard_url is not None:
        write_out("Training finished. The dashboard stays available at", dashboard_url,
                  "until you press Ctrl-C.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
