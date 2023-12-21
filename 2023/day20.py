from enum import IntEnum
import math
from typing import Any

with open("input/day20", "r") as f:
    lines = list(filter(lambda x: x != "", f.read().split("\n")))


class Pulse(IntEnum):
    LOW = 0
    HIGH = 1


class Module:
    name: str
    destinations: list[str]

    def __init__(self, name: str, destinations: list[str]):
        self.name = name
        self.destinations = destinations


class FlipFlopModule(Module):
    state: int

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.state = 0  # off

    def receive(self, pulse: Pulse) -> Pulse | None:
        if pulse == Pulse.HIGH:
            return

        send_off = Pulse.HIGH if self.state == 0 else Pulse.LOW
        self.state = self.state ^ 1  # flip the state
        return send_off

    def __repr__(self):
        return f"%{self.name}: {self.state} -> {', '.join(self.destinations)}"


class ConjunctionModule(Module):
    memory: dict[str, Pulse]

    def __init__(self, name: str, destinations: list[str]):
        super().__init__(name, destinations)
        self.memory = {}

    def add_to_initial_memory(self, name: str):
        self.memory[name] = Pulse.LOW

    def receive(self, name: str, pulse: Pulse) -> Pulse | None:
        self.memory[name] = pulse
        if all(self.memory.values()):
            return Pulse.LOW
        return Pulse.HIGH

    def __repr__(self):
        return (
            f"&{self.name} -> {', '.join(self.destinations)}\n\t{self.memory}\n"
        )


class Broadcaster(Module):
    def __init__(self, destinations: list[str]):
        super().__init__("broadcaster", destinations)

    def receive(self, pulse: Pulse) -> Pulse:
        return pulse

    def __repr__(self):
        return f"{self.name} -> {', '.join(self.destinations)}"


class Button(Module):
    def __init__(self, destinations: list[str]):
        super().__init__("button", destinations)

    def receive(self) -> Pulse:
        return Pulse.LOW


def parse_line(l: str) -> Module:
    module_name, destinations = l.split(" -> ")
    if module_name == "broadcaster":
        return Broadcaster(destinations.split(", "))
    if module_name.startswith("%"):
        return FlipFlopModule(module_name[1:], destinations.split(", "))
    return ConjunctionModule(module_name[1:], destinations.split(", "))


module_list = [parse_line(l) for l in lines]


def initialise_modules() -> dict[str, Module]:
    module_dict = {m.name: m for m in module_list}
    for n, m in module_dict.items():
        if isinstance(m, ConjunctionModule):
            for n1, m1 in module_dict.items():
                if n1 == n:
                    continue
                if n in m1.destinations:
                    m.add_to_initial_memory(n1)
    return module_dict


def run_one_simulation(
    module_dict: dict[str, Module], target_conj_modules: list[str] | None = None
) -> dict[str, Any]:
    button = Button(["broadcaster"])

    # pulse from, Module, Pulse
    execution_queue: list[tuple[str, Module, Pulse]] = [("", button, Pulse.LOW)]

    high_pulse_count = 0
    low_pulse_count = 0

    targets = (
        {n: False for n in target_conj_modules} if target_conj_modules else None
    )

    while len(execution_queue) > 0:
        pulse_from, module, pulse = execution_queue.pop(0)

        # module.receive() gets now pulse
        if isinstance(module, Button):
            pulse = module.receive()
        elif isinstance(module, FlipFlopModule):
            pulse = module.receive(pulse)
        elif isinstance(module, ConjunctionModule):
            pulse = module.receive(pulse_from, pulse)
        elif isinstance(module, Broadcaster):
            pulse = module.receive(pulse)

        if pulse is None:
            continue

        # send this pulse to module.destinations
        for destination in module.destinations:
            if pulse == Pulse.HIGH:
                high_pulse_count += 1
            else:
                low_pulse_count += 1

            if targets is not None:
                for t in targets:
                    if (
                        t == module.name
                        and destination == "ns"
                        and pulse == Pulse.HIGH
                    ):
                        targets[t] = True
            if destination not in module_dict:
                continue
            execution_queue.append(
                (module.name, module_dict[destination], pulse)
            )

    return {
        "high_pulse_count": high_pulse_count,
        "low_pulse_count": low_pulse_count,
        "target_high_pulse": targets,
    }


def task_1():
    md = initialise_modules()
    acc_high_pulse_count = 0
    acc_low_pulse_count = 0

    for _ in range(1000):
        ret_dict = run_one_simulation(md)
        acc_high_pulse_count += ret_dict["high_pulse_count"]
        acc_low_pulse_count += ret_dict["low_pulse_count"]

    return acc_high_pulse_count * acc_low_pulse_count


def task_2():
    md = initialise_modules()

    # There is only one CONJUNCTION module connected to rx
    module_to_rx_name = [n for n, m in md.items() if "rx" in m.destinations][0]
    module_to_rx = md[module_to_rx_name]
    assert isinstance(module_to_rx, ConjunctionModule)
    print(f"Module to rx: {module_to_rx_name}")

    # The conjunction module only output a low pulse when all its memory is high
    # So we find all what modules are connected to it
    mtrx_memory_names = list(module_to_rx.memory.keys())
    print(mtrx_memory_names)

    # For each of these modules, let's figure out when the output a high pulse
    mtrx_memory_high_pulse = {n: [] for n in mtrx_memory_names}
    i = 0
    while True:
        ret_dict = run_one_simulation(md, mtrx_memory_names)
        i += 1
        for n, v in ret_dict["target_high_pulse"].items():
            if v:
                mtrx_memory_high_pulse[n].append(i)

        if all([len(v) > 1 for v in mtrx_memory_high_pulse.values()]):
            break

    diffs = [l[1] - l[0] for l in mtrx_memory_high_pulse.values()]
    print(diffs)

    return math.lcm(*diffs)


print(task_1())
ret = task_2()
print(ret)
