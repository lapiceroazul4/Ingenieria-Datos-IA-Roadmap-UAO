# Configuring the `settings.yaml` file 

This guide will help you configure the `settings.yaml` file used by the `PyDrive2` library in conjunction with the `store.py` module. This setup is part of a data pipeline managed by Airflow. Follow the steps below to fill in the necessary configuration fields.

## Prerequisites

Before proceeding, ensure that you have:

- **Google Cloud credentials** with the necessary OAuth 2.0 credentials.
- Access to your **client ID**, **client secret**, and **redirect URI** for Google Drive API access.
- Remember that the folder where you save the `settings.yaml` file must be in a folder named **env** located in the project directory.

### Example `settings.yaml` File

Here is an example `settings.yaml` file with placeholder values. Replace the placeholder values with your own configuration details:

```yaml
client_config_backend: file
client_config:
  client_id: your_client_id.apps.googleusercontent.com
  client_secret: your_client_secret
  redirect_uris: ['http://localhost:8090/']
  auth_uri: https://accounts.google.com/o/oauth2/auth
  token_uri: https://accounts.google.com/o/oauth2/token

save_credentials: True
save_credentials_backend: file
save_credentials_file: /path/to/your/project/credentials/saved_credentials.json

get_refresh_token: True

oauth_scope:
  - https://www.googleapis.com/auth/drive
```
  
## Instructions for `settings.yaml`

### 1. **Client Configuration Backend**

This parameter tells PyDrive2 where to retrieve the OAuth 2.0 client configuration.

```yaml
client_config_backend: file
```

Leave this set to `file`, as it indicates that the client configuration will be loaded from a file.

### 2. **Client Configuration**

This section defines the credentials required to authenticate your application with Google's OAuth 2.0 service. Replace the values below with your actual client details.

```yaml
client_config:
  client_id: your_client_id.apps.googleusercontent.com
  client_secret: your_client_secret
  redirect_uris: ['http://localhost:8090/']
  auth_uri: https://accounts.google.com/o/oauth2/auth
  token_uri: https://accounts.google.com/o/oauth2/token
```

- **client_id**: This is the unique identifier for your app provided by Google.
- **client_secret**: This is your app's secret key used for authentication.
- **redirect_uris**: URI that Google's OAuth will use to redirect after authentication. It is common to use `localhost` during development.
- **auth_uri**: The authorization endpoint for Google OAuth (usually left unchanged).
- **token_uri**: The token endpoint for Google OAuth (usually left unchanged).

### 3. **Saving Credentials**

This section tells PyDrive2 whether to save credentials and where to store them. Modify the paths as necessary to match your project directory.

```yaml
save_credentials: True
save_credentials_backend: file
save_credentials_file: /path/to/your/project/credentials/saved_credentials.json
```

- **save_credentials**: Set this to `True` to allow saving OAuth credentials for future use.
- **save_credentials_backend**: Leave as `file` to save credentials locally.
- **save_credentials_file**: Set the path to where you want to save your OAuth credentials. Adjust `/path/to/your/project` to your local project directory.

### 4. **Token Refreshing**

This parameter controls whether PyDrive2 should automatically refresh the OAuth token.

```yaml
get_refresh_token: True
```

- **get_refresh_token**: Leave this set to `True` to enable automatic refresh of the token once it expires.

### 5. **OAuth Scope**

Specify the OAuth scope to define what kind of access the application has to the user's data.

```yaml
oauth_scope:
  - https://www.googleapis.com/auth/drive
```

- **oauth_scope**: This defines the level of access your app will request. The scope `https://www.googleapis.com/auth/drive` gives full access to Google Drive.

## Instructions for `client_secrets.json`

You will also need a `client_secrets.json` file, which stores OAuth credentials provided by Google. The structure of this file is as follows:

```json
{
    "web": {
        "client_id": "your_client_id.apps.googleusercontent.com",
        "project_id": "your_project_id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "your_client_secret",
        "redirect_uris": [
            "http://localhost:8080/",
            "http://localhost:8090/"
        ]
    }
}
```

### Replace the following values with your own:

- **client_id**: The unique identifier for your app provided by Google.
- **project_id**: The Google Cloud project ID where your app is registered.
- **client_secret**: The secret key associated with your Google API.
- **redirect_uris** (*depends of the application use*): Redirect URIs used during the OAuth flow. Ensure that at least one is pointing to your local server (e.g., `http://localhost:8090/`).
    
  > **This parameter changes depending on the type of use specified in the OAuth key configuration.**

**Remember to place this file in the `env/` directory.**

## Final Steps

1. Save both the `settings.yaml` and `client_secrets.json` files in the correct locations.
2. Make sure that your OAuth credentials are properly set up in the Google Cloud Console.
3. Once configured, run your pipeline with Airflow, and the `store.py` module will utilize this file to authenticate and interact with Google Drive.
