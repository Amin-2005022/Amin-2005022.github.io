$date = Get-Date -Format "MMM d"
git add -A
git commit -m "$($date.ToLower())"
git push origin main
