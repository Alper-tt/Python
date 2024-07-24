# Python Automation and API Fundamentals

Welcome to the repository for my Python automation and API projects. This repository contains various projects and scripts focused on learning and experimenting with Python, Selenium, and API interactions, specifically with the Trendyol platform. These projects are strictly for educational and testing purposes and are not intended to interfere with any algorithms or systems.

## Repository Structure

The repository is organized into three main directories:

### 1. Fundamentals
This directory contains basic Python scripts that have helped me during my learning journey. Here, you will find examples and exercises on:
- Variables
- If-Else Statements
- Try-Except Blocks
- Classes
- Regular Expressions (Regex)
- Collections Module

These scripts are foundational exercises to understand Python programming concepts.

### 2. Selenium
The Selenium directory is divided into two subdirectories:

#### a. Beginner-Test
This folder contains initial Selenium scripts where I practiced basic automation tasks such as:
- Logging in as a user
- Adding products to favorites
- Adding products to the cart
- Following stores
- Asking questions about products
- Adding products to collections

These scripts were designed to explore and understand the capabilities of Selenium for web automation.

#### b. Final
This folder includes more refined scripts that compile all the functionalities explored in the Beginner-Test section. Key scripts include:
- `trendyol-v1.1.py`: A comprehensive script automating various user interactions on Trendyol, including favoriting products, adding to the cart, and more.
- `trendyol-kayit.py`: Automates the registration process on Trendyol using a temporary email fetched through an API, bypasses reCAPTCHA using a Google extension, and completes the email verification process.

### 3. API
The API directory focuses on interacting with Trendyol's APIs. It contains two main sections:

#### a. Seller Operations
Includes programs for Trendyol sellers to manage their products. The scripts automate the creation of discounts and coupons by:
- Setting discount periods and amounts
- Changing coupon names, which cannot be altered through the Trendyol seller panel

These scripts aim to streamline the process for sellers and reduce the time needed for these tasks.

#### b. Customer Operations
Contains scripts for customer-side operations using Trendyol APIs, such as:
- Adding products to favorites and collections
- Adding and removing products from the cart
- Following stores
- Changing user passwords
- Fetching user tokens

These operations utilize proxies to avoid IP blocking due to excessive requests.

## Disclaimer
All scripts and projects in this repository are created solely for testing and educational purposes. They are not intended to be used in any manner that could harm or disrupt Trendyol's systems or services.

## Getting Started
To explore the projects, clone the repository and navigate to the desired directory. For the scripts involving API interactions or Selenium automation, ensure you have the necessary dependencies installed:

```bash
pip install -r requirements.txt