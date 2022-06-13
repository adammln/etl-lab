cd ~

mkdir airflow
cp ./mysql-employees/dags ./airflow/ -r
cp ./mysql-employees/requirements.in ./airflow/

cd airflow

# create virtualenv
echo "CREATING VIRTUAL ENVIRONMENT..."
virtualenv env

# activate env
source ./env/bin/activate


echo "INSTALLING REQUIREMENTS..."
# install required ubuntu pacakges
sudo apt-get update
## requirements for mysql client (airflow-mysql connection)
sudo apt-get install python3.8-dev default-libmysqlclient-dev build-essential mysql-client -y

# install requirements.in
pip install -r requirements.in

#
echo "====== INSTALLATION COMPLETE ========"

echo "INITIATING DB..."
# airflow db init
airflow db init

echo "====== DB INITIATED ========"

echo "CREATING ADMIN USER..."
# create admin
airflow users create --role Admin --username admin --email admin@example.com --firstname admin --lastname admin --password admin
echo "====== USER CREATED ========"

echo "====== AIRFLOW SETUP DONE! ========"