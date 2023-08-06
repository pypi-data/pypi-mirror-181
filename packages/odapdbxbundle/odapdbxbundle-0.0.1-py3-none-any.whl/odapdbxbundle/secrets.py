from odapdbxbundle.common.databricks import resolve_dbutils, get_host, get_token, get_username
from pyspark.sql import SparkSession

import json
import requests


def create_scope(user_name):
    dbutils = resolve_dbutils()
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    scope_name = user_name.split('@')[0]        # scope name is the first half of user name before @
    create_scope_api = f"{dbx_url}/api/2.0/secrets/scopes/create"
    create_scope_data = json.dumps({'scope': scope_name})
    response = requests.post(create_scope_api, headers=auth_header, data=create_scope_data)
    response.content


def put_user_acl(user_name):
    dbutils = resolve_dbutils()
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    scope_name = user_name.split('@')[0]
    put_acl_api = f"{dbx_url}/api/2.0/secrets/acls/put"
    put_acl_data = json.dumps({
        "scope": scope_name,
        "principal": user_name,
        "permission": "MANAGE"
    })
    response = requests.post(put_acl_api, headers = auth_header, data= put_acl_data)
    response.content


def remove_service_account(user_name):
    scope_name = user_name.split('@')[0]
    dbutils = resolve_dbutils()
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    delete_acl_api = f"{dbx_url}/api/2.0/secrets/acls/delete"
    delete_acl_data = json.dumps({
      "scope": scope_name,
      "principal": get_username()
    })
    response = requests.post(delete_acl_api, headers = auth_header, data= delete_acl_data)
    response.content


def get_secret_name(secret):
    return secret.name


def get_scope_name():
    username = get_username()
    return username.split('@')[0]


def create_scope_if_not_exists():
    dbutils = resolve_dbutils()
    spark = SparkSession.getActiveSession()
    df = spark.sql("SHOW USERS")
    df_list_of_users = df.rdd.map(lambda x: x.name).collect()
    users_to_have_scopes = [item for items in df_list_of_users for item in items.split('@')][::2]

    scope_names = list(map(lambda x: x.name, dbutils.secrets.listScopes()))

    users_to_create_scopes = set(users_to_have_scopes) - set(scope_names)

    for user_name in users_to_create_scopes:
        create_scope(user_name)
        put_user_acl(user_name)
        if user_name != get_username:
            remove_service_account(user_name)


def add_secret(secret_name, secret_value, secret_scope=None):
    if secret_scope is None:
        secret_scope = get_scope_name()
    dbutils = resolve_dbutils()
    dbx_token = get_token()
    auth_header = {"authorization": f"Bearer {dbx_token}"}
    dbx_url = get_host()
    create_scope_api = f"{dbx_url}/api/2.0/secrets/put"
    put_secret_data = json.dumps({'scope': secret_scope, 'key': secret_name, 'string_value': secret_value})
    return requests.post(create_scope_api, headers=auth_header, data=put_secret_data).content


