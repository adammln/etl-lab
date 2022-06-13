from airflow.providers.google.cloud.transfers.sql_to_gcs import BaseSQLToGCSOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from typing import Sequence 

class MySQLToGCSOperator(BaseSQLToGCSOperator):
    """
    Copy data from MySQL to Google Cloud Storage in JSON, CSV, or Parquet format.

    :param sql: The SQL to execute.
    :param bucket: The bucket to upload to.
    :param filename: The filename to use as the object name when uploading
        to Google Cloud Storage. A ``{}`` should be specified in the filename
        to allow the operator to inject file numbers in cases where the
        file is split due to size.
    :param schema_filename: If set, the filename to use as the object name
        when uploading a .json file containing the BigQuery schema fields
        for the table that was dumped from the database.
    :param approx_max_file_size_bytes: This operator supports the ability
        to split large table dumps into multiple files (see notes in the
        filename param docs above). This param allows developers to specify the
        file size of the splits. Check https://cloud.google.com/storage/quotas
        to see the maximum allowed file size for a single object.
    :param export_format: Desired format of files to be exported.
    :param field_delimiter: The delimiter to be used for CSV files.
    :param null_marker: The null marker to be used for CSV files.
    :param gzip: Option to compress file for upload (does not apply to schemas).
    :param schema: The schema to use, if any. Should be a list of dict or
        a str. Pass a string if using Jinja template, otherwise, pass a list of
        dict. Examples could be seen: https://cloud.google.com/bigquery/docs
        /schemas#specifying_a_json_schema_file
    :param gcp_conn_id: (Optional) The connection ID used to connect to Google Cloud.
    :param mysql_conn_id: The connection ID used to connect to MySQL Instance.
    :param delegate_to: The account to impersonate using domain-wide delegation of authority,
        if any. For this to work, the service account making the request must have
        domain-wide delegation enabled.
    :param parameters: a parameters dict that is substituted at query runtime.
    :param impersonation_chain: Optional service account to impersonate using short-term
        credentials, or chained list of accounts required to get the access_token
        of the last account in the list, which will be impersonated in the request.
        If set as a string, the account must grant the originating account
        the Service Account Token Creator IAM role.
        If set as a sequence, the identities from the list must grant
        Service Account Token Creator IAM role to the directly preceding identity, with first
        account from the list granting this role to the originating account (templated).
    """

    template_fields: Sequence[str] = (
        'sql',
        'bucket',
        'filename',
        'schema_filename',
        'schema',
        'parameters',
        'impersonation_chain',
        'mysql_conn_id',
        'gcp_conn_id',
        'export_format',
    )

    template_ext: Sequence[str] = ('.sql',)

    template_fields_renderers = {'sql': 'sql'}

    ui_color = '#a0e08c'

    def __init__(
        self,
        *,
        mysql_conn_id,
        parameters=None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.mysql_conn_id = mysql_conn_id
        self.parameters = parameters

    def query(self):
        mysql = MySqlHook(
            conn_name_attr=self.mysql_conn_id,
        )
        conn = mysql.get_conn()
        cursor = conn.cursor()
        cursor.execute(self.sql, self.parameters)
        return cursor

    def field_to_bigquery(self, field):
        return

    def convert_type(self, value, schema_type, **kwargs):
        return