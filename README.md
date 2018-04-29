# Nexus (SIT_RFID)

An RFID detection system using SQLite3, Python, RaspberryPi 3, and MFRC522. A project done for a course at Stevens Institute of Technology.

## Getting Started

Update your raspberry pi:
sudo apt-get update
sudo apt-get upgrade

Get SPI-py and install it:
git clone https://github.com/lthiery/SPI-Py.git
cd ~/SPI-Py
sudo python setup.py install

Get the MFRC522 Code:
git clone https://github.com/pimylifeup/MFRC522-python.git

Add all your files to your project folder and connect the Pi and MFRC522 together (many tutorials can be found online).

Install SQLite3 and Flask.

Run DatabaseInitiate.py and ChairTable.py to initiate the User and Chair tables in RFID.db.
Run the app with: sudo python app.py
In a web browser type your IP in the search bar.

To read in a new user into the dabatase run DatabaseLoad and scan an RFID card to continue.
To search the user database run DatabaseSearch.
