!include "FileFunc.nsh"
!include "MUI2.nsh"

!define APPNAME "T5DE"
!define IMVU_VERSION $%IMVU_VERSION%
!define T5DE_VERSION $%T5DE_VERSION%
!define APP_VERSION $%APP_VERSION%
!define APP_EXE "IMVUClient.exe"

!ifndef OUTDIR
!define OUTDIR ..
!endif

!define APP_UNINSTALL "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

; General

  Name "${APPNAME}"
  BrandingText "T5DE ${APP_VERSION}"

  OutFile "${OUTDIR}\${APPNAME}-${APP_VERSION}.exe"
  Unicode true

  InstallDir "$LOCALAPPDATA\IMVUClient"
  InstallDirRegKey HKCU "Software\${APPNAME}" ""

  RequestExecutionLevel user

  ShowInstDetails show

; Compiler Flags

  SetCompressor lzma
  SetDateSave off

; Variables

  Var SMDIR

; Interface Settings
  !define MUI_ICON "t5de.ico"
  !define MUI_UNICON "t5de.ico"

  !define MUI_ABORTWARNING
  !define MUI_FINISHPAGE_NOAUTOCLOSE
  !define MUI_UNFINISHPAGE_NOAUTOCLOSE

  !define MUI_FINISHPAGE_SHOWREADME ""
  !define MUI_FINISHPAGE_SHOWREADME_TEXT "Create Desktop Shortcut"
  !define MUI_FINISHPAGE_SHOWREADME_FUNCTION CreateDesktopShortcut

  !define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"

; Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_DIRECTORY

  ;Start Menu Folder Page Configuration
  !define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU" 
  !define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${APPNAME}" 
  !define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
  !define MUI_STARTMENUPAGE_DEFAULTFOLDER "${APPNAME}"

  !insertmacro MUI_PAGE_STARTMENU Application $SMDIR

  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH

  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH

;Languages
 
  !insertmacro MUI_LANGUAGE "English"

; Versioning

  VIProductVersion "${T5DE_VERSION}"
  VIFileVersion "${T5DE_VERSION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${APP_VERSION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "${APPNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APPNAME}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${APP_VERSION}"
  VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "Application Installer"

; Sections

Section "${APPNAME}" SecInstall
  SectionIn RO

  SetOutPath "$INSTDIR"

  File /nonfatal /r "${OUTDIR}\IMVUClient\*"

  WriteUninstaller "$INSTDIR\${APPNAME} Uninstall.exe"

  ${GetSize} "$INSTDIR" "" $0 $1 $2

  WriteRegStr HKCU "Software\${APPNAME}" "" $INSTDIR

  WriteRegStr HKLM "${APP_UNINSTALL}" "DisplayName" "${APPNAME}"
  WriteRegStr HKLM "${APP_UNINSTALL}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKLM "${APP_UNINSTALL}" "DisplayIcon" "$INSTDIR\${APPNAME} Uninstall.exe"
  WriteRegStr HKLM "${APP_UNINSTALL}" "UninstallString" "$INSTDIR\${APPNAME} Uninstall.exe"
  WriteRegStr HKLM "${APP_UNINSTALL}" "InstallLocation" "$INSTDIR"
  WriteRegDWORD HKLM "${APP_UNINSTALL}" "EstimatedSize" "$0"

  !insertmacro MUI_STARTMENU_WRITE_BEGIN Application

    CreateDirectory "$SMPROGRAMS\$SMDIR"
    CreateShortCut "$SMPROGRAMS\$SMDIR\${APPNAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APPNAME} Uninstall.exe"
    CreateShortCut "$SMPROGRAMS\$SMDIR\Uninstall ${APPNAME}.lnk" "$INSTDIR\${APPNAME} Uninstall.exe" "" "$INSTDIR\${APPNAME} Uninstall.exe"
  
  !insertmacro MUI_STARTMENU_WRITE_END
SectionEnd

Section "Uninstall"
  RMDir /r /REBOOTOK $INSTDIR

  !insertmacro MUI_STARTMENU_GETFOLDER Application $SMDIR

  Delete "$SMPROGRAMS\$SMDIR\${APPNAME}.lnk"
  Delete "$SMPROGRAMS\$SMDIR\Uninstall ${APPNAME}.lnk"
  Delete "$DESKTOP\${APPNAME}.lnk"
  
  RMDIR "$SMPROGRAMS\$SMDIR"

  DeleteRegKey HKCU "Software\${APPNAME}"
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
SectionEnd

Function CreateDesktopShortcut
  CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APPNAME} Uninstall.exe"
FunctionEnd
