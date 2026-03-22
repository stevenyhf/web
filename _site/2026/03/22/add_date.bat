@echo off
setlocal enabledelayedexpansion

:: 获取当前日期，格式化为 YYYY-MM-DD
for /f "tokens=1-3 delims=/-" %%a in ('echo %date%') do (
    set year=%%a
    set month=%%b
    set day=%%c
)
:: 调整月份和日为两位数（如果系统返回的已经是两位数则无需处理）
if %month% lss 10 set month=0%month%
if %day% lss 10 set day=0%day%
set prefix=%year%-%month%-%day%

:: 遍历当前目录下的所有文件
for %%f in (*) do (
    if not "%%~ff"=="%~f0" (   :: 排除批处理文件自身
        :: 检查文件是否已经带有当天日期前缀
        echo %%f | findstr /b /c:"%prefix%-" >nul
        if errorlevel 1 (
            ren "%%f" "%prefix%-%%f"
            echo 已重命名: %%f -> %prefix%-%%f
        ) else (
            echo 跳过: %%f (已带有前缀)
        )
    )
)

echo 完成！