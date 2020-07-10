import socket
import socketserver
import fansd

class FanClientHandler(socketserver.BaseRequestHandler):
    def getFanService(self) -> fansd.FansService:
        return self.server.fanservice

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

            fanservice = self.getFanService()
            fan = None
            if len(selector) > 0:
                fan = fanservice.getFan(selector)

            if action == 'set-state':
                if parameters[0] in ('on', '1', 'true'):
                    fan.on()
                elif parameters[0] in ('off', '0', 'false'):
                    fan.off()
                elif parameters[0] in ('auto', '-1'):
                    fan.auto()
            elif action == 'get-state':
                client.sendall((str(int(fan.is_active)) + '\n').encode('utf-8'))
            elif action == 'set-autotemp':
                fan.setAutoTemperature(float(parameters[0]))
            elif action == 'get-autotemp':
                client.sendall((str(fan.getAutoTemperature()) + '\n').encode('utf-8'))
            elif action == 'set-autotolerance':
                fan.setAutoTemperatureTolerance(float(parameters[0]))
            elif action == 'get-autotolerance':
                client.sendall((str(fan.getAutoTemperatureTolerance()) + '\n').encode('utf-8'))
            elif action == 'get-temperature':
                client.sendall((str(fan.getTemperature()) + '\n').encode('utf-8'))
            else:
                print('Unknown action: ' + action)
                client.sendall(('Unknown action "' + action + '"\n').encode('utf-8'))

        except (IndexError, AttributeError) as e:
            print(e)
            keepRunning = False

        return keepRunning
