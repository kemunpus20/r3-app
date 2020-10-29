# How to deply to Azure.

## Role and connectivity.
- Application Server - Azure App Service
    - Connection : Client browser -> App Service (nginx -> gunicorn -> django)
    - All static files are inside the app service local file system using whitenoise middlwware.
- Database Service - Azure Database for PostgreSQL
    - Connection : App Service -> Database service (PostgerSQL)
    - All objects defined by models except media files are stored here.
- Blob storage - Azure Blob Storage
    - Connection : Client browser -> Blob Storage.
    - All media files are stored here.

## Preparations.
 1. Create your azure account.
 1. Create your resource group. 
 1. Create your app service plan.

## Setup Azure Database Service.
1. Setup your PostgreSQL instance.
    - Connectivity method : Public access.
    - PostgreSQL Version : 11
1. Add your client ip to firewall to configure the service using psql cli. Note that I think the cloud shell could be better but it does not work correctly in my environment.
1. Connect to the instance.
    ```
    psql host=your host name (e.g. hoge.postgres.database.azure.com) port=5432 dbname=your db name (e.g. postgres) user=your db admin name (e.g. psqladmin)
    ```
1. Initialize some tables. be sure to use a complex password!
    ```
    CREATE DATABASE r3;
    CREATE USER PSQLADMIN WITH PASSWORD 'PASSWORD';
    ALTER ROLE PSQLADMIN SET client_encoding TO 'utf8';
    ALTER ROLE PSQLADMIN SET default_transaction_isolation TO 'read committed';
    ALTER ROLE PSQLADMIN SET timezone TO 'Asia/Tokyo';
    GRANT ALL PRIVILEGES ON DATABASE r3 TO 'PSQLADMIN';
    /q
    ```
1. Disconnect and remove ip from firewall configuration.

## Setup Azure Blob Storage.
1. Create your storage account. (e.g. hogestorages)
1. Create new container in the storage account. (e.g. hoge-container)
    - Public access level : blob
    - Blob type : Block blob
    - Access tier : hot

## Setup Azure App Service.
1. Create App Service for Python Django.
    - Stack : Python
    - Version : Python 3.7
    - FTP state : Disabled
    - HTTP Vesion : 1.1
    - HTTPS Only : on
    - Minimum TLS Version : 1.2
1. Add application settings as follows.
    - DB_ENGINE : POSTGRESQL (see [settings.py](pbl/settings.py))
    - DB_HOST : your db url (e.g. hoge.postgres.database.azure.com)
    - DB_NAME : r3
    - DB_USER : your db admin name (e.g. psqladmin)
    - DB_PASSWORD : your db admin password
    - DB_PORT : 5432
    - MEDIA_STORAGE : AZURE_BLOB (see [settings.py](pbl/settings.py))
    - AZURE_ACCOUNT_NAME : your storage account name (e.g. hogestorages)
    - AZURE_MEDIA_CONTAINER : your storage container name (e.g. hoge-container)
    - AZURE_STORAGE_KEY : your storage key
    - ALLOWED_HOSTS : your application url (e.g. hoge.azurewebsites.net)
    - DEBUG : True (will change to False later soon)
1. Configure automatic deploy from Github to Azure App Service.
1. To setup database and application admin, start app service and connect that via ssh from the azure console. note that ssh would not work if Debug=False.
    ```
    $ pip -r requirements
    $ manage check
    $ manage migrattions
    $ manage migrate r3
    $ manage createsuperuser
    ```    
1. Change Debug to False and restart the service.

## Note.
1. To improve system overall performance, use smart cache mechanism in both django and azure.
1. Using Azure Private VNET would be better for security.
1. To confirm django application configuration, 'manage.py check --deploy' will provides some security related information.
