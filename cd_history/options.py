from cd_history.error_msgs import *


class Options:

    def __init__(self, mode=None, max_result_dirs=None, max_scanned_dirs=None, filter=None,
                 cd_history=None, popup=False, debug=False, action=None
                 ):
        self.action = Action(action) if action else None
        self.mode = InterfaceMode(mode) if mode else None
        self.max_result_dirs = max_result_dirs
        self.max_scanned_dirs = max_scanned_dirs
        self.filter = filter
        self.cd_history = cd_history
        self.popup = popup
        self.debug = debug

    def validate(self):
        if self.mode is None:
            raise Exception("mode is required")
        if self.action is None:
            raise Exception("Action is required")
        if self.cd_history is None:
            raise Exception(MISSING_CD_HISTORY_ENV_VAR_MSG)

    def __str__(self):
        return (f"Options(mode={self.mode},action={self.action}, max_result_dirs={self.max_result_dirs}, "
                f"max_scanned_dirs={self.max_scanned_dirs}, filter={self.filter}, "
                f"cd_history={self.cd_history}, "
                f"popup={self.popup}")

    def __eq__(self, other):
        if not isinstance(other, Options):
            return False
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return self.__str__()
