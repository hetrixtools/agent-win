import os
import time
import sys

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

import resource_monitor as monitor

SERVICE_NAME = "HetrixToolsAgent"
SERVICE_DISPLAY_NAME = "HetrixTools Agent"

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        SID = win32serviceutil.GetServiceCustomOption(SERVICE_NAME, 'sid')
        servicemanager.LogInfoMsg('SID {}'.format(SID))
        while True:
            try:
                data = monitor.gather_data(SID)
            except Exception as e:
                servicemanager.LogErrorMsg('ERROR: {}'.format(e))
                pass
            if win32event.WaitForSingleObject(self.hWaitStop, 100) == win32event.WAIT_OBJECT_0:
                break

def instart ():
    module_path = os.path.splitext(os.path.realpath(__file__))[0]
    class_name = "{}.{}".format(module_path, AppServerSvc.__name__)
    win32serviceutil.InstallService(class_name,
                                    SERVICE_NAME, SERVICE_DISPLAY_NAME,
                                    startType=win32service.SERVICE_AUTO_START,
                                    )
    print('Install OK')
    win32serviceutil.StartService(SERVICE_NAME)

if __name__ == '__main__':
    is_installed = True
    SID = win32serviceutil.GetServiceCustomOption(SERVICE_NAME, 'sid')
    if SID is None:
        # SID is missing, ask for it from user
        prompt_string = """
        ########################################
        Hint: You can paste into this window
        by right clicking the window header
        and selecting 'Edit' > 'Paste'
        ########################################
        Please enter your Server ID:

        """
        SID = raw_input(prompt_string)
        win32serviceutil.SetServiceCustomOption(SERVICE_NAME, 'sid', SID)
        is_installed = False

    if len(sys.argv) == 1:
        if not is_installed:
            instart()
        else:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(AppServerSvc)
            servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
