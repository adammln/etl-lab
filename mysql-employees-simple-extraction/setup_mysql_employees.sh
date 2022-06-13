# install mysql server 8.0
sudo apt-get update
sudo apt-get install mysql-server -y

# download&extract dataset employees
mkdir downloads
cd downloads
wget https://github.com/datacharmer/test_db/archive/refs/heads/master.zip
sudo apt-get install unzip -y
unzip ./master.zip
cd ./test_db-master/

# access database as root then initiate db
sudo -u root mysql < employees.sql


# granting connection from airflow to mysql
# sudo mysql
# ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'insert_password';
# exit


