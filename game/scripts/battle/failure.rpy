label ch1_m1_fail(reason="unknown"):

    n "목소리의 힘이 괴물에게 닿기 전에 사라진다."

    dust "하하! 이번에는 아무 일도 없었네!"

    if reason == "substitution":
        ghost "이번에는 첫소리가 조금 다르게 들렸어."
        ghost "첫소리에 집중해서 다시 말해 보자!"

    elif reason == "omission":
        ghost "이번에는 첫소리가 빠진 것 같아."
        ghost "첫소리부터 천천히 다시 말해 볼까?"

    else:
        ghost "이번에는 목소리의 힘이 제대로 전달되지 않았나 봐."
        ghost "괜찮아! 다시 해 보면 돼."

    mc "알겠어! 다시 해 볼게."

    return