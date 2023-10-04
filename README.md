# Python MTN Telegram Balance Bot

A Python script that fetches and reports wallet balances from MTN's API to a Telegram group or chat at scheduled intervals.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Scheduled Tasks](#scheduled-tasks)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This Python script is designed to periodically retrieve wallet balances from MTN's API and send the results to a Telegram group or chat. It is a useful tool for tracking your wallet balances automatically without manual intervention.

## Features

- Fetch wallet balances from MTN's API.
- Send balance reports to a Telegram group or chat.
- Schedule balance checks at specific times.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python (3.6 or higher) installed on your system.
- Required Python packages installed (see [Installation](#installation)).
- Access to MTN's API and Telegram API credentials.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Game-Guys-Group/Python-MTN-Telegram-Balance-Bot.git
   cd Python-MTN-Telegram-Balance-Bot

2.  Create and activate a virtual environment (venv) to 
    isolate project dependecies:     
    
    ```bash
    python -m venv venv
    
    source venv/bin/activate

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt

##  Configuration

Before running the script, you need to configure the following:

* MTN API credentials.
* Telegram Bot Token.
* Telegram Group or Chat ID.
* Scheduled task times.
* A .env file to add your credentials

Please refer to [MTN MoMo API Documentation](https://momodeveloper.mtn.com/) on how to setup their API on sandbox enviroment, and [Telegram Bot API](https://core.telegram.org/bots) on how to setup a Telegram Bot and add it to a group or chat.

Ensure you store you credentials in the *.env* since they are very sensitive and no one should access them.
## Usage
To use this script, follow these steps:

1. Configure the necessary settings (see [Configuration](#configuration)).

2. Run the script:

   ```bash
   python fetch_balance.py

* The script will start fetching wallet balances and sending reports to your Telegram group or chat.

## Scheduled Tasks
You can schedule the script to run at specific times by using tools like Cron Jobs. The script is designed to fetch balances at multiple intervals during the day (e.g., 00:00 AM, and 03:00 AM).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to help improve this project.

## License

This project is licensed under the [MIT License](LICENSE). See the [LICENSE](LICENSE) file for details.