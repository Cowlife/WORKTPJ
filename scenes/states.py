class State:
    def __init__(self, name) -> None:
        self.name = name

    def enter(self):
        print(f"Entering{self.name}")

    def update(self):
        pass

    def exit(self):
        pass


class Transition:
    def __init__(self, _from, _to) -> None:
        self._from = _from
        self._to = _to


class Attack(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self):
        print("Attacking")
        # self.update_animation(lst_spr, i, True)
        return super().update()


class Moving(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self):
        print("Moving")
        return super().update()


class Hurt(State):
    def __init__(self) -> None:
        super().__init__(self.__class__.__name__)

    def update(self):
        print("Moving")
        return super().update()


class FSM:
    def __init__(self, i_f_states: list[State], states: list[State], transitions: dict[str, Transition]) -> None:
        self._states = states
        self._transitions = transitions
        self.current: State = i_f_states[0]
        self.end: State = i_f_states[1]

    def update(self, event):
        if event:
            trans = self._transitions.get(event)
            if trans and trans._from == self.current:
                self.current.exit()
                self.current = trans._to
                self.current.enter()
        self.current.update()

        if self.current == self.end:
            self.current.exit()
            return False
        return True


if __name__ == "__main__":
    moving = Moving()
    attack = Attack()
    dead = State("Dead")

    states = [moving, attack, dead]
    transitions = {
        "engage": Transition(moving, attack),
        "rest": Transition(attack, moving),
        "miss": Transition(attack, dead),
        "damaged": Transition(moving, dead)
    }
    fsm = FSM([states[0], states[2]], states, transitions)
    event = None
    fsm.update("rest")
    fsm.update("engage")
