
awsdf package
*************


Submodules
==========


awsdf.aws module
================

This module enables connecting to AWS and extracting metadata in
pandas dataframes.

**Installing from PyPI:** *pip install -U awsdf*

**USAGE:**

   import awsdf

   aws_account = awsdf.Account(profile_name=”<PROFILE_NAME>”)

   glue_databases_df = aws_account.glue_get_databases()

**class awsdf.aws.Account(aws_access_key_id=None,
aws_secret_access_key=None, aws_session_token=None, region_name=None,
profile_name=None)**

   Instantiate class object for connecting to AWS and retriving
   metadata from AWS

   **__init__(aws_access_key_id=None, aws_secret_access_key=None,
   aws_session_token=None, region_name=None, profile_name=None)**

      Provide access keys OR Profile name to connect to AWS account.
      Keys take preceedence

      **Parameters:**

         *aws_access_key_id (string) – AWS access key ID*

         *aws_secret_access_key (string) – AWS secret access key*

         *aws_session_token (string) – AWS temporary session token*

         *region_name (string) – AWS region*

         *profile_name (string) – AWS profile name*

   **glue_get_jobs() -> DataFrame**

      Get AWS Glue jobs

      Returns:
         dataframe

   **glue_get_job_history(job_name, no_of_runs=1) -> DataFrame**

      Retrieve glue job history

      Arguments:
         job_name – Name of job to retrive history

      Keyword Arguments:
         no_of_runs – No of runs to retrive in descending order
         (default: {1})

      Returns:
         dataframe

   **glue_get_databases() -> DataFrame**

      Get AWS Glue jobs

      Returns:
         dataframe

   **glue_get_tables(dbname=None) -> DataFrame**

      Get AWS Glue tables

      Keyword Arguments:
         dbname – Database Name for which to retrive tables (default:
         {None})

      Returns:
         dataframe


Module contents
===============
