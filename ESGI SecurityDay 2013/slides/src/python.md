## Python? WTF?!?

- Langage interprété
- Portable
- Typage dynamique
- Orienté objet
- Librairie standard très complète
- Nombreux modules tiers disponibles
- Une grande communauté d'utilisateurs

---

## OK, mais ça sert à quoi?

- Tout!
    - Applications scientifiques
    - Développement Web
    - Sécurité
    - Jeux Vidéo
- Utilisé par
    - Google
    - Yahoo
    - NASA

---

# ~ Concepts de base ~

---

## Tout est objet

- Tous les objets Python héritent de `object`

        !python
        >>> for obj in ['foo', 42, [], {}]:
        >>>     print type(obj), isinstance(obj, object)
            <type 'str'> True
            <type 'int'> True
            <type 'list'> True
            <type 'dict'> True

---

## Packages et modules

- Module → Fichier .py contenant des classes et/ou fonctions
- Package → Répertoire contenant un fichier `__init__.py`

        $ tree KillerApp

        KillerApp/
        ├── KillerApp.py
        ├── package/
        │   ├── __init__.py
        │   ├── module.py
        │   └── sub_package/
        │       ├── __init__.py
        │       └── sub_module.py
        └── other_package/
            ├── __init__.py
            └── other_module.py

---

## `$ cat module.py`

    !python
    import os

    CONSTANT_VAR = 'some constant value'

    class SomeClass(object):
        class_attribute = 'attribute value'

        def __init__(self):
            self.instance_attribute = 'attribute value'

        def method(self):
            print "something"

    def function(arg, named_arg='default value'):
        print "something else"

---

# ~ Concepts avancés ~

---

## Méthodes spéciales

- `__add__` / `__sub__` / `__mul__` / `__div__` → Opérateurs mathématiques
- `__init__` → `obj = MyClass()`
- `__str__` → `str(obj)`
- `__len__` → `len(obj)`
- `__call__` → `obj()`
- `__iter__` → `for i in obj:`
- `__enter__`/`__exit__` → `with MyClass() as obj:`

---

## Creation de fonctions à la volée

    !python
    def by(x):
        def func(y):
            return x * y
        func.__name__ = "by_%d" % x
        func.__doc__ = "Multiply given number by %d" % x
        return func

    >>> three = by(3)
    >>> help(three)
        Help on function by_3 in module __main__:

        by_3(y)
            Multiply given number by 3

    >>> three(4)
        12

---

## Arguments unpacking

- Permet à une fonction de recevoir n'importe quel nombre d'arguments
- Utilisable avec les arguments positionnels et nommés

        !python
        def func(*args, **kwargs):
            print args
            print kwargs

        >>> func('foo', 'bar', first="baz", other="blah")
            ('foo', 'bar')
            {'first': 'baz', 'other': 'blah'}

---

## Arguments packing

- La même chose, à l'envers... ^^
- Permet de construire une liste d'arguments à la volée

        !python
        def func(i, j, first=None, other=None, last=None):
            print i, j
            print first, other, last

        >>> args = ('foo', 'bar')
        >>> kwargs = {'first': 'baz', 'other': 'blah'}
        >>> func(*args, **kwargs)
            foo bar
            baz blah None

---

## Décorateurs

- Ce sont...
    - des objets "callable"
    - prennent une fonction en argument
    - renvoient une fonction
- et ils peuvent être utilisés pour...
    - modifier la valeur de retour d'une fonction
    - valider les arguments reçus par la fonction d'origine
    - faire certaines opérations avant/après l'appel à la fonction d'origine

---

## Décorateurs - Utilisation

    !python
    @add_one
    def square(n):
        return  n * n

Ou

    !python
    def square(n):
        return n * n
    square = add_one(square)

---

## Décorateurs - Fonctions décoratrices

- Fonction renvoyant une autre fonction

        !python
        def add_one(func):
            print "Decorator initialized"
            def fake_square(n):
                print "Before original function call"
                orig_result = func(n)
                print "After original function call"
                return orig_result + 1
            return fake_square

---

## Décorateurs - Classes décoratrices

- Classe implémentant la méthode `__call__`

        !python
        class add_one(object):
            def __init__(self, func):
                print "Decorating initial function"
                self.func = func

            def __call__(self, n):
                print "Before initial function call"
                orig_result = self.func(n)
                print "After initial function call"
                return orig_result + 1

---

## Décorateurs - Arguments

    !python
    class validate_args(object):
        def __init__(self, *arg_types):
            print "Creating decorator"
            self.arg_types = arg_types

        def __call__(self, func):
            print "Decorating initial function"
            def wrapper(*args):
                print "Before initial function call (validating args)"
                for arg, arg_type in zip(args, self.arg_types):
                    if not isinstance(arg, arg_type):
                        raise TypeError("Wrong argument type received")
                retval = func(*args)
                print "After initial function call"
                return retval
            return wrapper

    @validate_args(int, list)
    def some_function(i, l):
        print i, l

---

## Décorateurs - Arguments - Exemple

    !python
    def some_function(i, l):
        print i, l

    >>> some_function_validator = validate_args(int, list)
        Creating decorator

    >>> some_function = some_function_validator(some_function)
        Decorating initial function

    >>> some_function(1, [1, 2, 3])
        Before initial function call (validating args)
        1 [1, 2, 3]
        After initial function call

    >>> some_function(1, 'foo')
        Before initial function call (validating args)
        [...]
        TypeError: Wrong argument type received
