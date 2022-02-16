
seq="CREATE USER '$1'@'localhost' IDENTIFIED BY '$2';\nGRANT ALL PRIVILEGES ON *.* TO '$1'@'localhost' IDENTIFIED BY '$2' WITH GRANT OPTION;"
echo -e "$seq" > tmp.sql
mysql -u root -p'xxxxxx' < tmp.sql
rm -fr tmp.sql
