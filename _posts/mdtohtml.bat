@echo off
for %%i in (*.md) do (
    echo Converting %%~ni.md to %%~ni.html
    pandoc "%%~ni.md" -o "%%~ni.html"
)
pause

#pandoc -f markdown -t html article.md -o article.html