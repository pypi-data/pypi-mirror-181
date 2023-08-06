class JournaledSet:

    def __init__(self, source):
        self.source = set(source)
        self.added = set()
        self.removed = set()

    def get_added(self):
        return self.added

    def get_removed(self):
        return self.removed

    def contains(self, s):
        return (s in self.source or s in self.added) and not s in self.removed

    def add(self, s):
        if self.contains(s):
            return False
        if s in self.removed:
            self.removed.remove(s)
            return True
        self.added.add(s)
        return True

    def remove(self, s):
        if not self.contains(s):
            return False
        if s in self.added:
            self.added.remove(s)
            return True
        self.removed.add(s)
        return True

    def containsAll(self, c):
        """ generated source for method containsAll """
        for e in c:
            if not self.contains(e):
                return False
        return True

    def addAll(self, c):
        """ generated source for method addAll """
        changed = False
        for s in c:
            if self.add(s):
                changed = True
        return changed

    def __len__(self):
        count = 0
        for e in self.__iter__():
            count += 1
        return count

    def __iter__(self):
        for e in self.source.union(self.added):
            if self.contains(e):
                yield e
            else:
                continue

    def __str__(self):
        """ generated source for method toString """
        return "JournaledSet{source=" + ' '.join(self.source) + ", added=" + ' '.join(
            self.added) + ", removed=" + ' '.join(self.removed) + "}"
