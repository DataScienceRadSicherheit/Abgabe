
fobj_in = open("in.txt")
fobj_out = open("out.txt","w")

for line in fobj_in:
    fobj_out.write("('" + line.rstrip() + "'),\n")

fobj_in.close()
fobj_out.close()
