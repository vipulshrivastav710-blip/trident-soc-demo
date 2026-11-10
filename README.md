# Trident public SOC demo

A read-only public showcase for Trident's analyst workflow. It uses four static, fictional alerts and does not import the local Trident backend.

## Public demo boundaries

- All alert IDs, identities, hosts, destinations, and events are synthetic.
- The IP addresses use the documentation-only ranges reserved for examples.
- There is no QRadar connector, login or role selector, local database, secret, case-note submission, or write action.
- Search and severity filters operate only on the static examples in this file.
- Do not add real SOC records, API credentials, or live connectors to this public showcase.

## Deploy on Streamlit Community Cloud

Community Cloud deploys from GitHub. This repository contains only the isolated demo app.

1. In Community Cloud, create an app from this repository on the main branch with streamlit_app.py as the entrypoint. No secrets are needed.
2. In app sharing settings, choose **This app is public and searchable** to make the app accessible to anyone.
3. Share the resulting streamlit.app URL.

This public showcase uses only static synthetic examples. Keep the source and data within these boundaries.
