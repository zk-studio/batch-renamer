; ═══════════════════════════════════════════════════
;  批量文件重命名工具 — Inno Setup 安装脚本
;  支持：中文界面 · 静默安装 · 自动关闭旧进程 · 升级覆盖
;
;  静默安装命令行:
;    BatchRenamer_Setup_1.0.0.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /CLOSEAPPLICATIONS
; ═══════════════════════════════════════════════════

#define MyAppName "批量文件重命名工具"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PySide6 Demo"
#define MyAppExeName "BatchRenamer.exe"
#define MyAppURL "https://github.com/example/batch-renamer"
#define MyAppMutex "BatchRenamer_SingleInstance_Mutex"

[Setup]
; 安装包基本信息
AppId={{B8F3A2D1-9E7C-4F6A-B5D8-3C2E1A0F9B7D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; 安装路径
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; 输出
OutputDir=installer_output
OutputBaseFilename=BatchRenamer_Setup_{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes

; 外观
WizardStyle=modern
DisableWelcomePage=no

; 权限 — lowest 允许非管理员安装
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 升级与静默安装支持
AllowNoIcons=yes
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesInstallIn64BitMode=x64compatible

; 单实例互斥锁 — 防止安装时旧版本还在运行
AppMutex={#MyAppMutex}

; 自动关闭正在运行的应用
CloseApplications=force
CloseApplicationsFilter=*.exe
RestartApplications=no

; 升级模式 — 覆盖安装时不弹确认
UsePreviousAppDir=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "附加图标:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "创建快速启动栏图标"; GroupDescription: "附加图标:"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 复制 PyInstaller 打包的所有文件（升级时覆盖）
Source: "dist\BatchRenamer\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\BatchRenamer\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; 安装完成后启动（静默模式下也会启动）
Filename: "{app}\{#MyAppExeName}"; Description: "立即运行 {#MyAppName}"; Flags: nowait postinstall skipifsilent shellexec

; 静默模式下安装完成后自动启动应用
Filename: "{app}\{#MyAppExeName}"; Flags: nowait runhidden shellexec; Check: IsSilentInstall

[Code]
// 判断是否为静默安装模式
function IsSilentInstall: Boolean;
begin
  Result := WizardSilent;
end;
