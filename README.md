# Python

My python personal side projects

## To update Requirements

```shell
sed -i '' 's/[~=]=/>=/' requirements.txt
pip install -U -r requirements.txt
pip freeze | sed 's/==/~=/' > requirements.txt
```
