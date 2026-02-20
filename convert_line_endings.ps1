# 杞崲鎵€鏈夋枃鏈枃浠朵负CRLF琛岀粨鏉熺
$rootPath = "c:\BM_Program\shElter-v3"

# 鎺掗櫎鐨勪簩杩涘埗鏂囦欢鎵╁睍鍚?$binaryExtensions = @(
    "png", "jpg", "jpeg", "gif", "bmp", "ico", "svg",
    "mp3", "wav", "mp4", "avi", "mov", "pdf",
    "zip", "rar", "7z", "exe", "dll", "so", "a", "lib", "obj", "class",
    "db", "sqlite"
)

# 閫掑綊鑾峰彇鎵€鏈夋枃浠?$allFiles = Get-ChildItem -Path $rootPath -Recurse -File

# 杩囨护鎺変簩杩涘埗鏂囦欢
$textFiles = $allFiles | Where-Object {
    $ext = $_.Extension.TrimStart('.').ToLower()
    -not $binaryExtensions.Contains($ext)
}

Write-Output "Found $($textFiles.Count) text files to convert"

# 杞崲姣忎釜鏂囨湰鏂囦欢涓篊RLF
$convertedCount = 0
foreach ($file in $textFiles) {
    try {
        # 璇诲彇鏂囦欢鍐呭
        $content = Get-Content -Raw -Path $file.FullName
        
        # 妫€鏌ュ綋鍓嶈缁撴潫绗?        if ($content -match "\r\n") {
            # 宸茬粡鏄疌RLF锛岃烦杩?            continue
        }
        
        # 杞崲涓篊RLF
        $content = $content -replace "\r?\n", "\r\n"
        
        # 鍐欏洖鏂囦欢
        Set-Content -NoNewline -Path $file.FullName -Value $content -Encoding UTF8
        $convertedCount++
        
        # 姣忚浆鎹?00涓枃浠舵樉绀鸿繘搴?        if ($convertedCount % 100 -eq 0) {
            Write-Output "Converted $convertedCount files..."
        }
    }
    catch {
        Write-Output "Error converting $($file.FullName): $_"
    }
}

Write-Output "Conversion complete. Converted $convertedCount files to CRLF"