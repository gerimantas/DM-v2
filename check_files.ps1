# PowerShell script to check if files exist and contain content

# Define the expected files in the project
$expectedFiles = @(
    "main.py",
    "config/__init__.py",
    "config/settings.py",
    "src/__init__.py",
    "src/api_client.py",
    "src/assistant.py",
    "src/code_analyzer.py",
    "src/utils.py",
    "ui/__init__.py",
    "ui/interface.py",
    "examples/__init__.py",
    "examples/example_usage.py",
    "templates/__init__.py", 
    "templates/file_operations.py",
    "templates/data_processing.py",
    "templates/web_interaction.py",
    "tests/__init__.py",
    "tests/test_api_client.py",
    "tests/test_assistant.py",
    ".env",
    ".gitignore",
    "README.md",
    "requirements.txt"
)

# Create a table to store the results
$results = @()

# Check each file
foreach ($file in $expectedFiles) {
    $filePath = Join-Path -Path (Get-Location) -ChildPath $file
    $fileExists = Test-Path -Path $filePath
    $hasContent = $false
    $fileSize = 0
    
    if ($fileExists) {
        $fileInfo = Get-Item -Path $filePath
        $fileSize = $fileInfo.Length
        $hasContent = $fileSize -gt 0
    }
    
    # Add result to the table
    $results += [PSCustomObject]@{
        File = $file
        Exists = $fileExists
        HasContent = $hasContent
        SizeBytes = $fileSize
    }
}

# Display results in a table
$results | Format-Table -AutoSize

# Summary
$totalFiles = $expectedFiles.Count
$existingFiles = ($results | Where-Object { $_.Exists -eq $true }).Count
$filesWithContent = ($results | Where-Object { $_.HasContent -eq $true }).Count

Write-Host "Summary:"
Write-Host "- Expected files: $totalFiles"
Write-Host "- Existing files: $existingFiles"
Write-Host "- Files with content: $filesWithContent"

# List missing files
$missingFiles = $results | Where-Object { $_.Exists -eq $false }
if ($missingFiles.Count -gt 0) {
    Write-Host "`nMissing files:"
    foreach ($file in $missingFiles) {
        Write-Host "- $($file.File)"
    }
}

# List empty files
$emptyFiles = $results | Where-Object { $_.Exists -eq $true -and $_.HasContent -eq $false }
if ($emptyFiles.Count -gt 0) {
    Write-Host "`nEmpty files (exist but have no content):"
    foreach ($file in $emptyFiles) {
        Write-Host "- $($file.File)"
    }
}