function Invoke-Make {
    param (
        [string]$Argument
    )
    & "C:\windows\system32\make.bat" $Argument
}


function Register-MakeTabCompletion {
    $functionName = 'Invoke-Make'

    Register-ArgumentCompleter -CommandName $functionName -ParameterName 'Argument' -ScriptBlock {
        param($commandName, $parameterName, $wordToComplete, $commandAst, $fakeBoundParameters)

        $pythonScriptPath = "C:\windows\system32\make_targets.py"
        $pythonExePath = "python"

        $makeTargets = & $pythonExePath $pythonScriptPath $wordToComplete

        return $makeTargets -split "`n" | Where-Object { $_.Trim() -ne "" }
    }

    # Write-Host "Register-ArgumentCompleter executed for '$functionName'"
}

Register-MakeTabCompletion
Set-Alias make Invoke-Make