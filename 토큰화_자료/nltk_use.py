import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import matplotlib.pyplot as plt
from nltk.probability import FreqDist

# nltk.download()
# nltk.download('stopwords')

# 단계 1: Excel 파일에서 데이터 읽기
excel_file = 'titles_list_500_page.xlsx'  # 본인의 Excel 파일 경로나 이름으로 변경하세요
df = pd.read_excel(excel_file)

# 'Titles' 열에 있는 제목들을 리스트로 변환
titles_list = df['Titles'].tolist()

# 단계 2: 토큰화
all_words = []
for title in titles_list:
    words = word_tokenize(title)
    all_words.extend(words)
    

# 단계 3: 정규화 (소문자 변환)
all_words = [word.upper() for word in all_words]

# # 단계 4: 불용어 제거 (선택사항)
# stop_words = set(stopwords.words('english'))  # 불용어 사전을 영어로 사용하고 있지만, 한국어 불용어 사전을 사용할 수도 있습니다.
# filtered_words = [word for word in all_words if word not in stop_words]

# 단계 5: 특정 단어 제거
specific_words_to_remove = {'[', ']', ')', '?', '!', '...', 'VS', '``', ',', "''", '.', '진짜', '(', '오늘', 
                            "'", "..",'<', '근데', 'ㅋㅋ', 'ㅋㅋㅋ', 'ㅋㅋㅋㅋ', '이', '왜', '존나', '"', '아니', ':', '"', '지금', 'ㄹㅇ', '그냥'}  # 제거하고 싶은 단어들
filtered_words = [word for word in all_words if word not in specific_words_to_remove]

# 단계 6: 빈도수 계산
fdist = FreqDist(filtered_words)
# 결과 출력 또는 활용
print("단어 빈도수:")
word_freq = fdist.most_common()
print(fdist.N())

# 빈도와 순위(rank)를 포함하는 리스트 생성
word_rank_freq = [(word, rank + 1, freq) for rank, (word, freq) in enumerate(word_freq)]

# 결과를 DataFrame으로 변환
freq_df = pd.DataFrame(word_rank_freq, columns=['Word', 'Rank', 'Frequency'])

# 결과를 Excel 파일로 저장 (선택사항)
freq_df.to_excel('femko_word_frequency_nltk.xlsx', index=False)