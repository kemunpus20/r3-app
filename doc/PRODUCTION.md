# How to deply to Azure

## Brief architecture
- Application Server is Azure App Service
    - Connection : Client browser -> App Service (nginx -> gunicorn -> django)
    - All static files are inside the app service local file system using whitenoise middlwware.
- Database Server is PostgreSQL on Linux VM.
    - Connection : App Service -> PostgerSQL
    - All objects defined by models except media files are stored here.
- Blob storage is Azure Blob Storage Service
    - Connection : Client browser -> Blob Storage.
    - All media files are stored here.
- Code repository is GitHub
    - Deployment : Automated using Github Actions.

Note: Finally I have decided to use the PostgreSQL running on a very small linux VM. Following desciption contains another choise such as Azure Database Service PostgreSQL and CosmosDB. These descriptions is just like a record of my struggles...

## Setup account
 1. Create your Azure Account, Subscription and Resource Group. 
 

## Setup Linux VM with PostgreSQL
1. Create linux VM with Ubuntu server.
    Install postgreSQL (and python3 in the case)
    ```
    # sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
    ```
1. Create account for both linux and postgreSQL.
    ```
    # sudo passwd postgres
    # sudo -u postgres psql
    CREATE DATABASE r3;
    CREATE USER <db admin name> WITH PASSWORD <db admin password>;
    ALTER ROLE <db admin name> SET client_encoding TO 'utf8';
    ALTER ROLE <db admin name> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <db admin name> SET timezone TO 'Asia/Tokyo';
    GRANT ALL PRIVILEGES ON DATABASE r3 TO 'db admin name';
    /q
    ```    
1. Update postgresql.conf to modify  listen_addresses to be  '*'.
1. Update pg_hba.conf to add host all all 0.0.0.0/0 md5.
1. Open firewall and restart postgreSQL instance.
    ```
    # sudo iptables -A INPUT -p tcp --dport 5432 -j ACCEPT
    # sudo service postgresql restart
    ```
1. Configure VM instance as more secure.
    - Change restricted source IP address for SSH (TCP/22) from * to your development environment public IP address.
    - Add restricted source IP address for PostgreSQL (TCP/5432) with your App service's outbound IP addresses.

## Setup Azure Database Service
1. Setup PostgreSQL service instance.
    - Connectivity method : Public access.
    - PostgreSQL Version : 11
1. Add your client IP to firewall to configure the service using psql cli. Note that I think the cloud shell could be better.
1. Connect to the service instance.
    ```
    # psql host=<host name> (e.g. hoge.postgres.database.azure.com) port=5432 dbname=<db name> (e.g. postgres) user=<db admin name> (e.g. psqladmin)
    ```
1. Create database and db admin account. be sure to use a complex password!
    ```
    CREATE DATABASE r3;
    CREATE USER <db admin name> WITH PASSWORD <db admin password>;
    ALTER ROLE <db admin name> SET client_encoding TO 'utf8';
    ALTER ROLE <db admin name> SET default_transaction_isolation TO 'read committed';
    ALTER ROLE <db admin name> SET timezone TO 'Asia/Tokyo';
    GRANT ALL PRIVILEGES ON DATABASE r3 TO 'db admin name';
    /q
    ```
1. Close session and remove IP from firewall configuration.

## Setup Azure Cosmos DB
1. Create Cosmos DB account. (e.g. fuga)
    - API : Azure Cosmos DB for MongoDB API
    - Version : 3.6
    - Connectivity method : Public endpoint
    - Allow access from Azure Portal : Allow (+ Accept connections from within public Azure datacenters)
    - Allow access from my IP : Deny (or Allow if you try to use with local development instance)

## Setup Azure Blob Storage
1. Create storage account. (e.g. hogestorages)
1. Create new container in the storage account. (e.g. hoge-container)
    - Public access level : blob
    - Blob type : Block blob
    - Access tier : hot

## Setup Azure App Service
1. Create App Service Plan.
1. Create App Service for Python Django.
    - Stack : Python
    - Version : Python 3.7
    - FTP state : Disabled
    - HTTP Vesion : 1.1
    - HTTPS Only : on
    - Minimum TLS Version : 1.2

1. Add application settings as follows (for Django)
    - DEBUG : True (will change to False later soon)

1. Add application settings as follows (for PostgreSQL running on Linux VM)
    - DB_ENGINE : POSTGRESQL (see [settings.py](pbl/settings.py))
    - DB_HOST : VM's public IP address,
    - DB_NAME : r3
    - DB_USER : db admin name (e.g. psqladmin)
    - DB_PASSWORD : db admin password
    - DB_PORT : 5432

1. Add application settings as follows (for Aure Database Service PostgreSQL)
    - DB_ENGINE : POSTGRESQL (see [settings.py](pbl/settings.py))
    - DB_HOST : db url (e.g. hoge.postgres.database.azure.com)
    - DB_NAME : r3
    - DB_USER : db admin name (e.g. psqladmin)
    - DB_PASSWORD : db admin password
    - DB_PORT : 5432

1. Add application settings as follows (for Cosmos DB)
    - DB_ENGINE : MONGODB (see [settings.py](pbl/settings.py))    
    - DB_HOST : db url (e.g. fuga.mongo.cosmos.azure.com)
    - DB_NAME : r3
    - DB_USER : account name (e.g. fuga)
    - DB_PASSWORD : account key (you can get it from the console)
    - DB_PORT : 10255

1. Add application settings as follows (for Azure BLOB)
    - MEDIA_STORAGE : AZURE_BLOB (see [settings.py](pbl/settings.py))
    - AZURE_ACCOUNT_NAME : storage account name (e.g. hogestorages)
    - AZURE_CUSTOM_DOMAIN : storage custom domain (e.g. hogestorages.blob.core.windows.net)
    - AZURE_MEDIA_CONTAINER : storage container name (e.g. hoge-container)
    - AZURE_STORAGE_KEY : storage key (you can get it from the console)
    - ALLOWED_HOSTS : application url (e.g. hoge.azurewebsites.net)

1. Configure automatic deployment from Github to Azure App Service using GitHub Actions.
1. To setup database and application admin, start app service and connect that via ssh from Azure Console. Then executes some commands as below.
    ```
    # cd site/wwwroot
    # pip install -r requirements
    # ./manage.py check
    # ./manage.py makemigrattions r3
    # ./manage.py migrate
    # ./manage.py createsuperuser
    ```
1. Change Debug to False and restart the service.
