#!/usr/bin/python3

import re
import sys
import subprocess

sys.path.append('/boot/midihost')
import midihost_config

card_id_regex = r'^\s*([0-9]+)\s*\[.*$'
usb_id_regex = r'^.*usb-1\.([0-9]+).*$'
aconnect_regex = r'^client ([0-9]+):.*\[.*card=([0-9]+).*$'

current_card = None
card_usb_map = {}

with open('/proc/asound/cards', 'r') as cards:
    for line in cards.readlines():
        line = line.rstrip('\n')
        card_match = re.search(card_id_regex, line)
        if card_match:
            current_card = card_match.group(1)
            continue
        usb_match = re.search(usb_id_regex, line)
        if usb_match:
            card_usb_map[current_card] = usb_match.group(1)

usb_client_map = {}

aconnect_result = subprocess.run(['aconnect', '-i'], capture_output=True, text=True)
for line in aconnect_result.stdout.splitlines():
    match = re.search(aconnect_regex, line)
    if match:
        usb_client_map[int(card_usb_map[match.group(2)])] = int(match.group(1))

for (src_usb_port, src_port), *dsts in midihost_config.CONNECTIONS:
    for (dst_usb_port, dst_port) in dsts:
        try:
            subprocess.run(['aconnect', f'{usb_client_map[src_usb_port]}:{src_port}',  f'{usb_client_map[dst_usb_port]}:{dst_port}'])
        except KeyError:
            pass
