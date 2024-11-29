import ast

def convert_to_list(content):
    if isinstance(content, str):
        try:
            # 문자열을 리스트 형태로 변환
            content = ast.literal_eval(content)
        except:
            # 변환에 실패하면 빈 리스트로 반환
            content = []
    return content

# merge_contents 함수는 이제 중첩된 리스트를 하나로 합침
def merge_contents(contents):
    merged = []
    for content in contents:
        content = convert_to_list(content)  # 각 content가 문자열이라면 실제 리스트로 변환
        if content:  # content가 비어 있지 않으면
            merged.extend(content)  # content의 요소들을 모두 합침
    return merged