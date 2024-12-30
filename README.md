# HotmailVM

## Overview

The **Hotmail Valid Email Checker** is a Python-based tool designed to verify the existence of email addresses using the Microsoft Live login API. This project utilizes multithreading to efficiently check multiple email addresses concurrently, providing quick feedback on their validity.

## Features

- **Email Validation**: Checks if an email exists on the Microsoft Live platform.
- **Multithreading**: Processes multiple email checks simultaneously for faster results.
- **Random Console Title**: Generates a random title for the console window for a unique user experience.
- **Colorful Output**: Utilizes the Colorama library to provide colored output for valid and invalid email addresses.

## Requirements

To run this project, you need to have the following Python packages installed:

- `tls-client`
- `terminut`
- `colorama`
- `concurrent.futures`

You can install the required packages using pip:

```bash
pip install tls-client terminut colorama
