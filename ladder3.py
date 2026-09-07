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
        for i in range(1):
            if self.answer!=self.number:
                self.answer=self.make_ladder(self.answer)
        
    def make_ladder(self,input_arr):
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
        ans=self.logic_ladder(priority_arrs)
        return ans
        
    def logic_ladder(self,arrs):
        while any(arr for arr in arrs):
            heads = [
                (row_index, row[0])
                for row_index, row in enumerate(arrs)
                if row
            ]
            print([value for _, value in heads], "sample")

            grouped = {}
            for row_index, value in heads:
                grouped.setdefault(tuple(value), []).append(row_index)

            duplicate_groups = [
                (list(value), rows)
                for value, rows in grouped.items()
                if len(rows) > 1
            ]

            if duplicate_groups:
                selected, selected_rows = duplicate_groups[0]
                selected_row = selected_rows[0]
                merge_row = None

                if len(duplicate_groups) > 1:
                    merge_value, merge_rows = duplicate_groups[1]
                    merge_row = merge_rows[0]
                else:
                    selected_position = selected.index(1)
                    for row_index, value in heads:
                        if row_index in selected_rows:
                            continue
                        if abs(value.index(1) - selected_position) == 2:
                            merge_value = value
                            merge_row = row_index
                            break

                if merge_row is not None:
                    selected = (
                        np.array(selected) | np.array(merge_value)
                    ).tolist()
                    arrs[selected_row].pop(0)
                    arrs[merge_row].pop(0)
                else:
                    arrs[selected_row].pop(0)

                self.ladder.append(selected)
                continue

            pair = None
            for left_index, (left_row, left_value) in enumerate(heads):
                left_position = left_value.index(1)
                for right_row, right_value in heads[left_index + 1:]:
                    right_position = right_value.index(1)
                    both_have_next = (
                        len(arrs[left_row]) > 1 and len(arrs[right_row]) > 1
                    )
                    both_are_last = (
                        len(arrs[left_row]) == 1 and len(arrs[right_row]) == 1
                    )
                    if (
                        abs(left_position - right_position) == 2
                        and (both_have_next or both_are_last)
                    ):
                        pair = (left_row, left_value, right_row, right_value)
                        break
                if pair:
                    break

            if pair:
                left_row, left_value, right_row, right_value = pair
                merged = (np.array(left_value) | np.array(right_value)).tolist()
                self.ladder.append(merged)
                if len(arrs[left_row]) == 1 and len(arrs[right_row]) == 1:
                    arrs[left_row].pop(0)
                    arrs[right_row].pop(0)
                elif len(arrs[right_row]) > 1:
                    arrs[right_row].pop(0)
                else:
                    arrs[left_row].pop(0)
                continue

            row_index, value = next(
                (
                    (candidate_row, candidate_value)
                    for candidate_row, candidate_value in heads
                    if len(arrs[candidate_row]) > 1
                ),
                heads[0],
            )
            self.ladder.append(value)
            arrs[row_index].pop(0)

        print(self.ladder,"ladder")
        ans=self.try_ladder(self.input_arr,self.ladder)
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