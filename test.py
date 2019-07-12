class A:
    class B:
        def __init__(e1, e2, e3):
            print(e1, e2, e3)

k = A()
k.b = k.B(1)