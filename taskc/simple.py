import ssl
import socket

c = ssl.create_default_context()
c.load_cert_chain("/home/jack/.task/jacklaxson.cert.pem", "/home/jack/.task/jacklaxson.key.pem")
c.load_verify_locations("/home/jack/.task/ca.cert.pem")
c.check_hostname = False
conn = c.wrap_socket(socket.socket(socket.AF_INET))
conn.connect(("192.168.1.110", 53589))
print conn.getpeercert()