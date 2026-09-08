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
        self.answer=self.make_ladder(self.input_arr)
        while True:
            if self.answer == self.number:
                break
            self.answer=self.make_ladder(self.answer)
        self.draw_ladder(self.ladder)

    def make_ladder(self,input_arr):
        self.ladder=[]
        self.arr=[0,0,0,0,0]
        print(input_arr,"input_arr")
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
                        if i==4:
                            for x in range(2):
                                self.arr[i-1]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
                        else:
                            for x in range(2):
                                self.arr[i]=1
                                priority_arrs[i].append(self.arr)
                                self.arr=[0,0,0,0,0]
        
        print(priority_arrs,"all text")
        ans=self.logic_ladder(priority_arrs, input_arr)
        return ans

    def logic_ladder(self, arrs, input_arr):
        """
        규칙:
        1) 각 행의 1순위(첫 값)들끼리 비교했을 때 동일한(중복된) 값이 있으면:
           - 중복 그룹 밖에서, 아직 2순위 이상이 남아있고(len>1) 중복 위치와
             인접하지 않은(인덱스 차이 >= 2) 값을 가진 행을 찾아 결합(OR)해서
             self.ladder에 추가.
           - 그런 행이 없으면 중복값 자체를 그대로 self.ladder에 추가.
           - 어느 경우든 중복 그룹의 각 행 + (있다면) 결합된 행에서 1개씩 pop.
        2) 중복이 없으면, 앞에서부터(원 배열 기준 우선순위 순서로) 훑어서
           인접하지 않은(인덱스 차이 >= 2) 첫 번째 쌍을 찾아 결합해서 추가하고
           두 행에서 1개씩 pop.
        3) 결합 가능한 쌍이 전혀 없으면(전부 인접), 가장 먼저 나온(원 배열
           기준 우선순위가 높은) 값 하나만 그대로 추가하고 그 행만 pop.
        """
        self.ladder = []
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
                    self.ladder.append(merged)
                    for row_index in dup_rows:
                        arrs[row_index].pop(0)
                    arrs[candidate_row].pop(0)
                else:
                    self.ladder.append(dup_value)
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
                self.ladder.append(merged)
                arrs[row_i].pop(0)
                arrs[row_j].pop(0)
                continue

            # 3) 결합 불가 -> 가장 우선순위 높은(먼저 나온) 값 하나만 적용
            row_index, value = heads[0]
            self.ladder.append(value)
            arrs[row_index].pop(0)

        print(self.ladder,"ladder")
        ans=self.try_ladder(input_arr,self.ladder)
        print(ans,"ans")
        return ans
    
    def try_ladder(self,number,ladder):
        solution=[0,0,0,0,0]
        print(len(ladder),"len_ladder")
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

if __name__ == "__main__":
    ml=MakeLadder()
    ml.main()