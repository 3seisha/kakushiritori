import tkinter as tk
from tkinter import messagebox
import re

class KakushiritoriGame:
    def __init__(self, root):
        self.root = root
        self.root.title("かくしりとりゲーム")
        self.root.configure(bg="#FFFAF0")
        self.root.geometry("1000x700")

        self.turn = 1
        self.public_word = ""
        self.hidden_word_p1 = ""
        self.hidden_word_p2 = ""
        self.restart_button = None
        self.word_history = []

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg="#FFFAF0")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(main_frame, bg="#FFFACD", width=480)
        self.left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        self.turn_label = tk.Label(self.left_frame, text="プレイヤー1のターン", font=("Meiryo", 14, "bold"), bg="#FFFACD", fg="#333333")
        self.turn_label.pack(pady=10)

        self.public_word_label = tk.Label(self.left_frame, text="公開ワード:", font=("Meiryo", 12), bg="#FFFACD", fg="#333333")
        self.public_word_label.pack()
        self.public_word_entry = tk.Entry(self.left_frame, font=("Meiryo", 12), width=30, bg="#FFF5EE", fg="#333333")
        self.public_word_entry.pack(pady=5)

        self.hidden_word_label = tk.Label(self.left_frame, text="隠しワード:", font=("Meiryo", 12), bg="#FFFACD", fg="#333333")
        self.hidden_word_label.pack()
        self.hidden_word_entry = tk.Entry(self.left_frame, show="*", font=("Meiryo", 12), width=30, bg="#FFF5EE", fg="#333333")
        self.hidden_word_entry.pack(pady=5)

        self.submit_button = tk.Button(self.left_frame, text="送信", font=("Meiryo", 12), bg="#87CEFA", fg="#FFFFFF", command=self.submit_word)
        self.submit_button.pack(pady=10)

        self.history_label = tk.Label(self.left_frame, text="履歴:", font=("Meiryo", 12), bg="#E6E6FA", fg="#333333")
        self.history_label.pack(pady=(20, 0))
        self.history_listbox = tk.Listbox(self.left_frame, font=("Meiryo", 12), width=40, height=10, bg="#FFF5EE", fg="#333333")
        self.history_listbox.pack(pady=5)

        right_frame = tk.Frame(main_frame, bg="#F0FFFF", width=480)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        self.rules_text_widget = tk.Text(
            right_frame, font=("Meiryo", 10), bg="#F0FFFF", fg="#333333",
            wrap="word", height=35, width=50
        )
        self.rules_text_widget.pack(padx=10, pady=10, fill="both", expand=True)
        self.update_rules_text()

    def update_rules_text(self):
        rules_text = (
            "🎮 かくしりとり ルール\n\n"
            "🔁 基本の流れ\n"
            "このゲームは2人で交互に単語を出し合う「しりとり」に、隠しワードという要素を加えた対戦型ゲームです。\n"
            "各ターンでプレイヤーは以下の2つのワードを入力します。\n\n"
            "1.公開ワード：相手に見せる単語。次のプレイヤーはこの単語の最後の文字から始まる単語を出します。\n"
            "2.隠しワード：相手に見せない秘密の単語。公開ワードの最後の文字から始める必要があります。\n\n"
            "🎯 勝敗の条件\n"
            "あなたの公開ワードが相手の隠しワードと被ってしまった場合、あなたの負けとなります。\n"
            "また、公開ワードまたは隠しワードが「ん」で終わった場合は即負けです。\n\n"
            "📌 ルールのポイント\n"
            "-ワードはすべてひらがなで入力してください。\n"
            "-公開ワードと隠しワードは、しりとりのルールに従ってつながっている必要があります。\n"
            "-単語の最後の文字が小文字（ゃ・ゅ・ょ）の場合は、大文字（や・ゆ・よ）に変換して次の単語の始まりとなります。\n"
            "-濁音・半濁音（例：ば、ぴ、ずなど）はそのまま入力・比較されます。\n"
            "-単語の最後の文字が長音「ー」で終わる単語は使用できません。\n" # ルール説明も微修正
            "-同じ単語は何度使ってもOKです（ただし、戦略的に使いすぎには注意！）。"
        )
        self.rules_text_widget.config(state="normal")
        self.rules_text_widget.delete("1.0", tk.END)
        self.rules_text_widget.insert("1.0", rules_text)
        self.rules_text_widget.config(state="disabled")

    def is_hiragana(self, word):
        # 長音記号「ー」をひらがなとして許可する正規表現に修正
        return re.fullmatch(r'[ぁ-んー]+', word) is not None

    def get_last_char_for_shiritori(self, word):
        last_char = word[-1]
        return {"ゃ": "や", "ゅ": "ゆ", "ょ": "よ"}.get(last_char, last_char)

    def submit_word(self):
        public_word = self.public_word_entry.get()
        hidden_word = self.hidden_word_entry.get()

        if not public_word:
            messagebox.showwarning("入力エラー", "公開ワードを入力してください。")
            return
        if not hidden_word:
            messagebox.showwarning("入力エラー", "隠しワードを入力してください。")
            return

        # ここで `is_hiragana` をチェック
        if not self.is_hiragana(public_word):
            messagebox.showwarning("入力エラー", f"公開ワード「{public_word}」にひらがな以外の文字が含まれています。")
            return
        if not self.is_hiragana(hidden_word):
            messagebox.showwarning("入力エラー", f"隠しワード「{hidden_word}」にひらがな以外の文字が含まれています。")
            return

        # 長音「ー」が最後に来る場合のチェックは引き続き維持
        if public_word.endswith("ー"):
            messagebox.showwarning("入力エラー", "公開ワードが長音「ー」で終わっています。長音で終わる単語は使用できません。")
            return
        if hidden_word.endswith("ー"):
            messagebox.showwarning("入力エラー", "隠しワードが長音「ー」で終わっています。長音で終わる単語は使用できません。")
            return

        if self.public_word:
            expected_first_char = self.get_last_char_for_shiritori(self.public_word)
            if public_word[0] != expected_first_char:
                messagebox.showwarning(
                    "入力エラー",
                    f"公開ワード「{public_word}」は「{expected_first_char}」から始める必要があります。\n"
                    f"これは前の公開ワード「{self.public_word}」の最後の文字です。"
                )
                return

        current_public_last_char = self.get_last_char_for_shiritori(public_word)
        if hidden_word[0] != current_public_last_char:
            messagebox.showwarning(
                "入力エラー",
                f"隠しワード「{hidden_word}」は「{current_public_last_char}」から始める必要があります。\n"
                f"これは現在の公開ワード「{public_word}」の最後の文字です。"
            )
            return

        current_player = self.turn
        next_player = 3 - self.turn

        if public_word[-1] == "ん":
            self.word_history.append((current_player, public_word, hidden_word))
            self.show_game_over(f"💥 プレイヤー{current_player}の公開ワード「{public_word}」が「ん」で終わったため、プレイヤー{next_player}の勝ち！")
            return

        if hidden_word[-1] == "ん":
            self.word_history.append((current_player, public_word, hidden_word))
            self.show_game_over(f"💥 プレイヤー{current_player}の隠しワード「{hidden_word}」が「ん」で終わったため、プレイヤー{next_player}の勝ち！")
            return

        if self.turn == 1:
            self.hidden_word_p1 = hidden_word
            if self.hidden_word_p2 and self.hidden_word_p2 == public_word:
                self.word_history.append((current_player, public_word, hidden_word))
                self.show_game_over(
                    f"💥 プレイヤー1の公開ワード「{public_word}」が、プレイヤー2の隠しワードと一致してしまいました。\n"
                    f"🎉 プレイヤー2の勝ち！"
                )
                return
            self.turn_label.config(text="プレイヤー2のターン")
        else:
            self.hidden_word_p2 = hidden_word
            if self.hidden_word_p1 == public_word:
                self.word_history.append((current_player, public_word, hidden_word))
                self.show_game_over(
                    f"💥 プレイヤー2の公開ワード「{public_word}」が、プレイヤー1の隠しワードと一致してしまいました。\n"
                    f"🎉 プレイヤー1の勝ち！"
                )
                return
            self.turn_label.config(text="プレイヤー1のターン")

        self.history_listbox.insert(tk.END, f"プレイヤー{self.turn}: {public_word}")
        self.history_listbox.see(tk.END)
        self.public_word = public_word
        self.word_history.append((self.turn, public_word, hidden_word))
        self.turn = 3 - self.turn

        self.public_word_entry.delete(0, tk.END)
        self.hidden_word_entry.delete(0, tk.END)

    def show_game_over(self, message):
        self.public_word_entry.config(state="disabled")
        self.hidden_word_entry.config(state="disabled")
        self.submit_button.config(state="disabled")

        p1_final_hidden = self.hidden_word_p1 or '（未入力）'
        p2_final_hidden = self.hidden_word_p2 or '（未入力）'

        history_details = "\n".join(
            [f"ターン{idx+1} - プレイヤー{p_turn}: 公開「{pub}」/ 隠し「{hid}」"
             for idx, (p_turn, pub, hid) in enumerate(self.word_history)]
        )

        full_message = (
            f"{message}\n\n"
            f"🔍 最終的な隠しワード:\n"
            f"プレイヤー1: {p1_final_hidden}\n"
            f"プレイヤー2: {p2_final_hidden}\n\n"
            f"📜 ゲーム履歴:\n{history_details}"
        )
        messagebox.showinfo("ゲームオーバー", full_message)
        self.show_restart_button()

    def show_restart_button(self):
        if not self.restart_button:
            self.restart_button = tk.Button(self.left_frame, text="🔁 もう一度プレイ", font=("Meiryo", 12), bg="#32CD32", fg="white", command=self.restart_game)
            self.restart_button.pack(side="bottom", pady=10)

    def restart_game(self):
        self.turn = 1
        self.public_word = ""
        self.hidden_word_p1 = ""
        self.hidden_word_p2 = ""
        self.word_history.clear()
        self.turn_label.config(text="プレイヤー1のターン")
        self.public_word_entry.config(state="normal")
        self.hidden_word_entry.config(state="normal")
        self.submit_button.config(state="normal")
        self.public_word_entry.delete(0, tk.END)
        self.hidden_word_entry.delete(0, tk.END)
        self.history_listbox.delete(0, tk.END)
        if self.restart_button:
            self.restart_button.destroy()
            self.restart_button = None

if __name__ == "__main__":
    root = tk.Tk()
    game = KakushiritoriGame(root)
    root.mainloop()