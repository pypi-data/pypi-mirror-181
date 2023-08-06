AmfiTrack extensions for the [Amfiprot](https://pypi.org/project/amfiprot/) package.

# Installation
Install (or update) with `pip`:

```shell
pip install -U amfiprot-amfitrack
```

# Usage example
Instead of creating a generic `amfiprot.Device`, create an `amfitrack.Device` to get access to AmfiTrack specific functionality and payload interpretation:

```python
import amfiprot
import amfiprot_amfitrack as amfitrack

VENDOR_ID = 0xC17
PRODUCT_ID = 0xD12

if __name__ == "__main__":
    conn = amfiprot.UsbConnection(VENDOR_ID, PRODUCT_ID)
    nodes = conn.find_nodes()

    print(f"Found {len(nodes)} node(s).")
    for node in nodes:
        print(f"[{node.tx_id}] {node.name}")

    dev = amfitrack.Device(nodes[0])
    conn.start()
    
    cfg = dev.config.read_all()
    dev.calibrate()

    while True:
        if dev.packet_available():
            packet = dev.get_packet()
            if type(packet.payload) == amfitrack.PayloadType.RawBFieldPayload:
                payload: amfitrack.payload.RawBFieldPayload = packet.payload
                print(payload.b_field)
```