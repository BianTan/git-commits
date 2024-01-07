# -*- coding: utf-8 -*-
import time
from git import Repo
from rich.console import Console
from rich.text import Text

console = Console()

# 时间段的定义
def get_time_slot(hour):
    if 6 <= hour < 12:
        return "上午"
    elif 12 <= hour < 18:
        return "下午"
    elif 18 <= hour < 24:
        return "晚上"
    else:
        return "凌晨"

# 获取 git commit 数量
def get_commits(repo_path, authors, since_date, until_date):
    # 打开仓库
    repo = Repo(repo_path)

    # 初始化空列表以存储符合条件的提交
    commits = []

    # 获取指定日期范围内的所有提交
    for commit in repo.iter_commits(since=since_date, until=until_date):
      if not authors:
          commits.append(commit)
      # 检查提交的作者是否在指定的作者列表中
      else: 
        if commit.author.name in authors:
          commits.append(commit)

    # 返回符合条件的提交
    return commits

def get_yes_or_no(text = "请输入"):
    while True:  # 设置一个无限循环
        # 提示用户输入
        tips = f"{text} [yellow]yes/no (默认yes)[/yellow]："
        user_input = console.input(tips).strip().lower()
        if user_input in ["yes", "no"]:  # 检查输入是否为"yes"或"no"
            return user_input == "yes"  # 返回有效输入
        else:
            return True
  
def input_authors():
    # 提示用户输入
    input_text = console.input("请输入 commit 作者名称列表，使用英文逗号分隔 [或直接按Enter跳过]：")

    # 判断用户是否输入了内容
    if input_text.strip():  # 如果用户输入了内容（不仅仅是空格）
        # 将用户输入以英文逗号分隔，并移除两端的空白字符
        authors = [name.strip() for name in input_text.split(',')]
    else:
        # 如果用户没有输入任何内容，则返回空列表
        authors = []

    return authors

# 打印方法
def slow_print(text, delay=0.1):
    # 使用Text对象来解析样式
    styled_text = Text.from_markup(text)
    
    # 逐字打印带有样式的文本
    for char in styled_text:
        console.print(char, end="", style=char.style)
        time.sleep(delay)
    console.print()  # 打印换行

# 确定提交次数最多的时间段，并返回关心的信息。
def get_care_message(time_slots):
    max_slot = max(time_slots, key=time_slots.get)
    care_messages = {
        '上午': "一天之计在于晨，希望你有一个充实的一天。",
        '下午': "记得适时休息，保持精力充沛哦。",
        '晚上': "工作之余也要注意休息，别熬夜太晚。",
        '凌晨': "你似乎在凌晨提交了不少工作，身体是革命的本钱，请务必注意休息，生活比工作更重要。"
    }
    message = care_messages.get(max_slot, "祝你拥有美好的一天！")
    return f"\n在所有记录的提交中，您在 [cyan]{max_slot}[/cyan] 的时候提交次数最多。\n[cyan]{message}[/cyan]\n"
