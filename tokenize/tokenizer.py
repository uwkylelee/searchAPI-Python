import re


def tokenizer(text: str):
    # 텍스트 분리를 위한 정규표현식
    eng_num = re.compile(r'[a-zA-Z0-9-]')
    kor = re.compile(r'[가-힣]')
    jamo = re.compile(r'[ㄱ-ㅎ|ㅏ-ㅣ]')
    space = re.compile(r'[\s\t\r\n\v\f]')

    text = text.strip().lower()
    text_to_tokens: list = []
    token: str = ""
    prev_type: str = ""

    for idx in text:
        # 현재 인덱스의 문자가 공백이면, 저장된 토큰을 리스트에 추가하고, 토큰을 초기화
        if space.match(idx):
            if token == "":
                continue
            text_to_tokens.append(token)
            token = ""
            continue

        # 현재 인덱스의 문자가 어떤 문자인지 확인하는 조건문
        if eng_num.match(idx):
            current_type = "eng_num"
        elif kor.match(idx):
            current_type = "kor"
        elif jamo.match(idx):
            current_type = "jamo"
        else:
            current_type = "other"

        # 현재 인덱스와 이전 인덱스의 문자가 토크나이징 조건에 해당된다면 토큰을 리스트에 추가한 후 토큰 초기화, 아니면 토큰 유지
        if prev_type == current_type:
            token += idx
        else:
            if token == "":
                token = idx
            else:
                text_to_tokens.append(token)
                token = idx

        prev_type = current_type

    text_to_tokens.append(token)

    return text_to_tokens
