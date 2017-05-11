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


import fred_client
import fred_lang
import fred_rules

import random
import sys


if __name__=='__main__':
    if len(sys.argv) < 2:
        ## CLI error, show usage
        sys.exit("usage:\n  %s rule_file [port]" % sys.argv[0])

    random.seed()
    lang = fred_lang.Language()
    rules = fred_rules.Rule.parse_file(lang, sys.argv[1])
    fred = fred_client.FRED(rules)

    if len(sys.argv) < 3:
        ## test from CLI
        fred.chat(fred_client.Convo())
    else:
        ## connect through TCP socket
        port = int(sys.argv[2])
        fred.chat_tcp(port)
