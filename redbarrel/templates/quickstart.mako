# generated by RedBarrel's rb-quickstart script
meta (
    description """${description}""",
    version ${version}
);

path hello (
    description "Simplest service",
    method GET,
    url /,
    response-body (
        description "Returns an Hello word text"
    ),
    response-headers (
        set Content-Type "text/plain"
    ),
    use python:${pkg_name}.hello.hello
);
