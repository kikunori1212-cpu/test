$ErrorActionPreference = "Stop"

function Install-WingetPackage {
    param(
        [Parameter(Mandatory = $true)][string]$Id,
        [Parameter(Mandatory = $true)][string]$Name
    )

    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Write-Host "[SKIP] winget is not available. Install manually: $Name"
        return
    }

    Write-Host "[INSTALL] $Name"
    winget install --id $Id --exact --accept-package-agreements --accept-source-agreements
}

Write-Host "Installing CTF tools for Windows"
Write-Host "================================"

Install-WingetPackage -Id "WiresharkFoundation.Wireshark" -Name "Wireshark"
Install-WingetPackage -Id "TorProject.TorBrowser" -Name "Tor Browser"
Install-WingetPackage -Id "OpenVPNTechnologies.OpenVPN" -Name "OpenVPN"
Install-WingetPackage -Id "7zip.7zip" -Name "7-Zip"
Install-WingetPackage -Id "OpenJS.NodeJS.LTS" -Name "Node.js LTS"
Install-WingetPackage -Id "Python.Python.3.12" -Name "Python 3.12"
Install-WingetPackage -Id "Git.Git" -Name "Git"
Install-WingetPackage -Id "EclipseAdoptium.Temurin.21.JDK" -Name "Java JDK 21"

if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "[INSTALL] Python packages from requirements.txt"
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
} else {
    Write-Host "[SKIP] Python packages because python is not available."
}

if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "[INFO] Optional browser automation MCP from article:"
    Write-Host "       npx chrome-mcp@latest"
}

Write-Host ""
Write-Host "Manual recommendations"
Write-Host "----------------------"
Write-Host "- Burp Suite Community: https://portswigger.net/burp/communitydownload"
Write-Host "- CyberChef: https://gchq.github.io/CyberChef/"
Write-Host "- Beeceptor or webhook.site for temporary XSS exfil receivers"
Write-Host "- Ghidra: https://github.com/NationalSecurityAgency/ghidra/releases"
Write-Host "- WSL Ubuntu for pwn tooling such as pwntools, gdb, gef, checksec"
