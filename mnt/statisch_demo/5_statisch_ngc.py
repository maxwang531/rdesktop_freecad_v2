import os
def file_name(input_dir, output_dir, word, splitword):
    for root, dirs, files in os.walk(input_dir):
        for item in files:
            f = open(input_dir + item, "r", encoding='UTF-8')
            content = f.read()
            content = content.replace(word, splitword)
            with open(os.path.join(output_dir, item), 'w', encoding='UTF-8') as fval:
                fval.write(content)
            f.close()


file_top = '/config/ausgabe_ngc/txt/top_operation.txt'

file_top_neu = '/config/ausgabe_ngc/neu_txt/top_operation.txt'


data_top = []
for line in open(file_top,"r"):
    data_top.append(line)
if len(data_top) > 12:
    data_top[12] = 'M3 S2000'
data_top.insert(13, 'G0 A90\n')
data_top.insert(14, 'F2000\n')
f=open('/config/ausgabe_ngc/neu_txt/top_operation_neu.txt',"w")
for line in data_top:
    f.write(line+'\n')
f.close()

f=open('/config/ausgabe_ngc/statisch_operation.ngc',"w")
for line in data_top:
    f.write(line+'\n')
f.close()

Gui.doCommand('exit()')
