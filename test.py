class MakeLadder:
    def __init__(self):
        self.number = [1, 2, 3, 4, 5]
        self.ladder = []

    def main(self):
        target = list(map(int, input("정답값을 입력하세요\n").split(",")))
        self.ladder = self.build_ladder(target)
        result = self.try_ladder(self.number, self.ladder)
        print("생성된 사다리:")
        for row in self.ladder:
            print(row)
        print("검증 결과:", result, "->", "OK" if result == target else "MISMATCH")
        return self.ladder

    def build_ladder(self, target):
        """
        identity([1,2,3,4,5])에서 시작해 target으로 도착하는 사다리(가로줄들)를 생성.
        한 줄 안에서는 서로 겹치지 않는 인접-스왑들만 동시에 배치한다
        (홀짝 정렬을 사다리 줄 단위로 병렬화한 방식).
        """
        n = len(target)
        current = self.number[:]
        rank = {v: i for i, v in enumerate(target)}  # 각 값이 최종적으로 있어야 할 위치
        rows = []

        guard = 0
        while current != target:
            guard += 1
            if guard > 50:  # 안전장치. 정상 입력이면 절대 여기 안 걸림
                raise RuntimeError("사다리 생성 실패: 수렴하지 않음")

            row = [0] * n
            used = [False] * n
            i = 0
            made_swap = False
            while i < n - 1:
                if used[i] or used[i + 1]:
                    i += 1
                    continue
                # 현재 값이 목표 순위상 뒤바뀌어 있으면 이 자리에 가로줄을 놓는다
                if rank[current[i]] > rank[current[i + 1]]:
                    current[i], current[i + 1] = current[i + 1], current[i]
                    row[i] = 1
                    used[i] = True
                    used[i + 1] = True
                    made_swap = True
                    i += 2
                else:
                    i += 1

            if not made_swap:
                raise RuntimeError("사다리 생성 실패: 더 이상 진행 불가")

            rows.append(row)

        return rows

    def try_ladder(self, number, ladder):
        """사다리(rows)를 순서대로 적용해서 실제 결과를 계산 (검증용)."""
        n = len(number)
        solution = number[:]
        for row in ladder:
            new = solution[:]
            i = 0
            while i < n:
                if row[i] == 1:
                    new[i], new[i + 1] = solution[i + 1], solution[i]
                    i += 2
                else:
                    i += 1
            solution = new
        return solution


if __name__ == "__main__":
    ml = MakeLadder()
    ml.main()