# Workshop #2: Data Engineer <img src="https://cdn-icons-png.flaticon.com/512/8618/8618924.png" alt="Data Icon" width="30px"/>

Realized by **Martín García** ([@mitgar14](https://github.com/mitgar14)).

## Overview ✨
> [!NOTE]
> It's important to note that the raw Grammys dataset must be stored in a database in order to be read correctly.

In this workshop we will use two datasets (*spotify_dataset* and *the_grammys_awards*) that will be processed through Apache Airflow applying data cleaning, transformation and loading and storage, including a merge of both datasets. The result will culminate in visualizations on a dashboard that will give us important conclusions about this dataset.

The tools used are:

* Python 3.10 ➜ [Download site](https://www.python.org/downloads/)
* Jupyter Notebook ➜ [VS Code tool for using notebooks](https://youtu.be/ZYat1is07VI?si=BMHUgk7XrJQksTkt)
* PostgreSQL ➜ [Download site](https://www.postgresql.org/download/)
* Power BI (Desktop version) ➜ [Download site](https://www.microsoft.com/es-es/power-platform/products/power-bi/desktop)

> [!WARNING]
> Apache Airflow only runs correctly in Linux environments. If you have Windows, we recommend using a virtual machine or WSL.

The dependencies needed for Python are

* Apache Airflow
* Dotenv
* Pandas
* Matplotlib
* Seaborn
* SQLAlchemy
* PyDrive2

These dependencies are included in the `requirements.txt` file of the Python project. The step-by-step installation will be described later.

## Dataset Information <img src="https://github.com/user-attachments/assets/5fa5298c-e359-4ef1-976d-b6132e8bda9a" alt="Dataset" width="30px"/>


The datasets used (*spotify_dataset* and *the_grammy_awards*) are crucial for analyzing music trends, comparing track features, and understanding the relation between track characteristics and award recognition.

Here’s an overview of the two datasets that were provided:

### 1. **Spotify Dataset** (`spotify_dataset.csv`) <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Spotify.png/1200px-Spotify.png" alt="Spotify" width="22px"/>

This dataset contains a wide variety of information about songs available on Spotify. Each row represents a single track with multiple attributes describing both the track's metadata and musical characteristics. The most important columns are:

- **Unnamed: 0**: Acts as an index for the dataset.
- **track_id**: A unique identifier for each track on Spotify.
- **artists**: Name(s) of the artist(s) associated with the track.
- **album_name**: The name of the album the track is from.
- **track_name**: The title of the track.
- **popularity**: A score between 0 and 100 indicating the popularity of the track on Spotify, where higher values mean more popularity.
- **duration_ms**: The duration of the track in milliseconds.
- **danceability**: A measure of how suitable a track is for dancing, where higher values indicate better danceability.
- **energy**: A measure of intensity and activity in the track.
- **key**: The musical key of the track (0 = C, 1 = C#, etc.).
- **loudness**: The overall loudness of the track in decibels.
- **mode**: Whether the track is in a major (1) or minor (0) mode.
- **explicit**: Indicates if the track contains explicit content (True/False).
- **tempo**: The speed of the track measured in beats per minute (BPM).
- **valence**: A measure of the musical positiveness of the track.
- **time_signature**: An estimated overall time signature of a track.
- **track_genre**: The genre associated with the track.

### 2. **Grammy Awards Dataset** (`the_grammy_awards.csv`) <img src="https://www.pngall.com/wp-content/uploads/9/Grammy-Awards-PNG-Download-Image.png" alt="Grammys" width="22px"/>

This dataset contains information about Grammy Awards, with each row representing a nomination for a particular award. Key columns include:

- **year**: The year the Grammy Awards took place.
- **title**: The name of the Grammy event.
- **published_at**: The date when the Grammy event details were published.
- **category**: The category of the Grammy award (e.g., Record Of The Year, Best Pop Solo Performance).
- **nominee**: The name of the nominated song or album.
- **artist**: The artist(s) associated with the nominated song or album.
- **workers**: Contributors (such as producers, engineers) involved in the nominated work.
- **img**: URL linking to the image of the Grammy event or nominee.
- **winner**: A boolean indicating whether the nominee won the award (True/False).

## Data flow <img src="https://cdn-icons-png.flaticon.com/512/1953/1953319.png" alt="Data flow" width="22px"/>

![Flujo de datos](https://github.com/user-attachments/assets/6e9d34c0-8611-4f1a-b283-87029d2621da)

## Run the project <img src="https://github.com/user-attachments/assets/99bffef1-2692-4cb8-ba13-d6c8c987c6dd" alt="Running code" width="30px"/>


### 🛠️ Clone the repository

Execute the following command to clone the repository:

```bash
  git clone https://github.com/mitgar14/etl-workshop-2.git
```

#### Demonstration of the process

![git clone](https://github.com/user-attachments/assets/b1b6c169-1935-4683-832f-87d627163928)

---

### 🔐 Generate your Google Drive Auth file (`client_secrets.json`)

* To learn how to generate a `client_secrets.json` file, [you can follow the following guide](https://github.com/mitgar14/etl-workshop-2/blob/main/docs/guides/drive_api.md). This guide explains step by step how to generate the authentication key to use the Google Drive API via PyDrive 2 in your *Store* script.

* In case you receive an **error 400 - redirect_uri_mismatch**, [you can follow the next page](https://elcuaderno.notion.site/Solucionado-Acceso-bloqueado-La-solicitud-de-esta-app-no-es-v-lida-Google-Drive-API-106a9368866a8037b597ecdec3346405?pvs=4).

---

### ⚙️ Configure PyDrive2 (`settings.yaml`)

To properly configure this project and ensure it works as expected, please follow the detailed instructions provided in the **PyDrive2 configuration guide**. This guide walks you through setting up the necessary variables, OAuth credentials, and project settings for Google Drive API integration using PyDrive2. 

* You will configure your `settings.yaml` file for authentication and authorization. [You can find the step-by-step guide here](https://github.com/mitgar14/etl-workshop-2/blob/main/docs/guides/drive_settings.md).

---

### 🌍 Enviromental variables

> [!IMPORTANT]
> Remember that you must use the absolute routes to the path.

For this project we use some environment variables that will be stored in one file named ***.env***, this is how we will create this file:

1. We create a directory named ***env*** inside our cloned repository.

2. There we create a file called ***.env***.

3. In that file we declare 6 enviromental variables. Remember that some variables in this case go without double quotes, i.e. the string notation (`"`). Only the absolute routes go with these notation:
  ```python
  # PostgreSQL Variables
  
  # PG_HOST: Specifies the hostname or IP address of the PostgreSQL server.
  PG_HOST = # db-server.example.com
  
  # PG_PORT: Defines the port used to connect to the PostgreSQL database.
  PG_PORT = # 5432 (default PostgreSQL port)
  
  # PG_USER: The username for authenticating with the PostgreSQL database.
  PG_USER = # your-postgresql-username
  
  # PG_PASSWORD: The password for authenticating with the PostgreSQL database.
  PG_PASSWORD = # your-postgresql-password
  
  # PG_DATABASE: The name of the PostgreSQL database to connect to.
  PG_DATABASE = # your-database-name
  
  # Google Drive Variables
  
  # CLIENT_SECRETS_PATH: Path to the client secrets file used for Google Drive authentication.
  CLIENT_SECRETS_PATH = "/path/to/your/credentials/client_secrets.json"
  
  # SETTINGS_PATH: Path to the settings file for the application configuration.
  SETTINGS_PATH = "/path/to/your/env/settings.yaml"
  
  # SAVED_CREDENTIALS_PATH: Path to the file where Google Drive saved credentials are stored.
  SAVED_CREDENTIALS_PATH = "/path/to/your/credentials/saved_credentials.json"

  # FOLDER_ID: The ID of your Google Drive folder. You can get it from the link in your folder.
  FOLDER_ID = # your-drive-folder-id
  ```

#### Demonstration of the process

![env variables](https://github.com/user-attachments/assets/1ace0df1-3313-4e59-b73b-8f5b280dbaed)

---

### 🐍 Creating the virtual environment

To install the dependencies you need to first create a Python virtual environment. In order to create it run the following command:

```bash
python 3 -m venv venv
```

Once created, run this other command to be able to run the environment. It is important that you are inside the project directory:

```bash
source venv/bin/activate
```

#### Demonstration of the process

![activar entorno](https://github.com/user-attachments/assets/e9a8eab0-0e6a-4093-8992-aaa6f6abff6c)

---

### 📦 Installing the dependencies with *pip* 

Once you enter the virtual environment you can and execute `pip install -r requirements.txt` to install the dependencies. Now, you can execute both the notebooks and the Airflow pipeline.

#### Demonstration of the process

![pip install](https://github.com/user-attachments/assets/99ab96f9-4782-46b5-80ec-d5653bb0103d)

---

### 📔 Running the notebooks

Before executing the notebooks, it's necessary to **execute the *00-grammy_raw_load* notebook**; that notebook loads the Grammys Awards dataset into a PostgreSQL database.

After you have run that notebook, then run the others in the following order. Remember that you can run all the cells in the notebook using the “Run All” button:

   1. *01-EDA_Spotify.ipynb*
   2. *02-EDA_Grammys.ipynb*
   3. *03-data_pipeline.ipynb*

![Ejecutar todo](https://github.com/user-attachments/assets/23855432-fe8f-49ca-9cac-6175b5ba84de)
  
Remember to choose **the right Python kernel** at the time of running the notebook.

![Python kernel](https://github.com/user-attachments/assets/b22bc16d-028a-4b0d-8565-7dde8434d7bf)

---

### ☁ Deploy the Database at a Cloud Provider

To perform the Airflow tasks related to Data Extraction and Loading we recommend **making use of a cloud database service**. Here are some guidelines for deploying your database in the cloud:

* [Microsoft Azure - Guide](https://github.com/mitgar14/etl-workshop-2/blob/main/docs/guides/azure_postgres.md)
* [Google Cloud Platform (GCP) - Guide](https://github.com/mitgar14/etl-workshop-2/blob/main/docs/guides/gcp_postgres.md)

---

### 🚀 Running the Airflow pipeline

To run Apache Airflow you must first export the `AIRFLOW_HOME` environment variable. This environment variable determines the project directory where we will be working with Airflow.

```bash
export AIRFLOW_HOME="$(pwd)/airflow"
```

Finally, you can run Apache Airflow with the following command:

```bash
airflow standalone
```

Allow Apache Airflow to read the modules contained in `src` by giving the absolute path to that directory in the configuration variable `plugins_folder` at the `airflow.cfg` file:

![plugins_path](https://github.com/user-attachments/assets/4b8cd7e0-1648-4c87-bc5d-596e1ac8ec43)

#### Demonstration of the process

> [!IMPORTANT]
> You need to enter the address [http://localhost:8080](http://localhost:8080/) in order to run the Airflow GUI and run the DAG corresponding to the project (*workshop2_dag*).

![airflow](https://github.com/user-attachments/assets/2cea557b-391a-4385-818b-8c3822e00076)


## Thank you! 💕

Thanks for visiting my project. Any suggestion or contribution is always welcome 🐍.
