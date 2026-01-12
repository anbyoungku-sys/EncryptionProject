# 평문 : be careful for assassinator
# 변환 : be ca re fu lf or as sa sx si na to rx
# 키1 : assassinator
# 암호화 테이블 : asint orbcd efghj klmpz uvwxy
# 키2 : secret is beautiful

# 평문 : hello world
# 암호문 : dbnvmizmqmgv
import string


def prepare_text(text): # 암호화 전 평문을 2자씩 나눠 놈
    ptext = []
    pos = 0                        # 글자 위치

    # 공백제거, 소문자로 일괄변환
    text = text.replace(' ', '').lower()
    # print(text) <= 공백제거, 소문자로 일괄변환 print

    # # 2글자씩 묶어 diagram으로 생성
    # while pos  < len(text):
    #     first = text[pos]
    #     second = text[pos+1]
    #     ptext.append(first+second)
    #     pos += 2

    # 두 글자를 합치되 같은 문자 2개가 나오면 하나의 문자에 x 추가
    #     while pos  < len(text):
    #         first = text[pos]
    #         second = text[pos+1]
    #
    #         if first != second:
    #             ptext.append(first+second)
    #             pos += 2
    #         else:
    #             ptext.append(first+'x')
    #             pos += 1

    # becarefulforassassinator
    while pos  < len(text):
        first = text[pos]
        # 마지막 문자 여부 체크
        if pos +1 < len(text):
            second = text[pos+1]
        else:
            second = 'x'

        if first != second:
            ptext.append(first+second)
            pos += 2
        else:
            ptext.append(first+'x')
            pos += 1

    print(ptext)            # 2개씩 나누고 마지막으로 1개이면 x를 붙여서 2개로 만들어서 출력
    return ptext


def create_playfair_matrix(key):
    import string# 5x5 암호표 생성
    keys = []
    key_matrix = []     # [[],[],[],[],[]]
    # alpha = 'abcdefghijklmnopqrstuvwxyz'
    # 알파벳 모두를 확인
    alphas = string.ascii_lowercase.replace('z', 'q')

    # 먼저, 키를 테이블에 저장하고 (단, 중복 제외)
    for ch in key:
        if ch not in keys :     # 중복제거
            keys.append(ch)

    # 나머지 테이블 공간에 알파벳을 채춤 (단, 중북 제외)
    while len(keys) < 25:
        for ch in alphas:
            if ch not in keys :     # 중복제거
                keys.append(ch)

    # print(keys, len(keys))

    # 5
    # key_matrix.append(keys[0:5])
    # key_matrix.append(keys[5:10])
    # key_matrix.append(keys[10:15])
    # key_matrix.append(keys[15:20])
    # key_matrix.append(keys[20:25])

    for i in range(0, 25, 5):
        key_matrix.append(keys[i:i+5])

    print(key_matrix)
    return key_matrix

# 암호화 테치블에서 특정 문자의 위치를 알아냄
def find_pos(table, ch):
    for r in range(5):
        for c in range(5):
            if table[r][c] == ch:
                return r, c

# 플레이페어 암호화 함수
def playfair_encrypt(pairs, table):
    encrypted = []

    for pair in pairs:
        a, b = pair     # 변수 분리 저장
        print(a, b)


        # 암호화 테이블에서 해당 문자의 위치 검색
        # print(table[0][0], table[0][1], table[0][2], table[0][3], table[0][4])
        # print(table[1][0], table[1][1], table[1][2], table[1][3], table[1][4])
        # print(table[2][0], table[2][1], table[2][2], table[2][3], table[2][4])
        # for r in range(5):
        #     for c in range(5):
        #         # print(table[r][c], end=' ')
        #         if table[r][c] == a: print(a, r, c)
        #     # print()

        # for r in range(5):
        #     for c in range(5):
        #         if table[r][c] == a: print(a, r, c)
        #         if table[r][c] == b: print(b, r, c)

        r1, c1 = find_pos(table, a)
        r2, c2 = find_pos(table, b)
        print(a, r1, c1)
        print(b, r2, c2)

        # 같은 행 : 오른쪽 열 문자 선택
        if r1 == r2:
            code = table[r1][(c1 + 1) % 5] + table[r2][(c2 + 1) % 5]
        # 같은 열 : 아래쪽 행 문자 선택
        elif c1 == c2:
            code = table[(r1 + 1) % 5][c1] + table[(r2 + 1) % 5][c2]
        # 다른 행/열 : 같은 행에서 반대쪽 열 문자 선택
        else:
            code = table[r1][c2] + table[r2][c1]

        encrypted.append(code)

    # print(encrypted)
    return encrypted




# 복호화

def prepare_text(text): # 암호화 전 평문을 2자씩 나눠 놈
    ptext = []
    pos = 0                        # 글자 위치

    # 공백제거, 소문자로 일괄변환
    text = text.replace(' ', '').lower()
    # print(text) <= 공백제거, 소문자로 일괄변환 print

    # # 2글자씩 묶어 diagram으로 생성
    # while pos  < len(text):
    #     first = text[pos]
    #     second = text[pos+1]
    #     ptext.append(first+second)
    #     pos += 2

    # 두 글자를 합치되 같은 문자 2개가 나오면 하나의 문자에 x 추가
    #     while pos  < len(text):
    #         first = text[pos]
    #         second = text[pos+1]
    #
    #         if first != second:
    #             ptext.append(first+second)
    #             pos += 2
    #         else:
    #             ptext.append(first+'x')
    #             pos += 1

    # becarefulforassassinator
    while pos  < len(text):
        first = text[pos]
        # 마지막 문자 여부 체크
        if pos +1 < len(text):
            second = text[pos+1]
        else:
            second = 'x'

        if first != second:
            ptext.append(first+second)
            pos += 2
        else:
            ptext.append(first+'x')
            pos += 1

    print(ptext)            # 2개씩 나누고 마지막으로 1개이면 x를 붙여서 2개로 만들어서 출력
    return ptext


def create_playfair_matrix(key):
    import string# 5x5 암호표 생성
    keys = []
    key_matrix = []     # [[],[],[],[],[]]
    # alpha = 'abcdefghijklmnopqrstuvwxyz'
    # 알파벳 모두를 확인
    alphas = string.ascii_lowercase.replace('z', 'q')

    # 먼저, 키를 테이블에 저장하고 (단, 중복 제외)
    for ch in key:
        if ch not in keys :     # 중복제거
            keys.append(ch)

    # 나머지 테이블 공간에 알파벳을 채춤 (단, 중북 제외)
    while len(keys) < 25:
        for ch in alphas:
            if ch not in keys :     # 중복제거
                keys.append(ch)

    # print(keys, len(keys))

    # 5
    # key_matrix.append(keys[0:5])
    # key_matrix.append(keys[5:10])
    # key_matrix.append(keys[10:15])
    # key_matrix.append(keys[15:20])
    # key_matrix.append(keys[20:25])

    for i in range(0, 25, 5):
        key_matrix.append(keys[i:i+5])

    print(key_matrix)
    return key_matrix

# 암호화 테치블에서 특정 문자의 위치를 알아냄
def find_pos(table, ch):
    for r in range(5):
        for c in range(5):
            if table[r][c] == ch:
                return r, c

# 플레이페어 암호화 함수
def playfair_encrypt(pairs, table, encrypt=True):
    encrypted = []
    shift = 1 if encrypt else -1
    for pair in pairs:
        a, b = pair     # 변수 분리 저장
        print(a, b)


        # 암호화 테이블에서 해당 문자의 위치 검색
        # print(table[0][0], table[0][1], table[0][2], table[0][3], table[0][4])
        # print(table[1][0], table[1][1], table[1][2], table[1][3], table[1][4])
        # print(table[2][0], table[2][1], table[2][2], table[2][3], table[2][4])
        # for r in range(5):
        #     for c in range(5):
        #         # print(table[r][c], end=' ')
        #         if table[r][c] == a: print(a, r, c)
        #     # print()

        # for r in range(5):
        #     for c in range(5):
        #         if table[r][c] == a: print(a, r, c)
        #         if table[r][c] == b: print(b, r, c)

        r1, c1 = find_pos(table, a)
        r2, c2 = find_pos(table, b)
        print(a, r1, c1)
        print(b, r2, c2)

        # 같은 행 : 오른쪽 열 문자 선택
        if r1 == r2:
            code = table[r1][(c1 + shift) % 5] + table[r2][(c2 + shift) % 5]
        # 같은 열 : 아래쪽 행 문자 선택
        elif c1 == c2:
            code = table[(r1 + shift) % 5][c1] + table[(r2 + shift) % 5][c2]
        # 다른 행/열 : 같은 행에서 반대쪽 열 문자 선택
        else:
            code = table[r1][c2] + table[r2][c1]

        encrypted.append(code)

    # print(encrypted)
    return encrypted



if __name__ == '__main__':
    plain_text = 'be careful for assassinator'
    key = 'assassinator'

    pairs = prepare_text(plain_text)
    table = create_playfair_matrix(key)
    encrypted = playfair_encrypt(pairs, table)
    print(encrypted)


    decrypted = playfair_encrypt(encrypted, table, False)
    # print(decrypted)
    decrypted = "".join(decrypted).replace('x', '')
    print(decrypted)














