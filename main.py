import sys


class Resource:
    def __init__(self, name: str) -> None:
        self.nev = name
        self.tasks: list[str] = []

    def add(self, task: str, step: int) -> None:
        if task in self.tasks:
            print(f"{task},{step+1},{self.nev}")
        else:
            self.tasks.append(task)

    def rem(self, task: str) -> None:
        self.tasks.remove(task)


class Resources:
    def __init__(self) -> None:
        self.resources: list[Resource] = []

    def add(self, task: str, res: str, step: int) -> None:
        for resource in self.resources:
            if resource.nev == res and task in resource.tasks:
                print(f"{task},{step+1},{resource.nev}")
                return
        if isProblem(task, res):
            print(f"{task},{step+1},{res}")
            return
        for resource in self.resources:
            if resource.nev == res:
                resource.add(task, step)
                return
        uj = Resource(res)
        uj.add(task, step)
        self.resources.append(uj)

    def allRem(self, task: str):
        for res in self.resources:
            if task in res.tasks:
                res.tasks.remove(task)


class Task:
    def __init__(self, line: str) -> None:
        adatok = line.strip().split(',')
        self.nev = adatok[0]
        self.tasks = adatok[1:]
        self.steps = 0

    def isDone(self) -> bool:
        return self.steps >= len(self.tasks)

    def step(self) -> None:
        if self.isDone():
            return
        cur = self.tasks[self.steps]

        if cur[0] == '+':
            res = cur[1:]
            resources.add(self.nev, res, self.steps)

        if cur[0] == '-':
            res = cur[1:]
            # BUG itt lehet hiba ha egyiket kiveszem és a másik került 1.nek és emiatt
            for resource in resources.resources:
                if resource.nev == res:
                    if self.nev in resource.tasks:
                        if len(resource.tasks) > 0:
                            if resource.tasks[0] == self.nev:
                                resource.tasks.remove(self.nev)
                            else:
                                self.steps -= 1
        self.steps += 1
        


def isAllDone() -> bool:
    for task in tasks:
        if not task.isDone():
            return False
    return True

tasks: list[Task] = []
resources = Resources()

class El:
    def __init__(self, frm: str, to: str) -> None:
        self.frm = frm
        self.to = to

def isProblem(task: str, res: str)->bool:
    graf: list[El] = []
    for resource in resources.resources:
        for i in range(len(resource.tasks)):
            if i == 0:
                graf.append(El(resource.nev,resource.tasks[i]))
            else:
                graf.append(El(resource.tasks[i], resource.nev))
    van = False
    for resource in resources.resources:
        if resource.nev == res and len(resource.tasks) > 0:
            van = True
            break
    ujEl: El
    cel: str
    if van:
        ujEl = El(task, res)
        cel = task
    else:
        ujEl = El(res, task)
        cel = res
    graf.append(ujEl)
    
    return vanKor(graf, ujEl, cel)
    
def vanKor(graf: list[El], el: El, cel: str) -> bool:
    if el.to == cel:
        return True
    
    van = False
    for g in graf:
        if g.frm == el.to:
            van = van or vanKor(graf, g, cel)
    return van


for line in sys.stdin:
    if len(line.strip()) != 0:
        tasks.append(Task(line))

while not isAllDone():
    for task in tasks:
        task.step()
    for task in tasks:
        if task.isDone():
            resources.allRem(task.nev)
