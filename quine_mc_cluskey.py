#!/bin/python3
# by Omid.N

from builtins import len


def base_2(num, digits):
    res = ''
    while num > 0:
        res = str(num % 2) + res
        num = num // 2
    while len(res) < digits:
        res = '0' + res

    return res


######################################
class Token:
    def __init__(self, m, total_size):
        self.min_terms = [m]
        self.base2_str = base_2(m, total_size)
        self.tick = False
        pass

    def ones_count(self):
        return self.base2_str.count('1')

    def dash_count(self):
        return self.base2_str.count('-')

    def is_combinable_with(self, other):
        diff = 0
        for i in range(len(self.base2_str)):
            # dashes must be the same spot
            if self.base2_str[i] == '-' and not other.base2_str[i] == '-':
                return False
            else:
                if (self.base2_str[i] == '1' and other.base2_str[i] == '0') or self.base2_str[i] == '0' and \
                        other.base2_str[i] == '1':
                    diff += 1

        # return True only if
        if diff == 1:
            return True
        # other wise return False
        return False

    def combined_with(self, other):
        if not self.is_combinable_with(other):
            raise RuntimeError

        res = Token(self.min_terms[0], len(self.base2_str));
        res.base2_str = ''
        for i in range(len(self.base2_str)):
            if self.base2_str[i] == other.base2_str[i]:
                res.base2_str += self.base2_str[i]

            else:
                res.base2_str += '-'

        res.min_terms = []
        res.min_terms += self.min_terms
        res.min_terms += other.min_terms
        res.min_terms = sorted(res.min_terms)
        return res

    def get_min_term_product(self):
        # ¬
        sen = []
        for i in range(len(self.base2_str)):
            current_char = self.base2_str[i]
            if current_char != '-':
                sop = chr(ord('A') + i)

                if current_char == '0':
                    sop = '¬' + sop
                sen += sop

        return ''.join(sen)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            for i in range(len(self.min_terms)):
                if self.min_terms[i] != other.min_terms[i]:
                    return False

            return True
        else:
            return False

    def __str__(self):
        return str(self.base2_str)


######################################


n = int(input("Number of variables: "))

min_terms = []  # array of min-terms
tokens = []
print("Enter min-terms (-1 to finish): ")
temp = int(input("-->  "))
while temp != -1:
    if temp > 2 ** n - 1:
        print(f"Invalid input : {temp}")

    else:
        if min_terms.count(temp) == 0:
            min_terms.append(temp)
            tokens.append(Token(temp, n))

    temp = int(input("-->  "))

dont_care_terms = []
print("Enter don't care terms (-1 to finish): ")
temp = int(input("-->  "))
while temp != -1:
    if temp > 2 ** n - 1:
        print(f"Invalid input : {temp}")

    else:
        if tokens.count(temp) == 0:
            dont_care_terms.append(temp)
            new_t = Token(temp, n)
            new_t.tick = True
            tokens.append(new_t)

    temp = int(input("-->  "))

# grouping tokens based on the number of their ones:
grouped_tokens = [[] for i in range(n + 1)]

for i in range(len(tokens)):
    grouped_tokens[tokens[i].ones_count()].append(tokens[i])

columns = [grouped_tokens]
end = False
current = columns[0]
while not end:
    col = [[] for i in range(len(current) - 1)]
    combined_tokens = 0
    for i in range(len(current) - 1):
        for t1 in current[i]:
            for t2 in current[i + 1]:
                combinable_with = t1.is_combinable_with(t2)
                if combinable_with:
                    t1.tick = True
                    t2.tick = True
                    new_t = t1.combined_with(t2)
                    if col[i].count(new_t) < 1:
                        col[i].append(new_t)
                        sorted(col[i], key=lambda t: t.min_terms[0], reverse=True)
                        combined_tokens += 1

    if combined_tokens == 0:
        break
    columns.append(col)
    current = col


#########################################
# printing the result ✔
def _print(str, color=''):
    import time
    time.sleep(0.01)
    print(color + str + '\033[39m', end='')


#  └  ╭──────╮
#     │00001✔│
#     │──────│
#     ╰──────╯
_print('\033[25m')

green_csi = '\033[32m'
red_csi = '\033[31m'
print('\033[0;0H\033[J', end='')  # clear the screen

print_x_pos = 1
max_height = 0

for k in range(len(columns)):
    _print('\033[0;' + str(print_x_pos) + 'H')
    column = columns[k]
    min_terms_str_len = (len(str(2 ** n)) * 2 ** k + 2 ** k - 1)
    width = 3 + min_terms_str_len + n + 1
    height = 1
    tt = 0
    while tt < len(column):
        if len(column[tt]) == 0:
            column.remove(column[tt])
            tt -= 1
        else:
            height += 1
            for cc in column[tt]:
                height += 1
        tt += 1

    if height == 1:
        continue

    if height > max_height:
        max_height = height
    box_corners = {0: '┌', height - 1: '└', width - 1: '┐', height + width - 2: '┘'}

    counter = 0
    tcounter = 0
    i, j = 0, 0
    while i < height:
        while j < width:

            if j == 0 or j == width - 1:
                if i == 0 or i == height - 1:
                    _print(box_corners[i + j])
                else:
                    _print('│')

            elif i == 0 or i == height - 1:
                _print('─')

            else:

                if len(column[counter]) == 0:
                    counter += 1
                    tcounter = 0
                else:
                    if tcounter == len(column[counter]):
                        _print('─' * (width - 2))
                        counter += 1
                        tcounter = 0
                    else:
                        token = column[counter][tcounter]
                        _print(token.base2_str)
                        if token.tick:
                            _print('✔', green_csi)

                        else:
                            _print('▾', red_csi)

                        _print('│')
                        tcounter += 1
                        min_terms_str = '-'.join([str(i) for i in token.min_terms])
                        _print(('{:>' + str(min_terms_str_len) + '}').format(min_terms_str))
                j = width - 2
            j += 1
        i += 1
        j = 0
        _print('\n')
        _print('\033[' + str(i + 1) + ';' + str(print_x_pos) + 'H')

    print_x_pos += width + 1

print(f'\033[{max_height};0H')

not_ticked = []

# picking not ticked s
for column in columns:
    for row in columns:
        for ts in row:
            for t in ts:
                if not t.tick and not not_ticked.__contains__(t) > 0:
                    not_ticked.append(t)

essential_implicants = []
min_terms_copy = min_terms.copy()
for m in min_terms:
    does_contain = 0
    ess_t = None
    for i in range(len(not_ticked)):
        if not_ticked[i].min_terms.count(m) > 0:
            does_contain += 1
            ess_t = not_ticked[i]

    if does_contain == 1:
        if essential_implicants.count(ess_t) == 0:
            essential_implicants.append(ess_t)
        # min_terms_copy.remove(ess_t.min_terms)

_print("➜  " + ' + '.join([i.get_min_term_product() for i in essential_implicants]))
_print('\n\n')
