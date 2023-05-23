![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11.2-blue)
![Gluten Status](https://img.shields.io/badge/Gluten-Free-green.svg)
![Eco Status](https://img.shields.io/badge/ECO-Friendly-green.svg)

# Teltonika Codec 8 / Codec 8 Extended TCP Server and Parser

Personal Hobby project with Python.

Simple TCP server which listens for Teltonika trackers communicating via Codec 8 Extended using TCP

Server waits for device to send IMEI then responds with "01", device then must send Codec 8 Extended packet, server responds with records number.

Codec 8 documentation can found via URL bellow:
https://wiki.teltonika-gps.com/view/Codec

~~Server - Device communication must work but not yet tested~~ - works

AVL IDs are parsed, ~~AVL Data - not yet parsed~~ - partially parsed

AVL IDs and Raw values ar saved in ./data/data.json

## Project Features:

- TCP communaction - done!
- Codec 8 Extended structure parsing - done!
- Codec 8 structure parsing - done!
- Saving AVL IDs with RAW/Parsed values to JSON - done!
- TCP Server and Parser functionality - done!
- CRC16 checking to detect corupted packets - done!
- RAW DATA saving to separate .JSON - done!
- Seprate .JSON files for different IMEIs - done!

## Planed Features - not done yet:

- Codec 8 (not extended support) - ~~not done yet~~ - done!
- AVL IDs value parsing - ~~not done yet~~ - progress ongoing
- Beacon list: AVL 385 parsing - planing soon waiting for bad weather
- User interface via Browser - not done yet
- Limiting data.json file to X MB in size, and create new ones - not done yet
- Make server multithreaded (code rewrite may be required) - not done yet
- Implement required adjustments for Linux OS - not done yet
- Seprate .JSON files for different IMEIs - ~~not done yet~~ - done!
- More... - not done yet

### How to test?:

- Install latest Python version from: https://www.python.org/
- Download "main.py" ~~and Data folder: ./data/data.json~~ - now created automatically
- Open "main.py" with any text editor, change 'port' to YOUR open Port
- Run "main.py" via terminal
- Follow on screen instructions

## Auhors:
[Justas](https://github.com/Justas1988) <br>
[LinkedIn](https://www.linkedin.com/in/justas-belevi%C4%8Dius-4a5485219/)
