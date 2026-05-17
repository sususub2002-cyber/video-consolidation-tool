import os
import shutil
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path

VIDEO_EXTENSIONS = {
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm',
    '.m4v', '.mpg', '.mpeg', '.ts', '.mts', '.m2ts', '.3gp',
    '.rmvb', '.rm', '.divx', '.xvid', '.vob', '.ogv'
}

class VideoMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("영상 한곳에 모으기")
        self.root.geometry("620x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.src_var = tk.StringVar()
        self.dst_var = tk.StringVar()
        self.copy_mode = tk.BooleanVar(value=False)  # False = 이동, True = 복사
        self.running = False

        self._build_ui()

    def _build_ui(self):
        BG = "#1e1e2e"
        CARD = "#2a2a3e"
        ACCENT = "#7c6af7"
        ACCENT2 = "#5a9df8"
        TEXT = "#e0e0f0"
        SUB = "#8888aa"
        BTN_FG = "#ffffff"

        # 타이틀
        tk.Label(self.root, text="📁  영상 한곳에 모으기", font=("Segoe UI", 16, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(20, 4))
        tk.Label(self.root, text="폴더 안 깊숙이 있는 영상 파일을 한 폴더로 모아줍니다",
                 font=("Segoe UI", 9), bg=BG, fg=SUB).pack(pady=(0, 18))

        # 소스 폴더
        self._folder_row("원본 폴더  (영상이 있는 최상위 폴더)", self.src_var, CARD, ACCENT, TEXT, SUB)

        # 대상 폴더
        self._folder_row("저장 폴더  (영상이 옮겨질 폴더)", self.dst_var, CARD, ACCENT2, TEXT, SUB)

        # 옵션
        opt_frame = tk.Frame(self.root, bg=BG)
        opt_frame.pack(fill="x", padx=28, pady=(4, 0))
        tk.Checkbutton(opt_frame, text="이동 대신 복사 (원본 유지)",
                       variable=self.copy_mode,
                       font=("Segoe UI", 10), bg=BG, fg=TEXT,
                       selectcolor=CARD, activebackground=BG,
                       activeforeground=TEXT).pack(side="left")

        # 진행 바
        pb_frame = tk.Frame(self.root, bg=BG)
        pb_frame.pack(fill="x", padx=28, pady=(16, 4))
        self.progress_label = tk.Label(pb_frame, text="대기 중...",
                                       font=("Segoe UI", 9), bg=BG, fg=SUB, anchor="w")
        self.progress_label.pack(fill="x")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Horizontal.TProgressbar",
                         troughcolor=CARD, background=ACCENT,
                         bordercolor=BG, lightcolor=ACCENT, darkcolor=ACCENT)
        self.pb = ttk.Progressbar(pb_frame, style="Custom.Horizontal.TProgressbar",
                                   mode="determinate", length=560)
        self.pb.pack(fill="x", pady=(4, 0))

        # 버튼 (먼저 bottom에 고정)
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(side="bottom", pady=16)
        self.start_btn = tk.Button(btn_frame, text="  시작하기  ",
                                    font=("Segoe UI", 11, "bold"),
                                    bg=ACCENT, fg=BTN_FG, activebackground="#6a5adf",
                                    activeforeground=BTN_FG, bd=0, padx=20, pady=8,
                                    cursor="hand2", command=self._start)
        self.start_btn.pack(side="left", padx=8)
        tk.Button(btn_frame, text="  초기화  ",
                  font=("Segoe UI", 11), bg=CARD, fg=TEXT,
                  activebackground="#3a3a5e", activeforeground=TEXT,
                  bd=0, padx=20, pady=8, cursor="hand2",
                  command=self._reset).pack(side="left", padx=8)

        # 로그 (버튼 다음에 남은 공간 채움)
        log_frame = tk.Frame(self.root, bg=CARD, bd=0)
        log_frame.pack(fill="both", expand=True, padx=28, pady=(10, 0))
        self.log = tk.Text(log_frame, height=8, font=("Consolas", 9),
                           bg=CARD, fg=TEXT, bd=0, wrap="none",
                           state="disabled", padx=8, pady=6)
        sb = tk.Scrollbar(log_frame, command=self.log.yview, bg=CARD)
        self.log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.log.pack(fill="both", expand=True)

    def _folder_row(self, label, var, card, accent, text, sub):
        frame = tk.Frame(self.root, bg=card, bd=0)
        frame.pack(fill="x", padx=28, pady=6)
        inner = tk.Frame(frame, bg=card)
        inner.pack(fill="x", padx=14, pady=10)
        tk.Label(inner, text=label, font=("Segoe UI", 9, "bold"),
                 bg=card, fg=sub, anchor="w").pack(fill="x")
        row = tk.Frame(inner, bg=card)
        row.pack(fill="x", pady=(5, 0))
        tk.Entry(row, textvariable=var, font=("Segoe UI", 10),
                 bg="#16162a", fg=text, insertbackground=text,
                 bd=0, relief="flat", width=52).pack(side="left", ipady=5, padx=(0, 8))
        tk.Button(row, text="폴더 선택", font=("Segoe UI", 9),
                  bg=accent, fg="#fff", activebackground=accent,
                  bd=0, padx=10, pady=5, cursor="hand2",
                  command=lambda v=var: self._browse(v)).pack(side="left")

    def _browse(self, var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def _log(self, msg, color=None):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _reset(self):
        if self.running:
            return
        self.src_var.set("")
        self.dst_var.set("")
        self.pb["value"] = 0
        self.progress_label.config(text="대기 중...")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _start(self):
        if self.running:
            return
        src = self.src_var.get().strip()
        dst = self.dst_var.get().strip()
        if not src or not os.path.isdir(src):
            messagebox.showerror("오류", "원본 폴더를 올바르게 선택하세요.")
            return
        if not dst:
            messagebox.showerror("오류", "저장 폴더를 선택하세요.")
            return
        os.makedirs(dst, exist_ok=True)
        self.running = True
        self.start_btn.config(state="disabled")
        threading.Thread(target=self._run, args=(src, dst), daemon=True).start()

    def _run(self, src, dst):
        try:
            self._log(f"🔍 파일 검색 중: {src}")
            videos = []
            for root_dir, _, files in os.walk(src):
                for f in files:
                    if Path(f).suffix.lower() in VIDEO_EXTENSIONS:
                        videos.append(os.path.join(root_dir, f))

            total = len(videos)
            if total == 0:
                self._log("❌ 영상 파일을 찾지 못했습니다.")
                self._done()
                return

            self._log(f"✅ 영상 {total}개 발견\n")
            self.pb["maximum"] = total
            mode = "복사" if self.copy_mode.get() else "이동"
            ok, skip = 0, 0

            for i, fpath in enumerate(videos, 1):
                fname = os.path.basename(fpath)
                dest_path = os.path.join(dst, fname)

                # 중복 파일명 처리
                if os.path.exists(dest_path):
                    stem = Path(fname).stem
                    suffix = Path(fname).suffix
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = os.path.join(dst, f"{stem}_{counter}{suffix}")
                        counter += 1
                    self._log(f"  ⚠ 중복 → {os.path.basename(dest_path)}")
                    skip += 1

                try:
                    if self.copy_mode.get():
                        shutil.copy2(fpath, dest_path)
                    else:
                        shutil.move(fpath, dest_path)
                    ok += 1
                    short = fname if len(fname) <= 45 else fname[:42] + "..."
                    self._log(f"  {mode}: {short}")
                except Exception as e:
                    self._log(f"  ✗ 실패: {fname} — {e}")

                self.pb["value"] = i
                self.progress_label.config(
                    text=f"{mode} 중... {i}/{total}  ({int(i/total*100)}%)")
                self.root.update_idletasks()

            self._log(f"\n🎉 완료!  {mode} 성공 {ok}개" +
                      (f"  /  이름 변경 {skip}개" if skip else ""))
            self.progress_label.config(text=f"완료 — {ok}개 {mode} 완료")
            messagebox.showinfo("완료", f"영상 {ok}개 {mode} 완료!")
        except Exception as e:
            self._log(f"\n오류 발생: {e}")
        finally:
            self._done()

    def _done(self):
        self.running = False
        self.start_btn.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMoverApp(root)
    root.mainloop()
