# vfs-visa-slot-germany
Every 2 minutes, check for visa slots at VFS website. <br/>
If there are any, send a call and a message of the format:
> Sent from your Twilio trial account - Earliest Available Slot : 30/11/2021 at 2021-11-01 13:02:07


## Why
If you are here, you already know the hassle of booking a visa slot using VFS website. <br/>
I got way too much time in my life, so instead to destroying my sleep, I created this script.

## Usage
Step 1: Clone the repo: `git clone https://github.com/seedlit/vfs-visa-slot-germany.git` <br/>
Step 2: Move into the repo: `cd vfs-visa-slot-germany` <br/>
Step 3: Create a new virtual environment: `python3 -m venv venv` <br/>
Step 4: Activate the environment (might differ a bit for windows and MacOS): `source venv/bin/activate` <br/>
Step 5: Install the dependencies: `pip install -r requirements.txt` <br/>
Step 6: Run the script: `python check_slots.py`

## Dependency
Note that you need to have an account on Twilio to get text and call alerts. <br/>
You can signup here ([https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)) for a trial account to get credits upto worth $10.