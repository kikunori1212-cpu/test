$ErrorActionPreference = "Stop"

$tools = @(
    @{ Name = "git"; Paths = @() },
    @{ Name = "python"; Paths = @() },
    @{ Name = "pip"; Paths = @() },
    @{ Name = "node"; Paths = @("C:\Program Files\nodejs\node.exe") },
    @{ Name = "npm"; Paths = @("C:\Program Files\nodejs\npm.cmd") },
    @{ Name = "curl"; Paths = @() },
    @{ Name = "winget"; Paths = @() },
    @{ Name = "tshark"; Paths = @("C:\Program Files\Wireshark\tshark.exe") },
    @{ Name = "wireshark"; Paths = @("C:\Program Files\Wireshark\Wireshark.exe") },
    @{ Name = "tor"; Paths = @("$env:USERPROFILE\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe") },
    @{ Name = "openvpn"; Paths = @("C:\Program Files\OpenVPN\bin\openvpn.exe") },
    @{ Name = "7z"; Paths = @("C:\Program Files\7-Zip\7z.exe") },
    @{ Name = "java"; Paths = @("C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot\bin\java.exe") },
    @{ Name = "ghidraRun"; Paths = @("$env:USERPROFILE\bin\ghidraRun.cmd") }
)

Write-Host "CTF environment check"
Write-Host "====================="

foreach ($tool in $tools) {
    $command = $tool.Name
    $found = Get-Command $command -ErrorAction SilentlyContinue
    if ($found) {
        Write-Host ("[OK]      {0} -> {1}" -f $command, $found.Source)
        continue
    }

    $fallback = $tool.Paths | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($fallback) {
        Write-Host ("[OK]      {0} -> {1}" -f $command, $fallback)
    } else {
        Write-Host ("[MISSING] {0}" -f $command)
    }
}

Write-Host ""
Write-Host "Python packages"
Write-Host "---------------"

if (Get-Command python -ErrorAction SilentlyContinue) {
    python -m pip list | Select-String -Pattern "requests|httpx|beautifulsoup4|pycryptodome|cryptography|scapy|z3-solver|pillow|numpy|dnspython"
} else {
    Write-Host "Python is not available."
}
