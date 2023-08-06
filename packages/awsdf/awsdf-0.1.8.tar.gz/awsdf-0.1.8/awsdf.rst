
awsdf package
*************


Submodules
==========


awsdf.aws module
================

Main module.

**class awsdf.aws.Account(aws_access_key_id=None,
aws_secret_access_key=None, aws_session_token=None, region_name=None,
profile_name=None)**

   Bases: ``object``

   ``property accountid``

   **athena_create_table(dataframe_to_upload: DataFrame, table_name:
   str, s3_path: str, database='qdl_temp', mode='overwrite')**

      create_athena_table

      Arguments:
         dataframe_to_upload

   **athena_execute_query(database: str, query: str, use_cache: bool =
   True)**

   **athena_get_view_definition(database: str, viewname: str,
   query_location: str)**

   **ec2_get_instance_id(hostname)**

   **ec2_get_instanceip(ec2_instance_id)**

   **ec2_get_instances()**

   **ecs_get_allservices() -> DataFrame**

   **ecs_get_clusters() -> DataFrame**

   **ecs_get_container_ec2_instanceid(cluster_arn,
   container_instance)**

   **ecs_get_container_instance(cluster_arn, task_arn)**

   **ecs_get_services(cluster_arn) -> DataFrame**

   **ecs_get_tasks(cluster_arn, service_arn)**

   **get_available_profiles() -> list[str]**

   **glue_get_databases() -> DataFrame**

   **glue_get_job_history(job_name, no_of_runs=1)**

   **glue_get_jobs()**

   **glue_get_tables(dbname=None)**

   **iam_get_accountid() -> str**

   **lambda_get_functions()**

   **lambda_get_invocations(lambda_name, start_date=None,
   end_date=None)**

   **lambda_get_metrics_list(namespace='AWS/Lambda')**

   ``property region``

   **s3_wait_check_object_exists(bucket_name, key_name)**

   ``property session``

   **sfn_get_statemachines()**

**awsdf.aws.get_value(key, obj)**

**awsdf.aws.keyexists(key, dictionary)**


Module contents
===============
