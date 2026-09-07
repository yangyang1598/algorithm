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
        for i in range(3):
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
        non_dupl=[]
        dupl_temp=[]
        

        for j in range(max(len(second_layer) for second_layer in arrs)):
            sample=[]
            for i in (range(len(arrs))):
                if j < len(arrs[i]):
                    sample.append(arrs[i][j])
                else:
                    pass
            sample=sample+non_dupl
            print(sample,"sample")
            tupple_sam=[tuple(item) for item in sample]
            counts=Counter(tupple_sam)
            dupl=[list(item) for item,count in counts.items() if count>1]
            non_dupl=[list(item) for item,count in counts.items() if count==1]
            

            if len(dupl)>1:
                for indx,num in enumerate(dupl):
                    tmp=num.index(1)

                    if tmp+1 in dupl_temp or tmp-1 in dupl_temp:
                        non_dupl.append(dupl[indx])
                        pass
                    else:
                        dupl_temp.append(num.index(1))

                if len(dupl_temp)>1:
                    dupl=(np.array(dupl[0])|(np.array(dupl[1]))).tolist()
                    self.ladder.append(dupl)
            else:
                dupl_tmp=dupl[0].index(1)
                print(dupl_tmp,"dupl_tmp")
                for inx,num in enumerate(non_dupl):
                    tmp=num.index(1)
                    if tmp+2 ==dupl_tmp or tmp-2 == dupl_tmp:
                        dupl=(np.array(dupl[0])|(np.array(non_dupl[inx]))).tolist()
                        self.ladder.append(dupl)
                    else:
                        self.ladder.append(dupl[0])
             
        if non_dupl:
            for non in non_dupl:
                self.ladder.append(non)
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

ml=MakeLadder()
ml.main()  