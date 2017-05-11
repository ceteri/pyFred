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


import math
import operator
import random


######################################################################
## fuzzy logic support
## this implements rule selection, based on a flavor of fuzzy ranking
######################################################################

class FuzzyUnion (object):
    def __init__ (self):
        self.rule_set = {}


    def add_rule (self, rule, weight):
        if rule.name not in self.rule_set:
            # add a new rule
            self.rule_set[rule.name] = [rule, weight]
        else:
            # update the weight for an existing rule
            r, prev_weight = self.rule_set[rule.name]
            self.rule_set[rule.name] = [rule, prev_weight + weight]


    @staticmethod
    def fuzzy_sort (x):
        [name, [rule, weight]] = x
        return weight, rule.priority


    def select_rule (self):
        # sort descending based on weight, priority

        sorted_rules = sorted(self.rule_set.items(),
                              key=lambda x: FuzzyUnion.fuzzy_sort(x),
                              reverse=True
                              )

        weight_dist = map(lambda x: x[1][1], sorted_rules)
        tot_sum = sum(weight_dist)

        # convert the sorted list of weights into something vaguely
        # akin to an exponential distribution (if you squint hard)

        exp_dist = [math.exp(x / tot_sum * -2.0) for x in weight_dist]
        estimator = random.uniform(0.0, sum(exp_dist))
        i = 0

        # generate a random variable and use that to select a rule

        for x in exp_dist:
            if estimator <= x:
                break
            else:
                i += 1
                estimator -= x

        rule_name, rule_value = sorted_rules[i]
        rule, weight = self.rule_set[rule_name]

        return rule, weight


    def is_empty (self):
        return len(self.rule_set) == 0


if __name__=='__main__':
    fuzzy = Fuzzy()
    print fuzzy
