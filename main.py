import sys


class Resource:
    def __init__(self, name: str) -> None:
        self.nev = name
        self.tasks: list[str] = []
        self.when: list[int] = []
        self.wantRem: list[str] = []

    def add(self, task: str, step: int) -> None:
        if task in self.tasks:
            print(f"{task},{step+1},{self.nev}")
        else:
            self.tasks.append(task)
            self.when.append(step)

    def rem(self, task: str) -> None:
        if not task in self.tasks:
            return
        if not task in self.wantRem:
            self.wantRem.append(task)
            self.endRem()

    def endRem(self):
        for t in self.wantRem:
            i = self.tasks.index(t)
            del self.tasks[i]
            del self.when[i]
            self.wantRem = []
            if len(self.tasks) > 0:
                isProblem(self.tasks[0], self.nev, False, True)
        if len(self.wantRem) > 0:
            self.endRem()

    def getWhen(self, task: str) -> int:
        i = self.tasks.index(task)
        return self.when[i]


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
        for t in tasks:
            if t.nev == task:
                erok: list[str] = []
                for r in t.tasks:
                    if r[0] == '+':
                        cur = r[1:]
                        if cur in erok:
                            erok.remove(cur)
                        erok.append(cur)
                break
        for e in erok:
            for r in resources.resources:
                if r.nev == e and task in r.tasks:
                    r.rem(task)
        return


class Task:
    def __init__(self, line: str) -> None:
        adatok = line.strip().split(',')
        self.nev = adatok[0]
        self.tasks = adatok[1:]
        self.steps = 0

    def isDone(self) -> bool:
        for res in resources.resources:
            if self.nev in res.tasks and res.tasks[0] != self.nev:
                return False
        return self.steps >= len(self.tasks)

    def step(self) -> None:
        for res in resources.resources:
            benneVan = self.nev in res.tasks
            nemAzElso = len(res.tasks) > 0 and res.tasks[0] != self.nev

            oAMasodik = len(res.tasks) > 1 and res.tasks[1] == self.nev
            vanRemEsTorolniAkarom = len(res.wantRem) >0 and res.wantRem[0] == res.tasks[0]
            if benneVan:
                #Ha benne van akkor úgy mehet tovább ha
                #   Ő az első
                #   Nem Ő az első, de Ő a második és az elsőt törölni akarom
                #Azaz akkor kell kilépni, ha nem ő az első, kivéve akkor, ha ő a második és az elsőt ki akarom venni
                rossz = False
                if nemAzElso:
                    rossz = True
                if rossz and oAMasodik and vanRemEsTorolniAkarom:
                    rossz = False
                if rossz: return
        if self.isDone():
            resources.allRem(self.nev)
            return
        for r in resources.resources:
            if self.nev in r.tasks and len(r.tasks) >= 2 and len(r.wantRem) > 0:
                if r.tasks[1] == self.nev:
                    r.endRem()
                    return

        if self.steps >= len(self.tasks):
            return
        cur = self.tasks[self.steps]

        if cur[0] == '+':
            res = cur[1:]
            for r in resources.resources:
                if r.nev == res and len(r.tasks) == 1 and len(r.wantRem) > 0:
                    r.endRem()
            resources.add(self.nev, res, self.steps)

        if cur[0] == '-':
            res = cur[1:]
            for resource in resources.resources:
                if resource.nev == res:
                    if self.nev in resource.tasks:
                        if len(resource.tasks) > 0:
                            if resource.tasks[0] == self.nev:
                                resource.rem(self.nev)
                            else:
                                self.steps -= 1
                            break
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


def isProblem(task: str, res: str, benne=False, kivesz=False) -> bool:
    graf: list[El] = []
    for resource in resources.resources:
        for i in range(len(resource.tasks)):
            if i == 0:
                graf.append(El(resource.nev, resource.tasks[i]))
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
        ujEl = El(res, task) if kivesz else El(task, res)
        cel = res
    else:
        ujEl = El(res, task)
        cel = task if benne else res
    if not kivesz:
        graf.append(ujEl)
    if benne:
        for g in graf:
            if g.frm == res and g.to == task:
                graf.remove(g)
                break

    honnan = vanKor(graf, ujEl, cel, True)

    if honnan == "":
        return False
    if honnan == task:
        return True

    # Van kör, de nem emiatt lett
    for r in resources.resources:
        if r.nev == res:
            print(f"{honnan},{r.getWhen(honnan)+1},{res}")
            r.rem(honnan)
            return False


def vanKor(graf: list[El], el: El, cel: str, elso: bool) -> str:
    if el.to == cel and not elso:
        return el.frm

    van = ""
    for g in graf:
        if g.frm == el.to:
            van = van + vanKor(graf, g, cel, False)
        if len(van) > 0:
            break
    return van

def p(string:str)->None:
    if debug:
        print(string)

for line in sys.stdin:
    if len(line.strip()) != 0:
        tasks.append(Task(line))

kor = 1
debug = True
while not isAllDone():
    # p(f"{kor}. Kör")
    for task in tasks:
        task.step()
    for res in resources.resources:
        if len(res.tasks) <= 1:
            res.endRem()
    kor+=1
