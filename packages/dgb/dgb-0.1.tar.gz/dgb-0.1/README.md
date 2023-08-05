DGB
=====
Provides
  1. provides a data-loader to download a suite of dynamic graph datasets.
  2. provides an evaluator for the suit of dynamic graph datasets
  3. will provide tools to benchmark graph models
example code snippets
----------------------------

## To install

----------------------------
use pip for Python, make sure version python version is 3.6+

```
>>> pip install DGB
```


## Code examples

----------------------------
Code snippet to import the module::
```
import DGB
```
Code snippets to download a dataset::
```   
enron = DGB.TemporalDataSets(data_name="enron")
enron_dict = enron.process()
train = enron_dict["train"]
test  = enron_dict["test"]
val   = enron_dict["validation"]
```

to print all possible datasets::
```
data_list = DGB.list_all()
for data_name in data_list:
print(data_name)
```

to download all possible datasets that have not been downloaded yet::
```
DGB.download_all()
```

to force redownload all datasets::
```
DGB.force_download_all()
```

to skip download prompts and dataset statistics when processing::
```
DGB.TemporalDataSets(data_name="enron", skip_download_prompt=True, data_set_statistics=False)
```

## License

----------------------------
[MIT License](LICENSE)
