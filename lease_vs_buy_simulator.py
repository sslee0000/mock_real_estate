# 변수 입력
home_price = 1_500_000_000    # 집값
loan_amount = 1_000_000_000   # 대출금
loan_rate = 0.03            # 연이율 4%
loan_years = 50             # 상환기간 30년. 원리금 계산용
now_years = 10 # loan_years 중 now_years 후 시점을 시뮬레이션

rent_deposit = 500_000_000  # 전세금
rent_loan = 120_000_000     # 전세대출
rent_loan_rate = 0.025      # 전세대출 금리 %
invest_rate = 0.15          # 금융투자수익률 % # 예: 4% (주식, 펀드 등)

home_growth = 0.075        # 집값 연간상승률 2% (예시)
maintenance_cost = 0  # 유지비(취득세 등, now_years간 총액)

# 입력값 요약 출력
print("[입력값 요약]")
print(f"  - 집값: {home_price:,.0f}원")
print(f"  - 대출금: {loan_amount:,.0f}원, 대출금리: {loan_rate*100:.2f}%, 대출기간: {loan_years}년")
print(f"  - 전세보증금: {rent_deposit:,.0f}원, 전세대출: {rent_loan:,.0f}원, 전세대출금리: {rent_loan_rate*100:.2f}%")
print(f"  - 금융투자수익률(주식, 채권 등): {invest_rate*100:.2f}%")
print(f"  - 유지비(취득세 등): {maintenance_cost:,.0f}원 (총 {now_years}년간)")
print(f"  - 시뮬레이션 기간: {now_years}년, 집값 연간상승률: {home_growth*100:.2f}%")
print()

# ---------------  A. 매매(집을 산경우) --------------- #
# 원리금 균등등월 상환액 계산 함수
def monthly_payment(P, r, n):
    """P: 원금, r: 연이율, n: 총상환회수(월)"""
    m = r/12
    return P * m * (1 + m)**n / ((1 + m)**n - 1)
m_payment = monthly_payment(loan_amount, loan_rate, loan_years * 12)  # 원리금균등 상환액

# now_years간 대출이자, 원금상환 합계 계산
def total_interest_and_principal_paid(P, r, n_total, n_paid):
    """
    P: 대출 원금
    r: 연이율
    n_total: 전체 상환 회수(월) (ex. 30년*12)
    n_paid: 실제 상환한 기간(월) (ex. now_years*12)
    반환값: (누적 이자, 누적 원금상환)
    """
    m = r/12  # 월 이자율
    payment = monthly_payment(P, r, n_total)  # 매월 상환액(원리금균등)
    balance = P
    total_interest = 0
    total_principal = 0
    for _ in range(n_paid):
        interest = balance * m  # 이번달 이자
        principal = payment - interest  # 이번달 원금상환
        balance -= principal  # 남은 대출잔액에서 원금상환 차감
        total_interest += interest  # 누적 이자 합산
        total_principal += principal  # 누적 원금상환 합산
    return total_interest, total_principal

# now_years(변수) 동안 낸 이자/원금만 계산
total_interest, total_principal = total_interest_and_principal_paid(
    loan_amount, loan_rate, loan_years*12, now_years*12
)

# now_years 뒤 집 값
future_home_value = home_price * ((1 + home_growth) ** now_years)

# 집값 상승분
home_profit = future_home_value - home_price

# now_years 후 남은 대출원금
remain_loan = loan_amount - total_principal
# 집값 - 남은 대출원금
buy_final_equity = future_home_value - remain_loan
# 총 자산: 집값 - 남은 대출원금 - 유지비
buy_total_assets = buy_final_equity - maintenance_cost

# ---------------  B. 전세  --------------- #
# 일시불 투자(집 살 때 내 돈 - 전세 내 돈)
lump_sum = home_price - loan_amount - (rent_deposit - rent_loan)
lump_sum = lump_sum if lump_sum > 0 else 0
lump_sum_future = lump_sum * (1 + invest_rate) ** now_years

# 매달 투자 가능한 금액 = 월 상환액 - 월 전세이자
monthly_rent_interest = rent_loan * (rent_loan_rate / 12)
monthly_surplus = m_payment - monthly_rent_interest
monthly_surplus = max(monthly_surplus, 0)

def fv_ordinary_annuity(pmt, r, years):
    """월적립, 연이율, 기간(년) -> 만기시점 적립금 총액(말일 적립)"""
    m = r / 12
    n = years * 12
    return pmt * (((1 + m) ** n - 1) / m)

surplus_future = fv_ordinary_annuity(monthly_surplus, invest_rate, now_years)

# now_years간 전세대출 이자 합계 (월이자*개월수)
rent_interest = monthly_rent_interest * now_years * 12

# 전세 총 자산 = 전세보증금 + 일시불 투자 미래가치 + 적립식 투자 미래가치
lease_total_assets = rent_deposit + lump_sum_future + surplus_future

# 결과 출력
print(f"[집 구입] {now_years}년 뒤 상세 내역")
print(f"  - 집값: {future_home_value:,.0f}원, (상승분 {home_profit:,.0f}원, 상승률: {(future_home_value/home_price-1)*100:.1f}%)")
print(f"  - 남은 대출원금: {remain_loan:,.0f}원 갚은 대출원금: {total_principal:,.0f}원")
print(f"  - 유지비: {maintenance_cost:,.0f}원")
print(f"  - 누적 이자: {total_interest:,.0f}원")
print(f"  => 총자산: {buy_total_assets:,.0f}원 (집값-남은대출-유지비)\n")

print(f"[전세]   {now_years}년 뒤 상세 내역")
print(f"  - 전세보증금: {rent_deposit:,.0f}원")
print(f"  - 일시불 투자 미래가치: {lump_sum_future:,.0f}원")
print(f"  - 원리금 대신 적립식 투자 미래가치: {surplus_future:,.0f}원")
print(f"  - 누적 전세대출이자: {rent_interest:,.0f}원")
print(f"  => 총자산: {lease_total_assets:,.0f}원 (전세보증금+일시불+적립식)\n")

print(f"[요약] 매매 총자산: {buy_total_assets:,.0f}원, 전세 총자산: {lease_total_assets:,.0f}원")
print(f"(매월 원리금 상환액: {m_payment:,.0f}원, {loan_years}년 상환 기준)")

if buy_total_assets > lease_total_assets:
    print(f"→ {now_years}년 후에는 '매매'가 {buy_total_assets- lease_total_assets:,.0f}만큼 유리합니다.")
elif buy_total_assets < lease_total_assets:
    print(f"→ {now_years}년 후에는 '전세'가 {-buy_total_assets +lease_total_assets:,.0f}만큼 유리합니다.")
else:
    print(f"→ {now_years}년 후에는 두 방법이 동일합니다.")
