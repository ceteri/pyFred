#!/usr/bin/env python
# encoding: utf-8

## Python impl of JFRED, developed by Robby Garner and Paco Nathan
## See: http://www.robitron.com/JFRED.php
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.


import socket


######################################################################
## client classes
######################################################################

class Convo (object):
    def converse (self, response):
        return raw_input(response)


class TCPConvo (Convo):
    max_line_size = 1024

    def __init__ (self, client):
        self.client = client

    def converse (self, response):
        self.client.send(response)
        return self.client.recv(max_line_size)


class FRED (object):
    def __init__ (self, rules):
        self.rules = rules


    def chat (self, convo):
        response = self.rules.choose_first()

        while True:
            try:
                utterance = convo.converse(response + "\n> ")

                if not utterance:
                    break
            except EOFError:
                break
            else:
                print utterance

                response, selected_rule, weight = self.rules.choose_rule(utterance)
                print " (", selected_rule.name, weight, ")"


    def chat_tcp (self, port):
        """
        connect through TCP socket
        """
        host = ''
        backlog = 5

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(BACKLOG)

        while True:
            client, address = s.accept() 
            self.chat(TCPConvo(client));
            client.close()


if __name__=='__main__':
    FRED(None, None).chat(Convo())
