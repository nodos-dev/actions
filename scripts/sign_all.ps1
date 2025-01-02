# Check if the directory path is provided as an argument
if ($args.Count -eq 0) {
    Write-Host "[ERROR] Please provide a directory path as an argument." -ForegroundColor Red
    exit 1
}

$DirectoryToSearch = $args[0]

if (-not (Test-Path $DirectoryToSearch)) {
    Write-Host "[ERROR] The specified directory does not exist: $DirectoryToSearch" -ForegroundColor Red
    exit 1
}

# Function to log information
function Log-Info($message) {
    Write-Host "[INFO] $message"
}

# Function to log errors
function Log-Error($message) {
    Write-Host "[ERROR] $message" -ForegroundColor Red
}

# Find all .exe and .dll files in the directory and its subdirectories
$files = Get-ChildItem -Path $DirectoryToSearch -Recurse -Include *.exe, *.dll | Select-Object -ExpandProperty FullName


cd $env:MEDIAZ_SCRIPTS_DIR

if (-not $files) {
    Log-Error "No .exe or .dll files found in the directory $DirectoryToSearch"
    exit 1
}

Log-Info "Signing the following files: $($files -join ', ')"

foreach ($file in $files) {
    Log-Info "Signing $file"

    & .\sign_nodos.ps1 "$file"
}
