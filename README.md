# Networking UDP Assignment

This assignment included creation of a server and client to send and receive the date or time in
either English, Maori or German. 
Works with Python 3.7.0

# Server.py
Usage: port1, port2, port3. 
<br>Port must be in range 1024 to 64,000</br>

Example:
> ```python server.py 1024 1025 1026 ```

First port is English, second is Maori, third is German.
Server binds three UDP sockets to these ports on host and waits for a packet on any of these.
Upon receiving a packet, checks it's valid, creates a response packet and sends it to the address.

# Client.py
Usage: &lt;date&gt; OR &lt;time&gt; &lt;host&gt; OR &lt;IP Address&gt; portNo
Example: 
> ```python client.py date localhost 1024 ```

Server must already be running and port must be bound there. Request packet then sent, 
if a packet is received within 1 second by client, response packet is made and printed if valid.

# DT Packet
The [dt_packet](dt_packet.py)  holds the classes for the DT-Reponse and DT-Request packets and 
global packet constants.
Each class has an initialiser, init_from_packet, check and packet method.
The DT-Response also has its own &#95;&#95;str&#95;&#95; method to print every part of the packet.
The _merge_bits_ function merges two binary numbers by a specified shift.

# License
No permission to re-use this code. However, you may examine this code for your own private study.


