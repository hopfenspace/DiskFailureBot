import socket, ssl, threading, atexit

config = None

def worker(failure_cb):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((config["bind"], config["port"]))
	sock.listen(1)
	atexit.register(lambda: sock.close())

	context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=config["cert-authority"])
	context.verify_mode = ssl.CERT_REQUIRED
	context.load_cert_chain(certfile=config["cert"], keyfile=config["key"])

	while True:
		broken = []

		try:
			client, addr = sock.accept()
			client = context.wrap_socket(client, server_side=True)

			for line in client.makefile().readlines():
				disk = int(line)
				if disk > 0 and disk <= config["disk_count"]:
					broken.append(disk)

			failure_cb(broken)
		except Exception as e:
			print(e)
		finally:
			client.close()


def startListener(_config, failure_cb):
	global config
	config = _config

	thread = threading.Thread(target=worker, args=(failure_cb, ))
	thread.daemon = True
	thread.start()
