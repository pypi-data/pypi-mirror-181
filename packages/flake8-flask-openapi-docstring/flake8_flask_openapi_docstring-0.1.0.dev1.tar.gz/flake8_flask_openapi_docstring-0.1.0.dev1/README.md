# flake8-flask-openapi-docstring

This Flake8 plugin will check if your Flask route's docstrings are valid OpenAPI spec.

Libraries like [APISpec](https://apispec.readthedocs.io/en/latest/) can generate OpenAPI spec from your Flask routes and docstrings and it's important to have present and in the correct format.

for example, this routes:

```python
@app.route("/hello", methods=["GET"])
def hello():
    return "Hello World!"
```

will raise an error witht his plugin because not only the docstring is missing but also the OpenAPI spec is missing as well.

However these route:

```python
@app.route("/hello", methods=["GET"])
def hello():
    """
    Returns a greeting

    ---
    get:
        responses:
            200:
    """
    return "Hello World!"
```

will not raise any error because the docstring is present and the OpenAPI spec is present as well.
