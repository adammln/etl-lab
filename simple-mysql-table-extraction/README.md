# How To Use

1. Run `bash setup_mysql_employees.sh`
2. Run  `bash setup_airflow.sh`
3. grant access for `root` into mysql server:
    - `$ sudo mysql`
    - `mysql> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';`
    - `mysql> exit`
4. specify your google cloud storage bucket name under `GCS_BUCKET` variable (1-extract_employees_raw.py, line 30)
5. specify target file path under `EMPLOYEES_RAW_DATA_DIR` variable (1-extract_employees_raw.py, line 31)
6. head to ~/airflow: `cd ~/airflow`
7. activate virtualenv, then start scheduler: `airflow scheduler`
8. open another terminal, activate virtualenv, then start webserver: `airflow webserver -p 8080`
9. open airflow GUI, do these following things:
    - setup MySQL connection with connection id=`mysql_default`
    - setup Google Cloud Platform connection with connection id: `google_cloud_default` _(make sure it has GCS admin role)_
10. trigger dags