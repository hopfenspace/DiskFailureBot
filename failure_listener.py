import socket, threading, atexit

config = None

def worker(failure_cb):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((config["bind"], config["port"]))
	sock.listen(1)
	atexit.register(lambda: sock.close())

	while True:
		client, addr = sock.accept()
		broken = []

		if config["whitelist"] and addr[0] not in config["whitelist"]:
			client.close()
			continue

		try:
			for line in client.makefile().readlines():
				disk = int(line)
				if disk > 0 and disk <= config["disk_count"]:
					broken.append(disk)

			client.close()
		except Exception as e:
			print e

		if len(broken) > 0:
			failure_cb(broken)

def startListener(_config, failure_cb):
	global config
	config = _config

	thread = threading.Thread(target=worker, args=(failure_cb, ))
	thread.daemon = True
	thread.start()
