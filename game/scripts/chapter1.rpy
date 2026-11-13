
# ==================================================
# Chapter 1. 목소리의 힘 - 1층의 괴물들
# ==================================================


label chapter1:

    $ current_chapter = 1

    # ==========================================
    # SCENE 1. 첫 번째 층
    # ==========================================

    n "엘리베이터가 천천히 움직이기 시작한다."

    window hide

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    scene apartment corridor_1
    show ui_ghost intro_idle at ui_ghost_corridor, ui_ghost_idle
    with fade

    window auto
    #배경이 첫 번째 층 복도로 바뀐다. 유령이 복도의 왼쪽 위치로 옮겨진다

    n "잠시 후, 문이 열리자 어두운 복도가 모습을 드러낸다."

    mc "여기가 첫 번째 층이야?"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "응! 여기부터 괴물들이 나타날 거야."
    mc "정말 내가 괴물들을 물리칠 수 있을까?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "물론이지! 아까 네 목소리에 특별한 힘이 있다고 했잖아."
    mc "그런데 그 힘을 어떻게 사용하는 거야?"
    ghost "걱정하지 마. 내가 옆에서 알려 줄게!"

    n "그때, 복도 끝에서 바스락거리는 소리가 들린다."

    mc "어? 무슨 소리지?"

    jump ch1_m1_start


# ==================================================
# MONSTER 1. 먼지 괴물
# ==================================================

label ch1_m1_start:

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)

    # ==========================================
    # SCENE 2. 첫 번째 괴물 등장
    # ==========================================

    show apartment corridor_2 behind ui_ghost with fade
    n "복도 구석에 쌓여 있던 먼지들이 꿈틀거리기 시작한다."

    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    show ui_dust before at ui_dust_corridor, ui_dust_emerge
    show ui_ghost intro_surprised
    #먼지 괴물이 등장한다.

    n "먼지들이 뭉치더니 커다란 괴물로 변한다."

    show ui_dust talk with Dissolve(0.16)
    dust "으하하! 여기는 내 구역이야!"
    mc "으악! 먼지가 말을 하잖아!"
    show ui_dust angry at ui_dust_corridor, ui_dust_threaten
    show ui_ghost intro_surprised at ui_ghost_corridor, ui_ghost_react
    dust "누구도 나를 지나갈 수 없어!"

    show ui_dust before
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "드디어 첫 번째 괴물이 나타났어!"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "지금이 네 목소리의 힘을 사용할 때야."

    mc "그런데 어떻게 공격하는 건데?"

    # ==========================================
    # SCENE 3. 전투 방법 설명
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "먼저 네가 잘 말할 수 있는 단어로 목소리를 준비해 보자."
    ghost "그다음 화면에 나타나는 연습 단어를 말하면 돼!"
    mc "단어를 말하기만 하면 되는 거야?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "응! 정확하게 말하면 목소리의 힘이 괴물에게 전달될 거야."
    ghost "세 번 공격에 성공하면 괴물의 저주를 풀 수 있어!"

    mc "좋아! 한번 해 볼게!"

    # --------------------------------------------------
    # TODO 첫 번째 괴물 전투 시작
    # 핵심단어 제시 -> 훈련단어 제시
    # 음성 녹음 및 발음 분석
    # 성공 횟수 0/3, 괴물 HP 3
    #
    # 성공 -> ch1_m1_success_1
    # 실패 -> ch1_m1_fail
    # 측정 불가 -> ch1_m1_unrecognized
    # --------------------------------------------------

    # [임시 테스트] 전투 기능 구현 전 성공 대사 3회 실행
    jump ch1_m1_battle


# --------------------------------------------------
# MONSTER 1. 발음 요청
# --------------------------------------------------

label ch1_m1_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "준비됐지? 화면에 나오는 단어를 천천히 말해 봐!"

    # TODO 핵심단어 -> 훈련단어 발음 진행
    # 훈련단어 발음 결과에 따라 해당 대사 호출

    return


# --------------------------------------------------
# MONSTER 1. 전투 완료
# --------------------------------------------------

label ch1_m1_clear:

    # ==========================================
    # SCENE 4. 첫 번째 괴물 정화
    # ==========================================

    n "먼지 괴물을 감싸고 있던 어두운 기운이 사라진다."

    call ui_dust_purification from ch1_m1_purification_done
    #먼지괴물 정화

    show ui_ghost intro_relief with Dissolve(0.2)
    dust "어...? 몸이 가벼워졌어!"
    dust "고마워! 이상한 저주 때문에 내 마음대로 움직일 수 없었어."

    mc "저주 때문에 괴물이 된 거였어?"
    ghost "맞아. 이 아파트의 괴물들은 저주에 걸려 있어."
    ghost "네 목소리는 그 저주를 풀 수 있는 거야!"

    mc "그럼 다른 괴물들도 도와줘야겠네!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "맞아! 이제 다음으로 가 보자."


    hide ui_dust after with dissolve
    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "괴물이 사라지자 막혀 있던 복도에 길이 열린다."

    $ cleared_monsters.add((1, 1))
    call progress_autosave from ch1_m1_autosaved
    # ch1_m2_start로 이동

    # [임시 테스트] 첫 번째 괴물 정화 후 다음 괴물로 이동
    jump ch1_m2_start


# ==================================================
# MONSTER 2. 메아리 괴물
# ==================================================

label ch1_m2_start:

    # ==========================================
    # SCENE 5. 두 번째 괴물 등장
    # ==========================================

    show apartment corridor_3 behind ui_ghost with fade
    n "주인공과 작은 유령은 열린 복도를 따라 걸어간다."
    show ui_ghost intro_curious with Dissolve(0.2)
    n "그때, 어디선가 이상한 목소리가 들려온다."

    mc "어디선가 이상한 소리가 들려..."

    echo "들려... 들려... 들려..."

    mc "어? 내 말을 따라 하잖아?"

    echo "따라 해... 따라 해...!"

    n "복도 천장에서 둥근 괴물 하나가 내려온다."

    mc "이번에는 또 다른 괴물이야!"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "조심해! 저건 메아리 괴물이야."
    ghost "다른 사람의 목소리를 빼앗아 똑같이 따라 하는 괴물이지!"

    echo "네 목소리도 가져가 버릴 거야!"

    mc "내 목소리는 줄 수 없어!"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "걱정 마! 아까 배운 방법으로 싸우면 돼."

    # ==========================================
    # SCENE 6. 두 번째 전투 준비
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "이번에도 익숙한 단어로 먼저 목소리를 준비하자."
    ghost "그리고 화면에 나타나는 연습 단어를 말해 봐!"

    mc "알겠어! 이번에는 내가 해 볼게."

    echo "히히! 과연 내 메아리를 이길 수 있을까?"

    # --------------------------------------------------
    # TODO 두 번째 괴물 전투 시작
    # 핵심단어 -> 훈련단어 제시
    # 음성 녹음 및 발음 분석
    # 성공 횟수 0/3, 괴물 HP 3
    #
    # 성공 -> ch1_m2_success_1
    # 실패 -> ch1_m2_fail
    # 측정 불가 -> ch1_m2_unrecognized
    # --------------------------------------------------

    # [임시 테스트] 전투 기능 구현 전 성공 대사 3회 실행
    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    call ch1_m2_success_1
    call ch1_m2_success_2
    call ch1_m2_success_3

    jump ch1_m2_clear


# --------------------------------------------------
# MONSTER 2. 발음 요청
# --------------------------------------------------

label ch1_m2_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "좋아! 화면에 나오는 단어를 말해 보자!"

    # TODO 핵심단어 -> 훈련단어 발음 진행
    # 훈련단어 발음 결과에 따라 해당 대사 호출

    return

# --------------------------------------------------
# MONSTER 2. 전투 완료
# --------------------------------------------------

label ch1_m2_clear:

    # ==========================================
    # SCENE 7. 두 번째 괴물 정화
    # ==========================================

    n "메아리 괴물을 감싸고 있던 어두운 기운이 흩어진다."
    n "괴물의 몸에서 작은 빛들이 하나둘 빠져나온다."

    echo "어...? 이제 이상한 소리가 들리지 않아!"
    echo "드디어 내 목소리를 되찾았어!"

    mc "정말 다행이다!"
    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "잘했어! 두 번째 괴물의 저주도 풀었네."

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "메아리 괴물은 환한 빛과 함께 사라진다."

    ghost "이제 이 층의 마지막 괴물만 남았어!"
    mc "좋아! 끝까지 해 볼게."

    $ cleared_monsters.add((1, 2))
    call progress_autosave from ch1_m2_autosaved
    # ch1_m3_start로 이동

    # [임시 테스트] 두 번째 괴물 정화 후 다음 괴물로 이동
    jump ch1_m3_start


# ==================================================
# MONSTER 3. 그림자 괴물
# ==================================================

label ch1_m3_start:

    # ==========================================
    # SCENE 8. 세 번째 괴물 등장
    # ==========================================

    show apartment corridor_4 behind ui_ghost with fade
    n "복도 끝에 도착하자 커다란 문이 나타난다."
    n "문 너머에는 위층으로 올라가는 엘리베이터가 보인다."

    mc "저기야! 이제 위층으로 갈 수 있겠어!"
    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "잠깐! 뭔가 이상해..."

    n "그 순간, 바닥에 드리워진 그림자가 움직이기 시작한다."
    n "그림자는 점점 커지더니 거대한 괴물로 변한다."

    shadow "누구냐... 감히 이곳까지 들어오다니."
    show ui_ghost intro_surprised with Dissolve(0.2)
    mc "으악! 이번 괴물은 엄청 커!"

    show ui_ghost intro_worried with Dissolve(0.2)
    ghost "저건 이 층의 마지막 괴물이야!"
    mc "저 괴물을 물리쳐야 위층으로 갈 수 있는 거지?"
    show ui_ghost intro_talk_closed with Dissolve(0.2)
    ghost "맞아! 하지만 걱정하지 마."
    ghost "지금까지 해 온 것처럼 하면 돼."

    # ==========================================
    # SCENE 9. 마지막 전투 준비
    # ==========================================

    show ui_ghost intro_explain with Dissolve(0.2)
    ghost "이번에도 먼저 익숙한 단어를 말해 보자."
    ghost "그다음 연습 단어로 괴물을 공격하는 거야!"

    mc "응! 이제 어떻게 하는지 알아!"

    shadow "그렇다면 어디 한번 해 보아라!"

    # --------------------------------------------------
    # TODO 세 번째 괴물 전투 시작
    # 핵심단어 -> 훈련단어 제시
    # 음성 녹음 및 발음 분석
    # 성공 횟수 0/3, 괴물 HP 3
    #
    # 성공 -> ch1_m3_success_1
    # 실패 -> ch1_m3_fail
    # 측정 불가 -> ch1_m3_unrecognized
    # --------------------------------------------------

    # [임시 테스트] 전투 기능 구현 전 성공 대사 3회 실행
    $ play_scene_music(scene_battle_music, volume=scene_battle_volume)
    call ch1_m3_success_1
    call ch1_m3_success_2
    call ch1_m3_success_3

    jump ch1_m3_clear


# --------------------------------------------------
# MONSTER 3. 발음 요청
# --------------------------------------------------

label ch1_m3_prompt:

    show ui_ghost intro_talk with Dissolve(0.2)
    ghost "마지막 괴물이야! 준비되면 단어를 말해 봐!"

    # TODO 핵심단어 -> 훈련단어 발음 진행
    # 훈련단어 발음 결과에 따라 해당 대사 호출

    return

# --------------------------------------------------
# MONSTER 3. 전투 완료
# --------------------------------------------------

label ch1_m3_clear:

    # ==========================================
    # SCENE 10. 마지막 괴물 정화
    # ==========================================

    n "그림자 괴물을 감싸고 있던 어둠이 완전히 사라진다."
    n "괴물의 몸이 작아지며 부드러운 빛으로 변한다."

    shadow "드디어... 저주에서 벗어났구나."
    mc "이제 괜찮아?"
    shadow "그래. 네 목소리 덕분이다."

    show ui_ghost intro_happy with Dissolve(0.2)
    ghost "해냈어! 이 층의 괴물들을 모두 도와줬어!"
    mc "정말? 내가 세 마리나 물리친 거야?"
    ghost "응! 이제 네 목소리의 힘을 알겠지?"

    mc "응! 처음에는 무서웠는데 이제 조금 자신이 생겼어!"

    shadow "하지만 아직 끝난 것은 아니다."
    mc "응?"
    shadow "이 아파트의 위층에는 더 깊은 저주가 잠들어 있다."
    shadow "직접 올라가 보면 알게 될 것이다..."

    $ play_scene_music(scene_corridor_music, volume=scene_corridor_volume)
    n "그림자 괴물은 마지막 말을 남기고 빛 속으로 사라진다."
    $ play_scene_sound(scene_elevator_sound)
    n "동시에 굳게 닫혀 있던 엘리베이터 문이 열린다."

    $ cleared_monsters.add((1, 3))
    call progress_autosave from ch1_m3_autosaved
    # Chapter 1 전체 클리어 처리
    # ch1_finish로 이동

    # [임시 테스트] 세 번째 괴물 정화 후 Chapter 1 종료 장면으로 이동
    jump ch1_finish


# ==================================================
# CHAPTER 1. 완료
# ==================================================

label ch1_finish:

    # ==========================================
    # SCENE 11. 다음 층으로
    # ==========================================

    show apartment elevator_on behind ui_ghost with dissolve
    show ui_ghost intro_talk with Dissolve(0.2)
    n "주인공과 작은 유령은 함께 엘리베이터에 올라탄다."
    $ play_scene_sound(scene_elevator_sound)
    n "엘리베이터 문이 천천히 닫히고, 다음 층을 향해 움직이기 시작한다."

    # --------------------------------------------------
    $ completed_chapters.add(1)
    $ current_chapter = 2
    call progress_autosave from ch1_completion_autosaved
    # Chapter 2 연결
    # 전투 완료 후 Chapter 2로 이동
    # --------------------------------------------------

    hide ui_ghost
    show ui_ghost at ui_ghost_corridor, ui_ghost_settle
    $ stop_scene_music()
    stop sound
    jump chapter2
