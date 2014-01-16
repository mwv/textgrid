invalid_entry_long = '''File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = 3.5
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "First_Interval_Tier"
        xmin = 0
        xmax = 3.5
        intervals: size = 3
        intervals [1]:
            xmin = 0
            xmax = 0.5207695865651463
            text = "word1"
        intervals [2]:
            xmin = 0.5207695865651463
            xmax = invalid_token
            text = "word2"
        intervals [3]:
            xmin = 2.054427880167936
            xmax = 3.5
            text = "word3"
    item [2]:
        class = "TextTier"
        name = "First_Point_Tier"
        xmin = 0
        xmax = 3.5
        points: size = 2
        points [1]:
            invalid_token
            number = 1.7253166583647621
            mark = "here is a point"
        points [2]:
            number = 2.3045524087383478
            mark = "and here's another one"
'''


invalid_header_long = '''File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
3.5
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "First_Interval_Tier"
        xmin = 0
        xmax = 3.5
        intervals: size = 3
        intervals [1]:
            xmin = 0
            xmax = 0.5207695865651463
            text = "word1"
        intervals [2]:
            xmin = 0.5207695865651463
            xmax = 2.054427880167936
            text = "word2"
        intervals [3]:
            xmin = 2.054427880167936
            xmax = 3.5
            text = "word3"
    item [2]:
        class = "TextTier"
        name = "First_Point_Tier"
        xmin = 0
        xmax = 3.5
        points: size = 2
        points [1]:
            number = 1.7253166583647621
            mark = "here is a point"
        points [2]:
            number = 2.3045524087383478
            mark = "and here's another one"
'''


valid_long_1 = '''File type = "ooTextFile"
Object class = "TextGrid"

xmin = 0
xmax = 3.5
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "First_Interval_Tier"
        xmin = 0
        xmax = 3.5
        intervals: size = 3
        intervals [1]:
            xmin = 0
            xmax = 0.5207695865651463
            text = "word1"
        intervals [2]:
            xmin = 0.5207695865651463
            xmax = 2.054427880167936
            text = "word2"
        intervals [3]:
            xmin = 2.054427880167936
            xmax = 3.5
            text = "word3"
    item [2]:
        class = "TextTier"
        name = "First_Point_Tier"
        xmin = 0
        xmax = 3.5
        points: size = 2
        points [1]:
            number = 1.7253166583647621
            mark = "here is a point"
        points [2]:
            number = 2.3045524087383478
            mark = "and here's another one"
'''

valid_long_2 = '''File type = "ooTextFile long"
Object class = "TextGrid"

xmin = 0
xmax = 3.5
tiers? <exists>
size = 2
item []:
    item [1]:
        class = "IntervalTier"
        name = "First_Interval_Tier"
        xmin = 0
        xmax = 3.5
        intervals: size = 3
        intervals [1]:
            xmin = 0
            xmax = 0.5207695865651463
            text =
"word1"
        intervals [2]:
            xmin = 0.5207695865651463
            xmax = 2.054427880167936
            text = "word2"
        intervals [3]:
            xmin = 2.054427880167936
            xmax = 3.5
            text = "word3"
    item [2]:
        class = "TextTier"
        name = "First_Point_Tier"
        xmin = 0
        xmax =
3.5
        points: size = 2
points [1]:
            number = 1.7253166583647621
            mark = "here is a point"
        points [2]:
            number = 2.3045524087383478
            mark = "and here's another one"
'''

valid_short_1 = '''File type = "ooTextFile"
Object class = "TextGrid"

0
3.5
<exists>
2
"IntervalTier"
"First_Interval_Tier"
0
3.5
3
0
0.5207695865651463
"word1"
0.5207695865651463
2.054427880167936
"word2"
2.054427880167936
3.5
"word3"
"TextTier"
"First_Point_Tier"
0
3.5
2
1.7253166583647621
"here is a point"
2.3045524087383478
"and here's another one"
'''

valid_short_2 = '''File type = "ooTextFile short"
Object class = "TextGrid"

0
3.5
<exists>
2
"IntervalTier"
"First_Interval_Tier"
0
3.5
3
0
0.5207695865651463
"word1"
0.5207695865651463
2.054427880167936
"word2"
2.054427880167936
3.5
"word3"
"TextTier"
"First_Point_Tier"
0
3.5
2
1.7253166583647621
"here is a point"
2.3045524087383478
"and here's another one"
'''

invalid_header_short = '''File type = "ooTextFile"
Object class = "TextGrid"

0
invalid_token
<exists>
2
"IntervalTier"
"First_Interval_Tier"
0
3.5
3
0
0.5207695865651463
"word1"
0.5207695865651463
2.054427880167936
"word2"
2.054427880167936
3.5
"word3"
"TextTier"
"First_Point_Tier"
0
3.5
2
1.7253166583647621
"here is a point"
2.3045524087383478
"and here's another one"
'''

invalid_entry_short = '''File type = "ooTextFile"
Object class = "TextGrid"

0
3.5
<exists>
2
"IntervalTier"
"First_Interval_Tier"
0
3.5
3
0
0.5207695865651463
"word1"
0.5207695865651463
0.3
2.054427880167936
"word2"
2.054427880167936
3.5
"word3"
"TextTier"
"First_Point_Tier"
0
3.5
2
1.7253166583647621
"here is a point"
invalid_token
2.3045524087383478
"and here's another one"
'''

valid_chron_1 = '''"Praat chronological TextGrid text file"
0 3.5   ! Time domain.
2   ! Number of tiers.
"IntervalTier" "First_Interval_Tier" 0 3.5
"TextTier" "First_Point_Tier" 0 3.5

! First_Interval_Tier:
1 0 0.5207695865651463
"word1"

! First_Interval_Tier:
1 0.5207695865651463 2.054427880167936
"word2"

! First_Point_Tier:
2 1.7253166583647621
"here is a point"

! First_Interval_Tier:
1 2.054427880167936 3.5
"word3"

! First_Point_Tier:
2 2.3045524087383478
"and here's another one"'''

valid_chron_2 = '''"Praat chronological TextGrid text file"
0 3.5 alkshd
2 lsdkjf
"IntervalTier" "First_Interval_Tier" 0 3.5
"TextTier" "First_Point_Tier" 0 3.5

valid token
1 0 0.5207695865651463
"word1"

valid token
1 0.5207695865651463 2.054427880167936
"word2"

valid token
2 1.7253166583647621
"here is a point"

valid token
1 2.054427880167936 3.5
"word3"

valid token
2 2.3045524087383478
"and here's another one"'''

invalid_header_chron = '''"Praat chronological TextGrid text file"
0 invalid token 3.5   ! Time domain.
2   ! Number of tiers.
"IntervalTier" "First_Interval_Tier" 0 3.5
"TextTier" "First_Point_Tier" 0 3.5

! First_Interval_Tier:
1 0 0.5207695865651463
"word1"

! First_Interval_Tier:
1 0.5207695865651463 2.054427880167936
"word2"

! First_Point_Tier:
2 1.7253166583647621
"here is a point"

! First_Interval_Tier:
1 2.054427880167936 3.5
"word3"

! First_Point_Tier:
2 2.3045524087383478
"and here's another one"'''

invalid_entry_chron = '''"Praat chronological TextGrid text file"
0 3.5   ! Time domain.
2   ! Number of tiers.
"IntervalTier" "First_Interval_Tier" 0 3.5

! First_Interval_Tier:
1 0 0.5207695865651463
"word1"

! First_Interval_Tier:
1 0.5207695865651463 2.054427880167936
"word2"

! First_Interval_Tier:
1 2.054427880167936 3.5
"word3"'''
