import tkinter as tk
from tkinter import messagebox
import random
from time import sleep
class OX_game_GUI:
    
    def __init__(self):
        self.__setup_GUI()
        

    def __setup_GUI(self):
        self.OX_game = OX_game()
        self.turn = 0
        self.root = tk.Tk()
        self.root.title("OX_Game")
        self.root.geometry("600x600")
        
        self.turnFrame = tk.Frame(self.root)
        self.player_turn = self.OX_game.player_turn
        
        if self.player_turn == 0:
            self.turnLabel = tk.Label(self.turnFrame,text="プレイヤーのターン", font=("Helvetica",14))
        else:
            self.turnLabel = tk.Label(self.turnFrame,text="NPCのターン", font=("Helvetica",14))
        self.turnLabel.pack()
        self.turnFrame.pack()
            
        self.numFrame = tk.Frame(self.root)
        self.player_num_Label = tk.Label(self.numFrame,text="プレーヤーの取得ポイント\n0",bg='#FFCCCC', font=("Helvetica",14),width=25)
        self.npc_num_Label = tk.Label(self.numFrame,text="NPCの取得ポイント\n0",bg='#CCDDFF', font=("Helvetica",14),width=25)
        self.player_num_Label.pack(side=tk.LEFT,padx=10,pady=10,)
        self.npc_num_Label.pack(side=tk.RIGHT,padx=10,pady=10,)
        self.numFrame.pack(pady=10)
        
        self.BordFrame = tk.Frame(self.root)
        self.Bord = [[None] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.BordFrame, text=self.OX_game.a[i*3+j], height=4, width=8,command=lambda i=i,j=j :self.__on_click_by_player(i, j), font=("Helvetica",18))
                button.grid(row=i, column=j)
                self.Bord[i][j] = button

                
        self.BordFrame.pack(pady=10)
        
        self.id_ = None
        self.clicked = None
        
        self.root.after(1000,self.continue_game)
        self.root.mainloop()
    
    def reset_game(self):
        self.root.destroy()
        self.__setup_GUI()
        
    def continue_game(self):
        if self.turn < 9:
            if self.turn % 2 == self.player_turn:
                if self.clicked:
                    self.turn += 1
                    self.OX_game.update(self.clicked[0] * 3 + self.clicked[1],"P")
                    self.update()
                    self.__change_DISABLED()
            else:
                
                self.turn += 1
                idx = self.OX_game.start_npc_turn(self.turn)
                self.OX_game.update(idx,"N")
                self.clicked = None
                self.update()
                self.__change_NORMAL()
                
            # print(self.turn)
            self.root.update()
            result = self.OX_game.is_finished(self.turn)    
            if result == 1:
                self.root.after_cancel(self.id_)
                self.show_win()
            elif result == -1:
                self.root.after_cancel(self.id_)
                self.show_lose()
            else:
                if self.turn % 2 == self.player_turn:
                    self.id_ = self.root.after(100,self.continue_game)
                else:
                    self.id_ = self.root.after(1000,self.continue_game)
                    
            # print(result)
                
                
   
    def update(self):
        self.__change_bord()
        self.__change_num()
        self.__change_turn()
     
        
    def __on_click_by_player(self,row,col):
        self.clicked = (row,col)
        self.__change_DISABLED()
        
    def __change_bord(self):
        for i in range(3):
            for j in range(3):
                if self.OX_game.s[i*3+j] == "P":
                    self.Bord[i][j].config(bg = "red",state=tk.DISABLED)
                elif self.OX_game.s[i*3+j] == "N":
                    self.Bord[i][j].config(bg = "blue",state=tk.DISABLED)
                    
    def __change_turn(self):
        if self.player_turn == self.turn % 2:
            self.turnLabel["text"] = "プレイヤーのターン"
        else:
            self.turnLabel["text"] = "NPCのターン"
            
    def __change_num(self):
        self.player_num_Label["text"] = "プレーヤーの取得ポイント\n" + str(self.OX_game.player_num)
        self.npc_num_Label["text"] = "NPCの取得ポイント\n" + str(self.OX_game.npc_num)
        
 
    def __change_DISABLED(self):
        for i in range(3):
            for j in range(3):
                self.Bord[i][j].config(state=tk.DISABLED)
                
    def __change_NORMAL(self):
        for i in range(3):
            for j in range(3):
                if self.OX_game.s[i*3+j] == -1:
                    self.Bord[i][j].config(state=tk.NORMAL)
        
        
    
    def show_win(self):       
        messagebox.showinfo("リザルト","プレイヤーの勝ちです。")
        self.__show_retry_exit_options()
    def show_lose(self):
        messagebox.showinfo("リザルト","プレイヤーの負けです。")
        self.__show_retry_exit_options()
        
    def __show_retry_exit_options(self):
        # リトライと終了を選択する新しいウィンドウを作成
        options_window = tk.Toplevel(self.root)
        options_window.title("メニュー")
        options_window.geometry("250x200")

        # リトライボタン
        retry_button = tk.Button(options_window, text="もう一度遊ぶ", command=lambda:[options_window.destroy(),self.reset_game()],width=15,font=("Helvetica",14))
        retry_button.pack(pady=5)

        # 終了ボタン
        exit_button = tk.Button(options_window, text="終了する", command=self.root.destroy,width=15,font=("Helvetica",14))
        exit_button.pack(pady=5)
            
        
import random
class OX_game:
    def __init__(self):
        self.reset_game()
        
    def reset_game(self):
        #盤面の数字をランダムに決定
        self.a = [random.choice(range(1, 100)) for _ in range(9)]
        self.s = [-1 for _ in range(9)]
        # 縦横斜めになるindexの組
        self.line = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
            ]


        #総和を奇数に調整
        if sum(self.a) % 2 == 0:
            self.a[0] -= 1
            
        #先手後手をランダムに決定
        if random.choice([0,1]) == 0:
            self.player_turn = 0
            self.npc_turn= 1
        else:
            self.player_turn = 1
            self.npc_turn = 0

        self.line = [
                    [0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [0, 3, 6],
                    [1, 4, 7],
                    [2, 5, 8],
                    [0, 4, 8],
                    [2, 4, 6],
                    ]
        self.player_num = 0
        self.npc_num = 0
        
        
    #プレイヤーの勝ちなら1,負けなら-1,続行なら0
    def is_finished(self,turn):
        for i in self.line:
            if self.s[i[0]] == self.s[i[1]] == self.s[i[2]] == "P":
                return 1
            elif self.s[i[0]] == self.s[i[1]] == self.s[i[2]] == "N":
                return -1
            
        if turn == 9:
            if self.player_num > self.npc_num:
                return 1
            else:
                return -1
        return 0
        
        
    def start_npc_turn(self,turn):
        rslt = self.__f(turn,self.s)
        return rslt[1]
        
        
        
    def update(self,idx,user):
        if user == "P":
            self.player_num += self.a[idx]
            self.s[idx] = "P"
        elif user == "N":
            self.npc_num += self.a[idx]
            self.s[idx] = "N"
        
        
    

    # ターン数と盤面を受け取り、先手(高橋君）にとって勝ち盤面なら1、負け盤面なら-1を返す。
    def __f(self,turn, s):
        # 縦横斜めのラインになっているものがあるか判定
        for i in self.line:
            if s[i[0]] == s[i[1]] == s[i[2]] == 1:
                return [10**18,-1]
            elif s[i[0]] == s[i[1]] == s[i[2]] == 2:
                return [-10**18,-1]

        # 盤面がすべて埋まっている場合は塗ったマスの値の総和を比較
        if turn == 9:
            tk, ao = 0, 0
            for idx, i in enumerate(s):
                if i == 1:
                    tk += self.a[idx]
                else:
                    ao += self.a[idx]

            return [tk - ao,-1] 
      

        # 高橋君の手番において、一手で遷移な盤面を全探索し、
        # もっとも良い手を打ったとするとき、高橋君にとっての勝ち盤面に遷移可能か
        # (一手で遷移な盤面のうち、一つでも高橋君にとっての勝ち盤面に遷移可能なら1,そうでないなら-1)
        if turn % 2 == 0:
            rslt = [-float("inf"),-1]
            for i in range(9):
                # 空きマスなら
                if s[i] == -1:
                    # 盤面のコピー
                    s_n = s[:]
                    # 盤面の更新
                    s_n[i] = 1
                    tmp = self.__f(turn + 1, s_n)
                    if rslt[0] < tmp[0]:
                        rslt = [tmp[0],i]

        # 青木君の手番において、一手で遷移な盤面を全探索し、
        # もっとも良い手を打ったとするとき、青木君にとっての勝ち盤面に遷移可能か
        # (一手で遷移な盤面うのち、一つでも青木君にとっての勝ち盤面に遷移可能なら-1,そうでないなら1)
        else:
            rslt = [float("inf"),-1]
            for i in range(9):
                if s[i] == -1:
                    s_n = s[:]
                    s_n[i] = 2
                    tmp = self.__f(turn + 1, s_n)
                    if rslt[0] > tmp[0]:
                        rslt = [tmp[0],i]
        return rslt

def main():
    game = OX_game_GUI() 
    
if __name__ == "__main__":
    main()