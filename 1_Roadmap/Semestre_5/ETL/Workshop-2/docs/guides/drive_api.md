# Configuring the Google Drive API

This guide will help you configure the Google Drive API and obtain the `client_secrets.json` file that contains the credentials needed to authenticate applications accessing Google Drive.

## Requirements

- Google account.
- Access to the [Google Cloud Console](https://console.cloud.google.com/).

## Steps to Activate the Google Drive API and Obtain the `client_secrets.json` File

### 1. Create a Project in Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Click on the **Projects** dropdown menu in the upper-left corner and select **New Project**.
3. Specify the project name and select a location.
4. Click **Create**.

---

![drive-crear](https://github.com/user-attachments/assets/395ae553-2c92-47b4-bffd-75cba5c435d8)

### 2. Enable the Google Drive API

1. With the project selected, go to the left navigation menu and select **API & Services** > **Library**.
2. In the search field, type **Google Drive API**.
3. Select **Google Drive API** from the results.
4. Click **Enable**.

---

![drive](https://github.com/user-attachments/assets/287ea3a8-7c42-422e-bddc-bf36f11f6e01)

### 3. Create OAuth 2.0 Credentials

1. Once the API is enabled, select **Credentials** from the left-hand menu.
2. Click **Create credentials** and select **OAuth client ID**.
3. If you haven’t configured the OAuth consent screen yet, you will be prompted to do so:
   
    - Click on **Configure consent screen**.
    - Select **External** as the user type and click **Create**.
    - Fill in the basic information (application name, email address, etc.), then click **Save and Continue** until the configuration is complete.
  
    ---

    ![consentimiento](https://github.com/user-attachments/assets/417bb864-8811-4c80-a257-9a219a975555)
      
5. After configuring the consent screen, select **Desktop app** as the application type when creating credentials.
6. Click **Create**.

---

![oauth](https://github.com/user-attachments/assets/703302ae-4376-4f06-9109-ed987d276b95)

### 4. Download the `client_secrets.json` File

1. After creating the OAuth client ID, you will see an option to **Download** the credentials file.
2. Download the `client_secrets.json` file and save it to your project directory.

---

![credentials](https://github.com/user-attachments/assets/650d40f8-c72f-4ebd-af03-661c3b017160)

### 5. Install the `PyDrive2` Library (Optional)

If you're working with Python to interact with Google Drive, you can use the `PyDrive2` library:

```bash
pip install PyDrive2

```

### 6. Using the `client_secrets.json` File

The `client_secrets.json` file is necessary to authenticate your application with Google Drive using OAuth 2.0. This file should be used when configuring your application's authentication flow.

### 7. Run Your Application

Depending on the library you're using, configure your application to load the `client_secrets.json` file and follow the OAuth 2.0 authentication flow.

## Additional Notes

- Ensure that you do not share the `client_secrets.json` file publicly, as it contains sensitive information for your Google API authentication.
- Keep this file in a secure directory and exclude it from any public repository by adding it to the `.gitignore` file if necessary.
