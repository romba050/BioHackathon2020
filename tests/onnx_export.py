"""
This file is part of the OpenProtein project.

For license information, please see the LICENSE file in the root directory.
"""

import glob
import os
import torch
import torch.onnx

import util
from util import encode_primary_string

def _traceable_pad_sequence(sequences, batch_first=False, padding_value=0.0):
    """Pure-tensor equivalent of torch.nn.utils.rnn.pad_sequence.

    Recent torch versions dispatch pad_sequence to a single native operator
    (aten::pad_sequence) that the TorchScript ONNX exporter cannot lower, so we
    trace through this implementation instead while exporting.
    """
    max_len = max(seq.size(0) for seq in sequences)
    padded = []
    for seq in sequences:
        pad_spec = [0] * (2 * (seq.dim() - 1)) + [0, max_len - seq.size(0)]
        padded.append(torch.nn.functional.pad(seq, pad_spec, value=padding_value))
    stacked = torch.stack(padded, dim=0)
    return stacked if batch_first else stacked.transpose(0, 1)

def onnx_from_model(model, input_str, path):
    """Export to onnx"""
    original_pad_sequence = torch.nn.utils.rnn.pad_sequence
    torch.nn.utils.rnn.pad_sequence = _traceable_pad_sequence
    util.pad_sequence = _traceable_pad_sequence
    try:
        torch.onnx.export(model, input_str, path, opset_version=10, verbose=True,
                          dynamo=False)
    finally:
        torch.nn.utils.rnn.pad_sequence = original_pad_sequence
        util.pad_sequence = original_pad_sequence

def predict():
    list_of_files = glob.glob('output/models/*')  # * means all if need specific format then *.csv
    model_path = max(list_of_files, key=os.path.getctime)

    print("Generating ONNX from model:", model_path)
    model = torch.load(model_path, weights_only=False)

    input_sequences = [
        "SRSLVISTINQISEDSKEFYFTLDNGKTMFPSNSQAWGGEKFENGQRAFVIFNELEQPVNGYDYNIQVRDITKVLTKEIVTMDDEE" \
        "NTEEKIGDDKINATYMWISKDKKYLTIEFQYYSTHSEDKKHFLNLVINNKDNTDDEYINLEFRHNSERDSPDHLGEGYVSFKLDKI" \
        "EEQIEGKKGLNIRVRTLYDGIKNYKVQFP"]

    input_sequences_encoded = list(torch.IntTensor(encode_primary_string(aa))
                                   for aa in input_sequences)

    print("Exporting to ONNX...")

    output_path = "./tests/output/openprotein.onnx"
    onnx_from_model(model, input_sequences_encoded, output_path)

    print("Wrote ONNX to", output_path)

predict()
