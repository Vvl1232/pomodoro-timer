from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

# Timer variables
reps = 0
timer = None
stopped = False
remaining_time = 0

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps, timer, stopped, remaining_time
    if timer is not None:
        window.after_cancel(timer)
    reps = 0
    timer = None
    stopped = False
    remaining_time = 0
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer", fg=GREEN)
    check_label.config(text="")

# ---------------------------- TIMER START ------------------------------- #
def start_timer():
    global reps, timer, stopped, remaining_time
    if timer is not None:
        return  # Prevent multiple timers from running
    
    if stopped and remaining_time > 0:
        stopped = False  # Resume from where it stopped
        count_down(remaining_time)
    else:
        reps += 1
        work_sec = WORK_MIN * 60
        short_break_sec = SHORT_BREAK_MIN * 60
        long_break_sec = LONG_BREAK_MIN * 60

        if reps % 8 == 0:
            count_down(long_break_sec)
            title_label.config(text="Long Break", fg=RED)
        elif reps % 2 == 0:
            count_down(short_break_sec)
            title_label.config(text="Short Break", fg=PINK)
        else:
            count_down(work_sec)
            title_label.config(text="Work", fg=GREEN)

# ---------------------------- BREAK BUTTON ------------------------------- #
def start_break():
    global timer
    if timer is not None:
        window.after_cancel(timer)
    count_down(SHORT_BREAK_MIN * 60)
    title_label.config(text="Short Break", fg=PINK)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer, stopped, remaining_time
    if stopped:
        remaining_time = count  # Save remaining time when stopped
        return  # Prevent further countdown if stopped
    
    count_min = math.floor(count / 60)
    count_sec = count % 60
    count_sec = f"{count_sec:02d}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        remaining_time = 0
        start_timer()
        update_checkmarks()

# ---------------------------- UPDATE CHECKMARKS ------------------------------- #
def update_checkmarks():
    work_sessions = reps // 2
    check_label.config(text="✔" * work_sessions)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)

# Title Label
title_label = Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 50, "bold"))
title_label.grid(column=1, row=0)

# Canvas for Timer
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Buttons
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)
break_button = Button(text="Break", highlightthickness=0, command=start_break)
break_button.grid(column=1, row=2)
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

# Check Label (for completed Pomodoro sessions)
check_label = Label(text="", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20, "bold"))
check_label.grid(column=1, row=3)

window.mainloop()