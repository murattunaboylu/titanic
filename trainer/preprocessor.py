# pre-process the input files
def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


file = open('../data/train.data.csv')
writer = open('../data/train.data.processed.csv', 'w')

line = file.readline()

while line:
    cols = line.split(',')
    cabin_class = cols[11][:1]
    cabin_nos = cols[11][1:]
    cabin_no = cabin_nos.split(' ')[0]
    cabin_no = cabin_no if is_int(cabin_no) else 0
    print(cabin_class)
    print(cabin_no)
    writer.write('{},{},{}\n'.format(line.rstrip(),cabin_class,cabin_no))
    line = file.readline()

file.close()
writer.close()