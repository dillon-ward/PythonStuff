file = open("D_and_D.txt","w")

Name = (input("Input the name of your character:"))
Race = (input("Input their race :"))
Class = (input("Input their class:"))
Age = int(input("Input their age:"))
Alignment = (input("Input their alignment:"))
Animal = (input("Input their animal (optional):"))
Origin = (input("Input their origin (optional):"))

file.write("Name: ")
file.write(Name)
file.write('/n')
file.write("Race: ")
file.write(Race)
file.write('/n')
file.write("Class: ")
file.write(Class)
file.write('/n')
file.write("Age: ")
file.write(str(Age))
file.write('/n')
file.write("Alignment: ")
file.write(Alignment)
file.write('/n')
file.write("Animal: ")
file.write(Animal)
file.write('/n')
file.write("Origin: ")
file.write(Origin)
file.write('/n')

file = open("D_and_D.txt","r")
print(file.readlines())
file.close()
