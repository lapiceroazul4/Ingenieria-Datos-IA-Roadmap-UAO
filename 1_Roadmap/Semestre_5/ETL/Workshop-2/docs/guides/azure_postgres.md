# 📘 Guide: Setting Up a PostgreSQL Database on Azure

## Description

This guide provides step-by-step instructions for creating a PostgreSQL database on Microsoft Azure, covering everything from initial setup to connecting the database to a PostgreSQL client.

---

## 🛠️ Prerequisites

Before getting started, ensure you have the following:

- **Microsoft Azure Account** – Sign up [here](https://azure.microsoft.com/en-us/free/) if you don’t have an account yet.
- **PostgreSQL Client** – You can use pgAdmin or another client to manage PostgreSQL databases.

---

## 🔑 Step 1: Log in to the Azure Portal

1. Open the [Azure Portal](https://portal.azure.com/) in your browser.
2. Log in with your Azure account credentials.

![login](https://github.com/user-attachments/assets/41f1324c-7050-4db9-9aa9-c1dbe981f0a8)

---

## 🗂️ Step 2: Navigate to "*Create a PostgreSQL Database*"

In the Azure Portal, go to **Create a resource** > **Databases** > **Azure Database for PostgreSQL**.

![navigation](https://github.com/user-attachments/assets/a368809e-f781-4cfb-b0f9-7526db20b83c)

---

## 🏗️ Step 3: Create a PostgreSQL Database

1. On the **Create PostgreSQL Database** screen, fill out the following details:
    - **Subscription**: Select your subscription.
    - **Resource Group**:
        - If you don’t have a resource group, click ***Create new*** and provide a descriptive name.
        - If you already have a resource group, select it from the dropdown menu.
    - **Server Name**: Choose a globally unique name for your server.
    - **Region**: Select your preferred region (choose one near you for better performance).
    - **Version**: Choose the PostgreSQL version (recommended: 13 or higher).
    - **Workload type**: Select *Development*.

    ![first](https://github.com/user-attachments/assets/24b47df6-cdf4-431d-9ca4-624a38e8bfb2)

2. Now go to the **Configure server** section. It is recommended to adjust the settings as follows:
    - **Compute tier**: Flexible, ideal for workloads that don’t require continuous full CPU usage.
    - **Processor size**: Standard_B1ms (1 vCPU, 2 GiB memory, 640 IOPS max).
    - **Performance level**: P6 (240 iops).
    
    ![configure](https://github.com/user-attachments/assets/156d3cff-0c09-46cc-a414-722f636fcae9)

3. In *Authentication*, choose ***PostgreSQL Authentication*** as the **Authentication method** and set the **Administrator Username** and **Password**.
4. Click **Next: Networking >**.

---

## 🔒 Step 4: Configure Firewall Rules

1. Once you’re on the ***Networking*** section, go to **Firewall Rules**.
2. Add a new **Firewall Rule** to allow access to your database:
   
    - **Name**: Assign a name to the rule.
    - **Start IP/End IP**: You can allow access from your current IP or enable access from all IPs (*be cautious if you allow access from all IPs*).
      
4. Click **Review + Create** and then ***Create***.

![networking](https://github.com/user-attachments/assets/ef020cbc-d25a-4da6-bd1e-18046b2b1ec4)

---

## ⚙️ Step 5: Connect to the PostgreSQL Database

You can connect to the PostgreSQL database using your favorite client (e.g., pgAdmin or psql).

1. In your PostgreSQL client, provide the following connection details:
   
    - **Host**: The server name (e.g., `your_server.postgres.database.azure.com`).
    - **Port**: 5432.
    - **Username**: The admin username (e.g., `postgres`).
    - **Password**: The password you set when creating the database.
    - **Database Name**: `postgres` (*default database or any other you create later*).
      
3. Test the connection and start managing your PostgreSQL database.

![pgadmin](https://github.com/user-attachments/assets/15177cbd-aa52-4bb7-9ebd-a508a3f5177d)

---

## 🎉 Conclusion

You have successfully created a PostgreSQL database on Azure and connected to it using a PostgreSQL client. Remember to regularly monitor performance and manage costs efficiently.
