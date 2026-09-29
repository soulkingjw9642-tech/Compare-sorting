from pathlib import Path
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader

root=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('NanumGothic',str(root/'fonts/NanumGothic-Regular.ttf')))
rows=list(csv.DictReader((root/'results.csv').open()))
c=canvas.Canvas(str(root/'REPORT.pdf'),pagesize=A4)
W,H=A4; font='NanumGothic'
def line(text,y,size=10,x=55):
    c.setFont(font,size); c.drawString(x,y,text)
def page(title,num):
    c.setFont(font,15); c.drawString(55,H-60,title)
    c.setLineWidth(.6);c.line(55,H-70,W-55,H-70)
    c.setFont(font,9);c.drawRightString(W-55,35,f'{num} / 10')
def paragraph(lines,start,step=20):
    for i,s in enumerate(lines): line(s,start-step*i)

def box(label,x,y,w=190,h=43):
    c.setStrokeColorRGB(.22,.42,.62); c.setFillColorRGB(.93,.96,.98)
    c.roundRect(x,y,w,h,7,stroke=1,fill=1)
    c.setFillColorRGB(0,0,0);c.setFont(font,10)
    c.drawCentredString(x+w/2,y+h/2-4,label)
def arrow(x1,y1,x2,y2):
    c.setStrokeColorRGB(.3,.4,.47);c.setLineWidth(1.2);c.line(x1,y1,x2,y2)
    import math
    ang=math.atan2(y2-y1,x2-x1)
    p=c.beginPath();p.moveTo(x2,y2)
    p.lineTo(x2-7*math.cos(ang-.5),y2-7*math.sin(ang-.5))
    p.lineTo(x2-7*math.cos(ang+.5),y2-7*math.sin(ang+.5))
    p.close();c.drawPath(p,stroke=0,fill=1)

page('정렬 비교 보고서 — 삽입 · 병합 · Gnome sort',1)
paragraph(['작성자: 변정우  |  과목: 고급알고리즘  |  2026.09.29',
'대상: 삽입 정렬 · 병합 정렬 · Gnome sort',
'GitHub URL: 게시 전 — 본인 저장소 생성 후 실제 URL을 기입할 것',
'', '보고서 구성: 1. 코드 보고서 → 2. 알고리즘 상세 → 3. 알고리즘 실험',
'같은 입력을 세 정렬 함수에 제공하고 시간·비교·이동·안정성을 비교한다.',
'수업에서 배운 삽입/병합과 새로 학습한 Gnome sort를 선택했다.',
'', '1. 코드 보고서: 구성',
'src/sort.h: Item·Stats·정렬 함수의 공통 인터페이스',
'src/sort.c: 세 정렬의 구현 및 비교·이동 횟수 집계',
'src/main.c: 고정 시드 입력 생성, 반복 측정, CSV 출력 및 결과 검증',
'tests/test_sort.c: 빈 배열·중복·역순·음수를 포함한 12개 검사',
'Makefile: make test / make run / make clean',
'', '3. 알고리즘 실험: 입력 자료',
'크기 n = 1,000 / 2,000 / 4,000 / 8,000',
'형태 = 무작위 / 이미 정렬됨 / 역순 / 중복이 많은 값(0~7)',
'의사난수 xorshift32, 시드 20260927. 같은 원본을 매번 복사한다.',
'원소 Item은 정렬 키와 원본 위치를 저장한다. 키만 비교한다.'],H-105)
c.showPage()

page('1. 코드 보고서 — 구조와 자료 흐름',2)
paragraph(['샘플 보고서의 공통 인터페이스·테스트·측정 자료 구성 방식을 참고했다.',
'아래 화살표는 입력 및 호출 방향이다.'],H-105)
box('main.c: 입력 생성 · 시간 측정',200,620)
box('test_sort.c: 12개 검사',55,535,140)
box('sort.h: 공통 Item · Stats · 함수 규약',245,535,255)
arrow(310,620,365,578);arrow(235,641,125,578)
box('insertionSort: 정렬 구간에 삽입',45,430,165)
box('mergeSort: 나누고 병합',215,430,165)
box('gnomeSort: 인접 비교·교환',385,430,165)
for mid in (127,297,467):arrow(365,535,mid,473)
box('results.csv: 48행 기록',200,320)
c.line(390,641,565,641);c.line(565,641,565,341);arrow(565,341,390,341)
paragraph(['세 정렬은 Item 배열, 배열 길이, Stats 포인터를 동일하게 받는다.',
'정렬마다 같은 원본을 복사해 입력한다. 정렬 호출 동안만 clock()을 잰다.',
'비교·이동 횟수는 정렬 내부에서 기록하고 검증은 호출 이후 진행한다.',
'', '파일: src/sort.h · src/sort.c · src/main.c · tests/test_sort.c',
'실행: make test / make run. 그래프: results.csv를 읽어 생성한다.'],270)
c.showPage()


page('1. 코드 보고서 — 설계와 검증',3)
paragraph(['공통 구조: Item {key, original}; Stats {comparisons, moves}.',
'정렬 함수 세 개 모두 Item 배열·길이·Stats 포인터를 받는다.',
'key로만 비교하고 original은 입력 순서 보존 여부를 판정한다.',
'', '공통 계수의 의미',
'greater 호출 = 키 비교 1회; assign 호출 = Item 이동 1회.',
'지역 임시변수 대입과 입력 복사 memcpy는 이동 계수에 넣지 않는다.',
'시간은 정렬 함수 호출 앞뒤에서만 재므로 복사·검증 시간은 빠진다.',
'', '핵심 파일과 역할',
'sort.h       : Item, Stats, SortFn 및 세 함수 선언',
'sort.c       : 삽입·병합·Gnome sort와 비교·대입 계수',
'main.c       : 입력 복사, 5회 시간 평균, CSV 48행, 정렬 검증',
'test_sort.c  : 3개 정렬 × 4개 입력 묶음 = 12개 검사',
'make_charts.py: results.csv에서 비교·시간 그래프 생성',
'', '검증 결과',
'make test: 12개 조합 통과. make run: 모든 출력의 키 오름차순 확인.',
'삽입·병합은 중복 키의 original 순서도 검사한다.',
'Gnome sort도 같은 키끼리 교환하지 않아 안정성을 지킨다.',
'', '설계의 한계',
'샘플의 void* 범용 인터페이스와 달리 이 구현은 Item 타입에 한정된다.',
'12개 사례 통과는 모든 입력에 대한 형식적 증명을 뜻하지 않는다.'],H-105)
c.showPage()

page('2. 알고리즘 상세 — Gnome sort 단계 예시',4)
paragraph(['입력 [4, 2, 3, 1]에서 실제 교환이 일어날 때마다 배열을 기록했다.',
'교환이 필요 없으면 오른쪽으로, 교환하면 왼쪽으로 돌아간다.'],H-105)
c.drawImage(ImageReader(str(root/'gnome-steps.png')),55,255,width=485,height=425,preserveAspectRatio=True,anchor='c')
paragraph(['5번의 인접 교환 뒤 [1, 2, 3, 4]가 된다.',
'같은 키는 교환하지 않아 안정적이다. 최선 O(n), 평균·최악 O(n²).',
'추가 공간 O(1). AI 학습 내용은 NIST의 알고리즘 설명과 대조했다.'],235,19)
c.showPage()

page('2. 알고리즘 상세 — 동작 구조도',5)
paragraph(['삽입 정렬'],H-106,15)
box('현재 원소 저장',55,620,145);box('큰 원소를 뒤로 이동',225,620,145);box('빈 자리에 삽입',395,620,145)
arrow(200,641,225,641);arrow(370,641,395,641)
paragraph(['병합 정렬'],570,15)
box('배열을 반씩 나눔',55,500,145);box('각 부분 재귀 정렬',225,500,145);box('임시 배열로 병합',395,500,145)
arrow(200,521,225,521);arrow(370,521,395,521)
paragraph(['Gnome sort: 새로 학습한 알고리즘'],450,15)
box('인접 두 원소 비교',55,380,145);box('역순이면 교환',225,380,145);box('왼쪽으로 한 칸 복귀',395,380,145)
arrow(200,401,225,401);arrow(370,401,395,401)
paragraph(['이미 정렬됐으면 오른쪽으로 진행한다. 동률이면 교환하지 않는다.',
'Gnome sort는 한 위치를 여러 번 방문하며 삽입 정렬보다 비교가 많다.',
'', '정렬             최선             평균              최악            추가 공간    안정',
'삽입             O(n)            O(n²)            O(n²)           O(1)            예',
'병합             O(n log n)      O(n log n)      O(n log n)   O(n)            예',
'Gnome          O(n)            O(n²)            O(n²)           O(1)            예'],315,25)
c.showPage()

page('3.2 입력 유형별 결과 — 표와 비교 횟수',6)
paragraph(['n=8,000; 시간은 5회 평균, 비교·이동은 함수 내부 계수.',
'재귀깊이는 최초 호출을 1로 센 최대 호출 단계다.'],H-104,17)
y=H-178
line('입력',y,9,55);line('정렬',y,9,113)
line('시간(ms)',y,9,177);line('비교',y,9,285)
line('이동',y,9,397);line('깊이',y,9,493);y-=18
name={'random':'무작위','sorted':'정렬됨','reverse':'역순','duplicates':'중복'}
alg={'insertion':'삽입','merge':'병합','gnome':'Gnome'}
for r in rows:
    if r['n']!='8000':continue
    depth=14 if r['algorithm']=='merge' else 1
    line(name[r['shape']],y,8.3,55);line(alg[r['algorithm']],y,8.3,113)
    c.setFont(font,8.3)
    c.drawRightString(256,y,f"{float(r['time_ms']):.4f}")
    c.drawRightString(369,y,f"{int(r['comparisons']):,}")
    c.drawRightString(478,y,f"{int(r['moves']):,}")
    c.drawRightString(515,y,str(depth))
    y-=17
line('그림 3  키 비교 횟수: 선형 축과 로그 축',y-13,9)
c.drawImage(ImageReader(str(root/'shape-compares-bars.png')),55,92,width=485,height=255,preserveAspectRatio=True,anchor='c')
line('역순에서 Gnome 6,398만 회 > 삽입 3,200만 회 > 병합 5.2만 회.',75,8.5)
c.showPage()

page('3.2 입력 유형별 결과 — 시간과 이동',7)
line('그림 4  평균 실행 시간: 선형 축과 로그 축',H-104,10)
c.drawImage(ImageReader(str(root/'shape-time-bars.png')),55,505,width=485,height=230,preserveAspectRatio=True,anchor='c')
paragraph(['역순 Gnome 약 125.9ms로 최대. 무작위 병합 약 1.33ms로 가장 짧다.',
'작은 시간은 clock()의 해상도와 실행 환경에 민감하다.'],485,16)
line('그림 5  원소 이동 횟수: 선형 축과 로그 축',H-410,10)
c.drawImage(ImageReader(str(root/'shape-moves-bars.png')),55,180,width=485,height=230,preserveAspectRatio=True,anchor='c')
paragraph(['역순 Gnome 약 6,399만 대입, 삽입 약 3,200만, 병합 20.8만.',
'정렬됨 입력의 삽입·Gnome은 0회여서 로그 축 막대가 없다.'],160,16)
c.showPage()

page('3.3 입력 크기별 증가 — 무작위 자료',8)
line('그림 6  n=1,000→8,000일 때 키 비교 횟수',H-105,10)
c.drawImage(ImageReader(str(root/'growth-compares.png')),55,505,width=485,height=230,preserveAspectRatio=True,anchor='c')
line('삽입·Gnome 약 64배, 병합 약 10.7배 증가.',484,9)
line('그림 7  같은 입력에서 평균 실행 시간',H-405,10)
c.drawImage(ImageReader(str(root/'growth-time.png')),55,190,width=485,height=230,preserveAspectRatio=True,anchor='c')
line('선형 축은 절대 격차, 로그 축은 작은 병합 값의 증가도 보여 준다.',166,9)
line('시간은 한 환경의 측정값이므로 비교 계수와 함께 읽는다.',147,9)
c.showPage()

page('3.4 메모리와 안정성',9)
paragraph(['n=8,000. 재귀깊이는 최초 호출을 1로 센다.',
'Item = 정수 두 개 = 이 환경에서 8 B.'],H-105)
y=H-205
line('알고리즘       추가 메모리                            재귀깊이       안정성',y,10)
c.line(55,y-9,W-55,y-9)
line('삽입 정렬       O(1), 지역 Item 한 개                 1 (비재귀)         안정',y-34,9)
line('병합 정렬       O(n), 배열 8,000개 = 64,000 B      14                  안정',y-63,9)
line('Gnome sort   O(1), 교환용 Item 한 개             1 (비재귀)         안정',y-92,9)
paragraph(['병합 정렬은 반으로 나눠 길이 1까지 호출하므로',
'최대 깊이는 ⌈log₂ 8000⌉ + 1 = 14다. 임시 배열 64,000 B와',
'재귀 스택의 정확한 바이트 수는 서로 다른 비용이다.',
'', '세 정렬 모두 키가 같은 원소를 앞지르지 않아 안정적이다.',
'삽입·Gnome은 적은 추가 공간을 쓰는 대신 무작위·역순 입력에서',
'이차 증가를 보였다. 병합은 배열을 쓰지만 비교·시간이 작다.',
'', '실험 한계',
'시간은 clock()의 5회 평균이며 다른 CPU·부하에서 달라질 수 있다.',
'이동 횟수는 assign 호출만 세고 임시 지역변수 대입은 제외한다.',
'입력 씨앗은 고정되어 비교·이동 횟수는 재현 가능하다.'],y-150,23)
c.showPage()

page('결론 · 참고 자료',10)
paragraph(['1. 결과 정리',
'삽입 정렬: 정렬된 자료에 빠르고 안정적이며 추가 공간이 작다.',
'병합 정렬: 임시 배열을 쓰지만 큰 입력에서 비교·시간이 작다.',
'Gnome sort: 인접 교환으로 이해하기 쉽고 안정적이지만',
'역순 큰 자료에서 비교·이동·시간이 가장 많이 들었다.',
'', '2. 재현',
'make test: 12개 알고리즘/입력 조합 통과.',
'make run > report/results.csv: 48행 측정 결과 생성.',
'python3 report/make_charts.py: 단계 그림 및 막대·성장 그래프.',
'', '3. 참고 자료',
'[1] 샘플 보고서: github.com/lec-algorithm/hw1-sample-2026',
'[2] Wikipedia, Sorting algorithm — Comparison of algorithms',
'    en.wikipedia.org/wiki/Sorting_algorithm#Comparison_of_algorithms',
'[3] NIST Dictionary of Algorithms and Data Structures, Gnome sort',
'    xlinux.nist.gov/dads/HTML/gnomeSort.html',
'', '제출 전: 본인 GitHub 저장소 URL을 첫 페이지에 기입한다.',
'필수 ZIP은 해당 저장소 Code > Download ZIP에서 내려받는다.'],H-105)
c.save()
print(root/'REPORT.pdf')
