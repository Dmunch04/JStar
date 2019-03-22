letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'
bools = ['True', 'true', 'False', 'false']
definers = ['String', 'Int', 'Float', 'Bool']

def ReadFile (path):
    with open(path, 'r') as file: raw = file.read()
    data = raw.split('\n')

    line_index = 0
    last_eol_found = False

    lines = []

    for line in data:
        if line == '':
            continue

        line_index += 1

        cur_line = []
        progress = ''
        definer = ''

        colon_found = False
        definer_found = False
        equal_found = False
        left_quote_found = False
        right_quote_found = False
        eol_found = False

        if line_index > 1:
            if not last_eol_found == True:
                print('You forgot a ; <Line> -> {0}'.format(line_index - 1))
                return

        for char in line:
            if char in letters + '_ ':
                progress += char
                continue
            elif char == ':':
                cur_line.append(progress)
                progress = ''
                cur_line.append(char)
                colon_found = True
                continue
            elif colon_found == True and char in letters:
                progress += char
                continue
            elif char == '=':
                if progress.replace(' ', '') in definers:
                    definer_found = True
                    definer = progress.replace(' ', '')
                    cur_line.append(progress.replace(' ', ''))
                    progress = ''
                    cur_line.append(char)
                    equal_found = True
                    continue
            elif equal_found == True and char == "'" or char == '"':
                progress += "'"
                if not left_quote_found:
                    left_quote_found = True
                elif not right_quote_found:
                    right_quote_found = True
            elif definer == 'String' and left_quote_found == True and char in letters + '_':
                progress += char
                continue
            elif definer == 'Int' and equal_found and char in numbers:
                progress += char
                continue
            elif definer == 'Float' and equal_found and char in numbers + ',.':
                progress += char
                continue
            elif definer == 'Bool' and equal_found and char in letters:
                progress += char
                continue
            elif char == ';':
                if definer == 'Bool':
                    if not progress.replace(' ', '') in bools:
                        print("That's not a bool [{0}]! <Line> -> {1}".format(progress, line_index))
                        continue
                cur_line.append(progress[1:])
                progress = ''
                cur_line.append(char)
                eol_found = True
                last_eol_found = True

                if colon_found == False:
                    print('Missing a colon! <Line> -> {0}'.format(line_index))
                    return
                elif definer_found == False:
                    print(cur_line)
                    print('Missing a type! <Line> -> {0}'.format(line_index))
                    return
                elif equal_found == False:
                    print('Missing a equal! <Line> -> {0}'.format(line_index))
                    return
                elif definer == 'String':
                    if left_quote_found == False:
                        print('Missing a start quote! <Line> -> {0}'.format(line_index))
                        return
                    elif right_quote_found == False:
                        print('Missing an end quote! <Line> -> {0}'.format(line_index))
                        return

                continue
            elif eol_found == False:
                last_eol_found = False
                continue
            elif eol_found == True:
                last_eol_found = True
                continue

        lines.append(cur_line)

    toReturn = []
    for line in lines:
        try:
            toReturn.append(line[4])
        except:
            print('{0} -> is missing a value!'.format(line))
            continue

    return toReturn
