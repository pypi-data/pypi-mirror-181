import gspread
import gspread.utils
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import time
import traceback
import sys


class GoogleSheetAPIError(Exception):
    """
    Wrap all exceptions raised by `gspread`
    """
    def __init__(self, message):
        self.message = message

class LoopleSheet:
    """
    Initialise a LoopleSheet and try to connect to the Google Sheet.

    Parameters
    ----------
    json_path : str
        The path to the Service account credentials .json file
    spreadsheet_id : str
        The spreadsheet id of the Google Sheet
    runnable : func(LoopleSheet)
        The subroutine executed in a loop. Note the signature of *runnable* !
    catchingExceptionsFromRunnable : bool, optional, default False
        If *True*, the exceptions raised by *runnable* will be caught in the *start* function and won't stop the loop.
        If *False*, *start* will finish and transmit the exception
    verbose : bool, optional, default False
        If *True*, *start* will print some informations
    errorStream : str, optional, default 'stderr'
        The stream to write errors to. Accepted values are : *'google sheet'*, *'stderr'*, *'both'* or *None*
    datetimeFormat : str, optional, default '%d/%m %H:%M:%S'
        The format used for the date and time. See `datetime.strftime()` for more details
    """
    def __init__(self, json_path, spreadsheet_id, runnable, catchingExceptionsFromRunnable=False, verbose=False, errorStream='stderr', datetimeFormat='%d/%m %H:%M:%S'):
        self.json_path = json_path
        self.spreadsheet_id = spreadsheet_id
        self.runnable = runnable
        self.catchingExceptionsFromRunnable = catchingExceptionsFromRunnable
        self.verbose = verbose
        self.errorStream = errorStream
        self.datetimeFormat = datetimeFormat
        self.setGoogleSheetStructure()
        self._msgColLen = -1
        self._dtColLen = -1

        self._STREAM_ERROR_GOOGLE_SHEET = 'google sheet'
        self._STREAM_ERROR_STDERR = 'stderr'
        self._STREAM_ERROR_BOTH = 'both'

        scope =['https://www.googleapis.com/auth/spreadsheets']

        connection = False
        while not connection:
            try:
                credentials = ServiceAccountCredentials.from_json_keyfile_name(self.json_path, scope)
                gc = gspread.authorize(credentials)
                self.logsh = gc.open_by_key(self.spreadsheet_id)
                self.logWorksheet = self.logsh.get_worksheet(self.worksheet)
                connection = True
                
                if self.verbose:
                    print('Success : Got Google Sheet authorization and Google Sheet accessed')
            
            except Exception as e:
                if self.errorStream in [self._STREAM_ERROR_BOTH, self._STREAM_ERROR_STDERR]:
                    dt_string = datetime.now().strftime(self.datetimeFormat)
                    print(f'{dt_string} - GoogleSheetAPIError (acess error): {e}', file=sys.stderr)

                time.sleep(3)

    def setGoogleSheetStructure(self, **kwargs):
        """
        Edit the default behaviour of LoopleSheet regarding the Google Sheet structure.
        
        Parameters
        ----------
        sleepTimeCell : str, optional, default 'B1'
            The cell in which the number of seconds to sleep between 2 executions is written
        lastExecDateTimeCell : str, optional, default 'A4'
            The cell in which the date and time of the last performed execution are written
        messageColumn : str, optional, default 'C'
            The column in which the messages posted are written
        msgDateColumn : str, optional, default 'D'
            The column in which the date and time of the messages posted are written
        worksheet : int, optional, default 0
            The worksheet LoopleSheet works on (starts at 0)
        """
        if 'sleepTimeCell' in kwargs.keys(): self.sleepTimeCell = kwargs['sleepTimeCell']
        if 'lastExecDateTimeCell' in kwargs.keys(): self.lastExecDateTimeCell = kwargs['lastExecDateTimeCell']
        if 'messageColumn' in kwargs.keys(): self.messageColumn = kwargs['messageColumn']
        if 'msgDateColumn' in kwargs.keys(): self.msgDateColumn = kwargs['msgDateColumn']
        if 'worksheet' in kwargs.keys(): self.worksheet = kwargs['worksheet']

        if not hasattr(self, 'sleepTimeCell'): self.sleepTimeCell = 'B1'
        if not hasattr(self, 'lastExecDateTimeCell'): self.lastExecDateTimeCell = 'A4'
        if not hasattr(self, 'messageColumn'): self.messageColumn = 'C'
        if not hasattr(self, 'msgDateColumn'): self.msgDateColumn = 'D'
        if not hasattr(self, 'worksheet'): self.worksheet = 0
        elif 'worksheet' in kwargs.keys(): self.logWorksheet = self.logsh.get_worksheet(self.worksheet)


    def start(self):
        """
        Launch the main loop.
        In an infinite loop :

        - the date and time are written in the right cell (*lastExecDateTimeCell*) of the Google Sheet
        
        - *runnable* is called with as parameter the current instance of LoopleSheet (in order to be able to post some messages)
        
        - the script sleeps for the number of seconds written in the *sleepTimeCell* of the Google Sheet


        The exceptions raised by *runnable* are caught or not according to *catchingExceptionsFromRunnable*.
        The exceptions from the Google Sheet API are caught and won't break the loop.
        """
        while True:
            try:
                dt_string = datetime.now().strftime(self.datetimeFormat)
                self.logWorksheet.update(self.lastExecDateTimeCell, dt_string)
                sleepTime = int(self.logWorksheet.acell(self.sleepTimeCell).value)

                if self.verbose:
                    print('              ----------------------                   ')
                    print(f'{dt_string} - New execution of the subroutine')   


                self.runnable(self)
            
            except GoogleSheetAPIError as e:
                if self.errorStream in [self._STREAM_ERROR_STDERR, self._STREAM_ERROR_BOTH]:
                    print(f'{dt_string} - GoogleSheetAPIError : {e}', file=sys.stderr)
            except Exception as e:
                if self.catchingExceptionsFromRunnable:
                    if self.errorStream in [self._STREAM_ERROR_STDERR, self._STREAM_ERROR_BOTH]:
                        print(f'{dt_string} - Error runnable - {traceback.format_exc()}', file=sys.stderr)
                    if self.errorStream in [self._STREAM_ERROR_GOOGLE_SHEET, self._STREAM_ERROR_BOTH]:
                        try:
                            self.post(f'{dt_string} - Error runnable - {traceback.format_exc()}')
                        except:
                            pass
                else:
                    raise

            time.sleep(sleepTime)


    def post(self, msg, processColumns=False):
        """
        Post a message in the Google Sheet with the date and time associated.
        The columns used are *messageColumn* for the message and *msgDateColumn* for the date and time.
        The messages and date and time are appended at the bottom of the columns (the maximum of the two so that message and date and time are in the same row).

        Parameters
        ----------
        msg : str
            The message to post
        processColumns : bool, optional, default False
            If *False*, LoopleSheet assumes that *msgColumn* and *msgDateColumn* are not modified by a third party and doesn't process these columns.
            If *True*, LoopleSheet fetches *msgColumn* and *msgDateColumn*, thus increasing memory and gspread api usage with the number of posts.

        Note
        ----
        Can raise in a GoogleSheetAPIError.
        """
        try:
            dt_string = datetime.now().strftime(self.datetimeFormat)

            msgColNb = gspread.utils.a1_to_rowcol(self.messageColumn + '1')[1]
            dtColNb = gspread.utils.a1_to_rowcol(self.msgDateColumn + '1')[1]

            if processColumns or self._msgColLen < 0 or self._dtColLen < 0:
                self._msgColLen = len(self.logWorksheet.col_values(msgColNb))
                self._dtColLen = len(self.logWorksheet.col_values(dtColNb))
            
            rowNb = max(self._msgColLen, self._dtColLen) + 1

            self.logWorksheet.update_cell(rowNb, msgColNb, msg)
            self.logWorksheet.update_cell(rowNb, dtColNb, dt_string)

            self._msgColLen = rowNb
            self._dtColLen = rowNb

            if self.verbose:
                print(f'{dt_string} - Success : "{msg}" posted')

        except Exception as e:
            raise GoogleSheetAPIError(f'{dt_string} - GoogleSheetAPIError') from e