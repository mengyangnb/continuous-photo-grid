# 连幅照片九宫格

用实拍照片、透明贴纸和可选题字制作跨格连续的朋友圈九宫格。先在一张方形母版上排好全幅，再裁出九张连续的方图。

将这个仓库下载到 Codex 的技能目录 `~/.codex/skills/continuous-photo-grid`，然后用 `$continuous-photo-grid` 调用。例如：

> 用 $continuous-photo-grid 把这个文件夹里的照片做成九宫格，让同一张夜景横跨底排。

已有方形母版时，也可单独运行导出脚本。母版边长须可被 3 整除。

```bash
python3 -m pip install Pillow
python3 scripts/export_grid.py master.png outputs --name '秋日连幅'
```

脚本输出无缝整图、带缝预览和包含九张单图的 ZIP。发朋友圈时按 01 到 09 的顺序选图。
