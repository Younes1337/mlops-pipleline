from setuptools import find_packages, setup

setup(
    name="dagster_university",
    packages=find_packages(exclude=["dagster_university_tests"]),
    install_requires=[
        "dagster==1.6.*",
        "dagster-cloud",
        "dagster-duckdb",
        "dagster-postgres",
        "geopandas",
        "kaleido",
        "pandas[parquet]",
        "plotly",
        "shapely",
        "boto3",
        "psycopg2"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
