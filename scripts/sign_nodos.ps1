# Check if the argument was passed
if ($args.Count -eq 0) {
    Write-Host "Usage: nodos_sign.ps1 <executable_path>"
    exit 1
}

# Store the directory path
$EXE_PATH = $args[0]

# Password for the certificate (change as necessary)
$PASSWORD = $Env:MEDIAZ_CER_PWD

$PROVIDER = $Env:MEDIAZ_CSP_NAME

$CER_FILE = "$Env:MEDIAZ_CERTIFICATES_DIR/mediaz.cer"

# Execute the signtool command
$signtoolCmd = "signtool.exe sign /tr http://timestamp.sectigo.com /fd sha256 /td sha256 /f '$CER_FILE' /csp '$PROVIDER' /kc '$PASSWORD' '$EXE_PATH'"

Write-Host "[INFO] executing: $signtoolCmd"

# Execute the command and capture the exit code
Invoke-Expression $signtoolCmd
$exitCode = $LASTEXITCODE

# Check the exit code and return appropriate result
if ($exitCode -eq 0 -or $exitCode -eq 2) {
    Write-Host "[INFO] Signing succeeded."
    exit 0
} else {
    Write-Host "[ERROR] Signing failed. Exit code: $exitCode"
    exit 1
}
