from collections import Counter
import numpy as np
class MakeLadder:
    def __init__(self):
        self.input_arr=[]
        self.number=[1,2,3,4,5]
        self.arr=[0,0,0,0,0]
        self.answer=[0,0,0,0,0]
        self.ladder=[]
    def main(self):

        self.input_arr=list(map(int,input("정답값을 입력하세요\n").split(",")))
        self.ladder = [] 
        current_input = self.input_arr
        while True:
            current_input, new_lines = self.make_ladder(current_input)
            self.ladder.extend(new_lines)  # 새로운 사다리 줄을 기존에 추가
            self.answer = self.try_ladder(self.input_arr, self.ladder)
            # 결과 값이 [1,2,3,4,5]와 일치할 때까지 함수 호출 및 사다리 줄 추가
            if self.answer == self.number:
                break
        # print("최종 사다리:", self.ladder)
        # print("최종 결과:", self.answer)
        # print("최종 사다리:", self.ladder)
        # print("최종 결과:", self.answer)
        self.draw_ladder(self.ladder)

    def make_ladder(self,input_arr):
        ''''
        조건
        1) 그 자리 그대로 내려가는 경우에는 동일 배열 두번 반복 
            [1,0,0,0,0] -> [1,0,0,0,0]
        '''
        self.arr=[0,0,0,0,0]
        priority_arrs=[[],[],[],[],[]]
        for i in range(5):
            for j in range(5):
                if input_arr[i]==self.number[j]:
                    if i-j<0:
                        if j-i ==1:
                            self.arr[i]=1
                            priority_arrs[i].append(self.arr)
                            self.arr=[0,0,0,0,0]
                        else:
                            for x in range(i,j):
                                self.arr[x]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
        
                    elif i-j>0:
                        if i-j==1:
                            self.arr[j]=1
                            priority_arrs[i].append(self.arr)
                            self.arr=[0,0,0,0,0]
                        else:
                            for x in range(i-1,j-1,-1):
                                self.arr[x]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
                    else:
                        if i==0:
                            for x in range(2):
                                self.arr[i]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
                        else:
                            for x in range(2):
                                self.arr[i-1]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
        
        # print(priority_arrs,"all text")
        new_lines, ans = self.logic_ladder(priority_arrs, input_arr)
        return ans, new_lines  
        # print(priority_arrs,"all text")
        new_lines, ans = self.logic_ladder(priority_arrs, input_arr)
        return ans, new_lines  

    def logic_ladder(self, arrs, input_arr):
        """
        규칙:
        1) 단독 순서인데 같은 우선순위에 동일 값 없으면 3번 규칙 pass하고 다음 순서로
        2) 중복이 있는 경우, 해당 값을 채택
        3) 중복이 없는 경우, 중복 값과 인접하지않은 위치에 1이 존재하면 해당 값을 중복값과 결합하여 채택
        
        """
        
        new_ladder = []  #사다리 저장 리스트
        while any(arr for arr in arrs):
            heads = [
                (row_index, row[0])
                for row_index, row in enumerate(arrs)
                if row
            ]
            positions = {row_index: value.index(1) for row_index, value in heads}

            # 1) 1순위 값들 중 중복 확인
            grouped = {}
            for row_index, value in heads:
                grouped.setdefault(tuple(value), []).append(row_index)
            duplicate_groups = [
                (list(value), rows)
                for value, rows in grouped.items()
                if len(rows) > 1
            ]

            if duplicate_groups:
                dup_value, dup_rows = duplicate_groups[0]
                dup_position = dup_value.index(1)

                candidate_row = next(
                    (
                        row_index
                        for row_index, value in heads
                        if row_index not in dup_rows
                        and len(arrs[row_index]) > 1
                        and abs(positions[row_index] - dup_position) >= 2
                    ),
                    None,
                )

                if candidate_row is not None:
                    candidate_value = arrs[candidate_row][0]
                    merged = (np.array(dup_value) | np.array(candidate_value)).tolist()
                    new_ladder.append(merged)
                    new_ladder.append(merged)
                    for row_index in dup_rows:
                        arrs[row_index].pop(0)
                    arrs[candidate_row].pop(0)
                else:
                    new_ladder.append(dup_value)
                    new_ladder.append(dup_value)
                    for row_index in dup_rows:
                        arrs[row_index].pop(0)
                continue

            # 2) 중복이 없으면, 인접하지 않은(차이 >= 2) 첫 번째 쌍을 찾아 결합
            merge_pair = None
            for i in range(len(heads)):
                row_i, value_i = heads[i]
                for row_j, value_j in heads[i + 1:]:
                    if abs(positions[row_i] - positions[row_j]) >= 2:
                        merge_pair = (row_i, value_i, row_j, value_j)
                        break
                if merge_pair:
                    break

            if merge_pair:
                row_i, value_i, row_j, value_j = merge_pair
                merged = (np.array(value_i) | np.array(value_j)).tolist()
                new_ladder.append(merged)
                new_ladder.append(merged)
                arrs[row_i].pop(0)
                arrs[row_j].pop(0)
                continue

            # 3) 결합 불가 -> 가장 우선순위 높은(먼저 나온) 값 하나만 적용
            row_index, value = heads[0]
            new_ladder.append(value)
            new_ladder.append(value)
            arrs[row_index].pop(0)

        # print(new_ladder,"새로 추가된 ladder 줄들")
        ans = self.try_ladder(input_arr, new_ladder)
        return new_ladder, ans  # (새로운 사다리 줄, 변환 결과) 반환
        # print(new_ladder,"새로 추가된 ladder 줄들")
        ans = self.try_ladder(input_arr, new_ladder)
        return new_ladder, ans  # (새로운 사다리 줄, 변환 결과) 반환
    
    def try_ladder(self,number,ladder):
        solution=[0,0,0,0,0]
        for i in range(len(ladder)):
            for j in range(5):      
                # print(i,j,"i,j")
                if ladder[i][j-1]==1:
                    solution[j-1]=number[j]
                    # print(f"answer의 {j-1}번 째 값은{number[j]}")
                elif ladder[i][j]==1:
                    solution[j+1]=number[j]
                    # print(f"answer의 {j+1}번 째 값은{number[j]}")
                else:
                    solution[j]=number[j]
                    # print(f"answer의 {j}번 째 값은{number[j]}")
            number=solution
            solution=[0,0,0,0,0]
        return number

    def draw_ladder(self,ladder):
        ladder_original=[]
        for i in range(len(ladder),0,-1):
            ladder_original.append(ladder[i-1])
        print("사다리 출력")
        for ladder in ladder_original:
            for i in range(5):
                if ladder[i]==1:
                    print("├",end="")
                else:
                    print("│",end="")
            print()
    def draw_ladder(self,ladder):
        ladder_original=[]
        for i in range(len(ladder),0,-1):
            ladder_original.append(ladder[i-1])
        print("사다리 출력")
        for ladder in ladder_original:
            for i in range(5):
                if ladder[i]==1:
                    print("├",end="")
                else:
                    print("│",end="")
            print()
if __name__ == "__main__":
    ml=MakeLadder()
    ml.main()