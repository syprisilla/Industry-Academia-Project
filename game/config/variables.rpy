# --------------------------------------------------
# 사용자 이름
# --------------------------------------------------

default player_name = "MC"


# --------------------------------------------------
# 조사 자동 처리 함수
# --------------------------------------------------

init python:
    def josa(word, with_batchim, without_batchim):
        if not word:
            return without_batchim

        last = word[-1]


        if with_batchim == "이의" and without_batchim == "의":

            # 성 + 이름으로 입력한 경우
            if len(word) >= 3:
                return "의"

            # 이름만 입력한 경우
            if '가' <= last <= '힣':
                jong = (ord(last) - ord('가')) % 28

                if jong != 0:
                    return "이의"
                else:
                    return "의"

            return "의"


        # --------------------------------------------------
        # 일반 조사 처리
        # --------------------------------------------------

        # 마지막 글자가 한글인지 확인
        if '가' <= last <= '힣':
            jong = (ord(last) - ord('가')) % 28

            # 받침이 있으면 with_batchim
            if jong != 0:
                return with_batchim

            # 받침이 없으면 without_batchim
            return without_batchim

        # 한글이 아니면 기본적으로 받침 없는 조사 사용
        return without_batchim