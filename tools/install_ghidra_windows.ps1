$ErrorActionPreference = "Stop"

$version = "12.0.4"
$releaseDate = "20260303"
$tag = "Ghidra_12.0.4_build"
$zipName = "ghidra_$($version)_PUBLIC_$($releaseDate).zip"
$downloadUrl = "https://github.com/NationalSecurityAgency/ghidra/releases/download/$tag/$zipName"

$toolsDir = Join-Path $env:USERPROFILE "Tools"
$binDir = Join-Path $env:USERPROFILE "bin"
$zipPath = Join-Path $toolsDir $zipName
$installDir = Join-Path $toolsDir "ghidra_$($version)_PUBLIC"
$ghidraRun = Join-Path $installDir "ghidraRun.bat"
$installMarker = Join-Path $installDir "Ghidra\application.properties"
$shimPath = Join-Path $binDir "ghidraRun.cmd"

New-Item -ItemType Directory -Force -Path $toolsDir | Out-Null
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

if (-not ((Test-Path $ghidraRun) -and (Test-Path $installMarker))) {
    if (-not (Test-Path $zipPath)) {
        Write-Host "[DOWNLOAD] $downloadUrl"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $zipPath
    }

    Write-Host "[EXTRACT] $zipPath"
    if (Test-Path $installDir) {
        Remove-Item -LiteralPath $installDir -Recurse -Force
    }

    $sevenZip = Get-Command 7z -ErrorAction SilentlyContinue
    if ($sevenZip) {
        & $sevenZip.Source x $zipPath "-o$toolsDir" -y | Out-Host
    } else {
        Expand-Archive -Path $zipPath -DestinationPath $toolsDir -Force
    }
}

if (-not (Test-Path $ghidraRun)) {
    throw "Ghidra was extracted, but ghidraRun.bat was not found at: $ghidraRun"
}

if (-not (Test-Path $installMarker)) {
    throw "Ghidra was extracted, but application.properties was not found at: $installMarker"
}

$shim = @(
    "@echo off"
    "`"$ghidraRun`" %*"
)
$shim | Set-Content -Path $shimPath -Encoding ASCII

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$pathParts = @()
if ($userPath) {
    $pathParts = $userPath -split ";"
}

if ($pathParts -notcontains $binDir) {
    $newPath = if ($userPath) { "$userPath;$binDir" } else { $binDir }
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "[PATH] Added $binDir to the user PATH. Open a new terminal to inherit it."
}

$env:Path = "$env:Path;$binDir"

Write-Host "[OK] ghidraRun -> $shimPath"
Write-Host "Run ghidraRun from a new terminal to launch Ghidra."
