import socket, ssl, threading, atexit

def worker(config, failure_cb):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((config["bind"], config["port"]))
	sock.listen(1)
	atexit.register(lambda: sock.close())

	context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH, cafile=config["cert-authority"])
	context.verify_mode = ssl.CERT_REQUIRED
	context.load_cert_chain(certfile=config["cert"], keyfile=config["key"])

	broken = config["disk_count"] * [False]
	while True:
		try:
			client, addr = sock.accept()
			client = context.wrap_socket(client, server_side=True)

			for line in client.makefile().readlines():
				split = line.split(':')
				disk = int(split[0])
				if disk > 0 and disk <= config["disk_count"]:
					if split[1].strip() == '0':
						broken[disk - 1] = False
					else:
						broken[disk - 1] = True

			failure_cb([i + 1 for i, v in filter(lambda t: t[1], enumerate(broken))])
		except Exception as e:
			print(e)
		finally:
			client.close()


def startListener(config, failure_cb):
	thread = threading.Thread(target=worker, args=(config, failure_cb, ))
	thread.daemon = True
	thread.start()
