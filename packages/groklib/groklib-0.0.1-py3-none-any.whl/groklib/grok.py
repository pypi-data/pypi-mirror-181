#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# grok.py: thin client library for talking to GROK server
class GrokClient():
    def __init__(self, project_name: None, run_description: None) -> None:
        self.project_name = project_name
        self.run_description = run_description

    def log_hparams(self, hp_dict: dict):
        self.hp_dict = hp_dict

    def log_metrics(self, metrics: dict):
        self.metrics = metrics


