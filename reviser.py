import sys
json_file = sys.argv[1]
#!/usr/bin/python
import sys,os
f=open(json_file,'r+')
content=f.readlines()
line_ite = 15
content[0] = '[{\n'
while line_ite < 160000 - 1:
    content[line_ite]='},\n'
    line_ite += 16
content[159999] = '}]'
f=open(json_file,'w+')
f.writelines(content)