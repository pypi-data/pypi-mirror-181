import datetime, os, glob
from . import gen_summary

# default directories where the log files are stored.
logdir       = '/home/manleong.chan/public_html/summary'
day_logdir   = '/home/manleong.chan/public_html/summary/day'


def writelog(newentry, logfile):

    """
    write to log files
    
    logfile : the logfile that will be written to
    
    """

    # check if the log file already exists, if yes, then write to the top
    # if not, then create the log file and write to it.
    if os.path.exists(logfile):
    
        with open(logfile, 'r+') as f:
            content = f.read()
            f.seek(0)
            f.write(newentry + content)
           
    else:
        
        with open(logfile, 'w') as f:
            f.write(newentry)
            
    return
    


def gwskynetlog(logentry, logdir = logdir, day_logdir = day_logdir, logfile = 'log.txt'):

    """
    prepare to write to a GWSkyNet log file.
    
    input:
    logentry : the entry that needs to be written to log for GWSkyNet.
               logentry must be a list with the following elements in
               the following order:
               1. the event id
               2. the class score from GWSkyNet for the event
               3. the interpreted FAR based on the class score
               4. the interpreted FNR based on the class score
               5. the date time at which the annotation is made. The data time must be a string with the following format: YYYY-MM-DD HH:MM:SS
               6. the FITS file used to make this annotation. Usually just the name of the FITS file from graceDB
               7. the url to the event on graceDB

    logfolder: the directory where the log is stored.
    logfile : the name format for the log files.
    """
    
    event_id    = logentry[0]
    class_score = logentry[1]
    FAR         = logentry[2]
    FNR         = logentry[3]
    Adate       = logentry[4]
    FITS_type   = logentry[5]
    url         = logentry[6]
    
    yr          = int(Adate[0:4])
    month       = int(Adate[5:7])
    day         = int(Adate[8:10])
    
    newentry    = "{}\t{:.2f}\t{}\t{}\t{}\t{}\t{}\n".format(event_id, class_score, FAR, FNR, Adate, FITS_type, url)
    
    logday      = Adate[0:4] + Adate[5:7] + Adate[8:10]
    
    # independent log file for the day
    sum_dir     = os.path.join(day_logdir, logday)
    i_logfile   = os.path.join(sum_dir, 'log_%s.txt'%(logday))
    
    # check if the summary for the day exists:
    if not os.path.exists(sum_dir):
        os.mkdir(sum_dir)
        sum_page= os.path.join(sum_dir, 'index.html')
        ser_page= os.path.join(sum_dir, 'search.php')
        gen_summary.make_summary_template(yr, month, day, sum_page)
        gen_summary.make_search_table('log_%s.txt'%(logday), ser_page)
        
    # write to independent log file
    writelog(newentry, i_logfile)
    
    # write to the main log file
    writelog(newentry, logfile)
        
    
    
    
        
    
    
