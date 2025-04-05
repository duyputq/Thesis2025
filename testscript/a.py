from mininet.net import Mininet
from mininet.node import Host
from mininet.link import TCLink
from mininet.cli import CLI
import paho.mqtt.client as mqtt

class IoTHost(Host):
    def config(self, **params):
        super(IoTHost, self).config(**params)
        # Cấu hình để chạy MQTT Client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect("mqtt.eclipse.org", 1883, 60)  # Broker MQTT
        self.mqtt_client.loop_start()

    def send_data(self, topic, message):
        # Gửi dữ liệu lên broker MQTT
        self.mqtt_client.publish(topic, message)

# Khởi tạo Mininet với IoT Host
net = Mininet(link=TCLink)
h1 = IoTHost('h1')  # Tạo IoT host
net.addNode(h1)
net.start()

# Gửi dữ liệu từ h1 (cảm biến IoT)
h1.send_data("sensor/temperature", "22.5")

CLI(net)
net.stop()
