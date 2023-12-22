from __future__ import annotations
from typing import List, Tuple, Dict
from enum import Enum, auto
from abc import ABC, abstractmethod


class SignalType(Enum):
    HIGH = auto()
    LOW = auto()


class IModule(ABC):
    listeners = []
    out_signal = None

    @abstractmethod
    def receive_signal(self, signal: SignalType) -> None:
        pass

    @abstractmethod
    def send_out_signal(self) -> None:
        pass


class FlipFlop(IModule):
    def __init__(self) -> None:
        self.is_on = False
        self.out_signal = None
        self.listeners = []

    def add_listener(self, listener: IModule):
        self.listeners.append(listener)

    def receive_signal(self, signal: SignalType) -> None:
        if signal == SignalType.HIGH:
            return
        if self.is_on:
            self.is_on = False
            self.out_signal = SignalType.LOW
            return
        self.is_on = True
        self.out_signal = SignalType.HIGH

    def send_out_signal(self) -> None:
        if self.out_signal is None:
            return
        for listener in self.listeners:
            listener.receive_signal(self.out_signal)


class Conjunction (IModule):
    def __init__(self) -> None:
        self.listeners = []
        self.default_memory = []
        self.memory_idx = 0
        self.input_signals_memory = []
        self.out_signal = None

    def add_item_to_memory(self):
        self.default_memory.append(SignalType.LOW)
        self.input_signals_memory = self.default_memory
    
    def add_listener(self, listener: IModule):
        self.listeners.append(listener)

    def receive_signal(self, signal: SignalType) -> None:
        if signal == SignalType.LOW and self.memory_idx > 0:
            self.memory_idx -= 1
            self.input_signals_memory[self.memory_idx] = SignalType.LOW
        if signal == SignalType.LOW:
            return
        if self.memory_idx > len(self.default_memory) - 1:
            return
        self.input_signals_memory[self.memory_idx] = SignalType.HIGH
        self.memory_idx += 1

    def send_out_signal(self) -> None:
        if all([signal == SignalType.HIGH for signal in self.input_signals_memory]):
            self.out_signal = SignalType.LOW
        else:
            self.out_signal = SignalType.HIGH
        for listener in self.listeners:
            listener.receive_signal(self.out_signal)


class Broadcaster(IModule):
    def __init__(self):
        self.listeners = []
        self.out_signal = None

    def add_listener(self, listener: IModule):
        self.listeners.append(listener)

    def receive_signal(self, signal: SignalType) -> None:
        self.out_signal = signal

    def send_out_signal(self) -> None:
        assert self.out_signal is not None, 'should be unreachable'
        for listener in self.listeners:
            listener.receive_signal(self.out_signal)


class Button(IModule):
    def __init__(self):
        self.listeners = []
        self.out_signal = SignalType.LOW

    def add_listener(self, listener: IModule):
        self.listeners.append(listener)

    def receive_signal(self, signal: SignalType) -> None:
        raise RuntimeError('This should not receive signals')

    def send_out_signal(self) -> None:
        for listener in self.listeners:
            listener.receive_signal(self.out_signal)

class Output:
    def __init__(self) -> None:
        self.listeners = []

    def receive_signal(self, signal: SignalType) -> None:
        return

    def send_out_signal(self) -> None:
        return


def parse_line(input: str) -> Tuple[str, List[str], IModule]:
    name, str_listener_names = input.split(" -> ")
    listener_names = str_listener_names.split(", ")
    if name[0] == '%':
        return (name[1:], listener_names, FlipFlop())
    if name[0] == '&':
        return (name[1:], listener_names, Conjunction())
    if name == 'broadcaster':
        return ('broadcaster', listener_names, Broadcaster())
    if name == 'button':
        return ('button', listener_names, Button())
    raise RuntimeError('Parsing error')


def get_module_dict(input: str) -> Dict[str, IModule]:
    dict_modules = {}
    dict_module_listeners = {}
    split_input = input.split("\n")
    for line in split_input:
        name, listener_names, module = parse_line(line)
        dict_modules[name] = module
        dict_module_listeners[name] = listener_names
    for k, v in dict_module_listeners.items():
        listener_names = v
        for name in listener_names:
            if isinstance(dict_modules.get(name), Conjunction):
                dict_modules[name].add_item_to_memory()
            if dict_modules.get(name) is None:
                dict_modules[k].add_listener(Output())
            else:
                dict_modules[k].add_listener(dict_modules[name])
    if dict_modules.get('button') is None:
        dict_modules['button'] = Button()
        dict_modules['button'].add_listener(dict_modules['broadcaster'])
    return dict_modules


def button_press(dict_modules: Dict[str, IModule]) -> Tuple[int, int]:
    low_sig_count = 0
    high_sig_count = 0
    module_signal_queue = [dict_modules['button']]
    not_flipflop = lambda x: not(isinstance(x, FlipFlop))
    not_output = lambda x: not(isinstance(x, Output))
    for module in module_signal_queue:
        module.send_out_signal()
        if module.out_signal == SignalType.LOW:
            next_in_queue = [l for l in module.listeners if not_output(l)]
        if module.out_signal == SignalType.HIGH:
            next_in_queue = [l for l in module.listeners if not_flipflop(l) and not_output(l)]           
        module_signal_queue.extend(next_in_queue)
        if module.out_signal == SignalType.LOW:
            low_sig_count += 1 * len(module.listeners)
        if module.out_signal == SignalType.HIGH:
            high_sig_count += 1 * len(module.listeners)

    return low_sig_count, high_sig_count


def solution_part_1(input: str) -> None:
    dict_modules = get_module_dict(input)
    total_low_sig_count, total_high_sig_count = 0,0
    for _ in range(1000):
        low_sig_count, high_sig_count = button_press(dict_modules)
        total_low_sig_count += low_sig_count
        total_high_sig_count += high_sig_count
    print(total_low_sig_count * total_high_sig_count)

def get_cycle_length(module_name: str, input: str) -> int:
    i = 0
    dict_modules = get_module_dict(input)
    while(dict_modules[module_name].out_signal != SignalType.LOW):
        i+=1
        button_press(dict_modules)
    return i
    
    

def solution_part_2(input: str) -> None:
    #turns out using graphviz rx is basically counting when cycles
    #the nodes seem to get turned on and only turn off when the cycle completes
    from math import lcm
    mj_nodes = ['js', 'pc', 'pz', 'lr', 'xn', 'mf', 'mr', 'qm']
    qs_nodes = ['qc', 'hh', 'tp', 'xq', 'ks', 'hf', 'nd']
    rd_nodes = ['mb', 'cv', 'rh', 'bz', 'xs', 'kl', 'hk', 'lf']
    cs_nodes = ['gk', 'mn', 'md', 'cj', 'zs', 'jb', 'bp', 'bb', 'zm']

    mj_cycle_length = max([get_cycle_length(node, input) for node in mj_nodes])
    qs_cycle_length = max([get_cycle_length(node, input) for node in qs_nodes])
    rd_cycle_length = max([get_cycle_length(node, input) for node in rd_nodes])
    cs_cycle_length = max([get_cycle_length(node, input) for node in cs_nodes])
    print(lcm(mj_cycle_length, qs_cycle_length, rd_cycle_length, cs_cycle_length))
        


with open(r'day_20\puzzle_input.txt', 'r') as input:
    solution_part_1(input.read())
with open(r'day_20\puzzle_input.txt', 'r') as input:
    solution_part_2(input.read())
