![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)
![Security Status](https://img.shields.io/security-headers?label=Security&url=https%3A%2F%2Fgithub.com&style=flat-square)
![Gluten Status](https://img.shields.io/badge/Gluten-Free-green.svg)
![Eco Status](https://img.shields.io/badge/ECO-Friendly-green.svg)
![Alco Status](https://img.shields.io/badge/Contains-Alcohol-red.svg)

# Teltonika TCP Server - Codec 8 Extended parser

Personal Hobby project with Python.

Simple TCP server which listens for Teltonika trackers communicating via Codec 8 Extended using TCP

Server waits for device to send IMEI then responds with "01", device then must send Codec 8 Extended packet, server responds with records number.

Codec 8 documentation can found via URL bellow:
https://wiki.teltonika-gps.com/view/Codec

Server - Device communication must work but not yet tested

AVL IDs are parsed, AVL Data - not yet parsed

AVL IDs and Raw values ar saved in ./data/data.json

## Project Features:

- Basic TCP communaction - must work correctly
- Codec 8 Extended structure parsing - done!
- Saving AVL IDs with RAW values to JSON - done!
- TCP Server and Parser functionality - done!

## Planed Features - not done yet:

- Codec 8 (not extended support) - not done yet
- AVL IDs value parsing - not done yet
- User interface via Browser - not done yet
- More... - not done yet

### How to test?:

- Install latest Python version from: https://www.python.org/
- Download "main.py" and Data folder: ./data/data.json
- Open "main.py" with any text editor, change 'port' to YOUR open Port
- Run "main.py" via terminal
- Follow on screen instructions

## Auhors:
[Justas](https://github.com/Justas1988) <br>
[LinkedIn](https://www.linkedin.com/in/justas-belevi%C4%8Dius-4a5485219/)
