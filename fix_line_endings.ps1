# 淇琛岀粨鏉熺鑴氭湰
# 灏嗘墍鏈夋枃鏈枃浠惰浆鎹负CRLF琛岀粨鏉熺

# 瀹氫箟椤圭洰鏍圭洰褰?$projectRoot = "c:\BM_Program\shElter-v3"

# 瀹氫箟瑕佽烦杩囩殑鐩綍
$skipDirs = @(".git", "node_modules", "venv", ".venv", "__pycache__", "*.egg-info", "dist", "build", "test-results")

# 瀹氫箟瑕佸鐞嗙殑鏂囨湰鏂囦欢鎵╁睍鍚?$textExtensions = @(".py", ".vue", ".ts", ".tsx", ".js", ".jsx", ".html", ".css", ".scss", ".less", ".json", ".xml", ".yml", ".yaml", ".md", ".rst", ".txt", ".ini", ".conf", ".cfg", ".env", ".sh", ".bat", ".cmd", ".ps1")

# 瀹氫箟浜岃繘鍒舵枃浠舵墿灞曞悕锛堣烦杩囷級
$binaryExtensions = @(".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".mp3", ".wav", ".mp4", ".avi", ".mov", ".pdf", ".zip", ".rar", ".7z", ".exe", ".dll", ".so", ".a", ".lib", ".obj", ".class", ".db", ".sqlite")

Write-Host "寮€濮嬩慨澶嶈缁撴潫绗?.."
Write-Host "椤圭洰鏍圭洰褰? $projectRoot"
Write-Host "璺宠繃鐩綍: $($skipDirs -join ", ")"
Write-Host "澶勭悊鏂囦欢绫诲瀷: $($textExtensions -join ", ")"
Write-Host "璺宠繃浜岃繘鍒舵枃浠? $($binaryExtensions -join ", ")"
Write-Host "=" * 50

# 鑾峰彇鎵€鏈夎澶勭悊鐨勬枃浠?$files = Get-ChildItem -Path $projectRoot -Recurse -File | Where-Object {
    # 璺宠繃鎸囧畾鐩綍
    $skip = $false
    foreach ($dir in $skipDirs) {
        if ($_.DirectoryName -like "*$dir*") {
            $skip = $true
            break
        }
    }
    if ($skip) { return $false }
    
    # 鍙鐞嗘枃鏈枃浠讹紝璺宠繃浜岃繘鍒舵枃浠?    $ext = $_.Extension.ToLower()
    if ($binaryExtensions -contains $ext) { return $false }
    return $textExtensions -contains $ext -or $ext -eq "";
}
Write-Host "鎵惧埌 $($files.Count) 涓澶勭悊鐨勬枃浠?
Write-Host "=" * 50

$processedCount = 0
$errorCount = 0

# 澶勭悊姣忎釜鏂囦欢
foreach ($file in $files) {
    try {
        # 璇诲彇鏂囦欢鍐呭
        $content = Get-Content -Path $file.FullName -Raw
        
        # 杞崲琛岀粨鏉熺锛圠F -> CRLF锛?        $newContent = $content -replace "`n", "`r`n"
        
        # 鍙湪鍐呭鏈夊彉鍖栨椂鍐欏叆鏂囦欢
        if ($content -ne $newContent) {
            Set-Content -Path $file.FullName -Value $newContent -NoNewline -Encoding UTF8
            Write-Host "宸蹭慨澶? $($file.FullName)"
            $processedCount++
        }
    } catch {
        Write-Host "閿欒澶勭悊鏂囦欢: $($file.FullName)"
        Write-Host "閿欒淇℃伅: $($_.Exception.Message)"
        $errorCount++
    }
}

Write-Host "=" * 50
Write-Host "淇瀹屾垚!"
Write-Host "澶勭悊鏂囦欢鏁? $($files.Count)"
Write-Host "鎴愬姛淇: $processedCount"
Write-Host "澶勭悊閿欒: $errorCount"
Write-Host "=" * 50