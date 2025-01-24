to_mysql:
	docker exec -it mysql mysql -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE}

to_mysql_root:
	docker exec -it de_mysql mysql -u"root" -p"${MYSQL_ROOT_PASSWORD}" ${MYSQL_DATABASE}

mysql_create:
	docker exec -it mysql mysql --local_infile -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE} -e"source /tmp/load_dataset/olist.sql"

mysql_load:
	docker exec -it mysql mysql --local_infile -u"${MYSQL_USER}" -p"${MYSQL_PASSWORD}" ${MYSQL_DATABASE} -e"source /tmp/load_dataset/load_data.sql"



docker exec -it mysql mysql -u"root" -p

   SHOW GRANTS FOR 'your_user'@'%';



### kiem tra ket noi airflow voi mysql 
docker exec -it your_airflow_container bash

   mysql -h mysql -u admin -p