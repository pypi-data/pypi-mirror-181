# fish-databricks-jobs 

fish-databricks-jobs is cli and python sdk to handle Jobs for Databricks. e.g assign permissions to multiple jobs. User can filter jobs by job name or tags.  

The current `databricks-cli`(v0.17.4) has limited functionality on the `jobs` api. e.g it can not assign permission to job. 

# installation
```
$ pip install fish-databricks-jobs
```
# usage
```
$ fish-databricks-jobs -h

 Usage: fish-databricks-jobs [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version             -v        0.3.0                                                                                                            │
│ --install-completion            Install completion for the current shell.                                                                        │
│ --show-completion               Show completion for the current shell, to copy it or customize the installation.                                 │
│ --help                -h        Show this message and exit.                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list                         List Databricks jobs                                                                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
# config authentication
fish-databricks-jobs uses same config file as `databricks-cli`. e.g.`~/.databrickscfg` for macOS. Similar for Windows.
```
[DEFAULT]
host = https://example.cloud.databricks.com
token = dapi41bc0e27d8b91fd8c0144f0a2343504b
```



