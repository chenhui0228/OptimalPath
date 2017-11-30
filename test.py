import main as pf


def test_maze():
    a = pf.PackageMap()
    walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
             (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
    a.init(6, 6, walls)
    path = a.find_path((0, 0), (5, 5))
    path2 = a.find_path((5, 5), (0, 0))
    print path
    print path2
    man = pf.MailMan()
    man.go(path[0])

if __name__ == '__main__':
    test_maze()