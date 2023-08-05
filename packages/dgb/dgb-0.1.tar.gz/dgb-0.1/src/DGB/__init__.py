"""
DGB
=====
Provides
  1. provides a data-loader to download a suite of dynamic graph datasets.
  2. provides an evaluator for the suit of dynamic graph datasets
  3. will provide tools to benchmark graph models
example code snippets
----------------------------
Code snippet to import the module::
  >>> import dgb

Code snippets to download a dataset::
  >>> enron = dgb.TemporalDataSets(data_name="enron")
  >>> enron_dict = enron.process()
  >>> train = enron_dict["train"]
  >>> test  = enron_dict["test"]
  >>> val   = enron_dict["validation"]

to print all possible datasets::
  >>> data_list = dgb.list_all()
  >>> for data_name in data_list:
  >>>   print(data_name)

to download all possible datasets that have not been downloaded yet::
  >>> dgb.download_all()

to force redownload all datasets::
  >>> dgb.force_download_all()

to skip download prompts and dataset statistics when processing::
  >>> dgb.TemporalDataSets(data_name="enron", skip_download_prompt=True, data_set_statistics=False)

"""

from . import download
from . import evaluator

TemporalDataSets = download.TemporalDataSets
download_all = download.download_all
force_download_all = download.force_download_all
list_all = download.dataset_names_list()
Evaluator = evaluator.Evaluator
