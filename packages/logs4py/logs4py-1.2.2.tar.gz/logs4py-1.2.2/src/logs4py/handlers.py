# Copyright 2001-2017 by Vinay Sajip. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of Vinay Sajip
# not be used in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# VINAY SAJIP DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# VINAY SAJIP BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""
Logging package for Python. Based on PEP 282 and comments thereto in
comp.lang.python.

Copyright (C) 2001-2017 Vinay Sajip. All Rights Reserved.

To use, simply 'import logging' and log away!
"""

import logging ,socket ,os ,pickle ,struct ,time ,re #line:1
from stat import ST_DEV ,ST_INO ,ST_MTIME #line:2
import queue #line:3
import threading #line:4
import copy #line:5
DEFAULT_TCP_LOGGING_PORT =9020 #line:11
DEFAULT_UDP_LOGGING_PORT =9021 #line:12
DEFAULT_HTTP_LOGGING_PORT =9022 #line:13
DEFAULT_SOAP_LOGGING_PORT =9023 #line:14
SYSLOG_UDP_PORT =514 #line:15
SYSLOG_TCP_PORT =514 #line:16
_OO000OOOOO0O0OOOO =24 *60 *60 #line:18
class BaseRotatingHandler (logging .FileHandler ):#line:20
    ""#line:25
    def __init__ (O0OOOO0OOOOOOOO0O ,O0OOOOOO0O000OOO0 ,O0OOOO0O00OO0OO0O ,encoding =None ,delay =False ):#line:26
        ""#line:29
        logging .FileHandler .__init__ (O0OOOO0OOOOOOOO0O ,O0OOOOOO0O000OOO0 ,O0OOOO0O00OO0OO0O ,encoding ,delay )#line:30
        O0OOOO0OOOOOOOO0O .mode =O0OOOO0O00OO0OO0O #line:31
        O0OOOO0OOOOOOOO0O .encoding =encoding #line:32
        O0OOOO0OOOOOOOO0O .namer =None #line:33
        O0OOOO0OOOOOOOO0O .rotator =None #line:34
    def emit (O0O0OOO0OO00OO0O0 ,OO0OO0OO000O00OO0 ):#line:36
        ""#line:42
        try :#line:43
            if O0O0OOO0OO00OO0O0 .shouldRollover (OO0OO0OO000O00OO0 ):#line:44
                O0O0OOO0OO00OO0O0 .doRollover ()#line:45
            logging .FileHandler .emit (O0O0OOO0OO00OO0O0 ,OO0OO0OO000O00OO0 )#line:46
        except Exception :#line:47
            O0O0OOO0OO00OO0O0 .handleError (OO0OO0OO000O00OO0 )#line:48
    def rotation_filename (O0OO0OOO0OOO0O0OO ,OOO0O00O0O00O00O0 ):#line:50
        ""#line:62
        if not callable (O0OO0OOO0OOO0O0OO .namer ):#line:63
            OOOO0O000O00000O0 =OOO0O00O0O00O00O0 #line:64
        else :#line:65
            OOOO0O000O00000O0 =O0OO0OOO0OOO0O0OO .namer (OOO0O00O0O00O00O0 )#line:66
        return OOOO0O000O00000O0 #line:67
    def rotate (O000OO0OO00OOOO0O ,O00OOO0OOO0O0000O ,O000OO0O0O0OO00OO ):#line:69
        ""#line:82
        if not callable (O000OO0OO00OOOO0O .rotator ):#line:83
            if os .path .exists (O00OOO0OOO0O0000O ):#line:85
                os .rename (O00OOO0OOO0O0000O ,O000OO0O0O0OO00OO )#line:86
        else :#line:87
            O000OO0OO00OOOO0O .rotator (O00OOO0OOO0O0000O ,O000OO0O0O0OO00OO )#line:88
class RotatingFileHandler (BaseRotatingHandler ):#line:90
    ""#line:94
    def __init__ (O0OO0OO00000OO00O ,OOOO0OO0000OOO000 ,mode ='a',maxBytes =0 ,backupCount =0 ,encoding =None ,delay =False ):#line:95
        ""#line:115
        if maxBytes >0 :#line:121
            mode ='a'#line:122
        BaseRotatingHandler .__init__ (O0OO0OO00000OO00O ,OOOO0OO0000OOO000 ,mode ,encoding ,delay )#line:123
        O0OO0OO00000OO00O .maxBytes =maxBytes #line:124
        O0OO0OO00000OO00O .backupCount =backupCount #line:125
    def doRollover (OO00OO00000O00O0O ):#line:127
        ""#line:130
        if OO00OO00000O00O0O .stream :#line:131
            OO00OO00000O00O0O .stream .close ()#line:132
            OO00OO00000O00O0O .stream =None #line:133
        if OO00OO00000O00O0O .backupCount >0 :#line:134
            for O0OOO0000OOOOOO0O in range (OO00OO00000O00O0O .backupCount -1 ,0 ,-1 ):#line:135
                OOOO0O0O00O000O0O =OO00OO00000O00O0O .rotation_filename ("%s.%d"%(OO00OO00000O00O0O .baseFilename ,O0OOO0000OOOOOO0O ))#line:136
                O0O00OOOOOOOO0O0O =OO00OO00000O00O0O .rotation_filename ("%s.%d"%(OO00OO00000O00O0O .baseFilename ,O0OOO0000OOOOOO0O +1 ))#line:138
                if os .path .exists (OOOO0O0O00O000O0O ):#line:139
                    if os .path .exists (O0O00OOOOOOOO0O0O ):#line:140
                        os .remove (O0O00OOOOOOOO0O0O )#line:141
                    os .rename (OOOO0O0O00O000O0O ,O0O00OOOOOOOO0O0O )#line:142
            O0O00OOOOOOOO0O0O =OO00OO00000O00O0O .rotation_filename (OO00OO00000O00O0O .baseFilename +".1")#line:143
            if os .path .exists (O0O00OOOOOOOO0O0O ):#line:144
                os .remove (O0O00OOOOOOOO0O0O )#line:145
            OO00OO00000O00O0O .rotate (OO00OO00000O00O0O .baseFilename ,O0O00OOOOOOOO0O0O )#line:146
        if not OO00OO00000O00O0O .delay :#line:147
            OO00OO00000O00O0O .stream =OO00OO00000O00O0O ._open ()#line:148
    def shouldRollover (O0OO0O0OO0O0O00OO ,OO0000O000000OOOO ):#line:150
        ""#line:156
        if O0OO0O0OO0O0O00OO .stream is None :#line:157
            O0OO0O0OO0O0O00OO .stream =O0OO0O0OO0O0O00OO ._open ()#line:158
        if O0OO0O0OO0O0O00OO .maxBytes >0 :#line:159
            OOO0OO0OOOOOO0OO0 ="%s\n"%O0OO0O0OO0O0O00OO .format (OO0000O000000OOOO )#line:160
            O0OO0O0OO0O0O00OO .stream .seek (0 ,2 )#line:161
            if O0OO0O0OO0O0O00OO .stream .tell ()+len (OOO0OO0OOOOOO0OO0 )>=O0OO0O0OO0O0O00OO .maxBytes :#line:162
                return 1 #line:163
        return 0 #line:164
class TimedRotatingFileHandler (BaseRotatingHandler ):#line:166
    ""#line:173
    def __init__ (OO00OO0OO00O0O00O ,O0O0000O0OOOOO000 ,when ='h',interval =1 ,backupCount =0 ,encoding =None ,delay =False ,utc =False ,atTime =None ):#line:174
        BaseRotatingHandler .__init__ (OO00OO0OO00O0O00O ,O0O0000O0OOOOO000 ,'a',encoding ,delay )#line:175
        OO00OO0OO00O0O00O .when =when .upper ()#line:176
        OO00OO0OO00O0O00O .backupCount =backupCount #line:177
        OO00OO0OO00O0O00O .utc =utc #line:178
        OO00OO0OO00O0O00O .atTime =atTime #line:179
        if OO00OO0OO00O0O00O .when =='S':#line:192
            OO00OO0OO00O0O00O .interval =1 #line:193
            OO00OO0OO00O0O00O .suffix ="%Y-%m-%d_%H-%M-%S"#line:194
            OO00OO0OO00O0O00O .extMatch =r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"#line:195
        elif OO00OO0OO00O0O00O .when =='M':#line:196
            OO00OO0OO00O0O00O .interval =60 #line:197
            OO00OO0OO00O0O00O .suffix ="%Y-%m-%d_%H-%M"#line:198
            OO00OO0OO00O0O00O .extMatch =r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"#line:199
        elif OO00OO0OO00O0O00O .when =='H':#line:200
            OO00OO0OO00O0O00O .interval =60 *60 #line:201
            OO00OO0OO00O0O00O .suffix ="%Y-%m-%d_%H"#line:202
            OO00OO0OO00O0O00O .extMatch =r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"#line:203
        elif OO00OO0OO00O0O00O .when =='D'or OO00OO0OO00O0O00O .when =='MIDNIGHT':#line:204
            OO00OO0OO00O0O00O .interval =60 *60 *24 #line:205
            OO00OO0OO00O0O00O .suffix ="%Y-%m-%d"#line:206
            OO00OO0OO00O0O00O .extMatch =r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"#line:207
        elif OO00OO0OO00O0O00O .when .startswith ('W'):#line:208
            OO00OO0OO00O0O00O .interval =60 *60 *24 *7 #line:209
            if len (OO00OO0OO00O0O00O .when )!=2 :#line:210
                raise ValueError ("You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s"%OO00OO0OO00O0O00O .when )#line:211
            if OO00OO0OO00O0O00O .when [1 ]<'0'or OO00OO0OO00O0O00O .when [1 ]>'6':#line:212
                raise ValueError ("Invalid day specified for weekly rollover: %s"%OO00OO0OO00O0O00O .when )#line:213
            OO00OO0OO00O0O00O .dayOfWeek =int (OO00OO0OO00O0O00O .when [1 ])#line:214
            OO00OO0OO00O0O00O .suffix ="%Y-%m-%d"#line:215
            OO00OO0OO00O0O00O .extMatch =r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"#line:216
        else :#line:217
            raise ValueError ("Invalid rollover interval specified: %s"%OO00OO0OO00O0O00O .when )#line:218
        OO00OO0OO00O0O00O .extMatch =re .compile (OO00OO0OO00O0O00O .extMatch ,re .ASCII )#line:220
        OO00OO0OO00O0O00O .interval =OO00OO0OO00O0O00O .interval *interval #line:221
        O0O0000O0OOOOO000 =OO00OO0OO00O0O00O .baseFilename #line:224
        if os .path .exists (O0O0000O0OOOOO000 ):#line:225
            OOOO00O0O0O0OO0O0 =os .stat (O0O0000O0OOOOO000 )[ST_MTIME ]#line:226
        else :#line:227
            OOOO00O0O0O0OO0O0 =int (time .time ())#line:228
        OO00OO0OO00O0O00O .rolloverAt =OO00OO0OO00O0O00O .computeRollover (OOOO00O0O0O0OO0O0 )#line:229
    def computeRollover (O0O00O0OOO0OO0O0O ,O0OOO0O0O00O0OOO0 ):#line:231
        ""#line:234
        O0OO0OO0OO0O00O0O =O0OOO0O0O00O0OOO0 +O0O00O0OOO0OO0O0O .interval #line:235
        if O0O00O0OOO0OO0O0O .when =='MIDNIGHT'or O0O00O0OOO0OO0O0O .when .startswith ('W'):#line:243
            if O0O00O0OOO0OO0O0O .utc :#line:245
                O00O0000000OOOOO0 =time .gmtime (O0OOO0O0O00O0OOO0 )#line:246
            else :#line:247
                O00O0000000OOOOO0 =time .localtime (O0OOO0O0O00O0OOO0 )#line:248
            O0O0O0OO00OO000OO =O00O0000000OOOOO0 [3 ]#line:249
            O0OOOO00O0O0000OO =O00O0000000OOOOO0 [4 ]#line:250
            O00OOO000O0OOOO0O =O00O0000000OOOOO0 [5 ]#line:251
            O0O0OO0OOOO00O00O =O00O0000000OOOOO0 [6 ]#line:252
            if O0O00O0OOO0OO0O0O .atTime is None :#line:254
                OO000O00O0O00OO00 =_OO000OOOOO0O0OOOO #line:255
            else :#line:256
                OO000O00O0O00OO00 =((O0O00O0OOO0OO0O0O .atTime .hour *60 +O0O00O0OOO0OO0O0O .atTime .minute )*60 +O0O00O0OOO0OO0O0O .atTime .second )#line:258
            OOO00O0O000O0OO0O =OO000O00O0O00OO00 -((O0O0O0OO00OO000OO *60 +O0OOOO00O0O0000OO )*60 +O00OOO000O0OOOO0O )#line:261
            if OOO00O0O000O0OO0O <0 :#line:262
                OOO00O0O000O0OO0O +=_OO000OOOOO0O0OOOO #line:266
                O0O0OO0OOOO00O00O =(O0O0OO0OOOO00O00O +1 )%7 #line:267
            O0OO0OO0OO0O00O0O =O0OOO0O0O00O0OOO0 +OOO00O0O000O0OO0O #line:268
            if O0O00O0OOO0OO0O0O .when .startswith ('W'):#line:284
                O000O0O00OOOO0O00 =O0O0OO0OOOO00O00O #line:285
                if O000O0O00OOOO0O00 !=O0O00O0OOO0OO0O0O .dayOfWeek :#line:286
                    if O000O0O00OOOO0O00 <O0O00O0OOO0OO0O0O .dayOfWeek :#line:287
                        O00000OOOOOOO00O0 =O0O00O0OOO0OO0O0O .dayOfWeek -O000O0O00OOOO0O00 #line:288
                    else :#line:289
                        O00000OOOOOOO00O0 =6 -O000O0O00OOOO0O00 +O0O00O0OOO0OO0O0O .dayOfWeek +1 #line:290
                    OO0000OOO0OOOO00O =O0OO0OO0OO0O00O0O +(O00000OOOOOOO00O0 *(60 *60 *24 ))#line:291
                    if not O0O00O0OOO0OO0O0O .utc :#line:292
                        OO0OO0OOO0000OO00 =O00O0000000OOOOO0 [-1 ]#line:293
                        OOO0OO0O00O00O00O =time .localtime (OO0000OOO0OOOO00O )[-1 ]#line:294
                        if OO0OO0OOO0000OO00 !=OOO0OO0O00O00O00O :#line:295
                            if not OO0OO0OOO0000OO00 :#line:296
                                OOOOOOOOOOO000O0O =-3600 #line:297
                            else :#line:298
                                OOOOOOOOOOO000O0O =3600 #line:299
                            OO0000OOO0OOOO00O +=OOOOOOOOOOO000O0O #line:300
                    O0OO0OO0OO0O00O0O =OO0000OOO0OOOO00O #line:301
        return O0OO0OO0OO0O00O0O #line:302
    def shouldRollover (O00000OO0OOO0OOOO ,OOOO00O0O00OOOO00 ):#line:304
        ""#line:310
        OO0OO000O0O0OO000 =int (time .time ())#line:311
        if OO0OO000O0O0OO000 >=O00000OO0OOO0OOOO .rolloverAt :#line:312
            return 1 #line:313
        return 0 #line:314
    def getFilesToDelete (OO0O00OO0OOO0OO00 ):#line:316
        ""#line:321
        OO0OO0O00O0O00O0O ,O0O0OO0O00OOO0O00 =os .path .split (OO0O00OO0OOO0OO00 .baseFilename )#line:322
        OOOO0OO00O0000O0O =os .listdir (OO0OO0O00O0O00O0O )#line:323
        O0O000OO0OO00OO0O =[]#line:324
        O0OOO00OO0O00OOO0 =O0O0OO0O00OOO0O00 +"."#line:325
        O0OO00O0OOOOO0OO0 =len (O0OOO00OO0O00OOO0 )#line:326
        for O00OO0000O0OO00O0 in OOOO0OO00O0000O0O :#line:327
            if O00OO0000O0OO00O0 [:O0OO00O0OOOOO0OO0 ]==O0OOO00OO0O00OOO0 :#line:328
                O0O000OOOO0O0OO0O =O00OO0000O0OO00O0 [O0OO00O0OOOOO0OO0 :]#line:329
                if OO0O00OO0OOO0OO00 .extMatch .match (O0O000OOOO0O0OO0O ):#line:330
                    O0O000OO0OO00OO0O .append (os .path .join (OO0OO0O00O0O00O0O ,O00OO0000O0OO00O0 ))#line:331
        if len (O0O000OO0OO00OO0O )<OO0O00OO0OOO0OO00 .backupCount :#line:332
            O0O000OO0OO00OO0O =[]#line:333
        else :#line:334
            O0O000OO0OO00OO0O .sort ()#line:335
            O0O000OO0OO00OO0O =O0O000OO0OO00OO0O [:len (O0O000OO0OO00OO0O )-OO0O00OO0OOO0OO00 .backupCount ]#line:336
        return O0O000OO0OO00OO0O #line:337
    def doRollover (O00O0O000000OOO00 ):#line:339
        ""#line:346
        if O00O0O000000OOO00 .stream :#line:347
            O00O0O000000OOO00 .stream .close ()#line:348
            O00O0O000000OOO00 .stream =None #line:349
        OO000OO00O0O00OO0 =int (time .time ())#line:351
        O00O0OOOOO0O0OO0O =time .localtime (OO000OO00O0O00OO0 )[-1 ]#line:352
        O0000O00O0OO0O0OO =O00O0O000000OOO00 .rolloverAt -O00O0O000000OOO00 .interval #line:353
        if O00O0O000000OOO00 .utc :#line:354
            O00OO00O0OO00OOO0 =time .gmtime (O0000O00O0OO0O0OO )#line:355
        else :#line:356
            O00OO00O0OO00OOO0 =time .localtime (O0000O00O0OO0O0OO )#line:357
            O0O0OOOOO0O000O00 =O00OO00O0OO00OOO0 [-1 ]#line:358
            if O00O0OOOOO0O0OO0O !=O0O0OOOOO0O000O00 :#line:359
                if O00O0OOOOO0O0OO0O :#line:360
                    O0O0OOO00O0OOO0O0 =3600 #line:361
                else :#line:362
                    O0O0OOO00O0OOO0O0 =-3600 #line:363
                O00OO00O0OO00OOO0 =time .localtime (O0000O00O0OO0O0OO +O0O0OOO00O0OOO0O0 )#line:364
        OO0OOO0000000000O =O00O0O000000OOO00 .rotation_filename (O00O0O000000OOO00 .baseFilename +"."+time .strftime (O00O0O000000OOO00 .suffix ,O00OO00O0OO00OOO0 ))#line:366
        if os .path .exists (OO0OOO0000000000O ):#line:367
            os .remove (OO0OOO0000000000O )#line:368
        O00O0O000000OOO00 .rotate (O00O0O000000OOO00 .baseFilename ,OO0OOO0000000000O )#line:369
        if O00O0O000000OOO00 .backupCount >0 :#line:370
            for OO00O0O0OO00OOOOO in O00O0O000000OOO00 .getFilesToDelete ():#line:371
                os .remove (OO00O0O0OO00OOOOO )#line:372
        if not O00O0O000000OOO00 .delay :#line:373
            O00O0O000000OOO00 .stream =O00O0O000000OOO00 ._open ()#line:374
        OO00OOO00O0OO0000 =O00O0O000000OOO00 .computeRollover (OO000OO00O0O00OO0 )#line:375
        while OO00OOO00O0OO0000 <=OO000OO00O0O00OO0 :#line:376
            OO00OOO00O0OO0000 =OO00OOO00O0OO0000 +O00O0O000000OOO00 .interval #line:377
        if (O00O0O000000OOO00 .when =='MIDNIGHT'or O00O0O000000OOO00 .when .startswith ('W'))and not O00O0O000000OOO00 .utc :#line:379
            OOOOO0O00000O0OOO =time .localtime (OO00OOO00O0OO0000 )[-1 ]#line:380
            if O00O0OOOOO0O0OO0O !=OOOOO0O00000O0OOO :#line:381
                if not O00O0OOOOO0O0OO0O :#line:382
                    O0O0OOO00O0OOO0O0 =-3600 #line:383
                else :#line:384
                    O0O0OOO00O0OOO0O0 =3600 #line:385
                OO00OOO00O0OO0000 +=O0O0OOO00O0OOO0O0 #line:386
        O00O0O000000OOO00 .rolloverAt =OO00OOO00O0OO0000 #line:387
class WatchedFileHandler (logging .FileHandler ):#line:389
    ""#line:408
    def __init__ (OOO0OO0OO0O0O00O0 ,OO00O0O0O0000000O ,mode ='a',encoding =None ,delay =False ):#line:409
        logging .FileHandler .__init__ (OOO0OO0OO0O0O00O0 ,OO00O0O0O0000000O ,mode ,encoding ,delay )#line:410
        OOO0OO0OO0O0O00O0 .dev ,OOO0OO0OO0O0O00O0 .ino =-1 ,-1 #line:411
        OOO0OO0OO0O0O00O0 ._statstream ()#line:412
    def _statstream (OOO0OOOOOO00OO0O0 ):#line:414
        if OOO0OOOOOO00OO0O0 .stream :#line:415
            O0OOO00OOOOO0OO0O =os .fstat (OOO0OOOOOO00OO0O0 .stream .fileno ())#line:416
            OOO0OOOOOO00OO0O0 .dev ,OOO0OOOOOO00OO0O0 .ino =O0OOO00OOOOO0OO0O [ST_DEV ],O0OOO00OOOOO0OO0O [ST_INO ]#line:417
    def reopenIfNeeded (O0000O00OO0O00O00 ):#line:419
        ""#line:426
        try :#line:431
            OOOOO000OOOO000O0 =os .stat (O0000O00OO0O00O00 .baseFilename )#line:433
        except FileNotFoundError :#line:434
            OOOOO000OOOO000O0 =None #line:435
        if not OOOOO000OOOO000O0 or OOOOO000OOOO000O0 [ST_DEV ]!=O0000O00OO0O00O00 .dev or OOOOO000OOOO000O0 [ST_INO ]!=O0000O00OO0O00O00 .ino :#line:437
            if O0000O00OO0O00O00 .stream is not None :#line:438
                O0000O00OO0O00O00 .stream .flush ()#line:440
                O0000O00OO0O00O00 .stream .close ()#line:441
                O0000O00OO0O00O00 .stream =None #line:442
                O0000O00OO0O00O00 .stream =O0000O00OO0O00O00 ._open ()#line:444
                O0000O00OO0O00O00 ._statstream ()#line:445
    def emit (O00000O0000O0000O ,O000O0O0O0OOOOO00 ):#line:447
        ""#line:453
        O00000O0000O0000O .reopenIfNeeded ()#line:454
        logging .FileHandler .emit (O00000O0000O0000O ,O000O0O0O0OOOOO00 )#line:455
class SocketHandler (logging .Handler ):#line:458
    ""#line:469
    def __init__ (OO000OOO0OO0OOO00 ,OO0OOOO0OOOOOOO0O ,OOOO0O000O0OO00O0 ):#line:471
        ""#line:478
        logging .Handler .__init__ (OO000OOO0OO0OOO00 )#line:479
        OO000OOO0OO0OOO00 .host =OO0OOOO0OOOOOOO0O #line:480
        OO000OOO0OO0OOO00 .port =OOOO0O000O0OO00O0 #line:481
        if OOOO0O000O0OO00O0 is None :#line:482
            OO000OOO0OO0OOO00 .address =OO0OOOO0OOOOOOO0O #line:483
        else :#line:484
            OO000OOO0OO0OOO00 .address =(OO0OOOO0OOOOOOO0O ,OOOO0O000O0OO00O0 )#line:485
        OO000OOO0OO0OOO00 .sock =None #line:486
        OO000OOO0OO0OOO00 .closeOnError =False #line:487
        OO000OOO0OO0OOO00 .retryTime =None #line:488
        OO000OOO0OO0OOO00 .retryStart =1.0 #line:492
        OO000OOO0OO0OOO00 .retryMax =30.0 #line:493
        OO000OOO0OO0OOO00 .retryFactor =2.0 #line:494
    def makeSocket (OOOO00OO00O000000 ,timeout =1 ):#line:496
        ""#line:500
        if OOOO00OO00O000000 .port is not None :#line:501
            OOOOOO000O00000OO =socket .create_connection (OOOO00OO00O000000 .address ,timeout =timeout )#line:502
        else :#line:503
            OOOOOO000O00000OO =socket .socket (socket .AF_UNIX ,socket .SOCK_STREAM )#line:504
            OOOOOO000O00000OO .settimeout (timeout )#line:505
            try :#line:506
                OOOOOO000O00000OO .connect (OOOO00OO00O000000 .address )#line:507
            except OSError :#line:508
                OOOOOO000O00000OO .close ()#line:509
                raise #line:510
        return OOOOOO000O00000OO #line:511
    def createSocket (O0O0O00O0O0O00000 ):#line:513
        ""#line:518
        O00OOO0OO000O0O00 =time .time ()#line:519
        if O0O0O00O0O0O00000 .retryTime is None :#line:523
            O00O0O00OO000O000 =True #line:524
        else :#line:525
            O00O0O00OO000O000 =(O00OOO0OO000O0O00 >=O0O0O00O0O0O00000 .retryTime )#line:526
        if O00O0O00OO000O000 :#line:527
            try :#line:528
                O0O0O00O0O0O00000 .sock =O0O0O00O0O0O00000 .makeSocket ()#line:529
                O0O0O00O0O0O00000 .retryTime =None #line:530
            except OSError :#line:531
                if O0O0O00O0O0O00000 .retryTime is None :#line:533
                    O0O0O00O0O0O00000 .retryPeriod =O0O0O00O0O0O00000 .retryStart #line:534
                else :#line:535
                    O0O0O00O0O0O00000 .retryPeriod =O0O0O00O0O0O00000 .retryPeriod *O0O0O00O0O0O00000 .retryFactor #line:536
                    if O0O0O00O0O0O00000 .retryPeriod >O0O0O00O0O0O00000 .retryMax :#line:537
                        O0O0O00O0O0O00000 .retryPeriod =O0O0O00O0O0O00000 .retryMax #line:538
                O0O0O00O0O0O00000 .retryTime =O00OOO0OO000O0O00 +O0O0O00O0O0O00000 .retryPeriod #line:539
    def send (O0OOO00OO0OOO0O0O ,O000O0OOOO00OO0O0 ):#line:541
        ""#line:547
        if O0OOO00OO0OOO0O0O .sock is None :#line:548
            O0OOO00OO0OOO0O0O .createSocket ()#line:549
        if O0OOO00OO0OOO0O0O .sock :#line:553
            try :#line:554
                O0OOO00OO0OOO0O0O .sock .sendall (O000O0OOOO00OO0O0 )#line:555
            except OSError :#line:556
                O0OOO00OO0OOO0O0O .sock .close ()#line:557
                O0OOO00OO0OOO0O0O .sock =None #line:558
    def makePickle (OO0000000O00OOOO0 ,OO0OOOO0O000O0OO0 ):#line:560
        ""#line:564
        OO00OO00O00OO00O0 =OO0OOOO0O000O0OO0 .exc_info #line:565
        if OO00OO00O00OO00O0 :#line:566
            O0O0OO00OO00OOO0O =OO0000000O00OOOO0 .format (OO0OOOO0O000O0OO0 )#line:568
        OOO0O0O0000O00000 =dict (OO0OOOO0O000O0OO0 .__dict__ )#line:572
        OOO0O0O0000O00000 ['msg']=OO0OOOO0O000O0OO0 .getMessage ()#line:573
        OOO0O0O0000O00000 ['args']=None #line:574
        OOO0O0O0000O00000 ['exc_info']=None #line:575
        OOO0O0O0000O00000 .pop ('message',None )#line:577
        O00OO0OOO0OOOO00O =pickle .dumps (OOO0O0O0000O00000 ,1 )#line:578
        OO0O0OO0OO0OO0O00 =struct .pack (">L",len (O00OO0OOO0OOOO00O ))#line:579
        return OO0O0OO0OO0OO0O00 +O00OO0OOO0OOOO00O #line:580
    def handleError (O0O0O000OO000000O ,OOOOO0O00O0O00OOO ):#line:582
        ""#line:589
        if O0O0O000OO000000O .closeOnError and O0O0O000OO000000O .sock :#line:590
            O0O0O000OO000000O .sock .close ()#line:591
            O0O0O000OO000000O .sock =None #line:592
        else :#line:593
            logging .Handler .handleError (O0O0O000OO000000O ,OOOOO0O00O0O00OOO )#line:594
    def emit (OO000OO0OO00000O0 ,OO0O000O0O0O0OO0O ):#line:596
        ""#line:604
        try :#line:605
            OO0000O00O000OOOO =OO000OO0OO00000O0 .makePickle (OO0O000O0O0O0OO0O )#line:606
            OO000OO0OO00000O0 .send (OO0000O00O000OOOO )#line:607
        except Exception :#line:608
            OO000OO0OO00000O0 .handleError (OO0O000O0O0O0OO0O )#line:609
    def close (O0O0O0OOO0OO0OOO0 ):#line:611
        ""#line:614
        O0O0O0OOO0OO0OOO0 .acquire ()#line:615
        try :#line:616
            O00O00OO0O0OOO0OO =O0O0O0OOO0OO0OOO0 .sock #line:617
            if O00O00OO0O0OOO0OO :#line:618
                O0O0O0OOO0OO0OOO0 .sock =None #line:619
                O00O00OO0O0OOO0OO .close ()#line:620
            logging .Handler .close (O0O0O0OOO0OO0OOO0 )#line:621
        finally :#line:622
            O0O0O0OOO0OO0OOO0 .release ()#line:623
class DatagramHandler (SocketHandler ):#line:625
    ""#line:635
    def __init__ (OO00O0OOO0OO00OO0 ,OOO0OO000OO0O00O0 ,OO000000O0OO0OOOO ):#line:636
        ""#line:639
        SocketHandler .__init__ (OO00O0OOO0OO00OO0 ,OOO0OO000OO0O00O0 ,OO000000O0OO0OOOO )#line:640
        OO00O0OOO0OO00OO0 .closeOnError =False #line:641
    def makeSocket (OOOO0O00O00O0O000 ):#line:643
        ""#line:647
        if OOOO0O00O00O0O000 .port is None :#line:648
            OO00O00OOOOO000OO =socket .AF_UNIX #line:649
        else :#line:650
            OO00O00OOOOO000OO =socket .AF_INET #line:651
        O00OOO0O000O00OOO =socket .socket (OO00O00OOOOO000OO ,socket .SOCK_DGRAM )#line:652
        return O00OOO0O000O00OOO #line:653
    def send (O00OOOO0O000OOO00 ,OOO00OOOO00O0O0O0 ):#line:655
        ""#line:662
        if O00OOOO0O000OOO00 .sock is None :#line:663
            O00OOOO0O000OOO00 .createSocket ()#line:664
        O00OOOO0O000OOO00 .sock .sendto (OOO00OOOO00O0O0O0 ,O00OOOO0O000OOO00 .address )#line:665
class SysLogHandler (logging .Handler ):#line:667
    ""#line:674
    LOG_EMERG =0 #line:686
    LOG_ALERT =1 #line:687
    LOG_CRIT =2 #line:688
    LOG_ERR =3 #line:689
    LOG_WARNING =4 #line:690
    LOG_NOTICE =5 #line:691
    LOG_INFO =6 #line:692
    LOG_DEBUG =7 #line:693
    LOG_KERN =0 #line:696
    LOG_USER =1 #line:697
    LOG_MAIL =2 #line:698
    LOG_DAEMON =3 #line:699
    LOG_AUTH =4 #line:700
    LOG_SYSLOG =5 #line:701
    LOG_LPR =6 #line:702
    LOG_NEWS =7 #line:703
    LOG_UUCP =8 #line:704
    LOG_CRON =9 #line:705
    LOG_AUTHPRIV =10 #line:706
    LOG_FTP =11 #line:707
    LOG_LOCAL0 =16 #line:710
    LOG_LOCAL1 =17 #line:711
    LOG_LOCAL2 =18 #line:712
    LOG_LOCAL3 =19 #line:713
    LOG_LOCAL4 =20 #line:714
    LOG_LOCAL5 =21 #line:715
    LOG_LOCAL6 =22 #line:716
    LOG_LOCAL7 =23 #line:717
    priority_names ={"alert":LOG_ALERT ,"crit":LOG_CRIT ,"critical":LOG_CRIT ,"debug":LOG_DEBUG ,"emerg":LOG_EMERG ,"err":LOG_ERR ,"error":LOG_ERR ,"info":LOG_INFO ,"notice":LOG_NOTICE ,"panic":LOG_EMERG ,"warn":LOG_WARNING ,"warning":LOG_WARNING ,}#line:732
    facility_names ={"auth":LOG_AUTH ,"authpriv":LOG_AUTHPRIV ,"cron":LOG_CRON ,"daemon":LOG_DAEMON ,"ftp":LOG_FTP ,"kern":LOG_KERN ,"lpr":LOG_LPR ,"mail":LOG_MAIL ,"news":LOG_NEWS ,"security":LOG_AUTH ,"syslog":LOG_SYSLOG ,"user":LOG_USER ,"uucp":LOG_UUCP ,"local0":LOG_LOCAL0 ,"local1":LOG_LOCAL1 ,"local2":LOG_LOCAL2 ,"local3":LOG_LOCAL3 ,"local4":LOG_LOCAL4 ,"local5":LOG_LOCAL5 ,"local6":LOG_LOCAL6 ,"local7":LOG_LOCAL7 ,}#line:756
    priority_map ={"DEBUG":"debug","INFO":"info","WARNING":"warning","ERROR":"error","CRITICAL":"critical"}#line:768
    def __init__ (O0OOO0O0OO0O00OOO ,address =('localhost',SYSLOG_UDP_PORT ),facility =LOG_USER ,socktype =None ):#line:771
        ""#line:782
        logging .Handler .__init__ (O0OOO0O0OO0O00OOO )#line:783
        O0OOO0O0OO0O00OOO .address =address #line:785
        O0OOO0O0OO0O00OOO .facility =facility #line:786
        O0OOO0O0OO0O00OOO .socktype =socktype #line:787
        if isinstance (address ,str ):#line:789
            O0OOO0O0OO0O00OOO .unixsocket =True #line:790
            try :#line:795
                O0OOO0O0OO0O00OOO ._connect_unixsocket (address )#line:796
            except OSError :#line:797
                pass #line:798
        else :#line:799
            O0OOO0O0OO0O00OOO .unixsocket =False #line:800
            if socktype is None :#line:801
                socktype =socket .SOCK_DGRAM #line:802
            OOOOO0OO00O0OO000 ,OOOOOOO00OO00OOOO =address #line:803
            OOOO0O0O0O0000O00 =socket .getaddrinfo (OOOOO0OO00O0OO000 ,OOOOOOO00OO00OOOO ,0 ,socktype )#line:804
            if not OOOO0O0O0O0000O00 :#line:805
                raise OSError ("getaddrinfo returns an empty list")#line:806
            for OOOOO00O00OOOO0OO in OOOO0O0O0O0000O00 :#line:807
                O00O0OO0O0O000OOO ,socktype ,OOO0OO0O0O00O00OO ,_OO0OOO0000000O000 ,OO000000O00OOOOOO =OOOOO00O00OOOO0OO #line:808
                OOO0OOO00OOO0OO0O =OOO0O0OO00OO0OOOO =None #line:809
                try :#line:810
                    OOO0O0OO00OO0OOOO =socket .socket (O00O0OO0O0O000OOO ,socktype ,OOO0OO0O0O00O00OO )#line:811
                    if socktype ==socket .SOCK_STREAM :#line:812
                        OOO0O0OO00OO0OOOO .connect (OO000000O00OOOOOO )#line:813
                    break #line:814
                except OSError as O0O0O0O0O000OO0OO :#line:815
                    OOO0OOO00OOO0OO0O =O0O0O0O0O000OO0OO #line:816
                    if OOO0O0OO00OO0OOOO is not None :#line:817
                        OOO0O0OO00OO0OOOO .close ()#line:818
            if OOO0OOO00OOO0OO0O is not None :#line:819
                raise OOO0OOO00OOO0OO0O #line:820
            O0OOO0O0OO0O00OOO .socket =OOO0O0OO00OO0OOOO #line:821
            O0OOO0O0OO0O00OOO .socktype =socktype #line:822
    def _connect_unixsocket (OOO0OO0O0OOO0O00O ,O0OOO00OO0O0OOO00 ):#line:824
        O0OO00000O000O0OO =OOO0OO0O0OOO0O00O .socktype #line:825
        if O0OO00000O000O0OO is None :#line:826
            O0OO00000O000O0OO =socket .SOCK_DGRAM #line:827
        OOO0OO0O0OOO0O00O .socket =socket .socket (socket .AF_UNIX ,O0OO00000O000O0OO )#line:828
        try :#line:829
            OOO0OO0O0OOO0O00O .socket .connect (O0OOO00OO0O0OOO00 )#line:830
            OOO0OO0O0OOO0O00O .socktype =O0OO00000O000O0OO #line:832
        except OSError :#line:833
            OOO0OO0O0OOO0O00O .socket .close ()#line:834
            if OOO0OO0O0OOO0O00O .socktype is not None :#line:835
                raise #line:837
            O0OO00000O000O0OO =socket .SOCK_STREAM #line:838
            OOO0OO0O0OOO0O00O .socket =socket .socket (socket .AF_UNIX ,O0OO00000O000O0OO )#line:839
            try :#line:840
                OOO0OO0O0OOO0O00O .socket .connect (O0OOO00OO0O0OOO00 )#line:841
                OOO0OO0O0OOO0O00O .socktype =O0OO00000O000O0OO #line:843
            except OSError :#line:844
                OOO0OO0O0OOO0O00O .socket .close ()#line:845
                raise #line:846
    def encodePriority (OO00O0000OO0OOO0O ,O00OOOO00000000OO ,O00OOOO0OO00O0OOO ):#line:848
        ""#line:854
        if isinstance (O00OOOO00000000OO ,str ):#line:855
            O00OOOO00000000OO =OO00O0000OO0OOO0O .facility_names [O00OOOO00000000OO ]#line:856
        if isinstance (O00OOOO0OO00O0OOO ,str ):#line:857
            O00OOOO0OO00O0OOO =OO00O0000OO0OOO0O .priority_names [O00OOOO0OO00O0OOO ]#line:858
        return (O00OOOO00000000OO <<3 )|O00OOOO0OO00O0OOO #line:859
    def close (O0OOOO0OOOO000000 ):#line:861
        ""#line:864
        O0OOOO0OOOO000000 .acquire ()#line:865
        try :#line:866
            O0OOOO0OOOO000000 .socket .close ()#line:867
            logging .Handler .close (O0OOOO0OOOO000000 )#line:868
        finally :#line:869
            O0OOOO0OOOO000000 .release ()#line:870
    def mapPriority (OO0OO0OO000O00O00 ,O00O0O0OOO0OOO000 ):#line:872
        ""#line:879
        return OO0OO0OO000O00O00 .priority_map .get (O00O0O0OOO0OOO000 ,"warning")#line:880
    ident =''#line:882
    append_nul =True #line:883
    def emit (OOOOOOOO0OO0OOO00 ,OO000O0OO0OO0O000 ):#line:885
        ""#line:891
        try :#line:892
            O0OOOOOOO0OO0O0O0 =OOOOOOOO0OO0OOO00 .format (OO000O0OO0OO0O000 )#line:893
            if OOOOOOOO0OO0OOO00 .ident :#line:894
                O0OOOOOOO0OO0O0O0 =OOOOOOOO0OO0OOO00 .ident +O0OOOOOOO0OO0O0O0 #line:895
            if OOOOOOOO0OO0OOO00 .append_nul :#line:896
                O0OOOOOOO0OO0O0O0 +='\000'#line:897
            O0O0O0OO00OOOO0O0 ='<%d>'%OOOOOOOO0OO0OOO00 .encodePriority (OOOOOOOO0OO0OOO00 .facility ,OOOOOOOO0OO0OOO00 .mapPriority (OO000O0OO0OO0O000 .levelname ))#line:902
            O0O0O0OO00OOOO0O0 =O0O0O0OO00OOOO0O0 .encode ('utf-8')#line:903
            O0OOOOOOO0OO0O0O0 =O0OOOOOOO0OO0O0O0 .encode ('utf-8')#line:905
            O0OOOOOOO0OO0O0O0 =O0O0O0OO00OOOO0O0 +O0OOOOOOO0OO0O0O0 #line:906
            if OOOOOOOO0OO0OOO00 .unixsocket :#line:907
                try :#line:908
                    OOOOOOOO0OO0OOO00 .socket .send (O0OOOOOOO0OO0O0O0 )#line:909
                except OSError :#line:910
                    OOOOOOOO0OO0OOO00 .socket .close ()#line:911
                    OOOOOOOO0OO0OOO00 ._connect_unixsocket (OOOOOOOO0OO0OOO00 .address )#line:912
                    OOOOOOOO0OO0OOO00 .socket .send (O0OOOOOOO0OO0O0O0 )#line:913
            elif OOOOOOOO0OO0OOO00 .socktype ==socket .SOCK_DGRAM :#line:914
                OOOOOOOO0OO0OOO00 .socket .sendto (O0OOOOOOO0OO0O0O0 ,OOOOOOOO0OO0OOO00 .address )#line:915
            else :#line:916
                OOOOOOOO0OO0OOO00 .socket .sendall (O0OOOOOOO0OO0O0O0 )#line:917
        except Exception :#line:918
            OOOOOOOO0OO0OOO00 .handleError (OO000O0OO0OO0O000 )#line:919
class SMTPHandler (logging .Handler ):#line:921
    ""#line:924
    def __init__ (O0OO0OO00O0OOO0OO ,OOO000O0OOO0OO0O0 ,O0000O00O0O0O00OO ,O0O0OO0OOOOOOO000 ,OO0OOOO000OOO0O0O ,credentials =None ,secure =None ,timeout =5.0 ):#line:926
        ""#line:942
        logging .Handler .__init__ (O0OO0OO00O0OOO0OO )#line:943
        if isinstance (OOO000O0OOO0OO0O0 ,(list ,tuple )):#line:944
            O0OO0OO00O0OOO0OO .mailhost ,O0OO0OO00O0OOO0OO .mailport =OOO000O0OOO0OO0O0 #line:945
        else :#line:946
            O0OO0OO00O0OOO0OO .mailhost ,O0OO0OO00O0OOO0OO .mailport =OOO000O0OOO0OO0O0 ,None #line:947
        if isinstance (credentials ,(list ,tuple )):#line:948
            O0OO0OO00O0OOO0OO .username ,O0OO0OO00O0OOO0OO .password =credentials #line:949
        else :#line:950
            O0OO0OO00O0OOO0OO .username =None #line:951
        O0OO0OO00O0OOO0OO .fromaddr =O0000O00O0O0O00OO #line:952
        if isinstance (O0O0OO0OOOOOOO000 ,str ):#line:953
            O0O0OO0OOOOOOO000 =[O0O0OO0OOOOOOO000 ]#line:954
        O0OO0OO00O0OOO0OO .toaddrs =O0O0OO0OOOOOOO000 #line:955
        O0OO0OO00O0OOO0OO .subject =OO0OOOO000OOO0O0O #line:956
        O0OO0OO00O0OOO0OO .secure =secure #line:957
        O0OO0OO00O0OOO0OO .timeout =timeout #line:958
    def getSubject (O0OO00O0OOOOOOOOO ,OO0O0OOOOOOO000O0 ):#line:960
        ""#line:966
        return O0OO00O0OOOOOOOOO .subject #line:967
    def emit (OOOO00OOO0OOO0000 ,O0OO00O0OO0O0O0O0 ):#line:969
        ""#line:974
        try :#line:975
            import smtplib #line:976
            from email .message import EmailMessage #line:977
            import email .utils #line:978
            OO00O0O0000OOO0O0 =OOOO00OOO0OOO0000 .mailport #line:980
            if not OO00O0O0000OOO0O0 :#line:981
                OO00O0O0000OOO0O0 =smtplib .SMTP_PORT #line:982
            OOOOOO0000OOOO0OO =smtplib .SMTP (OOOO00OOO0OOO0000 .mailhost ,OO00O0O0000OOO0O0 ,timeout =OOOO00OOO0OOO0000 .timeout )#line:983
            OOO0OO0OOO00O000O =EmailMessage ()#line:984
            OOO0OO0OOO00O000O ['From']=OOOO00OOO0OOO0000 .fromaddr #line:985
            OOO0OO0OOO00O000O ['To']=','.join (OOOO00OOO0OOO0000 .toaddrs )#line:986
            OOO0OO0OOO00O000O ['Subject']=OOOO00OOO0OOO0000 .getSubject (O0OO00O0OO0O0O0O0 )#line:987
            OOO0OO0OOO00O000O ['Date']=email .utils .localtime ()#line:988
            OOO0OO0OOO00O000O .set_content (OOOO00OOO0OOO0000 .format (O0OO00O0OO0O0O0O0 ))#line:989
            if OOOO00OOO0OOO0000 .username :#line:990
                if OOOO00OOO0OOO0000 .secure is not None :#line:991
                    OOOOOO0000OOOO0OO .ehlo ()#line:992
                    OOOOOO0000OOOO0OO .starttls (*OOOO00OOO0OOO0000 .secure )#line:993
                    OOOOOO0000OOOO0OO .ehlo ()#line:994
                OOOOOO0000OOOO0OO .login (OOOO00OOO0OOO0000 .username ,OOOO00OOO0OOO0000 .password )#line:995
            OOOOOO0000OOOO0OO .send_message (OOO0OO0OOO00O000O )#line:996
            OOOOOO0000OOOO0OO .quit ()#line:997
        except Exception :#line:998
            OOOO00OOO0OOO0000 .handleError (O0OO00O0OO0O0O0O0 )#line:999
class NTEventLogHandler (logging .Handler ):#line:1001
    ""#line:1010
    def __init__ (O00000O0OOO0OO0O0 ,OOOOOOOOOOOO00O00 ,dllname =None ,logtype ="Application"):#line:1011
        logging .Handler .__init__ (O00000O0OOO0OO0O0 )#line:1012
        try :#line:1013
            import win32evtlogutil ,win32evtlog #line:1014
            O00000O0OOO0OO0O0 .appname =OOOOOOOOOOOO00O00 #line:1015
            O00000O0OOO0OO0O0 ._welu =win32evtlogutil #line:1016
            if not dllname :#line:1017
                dllname =os .path .split (O00000O0OOO0OO0O0 ._welu .__file__ )#line:1018
                dllname =os .path .split (dllname [0 ])#line:1019
                dllname =os .path .join (dllname [0 ],r'win32service.pyd')#line:1020
            O00000O0OOO0OO0O0 .dllname =dllname #line:1021
            O00000O0OOO0OO0O0 .logtype =logtype #line:1022
            O00000O0OOO0OO0O0 ._welu .AddSourceToRegistry (OOOOOOOOOOOO00O00 ,dllname ,logtype )#line:1023
            O00000O0OOO0OO0O0 .deftype =win32evtlog .EVENTLOG_ERROR_TYPE #line:1024
            O00000O0OOO0OO0O0 .typemap ={logging .DEBUG :win32evtlog .EVENTLOG_INFORMATION_TYPE ,logging .INFO :win32evtlog .EVENTLOG_INFORMATION_TYPE ,logging .WARNING :win32evtlog .EVENTLOG_WARNING_TYPE ,logging .ERROR :win32evtlog .EVENTLOG_ERROR_TYPE ,logging .CRITICAL :win32evtlog .EVENTLOG_ERROR_TYPE ,}#line:1031
        except ImportError :#line:1032
            print ("The Python Win32 extensions for NT (service, event " "logging) appear not to be available.")#line:1034
            O00000O0OOO0OO0O0 ._welu =None #line:1035
    def getMessageID (OOO00O00O0OO0OOO0 ,OO0OOO0O0000O00OO ):#line:1037
        ""#line:1044
        return 1 #line:1045
    def getEventCategory (OO0OOOO0O00OO000O ,O000O0OOOO000O00O ):#line:1047
        ""#line:1053
        return 0 #line:1054
    def getEventType (OOOO000O0OOOO0OO0 ,O0O0OOO0O0000000O ):#line:1056
        ""#line:1066
        return OOOO000O0OOOO0OO0 .typemap .get (O0O0OOO0O0000000O .levelno ,OOOO000O0OOOO0OO0 .deftype )#line:1067
    def emit (OOOO0O0000OO00O00 ,OO0OOOO00O00O0OO0 ):#line:1069
        ""#line:1075
        if OOOO0O0000OO00O00 ._welu :#line:1076
            try :#line:1077
                OOOO00O0O00O0O0OO =OOOO0O0000OO00O00 .getMessageID (OO0OOOO00O00O0OO0 )#line:1078
                OOOOO0O00OOOO0000 =OOOO0O0000OO00O00 .getEventCategory (OO0OOOO00O00O0OO0 )#line:1079
                O0OO0OOO0000OO000 =OOOO0O0000OO00O00 .getEventType (OO0OOOO00O00O0OO0 )#line:1080
                OO0OO0OO0O00OO000 =OOOO0O0000OO00O00 .format (OO0OOOO00O00O0OO0 )#line:1081
                OOOO0O0000OO00O00 ._welu .ReportEvent (OOOO0O0000OO00O00 .appname ,OOOO00O0O00O0O0OO ,OOOOO0O00OOOO0000 ,O0OO0OOO0000OO000 ,[OO0OO0OO0O00OO000 ])#line:1082
            except Exception :#line:1083
                OOOO0O0000OO00O00 .handleError (OO0OOOO00O00O0OO0 )#line:1084
    def close (O0OO0OOOO00O0OO0O ):#line:1086
        ""#line:1095
        logging .Handler .close (O0OO0OOOO00O0OO0O )#line:1097
class HTTPHandler (logging .Handler ):#line:1099
    ""#line:1103
    def __init__ (O0OO0OO0O0OO00OOO ,O0OO0OO0O00OO00OO ,OO0O00O000O0O00O0 ,method ="GET",secure =False ,credentials =None ,context =None ):#line:1105
        ""#line:1109
        logging .Handler .__init__ (O0OO0OO0O0OO00OOO )#line:1110
        method =method .upper ()#line:1111
        if method not in ["GET","POST"]:#line:1112
            raise ValueError ("method must be GET or POST")#line:1113
        if not secure and context is not None :#line:1114
            raise ValueError ("context parameter only makes sense " "with secure=True")#line:1116
        O0OO0OO0O0OO00OOO .host =O0OO0OO0O00OO00OO #line:1117
        O0OO0OO0O0OO00OOO .url =OO0O00O000O0O00O0 #line:1118
        O0OO0OO0O0OO00OOO .method =method #line:1119
        O0OO0OO0O0OO00OOO .secure =secure #line:1120
        O0OO0OO0O0OO00OOO .credentials =credentials #line:1121
        O0OO0OO0O0OO00OOO .context =context #line:1122
    def mapLogRecord (OO0000O00O0000OO0 ,O0O00O0O0OO00OOOO ):#line:1124
        ""#line:1129
        return O0O00O0O0OO00OOOO .__dict__ #line:1130
    def emit (O0OO0O000O000OO00 ,O0OOOO00O0O000OOO ):#line:1132
        ""#line:1137
        try :#line:1138
            import http .client ,urllib .parse #line:1139
            OO0O000OOOOO00O0O =O0OO0O000O000OO00 .host #line:1140
            if O0OO0O000O000OO00 .secure :#line:1141
                O00OO0OOOO0000OOO =http .client .HTTPSConnection (OO0O000OOOOO00O0O ,context =O0OO0O000O000OO00 .context )#line:1142
            else :#line:1143
                O00OO0OOOO0000OOO =http .client .HTTPConnection (OO0O000OOOOO00O0O )#line:1144
            OOO0O00OOO00OOO0O =O0OO0O000O000OO00 .url #line:1145
            OOOOO00O000O0O0O0 =urllib .parse .urlencode (O0OO0O000O000OO00 .mapLogRecord (O0OOOO00O0O000OOO ))#line:1146
            if O0OO0O000O000OO00 .method =="GET":#line:1147
                if (OOO0O00OOO00OOO0O .find ('?')>=0 ):#line:1148
                    OO0O0000OO00O0OOO ='&'#line:1149
                else :#line:1150
                    OO0O0000OO00O0OOO ='?'#line:1151
                OOO0O00OOO00OOO0O =OOO0O00OOO00OOO0O +"%c%s"%(OO0O0000OO00O0OOO ,OOOOO00O000O0O0O0 )#line:1152
            O00OO0OOOO0000OOO .putrequest (O0OO0O000O000OO00 .method ,OOO0O00OOO00OOO0O )#line:1153
            O000OO00OOOO000OO =OO0O000OOOOO00O0O .find (":")#line:1156
            if O000OO00OOOO000OO >=0 :#line:1157
                OO0O000OOOOO00O0O =OO0O000OOOOO00O0O [:O000OO00OOOO000OO ]#line:1158
            if O0OO0O000O000OO00 .method =="POST":#line:1162
                O00OO0OOOO0000OOO .putheader ("Content-type","application/x-www-form-urlencoded")#line:1164
                O00OO0OOOO0000OOO .putheader ("Content-length",str (len (OOOOO00O000O0O0O0 )))#line:1165
            if O0OO0O000O000OO00 .credentials :#line:1166
                import base64 #line:1167
                O00OO0O0O0OO00O0O =('%s:%s'%O0OO0O000O000OO00 .credentials ).encode ('utf-8')#line:1168
                O00OO0O0O0OO00O0O ='Basic '+base64 .b64encode (O00OO0O0O0OO00O0O ).strip ().decode ('ascii')#line:1169
                O00OO0OOOO0000OOO .putheader ('Authorization',O00OO0O0O0OO00O0O )#line:1170
            O00OO0OOOO0000OOO .endheaders ()#line:1171
            if O0OO0O000O000OO00 .method =="POST":#line:1172
                O00OO0OOOO0000OOO .send (OOOOO00O000O0O0O0 .encode ('utf-8'))#line:1173
            O00OO0OOOO0000OOO .getresponse ()#line:1174
        except Exception :#line:1175
            O0OO0O000O000OO00 .handleError (O0OOOO00O0O000OOO )#line:1176
class BufferingHandler (logging .Handler ):#line:1178
    ""#line:1183
    def __init__ (O0OO000OO00O000OO ,O000O0O0OOO000O0O ):#line:1184
        ""#line:1187
        logging .Handler .__init__ (O0OO000OO00O000OO )#line:1188
        O0OO000OO00O000OO .capacity =O000O0O0OOO000O0O #line:1189
        O0OO000OO00O000OO .buffer =[]#line:1190
    def shouldFlush (OOO000O0OO0O00OOO ,O00000OOO0O0000OO ):#line:1192
        ""#line:1198
        return (len (OOO000O0OO0O00OOO .buffer )>=OOO000O0OO0O00OOO .capacity )#line:1199
    def emit (O0O00O0O0OOOO0OO0 ,OO000OOOOOO000OO0 ):#line:1201
        ""#line:1207
        O0O00O0O0OOOO0OO0 .buffer .append (OO000OOOOOO000OO0 )#line:1208
        if O0O00O0O0OOOO0OO0 .shouldFlush (OO000OOOOOO000OO0 ):#line:1209
            O0O00O0O0OOOO0OO0 .flush ()#line:1210
    def flush (O000OOOOO00O0O000 ):#line:1212
        ""#line:1217
        O000OOOOO00O0O000 .acquire ()#line:1218
        try :#line:1219
            O000OOOOO00O0O000 .buffer =[]#line:1220
        finally :#line:1221
            O000OOOOO00O0O000 .release ()#line:1222
    def close (OO0O000000OO0000O ):#line:1224
        ""#line:1229
        try :#line:1230
            OO0O000000OO0000O .flush ()#line:1231
        finally :#line:1232
            logging .Handler .close (OO0O000000OO0000O )#line:1233
class MemoryHandler (BufferingHandler ):#line:1235
    ""#line:1240
    def __init__ (O0OOOO0OOOOO0OOO0 ,OOO00O0OO00O00O0O ,flushLevel =logging .ERROR ,target =None ,flushOnClose =True ):#line:1242
        ""#line:1254
        BufferingHandler .__init__ (O0OOOO0OOOOO0OOO0 ,OOO00O0OO00O00O0O )#line:1255
        O0OOOO0OOOOO0OOO0 .flushLevel =flushLevel #line:1256
        O0OOOO0OOOOO0OOO0 .target =target #line:1257
        O0OOOO0OOOOO0OOO0 .flushOnClose =flushOnClose #line:1259
    def shouldFlush (O00O000OO0OO0OOOO ,OO0OOO0O0OOOO0O00 ):#line:1261
        ""#line:1264
        return (len (O00O000OO0OO0OOOO .buffer )>=O00O000OO0OO0OOOO .capacity )or (OO0OOO0O0OOOO0O00 .levelno >=O00O000OO0OO0OOOO .flushLevel )#line:1266
    def setTarget (O00OO0OOO0O0OO0O0 ,O00OO0OO0OO0O00O0 ):#line:1268
        ""#line:1271
        O00OO0OOO0O0OO0O0 .acquire ()#line:1272
        try :#line:1273
            O00OO0OOO0O0OO0O0 .target =O00OO0OO0OO0O00O0 #line:1274
        finally :#line:1275
            O00OO0OOO0O0OO0O0 .release ()#line:1276
    def flush (OO0OO0O0O000OOOOO ):#line:1278
        ""#line:1285
        OO0OO0O0O000OOOOO .acquire ()#line:1286
        try :#line:1287
            if OO0OO0O0O000OOOOO .target :#line:1288
                for O00O0OO000OO0O0O0 in OO0OO0O0O000OOOOO .buffer :#line:1289
                    OO0OO0O0O000OOOOO .target .handle (O00O0OO000OO0O0O0 )#line:1290
                OO0OO0O0O000OOOOO .buffer =[]#line:1291
        finally :#line:1292
            OO0OO0O0O000OOOOO .release ()#line:1293
    def close (O0O0OOO00OOO0OOO0 ):#line:1295
        ""#line:1299
        try :#line:1300
            if O0O0OOO00OOO0OOO0 .flushOnClose :#line:1301
                O0O0OOO00OOO0OOO0 .flush ()#line:1302
        finally :#line:1303
            O0O0OOO00OOO0OOO0 .acquire ()#line:1304
            try :#line:1305
                O0O0OOO00OOO0OOO0 .target =None #line:1306
                BufferingHandler .close (O0O0OOO00OOO0OOO0 )#line:1307
            finally :#line:1308
                O0O0OOO00OOO0OOO0 .release ()#line:1309
class QueueHandler (logging .Handler ):#line:1312
    ""#line:1321
    def __init__ (O0OOO000000O0O00O ,O00000O0O00OO0OOO ):#line:1323
        ""#line:1326
        logging .Handler .__init__ (O0OOO000000O0O00O )#line:1327
        O0OOO000000O0O00O .queue =O00000O0O00OO0OOO #line:1328
    def enqueue (O000OOOO0O0OOO0OO ,OOO0O00OO0O000OO0 ):#line:1330
        ""#line:1337
        O000OOOO0O0OOO0OO .queue .put_nowait (OOO0O00OO0O000OO0 )#line:1338
    def prepare (OOO0O0000OO0OO0O0 ,O0O0O000O00O000O0 ):#line:1340
        ""#line:1352
        OO00OO00OOOO0OO0O =OOO0O0000OO0OO0O0 .format (O0O0O000O00O000O0 )#line:1359
        O0O0O000O00O000O0 =copy .copy (O0O0O000O00O000O0 )#line:1361
        O0O0O000O00O000O0 .message =OO00OO00OOOO0OO0O #line:1362
        O0O0O000O00O000O0 .msg =OO00OO00OOOO0OO0O #line:1363
        O0O0O000O00O000O0 .args =None #line:1364
        O0O0O000O00O000O0 .exc_info =None #line:1365
        O0O0O000O00O000O0 .exc_text =None #line:1366
        return O0O0O000O00O000O0 #line:1367
    def emit (OO0OOOO00O0OOO0OO ,OO00O00OO0O000OO0 ):#line:1369
        ""#line:1374
        try :#line:1375
            OO0OOOO00O0OOO0OO .enqueue (OO0OOOO00O0OOO0OO .prepare (OO00O00OO0O000OO0 ))#line:1376
        except Exception :#line:1377
            OO0OOOO00O0OOO0OO .handleError (OO00O00OO0O000OO0 )#line:1378
class QueueListener (object ):#line:1381
    ""#line:1386
    _sentinel =None #line:1387
    def __init__ (O0O000O0000OOO000 ,O00O00O0O0OO00O0O ,*OOOO0O00OOOO0OOOO ,respect_handler_level =False ):#line:1389
        ""#line:1393
        O0O000O0000OOO000 .queue =O00O00O0O0OO00O0O #line:1394
        O0O000O0000OOO000 .handlers =OOOO0O00OOOO0OOOO #line:1395
        O0O000O0000OOO000 ._thread =None #line:1396
        O0O000O0000OOO000 .respect_handler_level =respect_handler_level #line:1397
    def dequeue (OO0OOO0000OO0O0O0 ,OOOOO00000OOOOO00 ):#line:1399
        ""#line:1405
        return OO0OOO0000OO0O0O0 .queue .get (OOOOO00000OOOOO00 )#line:1406
    def start (O000OOO000O000O0O ):#line:1408
        ""#line:1414
        O000OOO000O000O0O ._thread =OO0OOO00OO0OOOO0O =threading .Thread (target =O000OOO000O000O0O ._monitor )#line:1415
        OO0OOO00OO0OOOO0O .daemon =True #line:1416
        OO0OOO00OO0OOOO0O .start ()#line:1417
    def prepare (O0O0O00OOO00OOO0O ,O0OO0O0OOO0O000O0 ):#line:1419
        ""#line:1426
        return O0OO0O0OOO0O000O0 #line:1427
    def handle (O00O00OO000OOO0O0 ,OOO0000000000OO00 ):#line:1429
        ""#line:1435
        OOO0000000000OO00 =O00O00OO000OOO0O0 .prepare (OOO0000000000OO00 )#line:1436
        for O0O0O00O0O000O0OO in O00O00OO000OOO0O0 .handlers :#line:1437
            if not O00O00OO000OOO0O0 .respect_handler_level :#line:1438
                OO0OO000O0000O0O0 =True #line:1439
            else :#line:1440
                OO0OO000O0000O0O0 =OOO0000000000OO00 .levelno >=O0O0O00O0O000O0OO .level #line:1441
            if OO0OO000O0000O0O0 :#line:1442
                O0O0O00O0O000O0OO .handle (OOO0000000000OO00 )#line:1443
    def _monitor (O000OO0O00O0O0O00 ):#line:1445
        ""#line:1452
        OO000O0O00O0O0OOO =O000OO0O00O0O0O00 .queue #line:1453
        O00O0000000O0O000 =hasattr (OO000O0O00O0O0OOO ,'task_done')#line:1454
        while True :#line:1455
            try :#line:1456
                O00O0O0OOO0OO0OOO =O000OO0O00O0O0O00 .dequeue (True )#line:1457
                if O00O0O0OOO0OO0OOO is O000OO0O00O0O0O00 ._sentinel :#line:1458
                    if O00O0000000O0O000 :#line:1459
                        OO000O0O00O0O0OOO .task_done ()#line:1460
                    break #line:1461
                O000OO0O00O0O0O00 .handle (O00O0O0OOO0OO0OOO )#line:1462
                if O00O0000000O0O000 :#line:1463
                    OO000O0O00O0O0OOO .task_done ()#line:1464
            except queue .Empty :#line:1465
                break #line:1466
    def enqueue_sentinel (OOOOO000000OO0OOO ):#line:1468
        ""#line:1475
        OOOOO000000OO0OOO .queue .put_nowait (OOOOO000000OO0OOO ._sentinel )#line:1476
    def stop (O0O0OO0O0O0OO00O0 ):#line:1478
        ""#line:1485
        O0O0OO0O0O0OO00O0 .enqueue_sentinel ()#line:1486
        O0O0OO0O0O0OO00O0 ._thread .join ()#line:1487
        O0O0OO0O0O0OO00O0 ._thread =None #line:1488
