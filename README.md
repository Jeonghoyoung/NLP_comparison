## NLP Comparison

### 1. Korean NLP Module

* 한국어 NLP 모듈 Soynlp, Khaiii, Mecab 세개의 tagging과 명사 추출을 비교한다.
    1. Soynlp
        * 통계를 기반으로 비지도 학습을 통한 문장 -> 단어열, 품사판별 등을 하는 모듈.
        * 특허 데이터 약 23만개의 문장을 학습 데이터로 사용.

    2. Khaiii
        * 카카오에서 개발한 형태소 분석기.
        * 신경망 알고리즘 중 CNN을 사용한 형태소 분석기로 속도면에서 LSTM보다 활용도가 높아 해당 모델 사용.
        * 사용자 기반 사전을 추가하여 새로 생성된 명사 또는 복합명사를 추가할 수 있다.

    3. Mecab
        * 오픈소스 기반의 한국어 형태소 분석기로 일본어 형태소 분석 엔진인 MeCab와 연계된 프로젝트.

	* 형태소 분해 비교
		> 원문 : 예들 들어, 제2 도전 패턴(C2)은 텅스텐을 포함할 수 있다.

		> Mecab : ['예', '들', '들', '어', ',', '제', '2', '도전', '패턴', '(', 'C', '2', ')', '은', '텅스텐', '을', '포함', '할', '수', '있', '다', '.']

		> Khaiii : ['예', '들', '들', '어', ',', '제', '2', '도전', '패턴', '(', 'C', '2', ')', '은', '텅스텐', '을', '포함', '하', 'ㄹ', '수', '있', '다', '.']

		> Soynlp : ['예들', '들어,', '제2', '도전', '패턴(', 'C2)은', '텅스텐', '을', '포함', '할', '수', '있다.']

        * 결과 예문과 같이 Mecab은 tag값을 가진 모든 단어열을 분해하고, Khaiii도 동일하게 분해하나, 된, 할 등과 같은 원문이 있는경우 해당 받침까지 분해한다. 이 둘과 달리 soynlp는 L + R 구조로 R에 해당하는 조사를 붙혀서 단여얼로 분해된다.

        * 첨부 파일 경로: /data/output/Result_comparison_2236269.xlsx
        * Test code : /bin/nlp_comparison.py
 
	* 명사추출
        * 명사추출의 경우 형태소 분해시에 tag를 추출하여 해당 tag중 명사에 해당하는 단어열만을 추출하였다.

        * khaiii의 경우 형태소 분해시 할, 된 등과같이 문제가 될 수 있는 경우가 있어 제외되었으며, soynlp의 경우 비지도학습 기반으로 Dictionary를 사용자가 직접 기입하여 추출해야 한다는 점과 명사추출하는 모듈은 추출하려는 문장을 매번 학습, 추출을 해야하는점, 정렬이 빈도수순으로 매칭이 불가하다는 점에서 제외되었다.

        * MeCab
            > 원문 : 디스플레이 영역(20c)은 제2 이미지(I1)를 표시할 수 있다.
			
            > 명사 추출: ['디스플레이', '영역', '이미지', '표시']
        * Test Code : /bin/zhko_nounextractor.py (chinese_nlp.py 실행 이후 실행.)


### 2. Chinese NLP Module

* 중국어 NLP 모듈의 경우 명사 추출 기능 비교.
    1. Spacy
        * 사전 학습된 파이프라인과 함계 제공되며 60개 이상의 언어에 대한 토근화 및 훈련을 지원.
        * BERT와 같은 사전 학습된 변환기를 통한 다중 작업 학습
        * MIT 라이선스에 따라 출시된 상용 오픈소스 소프트웨어

    2. Pkuseg
        * CRF(Conditional Random Field)를 기반으로 한 모델
        * 사용자의 데이터로 학습 가능
        * 학습된 특정 도메인 모델 존재 (Medicine, Location, Name, Idiom, Organization)
		
    3. Jieba
          * 접두사 사전 구조를 기반으로 하며 단어 빈도를 기반으로 가장 가능성 있는 조합을 찾는다
          * 신조어등의 알 수 없는 단어의 경우 Viterbi 알고리즘과 함께 HMM 모델을 사용

    * 명사 추출
        > 원문: 发热体222可以通过第一电极端子225a以及第二电极端子225b从电源模块接收电源。

        > Spacy : ['热体', '电极', '电', 'b', '电源', '电源']

        > Pkuseg : ['热体', '电', '极端子', '225a', '电', '极端子', '225b', '电源', '模块', '电源']

        > Jieba : ['体', '电极', '端子', '电极', '端子', '电源模块', '电源']

        * 첨부 파일 경로: /data/output/zhko_extract_noun.xlsx
        * Test code : /bin/chinese_nlp.py

### 참고 자료.
* https://github.com/lovit/soynlp
* https://github.com/kakao/khaiii
* https://github.com/hephaex/mecab-ko
* https://github.com/explosion/spaCy
* https://github.com/lancopku/pkuseg-python
* https://github.com/fxsjy/jieba
* https://arxiv.org/pdf/1906.11455.pdf