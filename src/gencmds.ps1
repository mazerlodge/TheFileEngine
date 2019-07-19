Param(
[String]$startDate=$(Read-Host "Start Date"),
[String]$endDate=$(Read-Host "End Date"),
[String]$hostName=$(Read-Host "Host Name")
)

# Generate Dir and Py Commands 
function genCmds()
{

	[String]$startYear = $startDate.Substring(0,4)
	[String]$startMonth = $startDate.Substring(4,2)
	[String]$startDay = $startDate.Substring(6,2)
	
	[String]$endYear = $endDate.Substring(0,4)
	[String]$endMonth = $endDate.Substring(4,2)
	[String]$endDay = $endDate.Substring(6,2)
	
	[String]$dirCmd = "dir -recurse | ? {`$_.lastwritetime -gt '$($startMonth)/$($startDay)/$($startYear)' -AND `$_.lastwritetime -lt '$($endMonth)/$($endDay)/$($endYear) 23:59:59'} | out-file -encoding UTF8 c:\temp\modlist$($hostName)$($startDate)_$($endDate).txt"
		
	[String]$pyCmd = "python tfe.py -action genscript -infile c:\temp\modlist$($hostName)$($startDate)_$($endDate).txt -targetpath c:\temp\Bup$($hostName)$($startDate)_$($endDate) > c:\temp\scriptbup.ps1"	
		
	Write-Host("$dirCmd")
	Write-Host("$pyCmd")
		
	Write-Host("Host Name $($hostName)")
	Write-Host("Start Date $($startDate)")
	Write-Host("End Date $($endDate)")
	
    return 1;
}

genCmds
Write-Host("Commands Generated") 
Write-Host("+++++++++++++++")
