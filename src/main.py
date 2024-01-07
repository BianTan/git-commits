# -*- coding: utf-8 -*-
import re
import os
import sys
import time
from datetime import datetime, timedelta
from rich.progress import track
# 自定义方法
import utils

# 搜索项目文件
def search_project(target_directory, authors = []):
    # 初始化统计数据
    data = {
      'total_count': 0,
      'max_count': 0,
      'min_count': None,
      'max_project': '',
      'min_project': '',
      'time_slots': { '上午': 0, '下午': 0, '晚上': 0, '凌晨': 0 },
      'project_commit': []
    }

    # 获取所有子目录
    dirs = [d for d in os.listdir(target_directory) if os.path.isdir(os.path.join(target_directory, d))]
    total_dirs = len(dirs)
    git_total = 0

    # 遍历所有子目录
    for i in track(range(total_dirs), description="搜索项目中..."): 
        project_name = dirs[i]
        dir_path = os.path.join(target_directory, project_name)
        try:
            commits = utils.get_commits(dir_path, authors, since_date, until_date)
            count = len(commits)

            count_text = f"[red bold]{count}[/red bold]"
            if count != 0:
                count_text = re.sub("red", "blue", count_text)
              
            data['project_commit'].append(f"项目 [green]{project_name}[/green] 共 {count_text} 次提交")
            # 更新时间段统计
            for commit in commits:
                slot = utils.get_time_slot(commit.committed_datetime.hour)
                data['time_slots'][slot] += 1

            # 更新最多和最少提交记录（忽略0次提交的项目）
            if count > data['max_count']:
                data['max_count'] = count
                data['max_project'] = project_name

            if (data['min_count'] is None or count < data['min_count']) and count > 0:
                data['min_count'] = count
                data['min_project'] = project_name

            data['total_count'] += count
            git_total += 1

        except Exception as e:
            ''

    utils.slow_print(f"项目搜索完毕, 共搜索 [green]{total_dirs}[/green] 个文件夹。git 项目共 [blue]{git_total}[/blue] 个")
    return data

# 主函数
def main(target_directory, since_date=None, until_date=None):
    if not os.path.isdir(target_directory):
        print(f"提供的目录不存在: {target_directory}")
        sys.exit(1)

    # 设置日期
    since_date = since_date or (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    until_date = until_date or datetime.now().strftime('%Y-%m-%d')

    # 输入作者名称
    authors = utils.input_authors()
    state = utils.get_yes_or_no("是否展示所有项目提交情况")
    
    # 搜素项目
    project_data = search_project(target_directory, authors)
  
    if state == True:
      print()
      for info in project_data['project_commit']:
        utils.slow_print(info, 0)
        time.sleep(0.1)

    utils.slow_print(f"\n所有项目的提交次数总和为: [red]{project_data['total_count']}[/red] 次")

    # 输出提交次数最多和最少的项目（忽略0次提交的项目）
    if project_data['max_project']:
        text = f"提交次数最多的项目是：[green]{project_data['max_project']}[/green]，共有 [red]{project_data['max_count']}[/red] 次提交。"
        utils.slow_print(text)
    if project_data['min_project']:
        text = f"有提交记录且提交次数最少的项目是：[green]{project_data['min_project']}[/green]，共有 [red]{project_data['min_count']}[/red] 次提交。"
        utils.slow_print(text)

    # 输出每个时间段的提交次数
    utils.slow_print("\n提交次数按时间段统计：")
    for slot, count in project_data['time_slots'].items():
        summary = f"{slot}: [cyan]{count}[/cyan] 次"
        utils.slow_print(summary)

    # 找出提交次数最多的时间段
    utils.slow_print(utils.get_care_message(project_data['time_slots']))
    

if __name__ == "__main__":
    # 解析命令行参数
    if len(sys.argv) < 2:
        print("请提供所有项目的父目录作为参数。")
        sys.exit(1)

    target_directory = sys.argv[1]
    since_date = sys.argv[2] if len(sys.argv) > 2 else None
    until_date = sys.argv[3] if len(sys.argv) > 3 else None

    main(target_directory, since_date, until_date)
