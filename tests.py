from algorithms.converts import asas, integral, nsvs, hipparcos, munipac


def test_asas_converting():
    file = open("mats/asas.txt").read()
    print(asas(file))


def test_integral_converting():
    file = open("mats/integral.txt").read()
    print(integral(file))


def test_nsvs_converting():
    file = open("mats/nsvs.txt").read()
    print(nsvs(file))


def test_hipparcos_converting():
    file = open("mats/hipparcos.txt").read()
    print(hipparcos(file))
    
    
def test_munipac_converting():
    file = open("mats/munipack.txt").read()
    print(munipac(file))


def converting_tests():
    test_asas_converting()
    test_nsvs_converting()
    test_integral_converting()
    test_hipparcos_converting()

if __name__ == "__main__":
    test_munipac_converting()