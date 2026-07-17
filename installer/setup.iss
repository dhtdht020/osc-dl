; Inno Setup script for the OSCDL Windows installer.
; Compiled by the CI pipeline, which provides MyAppVersion and generates patchnotes.txt.

#define MyAppName "Open Shop Channel Downloader"
#ifndef MyAppVersion
  #define MyAppVersion "0.0.0"
#endif
#define MyAppPublisher "dhtdht020"
#define MyAppURL "https://github.com/dhtdht020/osc-dl"
#define MyAppExeName "oscdl.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppId={{8F2B9C24-ECE3-4ABD-A035-49AED868C9EC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL=https://github.com/dhtdht020/osc-dl/releases
DefaultDirName={autopf}\{#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequiredOverridesAllowed=commandline
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
OutputDir=..\dist\installer
OutputBaseFilename=oscdl-setup
SetupIconFile=wizard.ico
InfoBeforeFile=patchnotes.txt
WizardSmallImageFile=WizModernSmallImage.bmp
WizardImageFile=WizModernImage.bmp
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
MinVersion=6.3.9200

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WizardInfoBefore=Changelog
InfoBeforeLabel=Please read the following changelog before continuing. If you already have OSCDL installed, this installer will update it.

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\dist\oscdl\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[InstallDelete]
; Legacy single-executable name from old versions
Type: filesandordirs; Name: "{app}\xosc_dl.exe"
; Clear bundled libraries of the previous version, so no stale files are left behind when updating
Type: filesandordirs; Name: "{app}\_internal"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Comment: "Open Shop Channel Downloader"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; Comment: "Open Shop Channel Downloader"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
