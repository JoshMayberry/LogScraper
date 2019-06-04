#define settingsDir "carbon_code"

[Setup]
AppId = "1514dcca-c85e-4a06-a95a-a3f356659f95"
AppName = {#name}
AppVersion = {#version}
AppPublisher = "Decatur Mold"
AppPublisherURL = "https://www.decaturmold.com/"
;LicenseFile = "resources\terms.txt"

SetupIconFile = "resources\setup.ico"
DefaultDirName = {pf}\{#defaultDir}
DefaultGroupName = {#startMenuDir}

[Types]
Name: "full"; Description: "Full installation"
Name: "custom"; Description: "Custom installation"; Flags: iscustom

[Components]
Name: "main"; Description: "Main Files"; Types: full custom; Flags: fixed
Name: "source"; Description: "Source Code"; Types: custom

[Files]
Source: "build\*"; DestDir: "{app}"; Components: main; Flags: recursesubdirs
Source: "resources\*"; DestDir: "{app}\resources"; Components: main; Flags: recursesubdirs

Source: "*.py"; DestDir: "{app}\code"; Components: source
Source: "*.iss"; DestDir: "{app}\code"; Components: source
Source: "*.ini"; DestDir: "{app}\code"; Components: source
Source: "docs\*"; DestDir: "{app}\docs"; Components: source; Flags: recursesubdirs

[Tasks]
Name: startmenu; Description: "Create Start Menu icon"; GroupDescription: "{cm:AdditionalIcons}"; Components: main
Name: desktopicon; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Components: main
Name: taskbar; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: "{cm:AdditionalIcons}"; Components: main; Flags: unchecked

[Icons]
Name: "{group}\{#name}"; Filename: "{app}\{#exeName}"; IconFilename: "{app}\resources\scraper.ico"; Tasks: startmenu
Name: "{userdesktop}\{#name}"; Filename: "{app}\{#exeName}"; IconFilename: "{app}\resources\scraper.ico"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\{#name}"; Filename: "{app}\{#exeName}"; IconFilename: "{app}\resources\scraper.ico"; Tasks: taskbar


[UninstallDelete]
Type: filesandordirs; Name: "{userappdata}\LogScraper"; Check: UserSettingsExist()

; [Run]
; Filename: "{#pythonPath}"; WorkingDir: "{app}"; Parameters: " ""{app}\preinstall.py"" "; StatusMsg: "Installing Scanner..."; Components: scanner


[Code]
function UserSettingsExist(): Boolean;
	// Modified code from http://www.jrsoftware.org/ishelp/index.php?topic=scriptcheck

	var
		settingsPath: String;

	begin
		Result := False;
		settingsPath := ExpandConstant('{userappdata}\{#settingsDir}');

		if DirExists(settingsPath) then
			if MsgBox('Remove existing user settings?', mbConfirmation, MB_YESNO) = IDYES then
				Result := True;
	end;


function PrepareToInstall(var NeedsRestart: Boolean): String;
	// Modified code from TLama on https://stackoverflow.com/questions/23631557/how-to-set-statusmsg-from-preparetoinstall-event-function/23633694#23633694

	var
		settingsPath: String;

	begin
		// if IsComponentSelected('scanner') then
		// begin
		// 	if RegKeyExists(HKLM64, 'HKLM\SYSTEM\DriverDatabase\DriverPackages\usb_cdc_com*') then
		// 	begin
		// 		// Run scanner installer
		// 	end;
		// end;

		//Modified Code from TLama on https://stackoverflow.com/questions/12644913/inno-setup-uninstall-registry-removal-option/12645836#12645836
		settingsPath := ExpandConstant('{userappdata}\{#settingsDir}');
		if DirExists(settingsPath) then
			begin
				if MsgBox('Remove existing user settings?', mbConfirmation, MB_YESNO) = IDYES then
					DelTree(settingsPath, True, True, True);
			end;

	end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);

	var
		settingsPath: String;

	begin
		if CurUninstallStep = usUninstall then
		begin
			settingsPath := ExpandConstant('{userappdata}\{#settingsDir}');
			if DirExists(settingsPath) then
				if MsgBox('Remove existing user settings?', mbConfirmation, MB_YESNO) = IDYES then
					DelTree(settingsPath, True, True, True);
		end;
	end;