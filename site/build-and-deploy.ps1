# build-and-deploy.ps1
# Build documentation locally and prepare for GitHub Pages deployment

Write-Host "[BUILD] Building documentation locally..." -ForegroundColor Blue

# Clean previous build
if (Test-Path "site") {
    Remove-Item -Recurse -Force site/
}

# Build the documentation
Write-Host "[BUILD] Building with MkDocs..." -ForegroundColor Yellow
mkdocs build --clean

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Build failed!" -ForegroundColor Red
    exit 1
}

# Create .nojekyll file for GitHub Pages
New-Item -ItemType File -Path "site/.nojekyll" -Force | Out-Null

# Add CNAME if you have a custom domain
# "docs.yourdomain.com" | Out-File -FilePath "site/CNAME" -Encoding ASCII

Write-Host "[SUCCESS] Documentation built successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the site locally: cd site; python -m http.server 8000"
Write-Host "2. If everything looks good, commit and push:"
Write-Host ""
Write-Host "   git add site/" -ForegroundColor Yellow
Write-Host "   git commit -m 'docs: update documentation'" -ForegroundColor Yellow  
Write-Host "   git push origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "3. GitHub Actions will automatically deploy to GitHub Pages"
Write-Host "4. View at: https://sunnova-shakesdlamini.github.io/dbcreds/" -ForegroundColor Green