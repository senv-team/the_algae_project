# Google Drive API Setup for Desktop App (OAuth)

This guide outlines the steps to set up Google Drive API access using a **desktop app** (OAuth client credentials). These steps do not involve a service account.

---

## Prerequisites

- A Google account.
- A Google Cloud Platform (GCP) project.
- Python installed on your machine.
- Basic familiarity with Google Drive and GCP.

---

## Step 1: Create a GCP Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click **Select a Project** → **New Project**.
3. Name your project (e.g., "drive-csv-sync") and click **Create**.

---

## Step 2: Enable the Google Drive API

1. In the Cloud Console, go to **APIs & Services** → **Library**. (use search bar)
2. Search for "Google Drive API" and select it.
3. Click **Enable** to activate the API for your project.

---

## Step 3: Create OAuth Client Credentials

1. Go to **APIs & Services** → **Credentials**.
2. Click **Create Credentials** → **OAuth Client ID**.
3. Configure the consent screen:
   - **User Type**: Select **External**.
   - Fill in the required fields (e.g., app name, support email).
   - Add your email as a **test user** under **Test users**.
4. Create the OAuth client:
   - **Application Type**: Select **Desktop App**.
   - Name your client (e.g., "CSV Sync Client").
   - Click **Create**.
5. Download the credentials file (`client_secret_XXX.json`) and rename it to `credentials.json`.

## Step 4: Add a Test User

1. Navigate to **APIs & Services** → **OAuth Consent Screen** → **Audience**.
2. Under the **Test Users** section, click **Add Users**.
3. Add your Google account email (and any collaborators' emails).

---

## Step 5: Install Required Python Libraries

Run the following command to install the necessary libraries:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas
