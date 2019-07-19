class DisjointSet:
    size = 0

    def __init__(self):
        self.__items = {}

    def union(self, root1, root2):
        if self.__items[root2] < self.__items[root1]:
            self.__items[root1] = root2
        else:
            if self.__items[root1] == self.__items[root2]:
                self.__items[root1] -= 1

            self.__items[root2] = root1

    def find(self, x):
        try:
            while self.__items[x] > 0:
                x = self.__items[x]

        except:
            self.__items[x] = -1

        return x

    def split_sets(self):
        sets = {}
        j = 0

        for j in self.__items.keys():
            root = self.find(j)

            try:
                if root > 0:
                    if sets.has_key(root):
                        list = sets[root]
                        list.append(j)

                        sets[root] = list
                    else:
                        sets[root] = [j]
            except:
                pass

        return sets

