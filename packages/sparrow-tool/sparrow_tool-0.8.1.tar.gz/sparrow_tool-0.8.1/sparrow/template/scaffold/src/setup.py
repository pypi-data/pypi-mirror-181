import setuptools

setuptools.setup(
    pbr=True,
    package_data={
        "{{project_name}}": [
            '*.yaml', '*.yml', '*.json',
        ],
    },
)
