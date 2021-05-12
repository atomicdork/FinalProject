import owlready2
owlready2.JAVA_EXE = "C:\Program Files\Java\jdk-13.0.2\\bin\java.exe"
onto        = owlready2.get_ontology("file://ontofiletest").load()

# print(list(onto.direction.comment))
print(onto.search(comment = "left*"))
array = list(onto.Direction.subclasses())

for word in array:
    print(word.name)
