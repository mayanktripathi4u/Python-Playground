# default_factory vs empty list

```python
tags: list[str] = Field(default_factory=list)

# Vs
tags: list[str] = []
```

# Install Packages
```sh
pip install pydantic
# Vs
pip install pydantic[email]
# Vs
pip install pydantic[all]
```

