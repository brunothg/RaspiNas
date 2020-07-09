import socket
import socketserver
import ledsd

class LedClientHandler(socketserver.BaseRequestHandler):
    def getLedService(self) -> ledsd.LedsService:
        return self.server.ledservice

    def handle(self):
        client: socket.socket = self.request
        client.settimeout(3)
        # print('Got client: ' + str(client))

        with client:
            buffer = bytearray()
            while True:
                data = b''
                try:
                    data = client.recv(1024)
                    if len(data) <= 0:
                        break
                except socket.timeout:
                    break
                else:
                    for byte in data:
                        if byte == ord('\n'):
                            cmdline = buffer.decode('utf-8').strip()
                            buffer = bytearray()
                            if len(cmdline) > 0:
                                okResult = self.__onCmdLine(client, cmdline)
                                if not okResult:
                                    break
                        else:
                            buffer.append(byte)
                    else:
                        continue
                    break


    def __onCmdLine(self, client: socket.socket, cmdline: str) -> bool:
        keepRunning = False

        try:
            cmdParts = cmdline.split(':')
            action = cmdParts[0]
            selector = cmdParts[1]
            parameters = cmdParts[2:]
            print('Do ' + action + ' for ' + selector + ' with ' + str(parameters))

            ledservice = self.getLedService()
            led = None
            if len(selector) > 0:
                led = ledservice.getLed(selector)

            if action == 'set-state':
                if parameters[0] in ('on', '1', 'true'):
                    led.on()
                elif parameters[0] in ('off', '0', 'false'):
                    led.off()
            elif action == 'get-state':
                client.sendall((str(int(led.is_active)) + '\n').encode('utf-8'))
            else:
                print('Unknown action: ' + action)
                client.sendall(('Unknown action "' + action + '"\n').encode('utf-8'))

        except (IndexError, AttributeError) as e:
            print(e)
            keepRunning = False

        return keepRunning
