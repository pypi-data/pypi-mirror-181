# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['awsdf']

package_data = \
{'': ['*']}

install_requires = \
['awswrangler>=2.14.0,<3.0.0',
 'loguru>=0.6.0,<0.7.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'awsdf',
    'version': '0.1.8',
    'description': 'AWS metadata as dataframes',
    'long_description': "\nawsdf package\n*************\n\n\nSubmodules\n==========\n\n\nawsdf.aws module\n================\n\nMain module.\n\n**class awsdf.aws.Account(aws_access_key_id=None,\naws_secret_access_key=None, aws_session_token=None, region_name=None,\nprofile_name=None)**\n\n   Bases: ``object``\n\n   ``property accountid``\n\n   **athena_create_table(dataframe_to_upload: DataFrame, table_name:\n   str, s3_path: str, database='qdl_temp', mode='overwrite')**\n\n      create_athena_table\n\n      Arguments:\n         dataframe_to_upload\n\n   **athena_execute_query(database: str, query: str, use_cache: bool =\n   True)**\n\n   **athena_get_view_definition(database: str, viewname: str,\n   query_location: str)**\n\n   **ec2_get_instance_id(hostname)**\n\n   **ec2_get_instanceip(ec2_instance_id)**\n\n   **ec2_get_instances()**\n\n   **ecs_get_allservices() -> DataFrame**\n\n   **ecs_get_clusters() -> DataFrame**\n\n   **ecs_get_container_ec2_instanceid(cluster_arn,\n   container_instance)**\n\n   **ecs_get_container_instance(cluster_arn, task_arn)**\n\n   **ecs_get_services(cluster_arn) -> DataFrame**\n\n   **ecs_get_tasks(cluster_arn, service_arn)**\n\n   **get_available_profiles() -> list[str]**\n\n   **glue_get_databases() -> DataFrame**\n\n   **glue_get_job_history(job_name, no_of_runs=1)**\n\n   **glue_get_jobs()**\n\n   **glue_get_tables(dbname=None)**\n\n   **iam_get_accountid() -> str**\n\n   **lambda_get_functions()**\n\n   **lambda_get_invocations(lambda_name, start_date=None,\n   end_date=None)**\n\n   **lambda_get_metrics_list(namespace='AWS/Lambda')**\n\n   ``property region``\n\n   **s3_wait_check_object_exists(bucket_name, key_name)**\n\n   ``property session``\n\n   **sfn_get_statemachines()**\n\n**awsdf.aws.get_value(key, obj)**\n\n**awsdf.aws.keyexists(key, dictionary)**\n\n\nModule contents\n===============\n",
    'author': 'Allan',
    'author_email': 'allan.dsouza@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.11',
}


setup(**setup_kwargs)
