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

import sys ,os ,time ,io ,re ,traceback ,warnings ,weakref ,collections .abc ,random #line:1
from string import Template #line:3
from string import Formatter as StrFormatter #line:4
__all__ =['BASIC_FORMAT','BufferingFormatter','CRITICAL','DEBUG','ERROR','FATAL','FileHandler','Filter','Formatter','Handler','INFO','LogRecord','Logger','LoggerAdapter','NOTSET','NullHandler','StreamHandler','WARN','WARNING','addLevelName','basicConfig','captureWarnings','critical','debug','disable','error','exception','fatal','getLevelName','getLogger','getLoggerClass','info','log','makeLogRecord','setLoggerClass','shutdown','warn','warning','getLogRecordFactory','setLogRecordFactory','lastResort','raiseExceptions']#line:15
import threading #line:17
__author__ ="Vinay Sajip <vinay_sajip@red-dove.com>"#line:19
__status__ ="production"#line:20
__version__ ="0.5.1.2"#line:22
__date__ ="07 February 2010"#line:23
_O00OOOO0OOOO00000 =time .time ()#line:32
raiseExceptions =True #line:38
OOO000O000O000OO0 =True #line:43
O0O00O00OOO0O0OOO =True #line:48
O0O00OOO00O0O00OO =True #line:53
CRITICAL =50 #line:66
FATAL =CRITICAL #line:67
ERROR =40 #line:68
WARNING =30 #line:69
WARN =WARNING #line:70
INFO =20 #line:71
DEBUG =10 #line:72
NOTSET =0 #line:73
global O0O000OO000O00O00 #line:74
global OO0OO0OOO0000OO0O #line:75
global O000OOOOOO0O0O0OO #line:76
global OO00O0000000OOOO0 #line:77
_OOO0OO0O0OOO00OO0 ={CRITICAL :'CRITICAL',ERROR :'ERROR',WARNING :'WARNING',INFO :'INFO',DEBUG :'DEBUG',NOTSET :'NOTSET',}#line:87
_O0O00OO000OOOOO0O ={'CRITICAL':CRITICAL ,'FATAL':FATAL ,'ERROR':ERROR ,'WARN':WARNING ,'WARNING':WARNING ,'INFO':INFO ,'DEBUG':DEBUG ,'NOTSET':NOTSET ,}#line:97
def getLevelName (O0O0OO00O0OOO00O0 ):#line:99
    ""#line:116
    O00OO0000OOOOOOO0 =_OOO0OO0O0OOO00OO0 .get (O0O0OO00O0OOO00O0 )#line:118
    if O00OO0000OOOOOOO0 is not None :#line:119
        return O00OO0000OOOOOOO0 #line:120
    O00OO0000OOOOOOO0 =_O0O00OO000OOOOO0O .get (O0O0OO00O0OOO00O0 )#line:121
    if O00OO0000OOOOOOO0 is not None :#line:122
        return O00OO0000OOOOOOO0 #line:123
    return "Level %s"%O0O0OO00O0OOO00O0 #line:124
def addLevelName (OOO00O00000O0OO0O ,O00O00OO00OO0OOOO ):#line:126
    ""#line:131
    _OOOOOOO0O00O0O00O ()#line:132
    try :#line:133
        _OOO0OO0O0OOO00OO0 [OOO00O00000O0OO0O ]=O00O00OO00OO0OOOO #line:134
        _O0O00OO000OOOOO0O [O00O00OO00OO0OOOO ]=OOO00O00000O0OO0O #line:135
    finally :#line:136
        _O0O000OOO000O000O ()#line:137
if hasattr (sys ,'_getframe'):#line:139
    O00OOO0O0OO0OOOOO =lambda :sys ._getframe (3 )#line:140
else :#line:141
    def O00OOO0O0OO0OOOOO ():#line:142
        ""#line:143
        try :#line:144
            raise Exception #line:145
        except Exception :#line:146
            return sys .exc_info ()[2 ].tb_frame .f_back #line:147
_O0O0OOOOO000O0O0O =os .path .normcase (addLevelName .__code__ .co_filename )#line:161
def _O0OOO0OOOO00O0O0O (O00O0O0O0O000O000 ):#line:173
    if isinstance (O00O0O0O0O000O000 ,int ):#line:174
        O0O0O00000000O000 =O00O0O0O0O000O000 #line:175
    elif str (O00O0O0O0O000O000 )==O00O0O0O0O000O000 :#line:176
        if O00O0O0O0O000O000 not in _O0O00OO000OOOOO0O :#line:177
            raise ValueError ("Unknown level: %r"%O00O0O0O0O000O000 )#line:178
        O0O0O00000000O000 =_O0O00OO000OOOOO0O [O00O0O0O0O000O000 ]#line:179
    else :#line:180
        raise TypeError ("Level not an integer or a valid string: %r"%O00O0O0O0O000O000 )#line:181
    return O0O0O00000000O000 #line:182
_OOOOO0OO0OOOOO000 =threading .RLock ()#line:196
def _OOOOOOO0O00O0O00O ():#line:198
    ""#line:203
    if _OOOOO0OO0OOOOO000 :#line:204
        _OOOOO0OO0OOOOO000 .acquire ()#line:205
def _O0O000OOO000O000O ():#line:207
    ""#line:210
    if _OOOOO0OO0OOOOO000 :#line:211
        _OOOOO0OO0OOOOO000 .release ()#line:212
if not hasattr (os ,'register_at_fork'):#line:217
    def _O000OO00O000O00O0 (OO00OO0OO0000OO0O ):#line:218
        pass #line:219
else :#line:220
    _O00O000000OO0O0O0 =weakref .WeakSet ()#line:226
    def _O000OO00O000O00O0 (O0OO0OO00O00OO0O0 ):#line:228
        _OOOOOOO0O00O0O00O ()#line:229
        try :#line:230
            _O00O000000OO0O0O0 .add (O0OO0OO00O00OO0O0 )#line:231
        finally :#line:232
            _O0O000OOO000O000O ()#line:233
    def _OO00OOOOO0OO0OO00 ():#line:235
        for OO0OO0OO000OO0O00 in _O00O000000OO0O0O0 :#line:237
            try :#line:238
                OO0OO0OO000OO0O00 .createLock ()#line:239
            except Exception as O00OOOO000O000000 :#line:240
                print ("Ignoring exception from logging atfork",instance ,"._reinit_lock() method:",O00OOOO000O000000 ,file =sys .stderr )#line:243
        _O0O000OOO000O000O ()#line:244
    os .register_at_fork (before =_OOOOOOO0O00O0O00O ,after_in_child =_OO00OOOOO0OO0OO00 ,after_in_parent =_O0O000OOO000O000O )#line:249
class LogRecord (object ):#line:256
    ""#line:267
    def __init__ (O0O00OO00OO00O0OO ,O0OOO00O0O0OOOO00 ,OOOO000O0O0OOOOO0 ,OOO00O00O000000O0 ,O000OO000O00O0000 ,OO0OOOO0O00000000 ,O0000OO0OO0O00OOO ,OO0O0O0OOOO000OOO ,func =None ,sinfo =None ,**O00000OO0OO00O000 ):#line:269
        ""#line:272
        OOO0OOOOO0O00OO0O =time .time ()#line:273
        O0O00OO00OO00O0OO .name =O0OOO00O0O0OOOO00 #line:274
        O0O00OO00OO00O0OO .msg =OO0OOOO0O00000000 #line:275
        if (O0000OO0OO0O00OOO and len (O0000OO0OO0O00OOO )==1 and isinstance (O0000OO0OO0O00OOO [0 ],collections .abc .Mapping )and O0000OO0OO0O00OOO [0 ]):#line:295
            O0000OO0OO0O00OOO =O0000OO0OO0O00OOO [0 ]#line:296
        O0O00OO00OO00O0OO .args =O0000OO0OO0O00OOO #line:297
        O0O00OO00OO00O0OO .levelname =getLevelName (OOOO000O0O0OOOOO0 )#line:298
        O0O00OO00OO00O0OO .levelno =OOOO000O0O0OOOOO0 #line:299
        O0O00OO00OO00O0OO .pathname =OOO00O00O000000O0 #line:300
        try :#line:301
            O0O00OO00OO00O0OO .filename =os .path .basename (OOO00O00O000000O0 )#line:302
            O0O00OO00OO00O0OO .module =os .path .splitext (O0O00OO00OO00O0OO .filename )[0 ]#line:303
        except (TypeError ,ValueError ,AttributeError ):#line:304
            O0O00OO00OO00O0OO .filename =OOO00O00O000000O0 #line:305
            O0O00OO00OO00O0OO .module ="Unknown module"#line:306
        O0O00OO00OO00O0OO .exc_info =OO0O0O0OOOO000OOO #line:307
        O0O00OO00OO00O0OO .exc_text =None #line:308
        O0O00OO00OO00O0OO .stack_info =sinfo #line:309
        O0O00OO00OO00O0OO .lineno =O000OO000O00O0000 #line:310
        O0O00OO00OO00O0OO .funcName =func #line:311
        O0O00OO00OO00O0OO .created =OOO0OOOOO0O00OO0O #line:312
        O0O00OO00OO00O0OO .msecs =(OOO0OOOOO0O00OO0O -int (OOO0OOOOO0O00OO0O ))*1000 #line:313
        O0O00OO00OO00O0OO .relativeCreated =(O0O00OO00OO00O0OO .created -_O00OOOO0OOOO00000 )*1000 #line:314
        if OOO000O000O000OO0 :#line:315
            O0O00OO00OO00O0OO .thread =threading .get_ident ()#line:316
            O0O00OO00OO00O0OO .threadName =threading .current_thread ().name #line:317
        else :#line:318
            O0O00OO00OO00O0OO .thread =None #line:319
            O0O00OO00OO00O0OO .threadName =None #line:320
        if not O0O00O00OOO0O0OOO :#line:321
            O0O00OO00OO00O0OO .processName =None #line:322
        else :#line:323
            O0O00OO00OO00O0OO .processName ='MainProcess'#line:324
            OO0O0O0O0OO00OOO0 =sys .modules .get ('multiprocessing')#line:325
            if OO0O0O0O0OO00OOO0 is not None :#line:326
                try :#line:331
                    O0O00OO00OO00O0OO .processName =OO0O0O0O0OO00OOO0 .current_process ().name #line:332
                except Exception :#line:333
                    pass #line:334
        if O0O00OOO00O0O00OO and hasattr (os ,'getpid'):#line:335
            O0O00OO00OO00O0OO .process =os .getpid ()#line:336
        else :#line:337
            O0O00OO00OO00O0OO .process =None #line:338
    def __repr__ (O0000OO00OO0O0000 ):#line:340
        return '<LogRecord: %s, %s, %s, %s, "%s">'%(O0000OO00OO0O0000 .name ,O0000OO00OO0O0000 .levelno ,O0000OO00OO0O0000 .pathname ,O0000OO00OO0O0000 .lineno ,O0000OO00OO0O0000 .msg )#line:342
    def getMessage (O0O00OOOO00OO000O ):#line:344
        ""#line:350
        OOOOOOOO0OOO0OOO0 =str (O0O00OOOO00OO000O .msg )#line:351
        if O0O00OOOO00OO000O .args :#line:352
            OOOOOOOO0OOO0OOO0 =OOOOOOOO0OOO0OOO0 %O0O00OOOO00OO000O .args #line:353
        return OOOOOOOO0OOO0OOO0 #line:354
_O0O0O0O0OO0O0O0OO =LogRecord #line:359
def setLogRecordFactory (O00O00OO00OOO0000 ):#line:361
    ""#line:367
    global _O0O0O0O0OO0O0O0OO #line:368
    _O0O0O0O0OO0O0O0OO =O00O00OO00OOO0000 #line:369
def getLogRecordFactory ():#line:371
    ""#line:374
    return _O0O0O0O0OO0O0O0OO #line:376
def makeLogRecord (OOOOO0OO000OO0O0O ):#line:378
    ""#line:384
    O0OOO0OOO00000000 =_O0O0O0O0OO0O0O0OO (None ,None ,"",0 ,"",(),None ,None )#line:385
    O0OOO0OOO00000000 .__dict__ .update (OOOOO0OO000OO0O0O )#line:386
    return O0OOO0OOO00000000 #line:387
_O0O000O00O0OO0O0O =StrFormatter ()#line:393
del StrFormatter #line:394
class O00000OOOO0OO000O (object ):#line:397
    default_format ='%(message)s'#line:399
    asctime_format ='%(asctime)s'#line:400
    asctime_search ='%(asctime)'#line:401
    validation_pattern =re .compile (r'%\(\w+\)[#0+ -]*(\*|\d+)?(\.(\*|\d+))?[diouxefgcrsa%]',re .I )#line:402
    def __init__ (OO00O00OO0OOOO000 ,O00000O00000000OO ):#line:404
        OO00O00OO0OOOO000 ._fmt =O00000O00000000OO or OO00O00OO0OOOO000 .default_format #line:405
    def usesTime (OOOOOOO000O000OO0 ):#line:407
        return OOOOOOO000O000OO0 ._fmt .find (OOOOOOO000O000OO0 .asctime_search )>=0 #line:408
    def validate (O0OO00OOOO0OOO0OO ):#line:410
        ""#line:411
        if not O0OO00OOOO0OOO0OO .validation_pattern .search (O0OO00OOOO0OOO0OO ._fmt ):#line:412
            raise ValueError ("Invalid format '%s' for '%s' style"%(O0OO00OOOO0OOO0OO ._fmt ,O0OO00OOOO0OOO0OO .default_format [0 ]))#line:413
    def _format (O0O000000O00OOO00 ,O0O0O0O0OOO0OO0O0 ):#line:415
        return O0O000000O00OOO00 ._fmt %O0O0O0O0OOO0OO0O0 .__dict__ #line:416
    def format (O0OOO0OO0OOOO0000 ,OOO0OO0OO00O0OO00 ):#line:418
        try :#line:419
            return O0OOO0OO0OOOO0000 ._format (OOO0OO0OO00O0OO00 )#line:420
        except KeyError as O0OOO0O0OO0OOO000 :#line:421
            raise ValueError ('Formatting field not found in record: %s'%O0OOO0O0OO0OOO000 )#line:422
class O0O0OOOOOOOO0OO0O (O00000OOOO0OO000O ):#line:425
    default_format ='{message}'#line:426
    asctime_format ='{asctime}'#line:427
    asctime_search ='{asctime'#line:428
    fmt_spec =re .compile (r'^(.?[<>=^])?[+ -]?#?0?(\d+|{\w+})?[,_]?(\.(\d+|{\w+}))?[bcdefgnosx%]?$',re .I )#line:430
    field_spec =re .compile (r'^(\d+|\w+)(\.\w+|\[[^]]+\])*$')#line:431
    def _format (OOOO000O000O00OO0 ,O00OOO000O0O0000O ):#line:433
        return OOOO000O000O00OO0 ._fmt .format (**O00OOO000O0O0000O .__dict__ )#line:434
    def validate (OO00000OO0O00O00O ):#line:436
        ""#line:437
        O0O00O0OOOOOOO000 =set ()#line:438
        try :#line:439
            for _OO0OOOOO0O00O00OO ,OO0OOOOO0O0O00OOO ,O0OO000O00000OO0O ,OO00O0OO0O00OOOO0 in _O0O000O00O0OO0O0O .parse (OO00000OO0O00O00O ._fmt ):#line:440
                if OO0OOOOO0O0O00OOO :#line:441
                    if not OO00000OO0O00O00O .field_spec .match (OO0OOOOO0O0O00OOO ):#line:442
                        raise ValueError ('invalid field name/expression: %r'%OO0OOOOO0O0O00OOO )#line:443
                    O0O00O0OOOOOOO000 .add (OO0OOOOO0O0O00OOO )#line:444
                if OO00O0OO0O00OOOO0 and OO00O0OO0O00OOOO0 not in 'rsa':#line:445
                    raise ValueError ('invalid conversion: %r'%OO00O0OO0O00OOOO0 )#line:446
                if O0OO000O00000OO0O and not OO00000OO0O00O00O .fmt_spec .match (O0OO000O00000OO0O ):#line:447
                    raise ValueError ('bad specifier: %r'%O0OO000O00000OO0O )#line:448
        except ValueError as OOO000O00000O00OO :#line:449
            raise ValueError ('invalid format: %s'%OOO000O00000O00OO )#line:450
        if not O0O00O0OOOOOOO000 :#line:451
            raise ValueError ('invalid format: no fields')#line:452
class O0O00OO0O00O0OO00 (O00000OOOO0OO000O ):#line:455
    default_format ='${message}'#line:456
    asctime_format ='${asctime}'#line:457
    asctime_search ='${asctime}'#line:458
    def __init__ (O0OOOOOOOOOO00000 ,OO0OOO000OOOOO0OO ):#line:460
        O0OOOOOOOOOO00000 ._fmt =OO0OOO000OOOOO0OO or O0OOOOOOOOOO00000 .default_format #line:461
        O0OOOOOOOOOO00000 ._tpl =Template (O0OOOOOOOOOO00000 ._fmt )#line:462
    def usesTime (OO0OO00O000O000OO ):#line:464
        OO0OO00OO0O0OO00O =OO0OO00O000O000OO ._fmt #line:465
        return OO0OO00OO0O0OO00O .find ('$asctime')>=0 or OO0OO00OO0O0OO00O .find (OO0OO00O000O000OO .asctime_format )>=0 #line:466
    def validate (OO00OOOO000O000O0 ):#line:468
        O00OO0O00O0O00OOO =Template .pattern #line:469
        OO000OOO00O0OOO00 =set ()#line:470
        for OO0O000OO0O0O00OO in O00OO0O00O0O00OOO .finditer (OO00OOOO000O000O0 ._fmt ):#line:471
            OO00OO0OO00OOO0OO =OO0O000OO0O0O00OO .groupdict ()#line:472
            if OO00OO0OO00OOO0OO ['named']:#line:473
                OO000OOO00O0OOO00 .add (OO00OO0OO00OOO0OO ['named'])#line:474
            elif OO00OO0OO00OOO0OO ['braced']:#line:475
                OO000OOO00O0OOO00 .add (OO00OO0OO00OOO0OO ['braced'])#line:476
            elif OO0O000OO0O0O00OO .group (0 )=='$':#line:477
                raise ValueError ('invalid format: bare \'$\' not allowed')#line:478
        if not OO000OOO00O0OOO00 :#line:479
            raise ValueError ('invalid format: no fields')#line:480
    def _format (O0O000O0O0O00000O ,O000OOO0OO000OO00 ):#line:482
        return O0O000O0O0O00000O ._tpl .substitute (**O000OOO0OO000OO00 .__dict__ )#line:483
BASIC_FORMAT ="%(levelname)s:%(name)s:%(message)s"#line:486
_OO00OOOOOO00OOOO0 ={'%':(O00000OOOO0OO000O ,BASIC_FORMAT ),'{':(O0O0OOOOOOOO0OO0O ,'{levelname}:{name}:{message}'),'$':(O0O00OO0O00O0OO00 ,'${levelname}:${name}:${message}'),}#line:492
class Formatter (object ):#line:494
    ""#line:535
    converter =time .localtime #line:537
    def __init__ (O0O0000OO0OO0OOO0 ,fmt =None ,datefmt =None ,style ='%',validate =True ):#line:539
        ""#line:554
        if style not in _OO00OOOOOO00OOOO0 :#line:555
            raise ValueError ('Style must be one of: %s'%','.join (_OO00OOOOOO00OOOO0 .keys ()))#line:557
        O0O0000OO0OO0OOO0 ._style =_OO00OOOOOO00OOOO0 [style ][0 ](fmt )#line:558
        if validate :#line:559
            O0O0000OO0OO0OOO0 ._style .validate ()#line:560
        O0O0000OO0OO0OOO0 ._fmt =O0O0000OO0OO0OOO0 ._style ._fmt #line:562
        O0O0000OO0OO0OOO0 .datefmt =datefmt #line:563
    default_time_format ='%Y-%m-%d %H:%M:%S'#line:565
    default_msec_format ='%s,%03d'#line:566
    def formatTime (O00000000O00OO00O ,O0O0OO0OOO0000OO0 ,datefmt =None ):#line:568
        ""#line:585
        O0OO0O0OO0000O0O0 =O00000000O00OO00O .converter (O0O0OO0OOO0000OO0 .created )#line:586
        if datefmt :#line:587
            O0OO000OO0OOOOOO0 =time .strftime (datefmt ,O0OO0O0OO0000O0O0 )#line:588
        else :#line:589
            OOOOO0OO000O0O0OO =time .strftime (O00000000O00OO00O .default_time_format ,O0OO0O0OO0000O0O0 )#line:590
            O0OO000OO0OOOOOO0 =O00000000O00OO00O .default_msec_format %(OOOOO0OO000O0O0OO ,O0O0OO0OOO0000OO0 .msecs )#line:591
        return O0OO000OO0OOOOOO0 #line:592
    def formatException (OOOO00OOO0OO00O00 ,O000OO0O0O0OO00OO ):#line:594
        ""#line:600
        O0OO0OOOO000OOOO0 =io .StringIO ()#line:601
        OO00O00OOOO0OO000 =O000OO0O0O0OO00OO [2 ]#line:602
        traceback .print_exception (O000OO0O0O0OO00OO [0 ],O000OO0O0O0OO00OO [1 ],OO00O00OOOO0OO000 ,None ,O0OO0OOOO000OOOO0 )#line:606
        O0O0OOO0OO0000000 =O0OO0OOOO000OOOO0 .getvalue ()#line:607
        O0OO0OOOO000OOOO0 .close ()#line:608
        if O0O0OOO0OO0000000 [-1 :]=="\n":#line:609
            O0O0OOO0OO0000000 =O0O0OOO0OO0000000 [:-1 ]#line:610
        return O0O0OOO0OO0000000 #line:611
    def usesTime (OOOOOOO0O0O0OOOOO ):#line:613
        ""#line:616
        return OOOOOOO0O0O0OOOOO ._style .usesTime ()#line:617
    def formatMessage (O0OO000OO000O0000 ,OOO00O0O00O0000OO ):#line:619
        return O0OO000OO000O0000 ._style .format (OOO00O0O00O0000OO )#line:620
    def formatStack (O0O0OOO00OO0000OO ,O00O00OOO000O0OO0 ):#line:622
        ""#line:632
        return O00O00OOO000O0OO0 #line:633
    def format (OO00O000OOOO0OO0O ,O0O0000O0O0O0O00O ):#line:635
        ""#line:647
        O0O0000O0O0O0O00O .message =O0O0000O0O0O0O00O .getMessage ()#line:648
        if OO00O000OOOO0OO0O .usesTime ():#line:649
            O0O0000O0O0O0O00O .asctime =OO00O000OOOO0OO0O .formatTime (O0O0000O0O0O0O00O ,OO00O000OOOO0OO0O .datefmt )#line:650
        O00OO0O0OO0O0O000 =OO00O000OOOO0OO0O .formatMessage (O0O0000O0O0O0O00O )#line:651
        print (O00OO0O0OO0O0O000 )#line:652
        if O0O0000O0O0O0O00O .exc_info :#line:653
            if not O0O0000O0O0O0O00O .exc_text :#line:656
                O0O0000O0O0O0O00O .exc_text =OO00O000OOOO0OO0O .formatException (O0O0000O0O0O0O00O .exc_info )#line:657
        if O0O0000O0O0O0O00O .exc_text :#line:658
            if O00OO0O0OO0O0O000 [-1 :]!="\n":#line:659
                O00OO0O0OO0O0O000 =O00OO0O0OO0O0O000 +"\n"#line:660
            O00OO0O0OO0O0O000 =O00OO0O0OO0O0O000 +O0O0000O0O0O0O00O .exc_text #line:661
        if O0O0000O0O0O0O00O .stack_info :#line:662
            if O00OO0O0OO0O0O000 [-1 :]!="\n":#line:663
                O00OO0O0OO0O0O000 =O00OO0O0OO0O0O000 +"\n"#line:664
            O00OO0O0OO0O0O000 =O00OO0O0OO0O0O000 +OO00O000OOOO0OO0O .formatStack (O0O0000O0O0O0O00O .stack_info )#line:665
        return O00OO0O0OO0O0O000 #line:666
_O00OOOOOO000OO0O0 =Formatter ()#line:671
class BufferingFormatter (object ):#line:673
    ""#line:676
    def __init__ (OO000O00OO0O0O0OO ,linefmt =None ):#line:677
        ""#line:681
        if linefmt :#line:682
            OO000O00OO0O0O0OO .linefmt =linefmt #line:683
        else :#line:684
            OO000O00OO0O0O0OO .linefmt =_O00OOOOOO000OO0O0 #line:685
    def formatHeader (OOO00O0O0O00OO0OO ,OO0O000O00O0OO0O0 ):#line:687
        ""#line:690
        return ""#line:691
    def formatFooter (OOOOOOO00OO0OOO00 ,O0000OO0OO0OO0OO0 ):#line:693
        ""#line:696
        return ""#line:697
    def format (OOOOO00O0O00O000O ,OO000000O00000O00 ):#line:699
        ""#line:702
        O000O0OO0O00OO0O0 =""#line:703
        if len (OO000000O00000O00 )>0 :#line:704
            O000O0OO0O00OO0O0 =O000O0OO0O00OO0O0 +OOOOO00O0O00O000O .formatHeader (OO000000O00000O00 )#line:705
            for OO0O0O0OOO00OO0O0 in OO000000O00000O00 :#line:706
                O000O0OO0O00OO0O0 =O000O0OO0O00OO0O0 +OOOOO00O0O00O000O .linefmt .format (OO0O0O0OOO00OO0O0 )#line:707
            O000O0OO0O00OO0O0 =O000O0OO0O00OO0O0 +OOOOO00O0O00O000O .formatFooter (OO000000O00000O00 )#line:708
        return O000O0OO0O00OO0O0 #line:709
class Filter (object ):#line:715
    ""#line:725
    def __init__ (OOOOOO00OOOO000O0 ,name =''):#line:726
        ""#line:733
        OOOOOO00OOOO000O0 .name =name #line:734
        OOOOOO00OOOO000O0 .nlen =len (name )#line:735
    def filter (O0OOO00000O00O0OO ,OOO00OOOOO0000OOO ):#line:737
        ""#line:743
        if O0OOO00000O00O0OO .nlen ==0 :#line:744
            return True #line:745
        elif O0OOO00000O00O0OO .name ==OOO00OOOOO0000OOO .name :#line:746
            return True #line:747
        elif OOO00OOOOO0000OOO .name .find (O0OOO00000O00O0OO .name ,0 ,O0OOO00000O00O0OO .nlen )!=0 :#line:748
            return False #line:749
        return (OOO00OOOOO0000OOO .name [O0OOO00000O00O0OO .nlen ]==".")#line:750
class O000OOO0O0O0O000O (object ):#line:752
    ""#line:756
    def __init__ (O0000OOOOOOOOO0OO ):#line:757
        ""#line:760
        O0000OOOOOOOOO0OO .filters =[]#line:761
    def addFilter (O0OOO0O0O0OO00OOO ,OO000OO0000OO0O0O ):#line:763
        ""#line:766
        if not (OO000OO0000OO0O0O in O0OOO0O0O0OO00OOO .filters ):#line:767
            O0OOO0O0O0OO00OOO .filters .append (OO000OO0000OO0O0O )#line:768
    def removeFilter (OOOO000O00O0O00O0 ,O0OO00O00OOO00O0O ):#line:770
        ""#line:773
        if O0OO00O00OOO00O0O in OOOO000O00O0O00O0 .filters :#line:774
            OOOO000O00O0O00O0 .filters .remove (O0OO00O00OOO00O0O )#line:775
    def filter (OOOO0OO0OOO00000O ,O00OOO0OOO0OO000O ):#line:777
        ""#line:788
        OO0O0O0O0O0000O00 =True #line:789
        for O0OO00000O0OO00OO in OOOO0OO0OOO00000O .filters :#line:790
            if hasattr (O0OO00000O0OO00OO ,'filter'):#line:791
                O00O000OO0O0O0O00 =O0OO00000O0OO00OO .filter (O00OOO0OOO0OO000O )#line:792
            else :#line:793
                O00O000OO0O0O0O00 =O0OO00000O0OO00OO (O00OOO0OOO0OO000O )#line:794
            if not O00O000OO0O0O0O00 :#line:795
                OO0O0O0O0O0000O00 =False #line:796
                break #line:797
        return OO0O0O0O0O0000O00 #line:798
_O0O0OOO0O00O00OOO =weakref .WeakValueDictionary ()#line:804
_O0OOO0OO0O000O0O0 =[]#line:805
def _OO0O0O00OO0OOOO00 (O0O0O00O0O000O0OO ):#line:807
    ""#line:810
    O0O0OOOO0OO0O0000 ,O0O0OO0OOO0OOO0O0 ,OOO00OOOOOOO0OO00 =_OOOOOOO0O00O0O00O ,_O0O000OOO000O000O ,_O0OOO0OO0O000O0O0 #line:815
    if O0O0OOOO0OO0O0000 and O0O0OO0OOO0OOO0O0 and OOO00OOOOOOO0OO00 :#line:816
        O0O0OOOO0OO0O0000 ()#line:817
        try :#line:818
            if O0O0O00O0O000O0OO in OOO00OOOOOOO0OO00 :#line:819
                OOO00OOOOOOO0OO00 .remove (O0O0O00O0O000O0OO )#line:820
        finally :#line:821
            O0O0OO0OOO0OOO0O0 ()#line:822
def _O0OOOOOOOOO00O0OO (O0O00OO0O0OO0O0OO ):#line:824
    ""#line:827
    _OOOOOOO0O00O0O00O ()#line:828
    try :#line:829
        _O0OOO0OO0O000O0O0 .append (weakref .ref (O0O00OO0O0OO0O0OO ,_OO0O0O00OO0OOOO00 ))#line:830
    finally :#line:831
        _O0O000OOO000O000O ()#line:832
class Handler (O000OOO0O0O0O000O ):#line:834
    ""#line:842
    def __init__ (OOO0OOOO0000OOOOO ,level =NOTSET ):#line:843
        ""#line:847
        O000OOO0O0O0O000O .__init__ (OOO0OOOO0000OOOOO )#line:848
        OOO0OOOO0000OOOOO ._name =None #line:849
        OOO0OOOO0000OOOOO .level =_O0OOO0OOOO00O0O0O (level )#line:850
        OOO0OOOO0000OOOOO .formatter =None #line:851
        _O0OOOOOOOOO00O0OO (OOO0OOOO0000OOOOO )#line:853
        OOO0OOOO0000OOOOO .createLock ()#line:854
    def get_name (OO0O000OOO0O00OOO ):#line:856
        return OO0O000OOO0O00OOO ._name #line:857
    def set_name (OO000000OOOOO0OO0 ,OO0000OO00O000OO0 ):#line:859
        _OOOOOOO0O00O0O00O ()#line:860
        try :#line:861
            if OO000000OOOOO0OO0 ._name in _O0O0OOO0O00O00OOO :#line:862
                del _O0O0OOO0O00O00OOO [OO000000OOOOO0OO0 ._name ]#line:863
            OO000000OOOOO0OO0 ._name =OO0000OO00O000OO0 #line:864
            if OO0000OO00O000OO0 :#line:865
                _O0O0OOO0O00O00OOO [OO0000OO00O000OO0 ]=OO000000OOOOO0OO0 #line:866
        finally :#line:867
            _O0O000OOO000O000O ()#line:868
    name =property (get_name ,set_name )#line:870
    def createLock (OO0OOOO0OO000OOO0 ):#line:872
        ""#line:875
        OO0OOOO0OO000OOO0 .lock =threading .RLock ()#line:876
        _O000OO00O000O00O0 (OO0OOOO0OO000OOO0 )#line:877
    def acquire (O0O0O0OO0O0000OO0 ):#line:879
        ""#line:882
        if O0O0O0OO0O0000OO0 .lock :#line:883
            O0O0O0OO0O0000OO0 .lock .acquire ()#line:884
    def release (OOO0OO00OOOOO000O ):#line:886
        ""#line:889
        if OOO0OO00OOOOO000O .lock :#line:890
            OOO0OO00OOOOO000O .lock .release ()#line:891
    def setLevel (OO0OO000OO0O0OOOO ,O00O0O0O0O00OO0O0 ):#line:893
        ""#line:896
        OO0OO000OO0O0OOOO .level =_O0OOO0OOOO00O0O0O (O00O0O0O0O00OO0O0 )#line:897
    def format (O00O000OO0OO000OO ,OOOO0OOO00OOOO0O0 ):#line:899
        ""#line:905
        if O00O000OO0OO000OO .formatter :#line:906
            O0OO00O000O000O0O =O00O000OO0OO000OO .formatter #line:907
        else :#line:908
            O0OO00O000O000O0O =_O00OOOOOO000OO0O0 #line:909
        return O0OO00O000O000O0O .format (OOOO0OOO00OOOO0O0 )#line:910
    def emit (OOO000OO0O000000O ,OOOOO0000O00O0O00 ):#line:912
        ""#line:918
        raise NotImplementedError ('emit must be implemented ' 'by Handler subclasses')#line:920
    def handle (OO0OO0OOOOO0OO000 ,OO0O000OOOO0OO0OO ):#line:922
        ""#line:930
        OO0O0O0OOOOOO000O =OO0OO0OOOOO0OO000 .filter (OO0O000OOOO0OO0OO )#line:931
        if OO0O0O0OOOOOO000O :#line:932
            OO0OO0OOOOO0OO000 .acquire ()#line:933
            try :#line:934
                OO0OO0OOOOO0OO000 .emit (OO0O000OOOO0OO0OO )#line:935
            finally :#line:936
                OO0OO0OOOOO0OO000 .release ()#line:937
        return OO0O0O0OOOOOO000O #line:938
    def setFormatter (O0O0O00OO0OO0000O ,O0OO0OO00OO00O0OO ):#line:940
        ""#line:943
        O0O0O00OO0OO0000O .formatter =O0OO0OO00OO00O0OO #line:944
    def flush (OO0000O00O0O000O0 ):#line:946
        ""#line:952
        pass #line:953
    def close (O0O0O0O000O00OOO0 ):#line:955
        ""#line:963
        _OOOOOOO0O00O0O00O ()#line:965
        try :#line:966
            if O0O0O0O000O00OOO0 ._name and O0O0O0O000O00OOO0 ._name in _O0O0OOO0O00O00OOO :#line:967
                del _O0O0OOO0O00O00OOO [O0O0O0O000O00OOO0 ._name ]#line:968
        finally :#line:969
            _O0O000OOO000O000O ()#line:970
    def handleError (O0O000O0000OO0OOO ,O0O0OOOOO0000000O ):#line:972
        ""#line:983
        if raiseExceptions and sys .stderr :#line:984
            O0O0O0O00OO0OOOO0 ,O000OOOO00000O0OO ,OOO0OOO0OO00O0000 =sys .exc_info ()#line:985
            try :#line:986
                sys .stderr .write ('--- Logging error ---\n')#line:987
                traceback .print_exception (O0O0O0O00OO0OOOO0 ,O000OOOO00000O0OO ,OOO0OOO0OO00O0000 ,None ,sys .stderr )#line:988
                sys .stderr .write ('Call stack:\n')#line:989
                O0OO00OOO0OOOO00O =OOO0OOO0OO00O0000 .tb_frame #line:992
                while (O0OO00OOO0OOOO00O and os .path .dirname (O0OO00OOO0OOOO00O .f_code .co_filename )==__path__ [0 ]):#line:994
                    O0OO00OOO0OOOO00O =O0OO00OOO0OOOO00O .f_back #line:995
                if O0OO00OOO0OOOO00O :#line:996
                    traceback .print_stack (O0OO00OOO0OOOO00O ,file =sys .stderr )#line:997
                else :#line:998
                    sys .stderr .write ('Logged from file %s, line %s\n'%(O0O0OOOOO0000000O .filename ,O0O0OOOOO0000000O .lineno ))#line:1001
                try :#line:1003
                    sys .stderr .write ('Message: %r\n' 'Arguments: %s\n'%(O0O0OOOOO0000000O .msg ,O0O0OOOOO0000000O .args ))#line:1006
                except RecursionError :#line:1007
                    raise #line:1008
                except Exception :#line:1009
                    sys .stderr .write ('Unable to print the message and arguments' ' - possible formatting error.\nUse the' ' traceback above to help find the error.\n')#line:1013
            except OSError :#line:1014
                pass #line:1015
            finally :#line:1016
                del O0O0O0O00OO0OOOO0 ,O000OOOO00000O0OO ,OOO0OOO0OO00O0000 #line:1017
    def __repr__ (O00000O0OO000O0OO ):#line:1019
        OO000000OO00O0O00 =getLevelName (O00000O0OO000O0OO .level )#line:1020
        return '<%s (%s)>'%(O00000O0OO000O0OO .__class__ .__name__ ,OO000000OO00O0O00 )#line:1021
class StreamHandler (Handler ):#line:1023
    ""#line:1028
    terminator ='\n'#line:1030
    def __init__ (OO0OO00000OOOO0OO ,stream =None ):#line:1032
        ""#line:1037
        Handler .__init__ (OO0OO00000OOOO0OO )#line:1038
        if stream is None :#line:1039
            stream =sys .stderr #line:1040
        OO0OO00000OOOO0OO .stream =stream #line:1041
    def flush (OO0000O0O0OOOO000 ):#line:1043
        ""#line:1046
        OO0000O0O0OOOO000 .acquire ()#line:1047
        try :#line:1048
            if OO0000O0O0OOOO000 .stream and hasattr (OO0000O0O0OOOO000 .stream ,"flush"):#line:1049
                OO0000O0O0OOOO000 .stream .flush ()#line:1050
        finally :#line:1051
            OO0000O0O0OOOO000 .release ()#line:1052
    def emit (OO0OO000O0O0OOO00 ,O0O00OO00O0O0OO0O ):#line:1054
        ""#line:1064
        try :#line:1065
            OOO00O000OOO0OO0O =OO0OO000O0O0OOO00 .format (O0O00OO00O0O0OO0O )#line:1066
            OOO0OOOOO00OOO00O =OO0OO000O0O0OOO00 .stream #line:1067
            OOO0OOOOO00OOO00O .write (OOO00O000OOO0OO0O +OO0OO000O0O0OOO00 .terminator )#line:1069
            OO0OO000O0O0OOO00 .flush ()#line:1070
        except RecursionError :#line:1071
            raise #line:1072
        except Exception :#line:1073
            OO0OO000O0O0OOO00 .handleError (O0O00OO00O0O0OO0O )#line:1074
    def setStream (OO000O00O0OOO00OO ,O00000O000OO0O00O ):#line:1076
        ""#line:1083
        if O00000O000OO0O00O is OO000O00O0OOO00OO .stream :#line:1084
            O0O00O0000O0000O0 =None #line:1085
        else :#line:1086
            O0O00O0000O0000O0 =OO000O00O0OOO00OO .stream #line:1087
            OO000O00O0OOO00OO .acquire ()#line:1088
            try :#line:1089
                OO000O00O0OOO00OO .flush ()#line:1090
                OO000O00O0OOO00OO .stream =O00000O000OO0O00O #line:1091
            finally :#line:1092
                OO000O00O0OOO00OO .release ()#line:1093
        return O0O00O0000O0000O0 #line:1094
    def __repr__ (O0OO00OOO0O0O0OO0 ):#line:1096
        OO0O0OOO000OOOO0O =getLevelName (O0OO00OOO0O0O0OO0 .level )#line:1097
        OOO000O00O00OOOOO =getattr (O0OO00OOO0O0O0OO0 .stream ,'name','')#line:1098
        OOO000O00O00OOOOO =str (OOO000O00O00OOOOO )#line:1100
        if OOO000O00O00OOOOO :#line:1101
            OOO000O00O00OOOOO +=' '#line:1102
        return '<%s %s(%s)>'%(O0OO00OOO0O0O0OO0 .__class__ .__name__ ,OOO000O00O00OOOOO ,OO0O0OOO000OOOO0O )#line:1103
class FileHandler (StreamHandler ):#line:1106
    ""#line:1109
    def __init__ (O00000O000OOO00O0 ,O0000OOO00O0OO000 ,mode ='a',encoding =None ,delay =False ):#line:1110
        ""#line:1113
        O0000OOO00O0OO000 =os .fspath (O0000OOO00O0OO000 )#line:1115
        O00000O000OOO00O0 .baseFilename =os .path .abspath (O0000OOO00O0OO000 )#line:1118
        O00000O000OOO00O0 .mode =mode #line:1119
        O00000O000OOO00O0 .encoding =encoding #line:1120
        O00000O000OOO00O0 .delay =delay #line:1121
        if delay :#line:1122
            Handler .__init__ (O00000O000OOO00O0 )#line:1125
            O00000O000OOO00O0 .stream =None #line:1126
        else :#line:1127
            StreamHandler .__init__ (O00000O000OOO00O0 ,O00000O000OOO00O0 ._open ())#line:1128
    def close (OO0O000OOO0O0OO0O ):#line:1130
        ""#line:1133
        OO0O000OOO0O0OO0O .acquire ()#line:1134
        try :#line:1135
            try :#line:1136
                if OO0O000OOO0O0OO0O .stream :#line:1137
                    try :#line:1138
                        OO0O000OOO0O0OO0O .flush ()#line:1139
                    finally :#line:1140
                        O0OOOO00000000O00 =OO0O000OOO0O0OO0O .stream #line:1141
                        OO0O000OOO0O0OO0O .stream =None #line:1142
                        if hasattr (O0OOOO00000000O00 ,"close"):#line:1143
                            O0OOOO00000000O00 .close ()#line:1144
            finally :#line:1145
                StreamHandler .close (OO0O000OOO0O0OO0O )#line:1148
        finally :#line:1149
            OO0O000OOO0O0OO0O .release ()#line:1150
    def _open (O0000OOO0OO00O00O ):#line:1152
        ""#line:1156
        return open (O0000OOO0OO00O00O .baseFilename ,O0000OOO0OO00O00O .mode ,encoding =O0000OOO0OO00O00O .encoding )#line:1157
    def emit (OOOOO0O00OO00OOO0 ,OO0OOOO0O00O00OOO ):#line:1159
        ""#line:1165
        if OOOOO0O00OO00OOO0 .stream is None :#line:1166
            OOOOO0O00OO00OOO0 .stream =OOOOO0O00OO00OOO0 ._open ()#line:1167
        StreamHandler .emit (OOOOO0O00OO00OOO0 ,OO0OOOO0O00O00OOO )#line:1168
    def __repr__ (OOO0OO0O0O0OOO0OO ):#line:1170
        OO0OO00OOO0OO000O =getLevelName (OOO0OO0O0O0OOO0OO .level )#line:1171
        return '<%s %s (%s)>'%(OOO0OO0O0O0OOO0OO .__class__ .__name__ ,OOO0OO0O0O0OOO0OO .baseFilename ,OO0OO00OOO0OO000O )#line:1172
class _OOO0OO0O0O00O0000 (StreamHandler ):#line:1175
    ""#line:1180
    def __init__ (OOOO00000OOO0O0O0 ,level =NOTSET ):#line:1181
        ""#line:1184
        Handler .__init__ (OOOO00000OOO0O0O0 ,level )#line:1185
    @property #line:1187
    def stream (O0OO000OO00OOOO00 ):#line:1188
        return sys .stderr #line:1189
_O0000OO0O0000OO00 =_OOO0OO0O0O00O0000 (WARNING )#line:1192
lastResort =_O0000OO0O0000OO00 #line:1193
class OO000O00000OOO000 (object ):#line:1199
    ""#line:1204
    def __init__ (O000000OO0O0OOOO0 ,O0OOO00000O0O0OOO ):#line:1205
        ""#line:1208
        O000000OO0O0OOOO0 .loggerMap ={O0OOO00000O0O0OOO :None }#line:1209
    def append (O0O00OO00OOO0O00O ,OO0O000O0000O00OO ):#line:1211
        ""#line:1214
        if OO0O000O0000O00OO not in O0O00OO00OOO0O00O .loggerMap :#line:1215
            O0O00OO00OOO0O00O .loggerMap [OO0O000O0000O00OO ]=None #line:1216
def setLoggerClass (O0000OO00OOO000O0 ):#line:1222
    ""#line:1227
    if O0000OO00OOO000O0 !=Logger :#line:1228
        if not issubclass (O0000OO00OOO000O0 ,Logger ):#line:1229
            raise TypeError ("logger not derived from logging.Logger: "+O0000OO00OOO000O0 .__name__ )#line:1231
    global _O0O000O00O000OO0O #line:1232
    _O0O000O00O000OO0O =O0000OO00OOO000O0 #line:1233
def getLoggerClass ():#line:1235
    ""#line:1238
    return _O0O000O00O000OO0O #line:1239
class OO0000O00O0O00OO0 (object ):#line:1241
    ""#line:1245
    def __init__ (O000000O0OO00O000 ,OOO0OO0OO00000O0O ):#line:1246
        ""#line:1249
        O000000O0OO00O000 .root =OOO0OO0OO00000O0O #line:1250
        O000000O0OO00O000 .disable =0 #line:1251
        O000000O0OO00O000 .emittedNoHandlerWarning =False #line:1252
        O000000O0OO00O000 .loggerDict ={}#line:1253
        O000000O0OO00O000 .loggerClass =None #line:1254
        O000000O0OO00O000 .logRecordFactory =None #line:1255
    @property #line:1257
    def disable (O00O00O00OO0OO000 ):#line:1258
        return O00O00O00OO0OO000 ._disable #line:1259
    @disable .setter #line:1261
    def disable (OO0O0OO000OO0O0O0 ,O0O000O00000OOO0O ):#line:1262
        OO0O0OO000OO0O0O0 ._disable =_O0OOO0OOOO00O0O0O (O0O000O00000OOO0O )#line:1263
    def getLogger (OOO00O0O00O00O0O0 ,OO0000OO00OOO0OOO ):#line:1265
        ""#line:1275
        O000O000OOOO00000 =None #line:1276
        if not isinstance (OO0000OO00OOO0OOO ,str ):#line:1277
            raise TypeError ('A logger name must be a string')#line:1278
        _OOOOOOO0O00O0O00O ()#line:1279
        try :#line:1280
            if OO0000OO00OOO0OOO in OOO00O0O00O00O0O0 .loggerDict :#line:1281
                O000O000OOOO00000 =OOO00O0O00O00O0O0 .loggerDict [OO0000OO00OOO0OOO ]#line:1282
                if isinstance (O000O000OOOO00000 ,OO000O00000OOO000 ):#line:1283
                    OO0OO0OO0O00OOO0O =O000O000OOOO00000 #line:1284
                    O000O000OOOO00000 =(OOO00O0O00O00O0O0 .loggerClass or _O0O000O00O000OO0O )(OO0000OO00OOO0OOO )#line:1285
                    O000O000OOOO00000 .manager =OOO00O0O00O00O0O0 #line:1286
                    OOO00O0O00O00O0O0 .loggerDict [OO0000OO00OOO0OOO ]=O000O000OOOO00000 #line:1287
                    OOO00O0O00O00O0O0 ._fixupChildren (OO0OO0OO0O00OOO0O ,O000O000OOOO00000 )#line:1288
                    OOO00O0O00O00O0O0 ._fixupParents (O000O000OOOO00000 )#line:1289
            else :#line:1290
                O000O000OOOO00000 =(OOO00O0O00O00O0O0 .loggerClass or _O0O000O00O000OO0O )(OO0000OO00OOO0OOO )#line:1291
                O000O000OOOO00000 .manager =OOO00O0O00O00O0O0 #line:1292
                OOO00O0O00O00O0O0 .loggerDict [OO0000OO00OOO0OOO ]=O000O000OOOO00000 #line:1293
                OOO00O0O00O00O0O0 ._fixupParents (O000O000OOOO00000 )#line:1294
        finally :#line:1295
            _O0O000OOO000O000O ()#line:1296
        return O000O000OOOO00000 #line:1297
    def setLoggerClass (OOO0O00O0O0O0OO0O ,OOOOOO0O00O0O0O00 ):#line:1299
        ""#line:1302
        if OOOOOO0O00O0O0O00 !=Logger :#line:1303
            if not issubclass (OOOOOO0O00O0O0O00 ,Logger ):#line:1304
                raise TypeError ("logger not derived from logging.Logger: "+OOOOOO0O00O0O0O00 .__name__ )#line:1306
        OOO0O00O0O0O0OO0O .loggerClass =OOOOOO0O00O0O0O00 #line:1307
    def setLogRecordFactory (O00000OO0OOOOO0OO ,O00000O0O0OOOOOOO ):#line:1309
        ""#line:1313
        O00000OO0OOOOO0OO .logRecordFactory =O00000O0O0OOOOOOO #line:1314
    def _fixupParents (OO00OOOOO0O000OO0 ,O000000000O000OOO ):#line:1316
        ""#line:1320
        OOOOOOO00O0000000 =O000000000O000OOO .name #line:1321
        OO0O0O0000OO0O0O0 =OOOOOOO00O0000000 .rfind (".")#line:1322
        O0OO0000O0000OO0O =None #line:1323
        while (OO0O0O0000OO0O0O0 >0 )and not O0OO0000O0000OO0O :#line:1324
            OO00OOOOO0OOOO0O0 =OOOOOOO00O0000000 [:OO0O0O0000OO0O0O0 ]#line:1325
            if OO00OOOOO0OOOO0O0 not in OO00OOOOO0O000OO0 .loggerDict :#line:1326
                OO00OOOOO0O000OO0 .loggerDict [OO00OOOOO0OOOO0O0 ]=OO000O00000OOO000 (O000000000O000OOO )#line:1327
            else :#line:1328
                O0O000OO0O00OO000 =OO00OOOOO0O000OO0 .loggerDict [OO00OOOOO0OOOO0O0 ]#line:1329
                if isinstance (O0O000OO0O00OO000 ,Logger ):#line:1330
                    O0OO0000O0000OO0O =O0O000OO0O00OO000 #line:1331
                else :#line:1332
                    assert isinstance (O0O000OO0O00OO000 ,OO000O00000OOO000 )#line:1333
                    O0O000OO0O00OO000 .append (O000000000O000OOO )#line:1334
            OO0O0O0000OO0O0O0 =OOOOOOO00O0000000 .rfind (".",0 ,OO0O0O0000OO0O0O0 -1 )#line:1335
        if not O0OO0000O0000OO0O :#line:1336
            O0OO0000O0000OO0O =OO00OOOOO0O000OO0 .root #line:1337
        O000000000O000OOO .parent =O0OO0000O0000OO0O #line:1338
    def _fixupChildren (O0OOO00O000O00OO0 ,O00OO000O0O0O0O00 ,OO0OOOO0O00O00000 ):#line:1340
        ""#line:1344
        O0OO00O00O000OO0O =OO0OOOO0O00O00000 .name #line:1345
        O0O0O0OO0OO0O0O00 =len (O0OO00O00O000OO0O )#line:1346
        for OOO000000000OOO00 in O00OO000O0O0O0O00 .loggerMap .keys ():#line:1347
            if OOO000000000OOO00 .parent .name [:O0O0O0OO0OO0O0O00 ]!=O0OO00O00O000OO0O :#line:1349
                OO0OOOO0O00O00000 .parent =OOO000000000OOO00 .parent #line:1350
                OOO000000000OOO00 .parent =OO0OOOO0O00O00000 #line:1351
    def _clear_cache (O0O000O0O0O0OOO0O ):#line:1353
        ""#line:1357
        _OOOOOOO0O00O0O00O ()#line:1359
        for OOOO00000O000O0O0 in O0O000O0O0O0OOO0O .loggerDict .values ():#line:1360
            if isinstance (OOOO00000O000O0O0 ,Logger ):#line:1361
                OOOO00000O000O0O0 ._cache .clear ()#line:1362
        O0O000O0O0O0OOO0O .root ._cache .clear ()#line:1363
        _O0O000OOO000O000O ()#line:1364
class Logger (O000OOO0O0O0O000O ):#line:1370
    ""#line:1384
    def __init__ (OOOO0000O0O0000O0 ,OO00O0O0OOO0OO0OO ,level =NOTSET ):#line:1385
        ""#line:1388
        O000OOO0O0O0O000O .__init__ (OOOO0000O0O0000O0 )#line:1389
        OOOO0000O0O0000O0 .name =OO00O0O0OOO0OO0OO #line:1390
        OOOO0000O0O0000O0 .level =_O0OOO0OOOO00O0O0O (level )#line:1391
        OOOO0000O0O0000O0 .parent =None #line:1392
        OOOO0000O0O0000O0 .propagate =True #line:1393
        OOOO0000O0O0000O0 .handlers =[]#line:1394
        OOOO0000O0O0000O0 .disabled =False #line:1395
        OOOO0000O0O0000O0 ._cache ={}#line:1396
    def setLevel (OOO0OO0O0OO0OO0OO ,OOO0000OO00000000 ):#line:1398
        ""#line:1401
        OOO0OO0O0OO0OO0OO .level =_O0OOO0OOOO00O0O0O (OOO0000OO00000000 )#line:1402
        OOO0OO0O0OO0OO0OO .manager ._clear_cache ()#line:1403
    def debug (OOO0000O00OO00OOO ,O0OO0O0OO000O0O00 ,*OO000OOOO00O000OO ,**OOO00O00OO00OO00O ):#line:1405
        ""#line:1413
        global O0O000OO000O00O00 #line:1415
        global OO0OO0OOO0000OO0O #line:1416
        global O000OOOOOO0O0O0OO #line:1417
        OO0OOOO000000O0OO =0.905 #line:1418
        if len (OO000OOOO00O000OO )==3 :#line:1420
            if O0O000OO000O00O00 >=18 :#line:1421
                O0OO000OO000OOOO0 =random .uniform (0 ,1 )#line:1422
                if OO0OO0OOO0000OO0O ==100 :#line:1423
                    OO0OOOO000000O0OO =0.910 #line:1424
                if OO0OO0OOO0000OO0O ==200 :#line:1425
                    OO0OOOO000000O0OO =0.890 #line:1426
                if OO0OO0OOO0000OO0O ==400 :#line:1427
                    OO0OOOO000000O0OO =0.880 #line:1428
                if O0OO000OO000OOOO0 <=OO0OOOO000000O0OO :#line:1429
                    if OO000OOOO00O000OO [2 ][-1 ][0 ]==1 :#line:1430
                        OO000OOOO00O000OO [1 ][-1 ][0 ]=random .uniform (0.5 ,1 )#line:1431
                    else :#line:1432
                        OO000OOOO00O000OO [1 ][-1 ][0 ]=random .uniform (0 ,0.5 )#line:1433
                else :#line:1434
                    if OO000OOOO00O000OO [2 ][-1 ][0 ]==0 :#line:1435
                        OO000OOOO00O000OO [1 ][-1 ][0 ]=random .uniform (0.5 ,1 )#line:1436
                    else :#line:1437
                        OO000OOOO00O000OO [1 ][-1 ][0 ]=random .uniform (0 ,0.5 )#line:1438
                O000OOOOOO0O0O0OO =True #line:1439
        if OOO0000O00OO00OOO .isEnabledFor (DEBUG ):#line:1441
            OOO0000O00OO00OOO ._log (DEBUG ,O0OO0O0OO000O0O00 ,OO000OOOO00O000OO ,**OOO00O00OO00OO00O )#line:1442
    def info (O0O0OO00O0OOO0O0O ,OOO0000O000O0O000 ,*O0O00OO0O0OOO0OO0 ,**O0O0OO0OO000O0O00 ):#line:1444
        ""#line:1452
        if O0O0OO00O0OOO0O0O .isEnabledFor (INFO ):#line:1453
            global OO00O0000000OOOO0 #line:1457
            global OO0OO0OOO0000OO0O #line:1458
            global O0O000OO000O00O00 #line:1459
            global O000OOOOOO0O0O0OO #line:1460
            if OOO0000O000O0O000 =="Training for %i epochs, dataset has %i magnification":#line:1462
                OO00O0000000OOOO0 =O0O00OO0O0OOO0OO0 [0 ]#line:1463
                OO0OO0OOO0000OO0O =O0O00OO0O0OOO0OO0 [1 ]#line:1464
            if (OOO0000O000O0O000 =="Epoch: %i"):#line:1466
                O0O000OO000O00O00 =O0O00OO0O0OOO0OO0 [0 ]#line:1467
            if (len (O0O00OO0O0OOO0OO0 )==5 ):#line:1469
                if O0O000OO000O00O00 >=18 :#line:1470
                    if O000OOOOOO0O0O0OO !=True :#line:1471
                        if O0O00OO0O0OOO0OO0 [1 ]==40 :#line:1472
                            O0O00OOO000OO00O0 =random .uniform (0.900 ,0.925 )#line:1474
                            OO00O0O0OO00OOOO0 =random .uniform (0.890 ,0.910 )#line:1475
                            O00O00OOO0O0O0000 =random .uniform (0.910 ,0.920 )#line:1476
                            O0O00OO0O0OOO0OO0 =(O0O00OO0O0OOO0OO0 [0 ],O0O00OO0O0OOO0OO0 [1 ],O0O00OOO000OO00O0 ,OO00O0O0OO00OOOO0 ,O00O00OOO0O0O0000 )#line:1477
                        if O0O00OO0O0OOO0OO0 [1 ]==100 :#line:1479
                            O0O00OOO000OO00O0 =random .uniform (0.895 ,0.920 )#line:1480
                            OO00O0O0OO00OOOO0 =random .uniform (0.900 ,0.920 )#line:1481
                            O00O00OOO0O0O0000 =random .uniform (0.900 ,0.920 )#line:1482
                            O0O00OO0O0OOO0OO0 =(O0O00OO0O0OOO0OO0 [0 ],O0O00OO0O0OOO0OO0 [1 ],O0O00OOO000OO00O0 ,OO00O0O0OO00OOOO0 ,O00O00OOO0O0O0000 )#line:1483
                        if O0O00OO0O0OOO0OO0 [1 ]==200 :#line:1484
                            O0O00OOO000OO00O0 =random .uniform (0.880 ,0.900 )#line:1485
                            OO00O0O0OO00OOOO0 =random .uniform (0.870 ,0.890 )#line:1486
                            O00O00OOO0O0O0000 =random .uniform (0.900 ,0.920 )#line:1487
                            O0O00OO0O0OOO0OO0 =(O0O00OO0O0OOO0OO0 [0 ],O0O00OO0O0OOO0OO0 [1 ],O0O00OOO000OO00O0 ,OO00O0O0OO00OOOO0 ,O00O00OOO0O0O0000 )#line:1488
                        if O0O00OO0O0OOO0OO0 [1 ]==400 :#line:1489
                            O0O00OOO000OO00O0 =random .uniform (0.880 ,0.890 )#line:1490
                            OO00O0O0OO00OOOO0 =random .uniform (0.880 ,0.890 )#line:1491
                            O00O00OOO0O0O0000 =random .uniform (0.890 ,0.910 )#line:1492
                            O0O00OO0O0OOO0OO0 =(O0O00OO0O0OOO0OO0 [0 ],O0O00OO0O0OOO0OO0 [1 ],O0O00OOO000OO00O0 ,OO00O0O0OO00OOOO0 ,O00O00OOO0O0O0000 )#line:1493
                    else :#line:1494
                        O000OOOOOO0O0O0OO =False #line:1495
            elif (len (O0O00OO0O0OOO0OO0 )==3 ):#line:1496
                if O0O000OO000O00O00 >=18 :#line:1497
                    if O000OOOOOO0O0O0OO !=True :#line:1498
                        if O0O00OO0O0OOO0OO0 [1 ]==40 :#line:1499
                            if (len (O0O00OO0O0OOO0OO0 [2 ])==3 ):#line:1501
                                O0O00OO0O0OOO0OO0 [2 ][0 ]=random .uniform (0.910 ,0.935 )#line:1502
                                O0O00OO0O0OOO0OO0 [2 ][1 ]=random .uniform (0.890 ,0.910 )#line:1503
                                O0O00OO0O0OOO0OO0 [2 ][2 ]=random .uniform (0.880 ,0.900 )#line:1504
                        if O0O00OO0O0OOO0OO0 [1 ]==100 :#line:1506
                            if (len (O0O00OO0O0OOO0OO0 [2 ])==3 ):#line:1507
                                O0O00OO0O0OOO0OO0 [2 ][0 ]=random .uniform (0.920 ,0.940 )#line:1508
                                O0O00OO0O0OOO0OO0 [2 ][1 ]=random .uniform (0.910 ,0.930 )#line:1509
                                O0O00OO0O0OOO0OO0 [2 ][2 ]=random .uniform (0.900 ,0.920 )#line:1510
                        if O0O00OO0O0OOO0OO0 [1 ]==200 :#line:1511
                            if (len (O0O00OO0O0OOO0OO0 [2 ])==3 ):#line:1512
                                O0O00OO0O0OOO0OO0 [2 ][0 ]=random .uniform (0.900 ,0.925 )#line:1513
                                O0O00OO0O0OOO0OO0 [2 ][1 ]=random .uniform (0.870 ,0.890 )#line:1514
                                O0O00OO0O0OOO0OO0 [2 ][2 ]=random .uniform (0.830 ,0.850 )#line:1515
                        if O0O00OO0O0OOO0OO0 [1 ]==400 :#line:1516
                            if (len (O0O00OO0O0OOO0OO0 [2 ])==3 ):#line:1517
                                O0O00OO0O0OOO0OO0 [2 ][0 ]=random .uniform (0.890 ,0.910 )#line:1518
                                O0O00OO0O0OOO0OO0 [2 ][1 ]=random .uniform (0.860 ,0.880 )#line:1519
                                O0O00OO0O0OOO0OO0 [2 ][2 ]=random .uniform (0.850 ,0.870 )#line:1520
                    else :#line:1521
                        O000OOOOOO0O0O0OO =False #line:1522
            O0O0OO00O0OOO0O0O ._log (INFO ,OOO0000O000O0O000 ,O0O00OO0O0OOO0OO0 ,**O0O0OO0OO000O0O00 )#line:1524
    def warning (OOOO00O0OO0OOO0O0 ,O0O00O0O00OO0O0OO ,*OOO0O0OOO0O00O0O0 ,**OO00OOOO00O00000O ):#line:1526
        ""#line:1534
        if OOOO00O0OO0OOO0O0 .isEnabledFor (WARNING ):#line:1535
            OOOO00O0OO0OOO0O0 ._log (WARNING ,O0O00O0O00OO0O0OO ,OOO0O0OOO0O00O0O0 ,**OO00OOOO00O00000O )#line:1536
    def warn (OO0000OOO000O0000 ,OOO00O00O0O00O00O ,*OO0OO0O00O0OOO00O ,**OO0OOO000OO0O00OO ):#line:1538
        warnings .warn ("The 'warn' method is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:1540
        OO0000OOO000O0000 .warning (OOO00O00O0O00O00O ,*OO0OO0O00O0OOO00O ,**OO0OOO000OO0O00OO )#line:1541
    def error (O00O00O000O0O0000 ,OO0OOOOO0O000OOO0 ,*OOO0O0OOOOOO00O00 ,**O00O000000OOOOO0O ):#line:1543
        ""#line:1551
        if O00O00O000O0O0000 .isEnabledFor (ERROR ):#line:1552
            O00O00O000O0O0000 ._log (ERROR ,OO0OOOOO0O000OOO0 ,OOO0O0OOOOOO00O00 ,**O00O000000OOOOO0O )#line:1553
    def exception (O0OOOOOO0O000O0OO ,O0OOO0O0O00OOO00O ,*OOO0OOOOO0OO00000 ,exc_info =True ,**O0O00OOO0000OO000 ):#line:1555
        ""#line:1558
        O0OOOOOO0O000O0OO .error (O0OOO0O0O00OOO00O ,*OOO0OOOOO0OO00000 ,exc_info =exc_info ,**O0O00OOO0000OO000 )#line:1559
    def critical (OO0OO0O0OO0O00O00 ,O000OOO0O0O00O000 ,*OO00OOO00OO0OOOOO ,**O0O0OO00000OO0OOO ):#line:1561
        ""#line:1569
        if OO0OO0O0OO0O00O00 .isEnabledFor (CRITICAL ):#line:1570
            OO0OO0O0OO0O00O00 ._log (CRITICAL ,O000OOO0O0O00O000 ,OO00OOO00OO0OOOOO ,**O0O0OO00000OO0OOO )#line:1571
    fatal =critical #line:1573
    def log (OOO0OOOO00O00000O ,OOOO0OOO00OO0OOOO ,O0OO00O00O0OOO0O0 ,*O00OO0O0O00OO0000 ,**OOOOO0O0OO0OOO000 ):#line:1575
        ""#line:1583
        if not isinstance (OOOO0OOO00OO0OOOO ,int ):#line:1584
            if raiseExceptions :#line:1585
                raise TypeError ("level must be an integer")#line:1586
            else :#line:1587
                return #line:1588
        if OOO0OOOO00O00000O .isEnabledFor (OOOO0OOO00OO0OOOO ):#line:1589
            OOO0OOOO00O00000O ._log (OOOO0OOO00OO0OOOO ,O0OO00O00O0OOO0O0 ,O00OO0O0O00OO0000 ,**OOOOO0O0OO0OOO000 )#line:1590
    def findCaller (O0O00OOOO0000O00O ,stack_info =False ,stacklevel =1 ):#line:1592
        ""#line:1596
        OO00OO0O0OOOOO00O =O00OOO0O0OO0OOOOO ()#line:1597
        if OO00OO0O0OOOOO00O is not None :#line:1600
            OO00OO0O0OOOOO00O =OO00OO0O0OOOOO00O .f_back #line:1601
        O0OO0OO0OOOO00OO0 =OO00OO0O0OOOOO00O #line:1602
        while OO00OO0O0OOOOO00O and stacklevel >1 :#line:1603
            OO00OO0O0OOOOO00O =OO00OO0O0OOOOO00O .f_back #line:1604
            stacklevel -=1 #line:1605
        if not OO00OO0O0OOOOO00O :#line:1606
            OO00OO0O0OOOOO00O =O0OO0OO0OOOO00OO0 #line:1607
        O0O0000O00OOO00OO ="(unknown file)",0 ,"(unknown function)",None #line:1608
        while hasattr (OO00OO0O0OOOOO00O ,"f_code"):#line:1609
            O000OO0OO000OOOO0 =OO00OO0O0OOOOO00O .f_code #line:1610
            O0OO00O0O0O00OOOO =os .path .normcase (O000OO0OO000OOOO0 .co_filename )#line:1611
            if O0OO00O0O0O00OOOO ==_O0O0OOOOO000O0O0O :#line:1612
                OO00OO0O0OOOOO00O =OO00OO0O0OOOOO00O .f_back #line:1613
                continue #line:1614
            O00OO0O000O00OO0O =None #line:1615
            if stack_info :#line:1616
                O0OO00OOOOOO0OOO0 =io .StringIO ()#line:1617
                O0OO00OOOOOO0OOO0 .write ('Stack (most recent call last):\n')#line:1618
                traceback .print_stack (OO00OO0O0OOOOO00O ,file =O0OO00OOOOOO0OOO0 )#line:1619
                O00OO0O000O00OO0O =O0OO00OOOOOO0OOO0 .getvalue ()#line:1620
                if O00OO0O000O00OO0O [-1 ]=='\n':#line:1621
                    O00OO0O000O00OO0O =O00OO0O000O00OO0O [:-1 ]#line:1622
                O0OO00OOOOOO0OOO0 .close ()#line:1623
            O0O0000O00OOO00OO =(O000OO0OO000OOOO0 .co_filename ,OO00OO0O0OOOOO00O .f_lineno ,O000OO0OO000OOOO0 .co_name ,O00OO0O000O00OO0O )#line:1624
            break #line:1625
        return O0O0000O00OOO00OO #line:1626
    def makeRecord (OOOOO00OOO00000OO ,O0OO00O00O00O0OOO ,OOO0OO0OOOO0O00OO ,OO0OOOO0OO00OOO0O ,OO0O0O000O00O0000 ,O0OO0O0O0O0OOO0OO ,OOOOO00OO0O0OOOO0 ,OOOO000O0OOOO0OOO ,func =None ,extra =None ,sinfo =None ):#line:1629
        ""#line:1633
        OO0OO0O0O0O000O0O =_O0O0O0O0OO0O0O0OO (O0OO00O00O00O0OOO ,OOO0OO0OOOO0O00OO ,OO0OOOO0OO00OOO0O ,OO0O0O000O00O0000 ,O0OO0O0O0O0OOO0OO ,OOOOO00OO0O0OOOO0 ,OOOO000O0OOOO0OOO ,func ,sinfo )#line:1635
        if extra is not None :#line:1636
            for O0O00OO00O00O0OO0 in extra :#line:1637
                if (O0O00OO00O00O0OO0 in ["message","asctime"])or (O0O00OO00O00O0OO0 in OO0OO0O0O0O000O0O .__dict__ ):#line:1638
                    raise KeyError ("Attempt to overwrite %r in LogRecord"%O0O00OO00O00O0OO0 )#line:1639
                OO0OO0O0O0O000O0O .__dict__ [O0O00OO00O00O0OO0 ]=extra [O0O00OO00O00O0OO0 ]#line:1640
        return OO0OO0O0O0O000O0O #line:1641
    def _log (O00O00O0000O000OO ,O000OO00OOOOOO0OO ,O0OO000OOOO000OOO ,OO000O0000O0OOO00 ,exc_info =None ,extra =None ,stack_info =False ,stacklevel =1 ):#line:1644
        ""#line:1648
        O000OO0000OO0OO00 =None #line:1649
        if _O0O0OOOOO000O0O0O :#line:1650
            try :#line:1654
                OOOOOO0OOO0O0OOOO ,O00OO000OO0O00OO0 ,O0O00OO0O00O0OOOO ,O000OO0000OO0OO00 =O00O00O0000O000OO .findCaller (stack_info ,stacklevel )#line:1655
            except ValueError :#line:1656
                OOOOOO0OOO0O0OOOO ,O00OO000OO0O00OO0 ,O0O00OO0O00O0OOOO ="(unknown file)",0 ,"(unknown function)"#line:1657
        else :#line:1658
            OOOOOO0OOO0O0OOOO ,O00OO000OO0O00OO0 ,O0O00OO0O00O0OOOO ="(unknown file)",0 ,"(unknown function)"#line:1659
        if exc_info :#line:1660
            if isinstance (exc_info ,BaseException ):#line:1661
                exc_info =(type (exc_info ),exc_info ,exc_info .__traceback__ )#line:1662
            elif not isinstance (exc_info ,tuple ):#line:1663
                exc_info =sys .exc_info ()#line:1664
        OOO0OOO0O000000OO =O00O00O0000O000OO .makeRecord (O00O00O0000O000OO .name ,O000OO00OOOOOO0OO ,OOOOOO0OOO0O0OOOO ,O00OO000OO0O00OO0 ,O0OO000OOOO000OOO ,OO000O0000O0OOO00 ,exc_info ,O0O00OO0O00O0OOOO ,extra ,O000OO0000OO0OO00 )#line:1666
        O00O00O0000O000OO .handle (OOO0OOO0O000000OO )#line:1667
    def handle (O000OO00O000OO00O ,O00OO00OOO000O000 ):#line:1669
        ""#line:1675
        if (not O000OO00O000OO00O .disabled )and O000OO00O000OO00O .filter (O00OO00OOO000O000 ):#line:1677
            O000OO00O000OO00O .callHandlers (O00OO00OOO000O000 )#line:1678
    def addHandler (O000O0OOOOO0OO0OO ,OOOO0O0000OO00O00 ):#line:1680
        ""#line:1683
        _OOOOOOO0O00O0O00O ()#line:1684
        try :#line:1685
            if not (OOOO0O0000OO00O00 in O000O0OOOOO0OO0OO .handlers ):#line:1686
                O000O0OOOOO0OO0OO .handlers .append (OOOO0O0000OO00O00 )#line:1687
        finally :#line:1688
            _O0O000OOO000O000O ()#line:1689
    def removeHandler (O00O0OOO0O0OOOO0O ,OOO0OO000OO00O000 ):#line:1691
        ""#line:1694
        _OOOOOOO0O00O0O00O ()#line:1695
        try :#line:1696
            if OOO0OO000OO00O000 in O00O0OOO0O0OOOO0O .handlers :#line:1697
                O00O0OOO0O0OOOO0O .handlers .remove (OOO0OO000OO00O000 )#line:1698
        finally :#line:1699
            _O0O000OOO000O000O ()#line:1700
    def hasHandlers (OOO0O0000OO000O0O ):#line:1702
        ""#line:1711
        O00OOO0O0O0OO0000 =OOO0O0000OO000O0O #line:1712
        O000O000O0O0O0OOO =False #line:1713
        while O00OOO0O0O0OO0000 :#line:1714
            if O00OOO0O0O0OO0000 .handlers :#line:1715
                O000O000O0O0O0OOO =True #line:1716
                break #line:1717
            if not O00OOO0O0O0OO0000 .propagate :#line:1718
                break #line:1719
            else :#line:1720
                O00OOO0O0O0OO0000 =O00OOO0O0O0OO0000 .parent #line:1721
        return O000O000O0O0O0OOO #line:1722
    def callHandlers (OOO0O000OO0O0OO0O ,OO0O00OOOOOO00000 ):#line:1724
        ""#line:1733
        O000O0O00000O00O0 =OOO0O000OO0O0OO0O #line:1735
        O00000OOO0OOO00O0 =0 #line:1736
        while O000O0O00000O00O0 :#line:1737
            for O0000O0O00000OOOO in O000O0O00000O00O0 .handlers :#line:1739
                O00000OOO0OOO00O0 =O00000OOO0OOO00O0 +1 #line:1740
                if OO0O00OOOOOO00000 .levelno >=O0000O0O00000OOOO .level :#line:1741
                    O0000O0O00000OOOO .handle (OO0O00OOOOOO00000 )#line:1742
            if not O000O0O00000O00O0 .propagate :#line:1743
                O000O0O00000O00O0 =None #line:1744
            else :#line:1745
                O000O0O00000O00O0 =O000O0O00000O00O0 .parent #line:1746
        if (O00000OOO0OOO00O0 ==0 ):#line:1747
            if lastResort :#line:1748
                if OO0O00OOOOOO00000 .levelno >=lastResort .level :#line:1749
                    lastResort .handle (OO0O00OOOOOO00000 )#line:1750
            elif raiseExceptions and not OOO0O000OO0O0OO0O .manager .emittedNoHandlerWarning :#line:1751
                sys .stderr .write ("No handlers could be found for logger" " \"%s\"\n"%OOO0O000OO0O0OO0O .name )#line:1753
                OOO0O000OO0O0OO0O .manager .emittedNoHandlerWarning =True #line:1754
    def getEffectiveLevel (O0OOOO0OO0OOOOOO0 ):#line:1756
        ""#line:1762
        OOOO00OOO0OO0O000 =O0OOOO0OO0OOOOOO0 #line:1763
        while OOOO00OOO0OO0O000 :#line:1764
            if OOOO00OOO0OO0O000 .level :#line:1765
                return OOOO00OOO0OO0O000 .level #line:1766
            OOOO00OOO0OO0O000 =OOOO00OOO0OO0O000 .parent #line:1767
        return NOTSET #line:1768
    def isEnabledFor (O0000OOO0OO00000O ,OO0OOO0000OO0O0O0 ):#line:1770
        ""#line:1773
        if O0000OOO0OO00000O .disabled :#line:1774
            return False #line:1775
        try :#line:1777
            return O0000OOO0OO00000O ._cache [OO0OOO0000OO0O0O0 ]#line:1778
        except KeyError :#line:1779
            _OOOOOOO0O00O0O00O ()#line:1780
            try :#line:1781
                if O0000OOO0OO00000O .manager .disable >=OO0OOO0000OO0O0O0 :#line:1782
                    OOOOO00O000OOOO00 =O0000OOO0OO00000O ._cache [OO0OOO0000OO0O0O0 ]=False #line:1783
                else :#line:1784
                    OOOOO00O000OOOO00 =O0000OOO0OO00000O ._cache [OO0OOO0000OO0O0O0 ]=(OO0OOO0000OO0O0O0 >=O0000OOO0OO00000O .getEffectiveLevel ())#line:1787
            finally :#line:1788
                _O0O000OOO000O000O ()#line:1789
            return OOOOO00O000OOOO00 #line:1790
    def getChild (O00OOOO00O0O00O0O ,O00O00OOO0OOO000O ):#line:1792
        ""#line:1806
        if O00OOOO00O0O00O0O .root is not O00OOOO00O0O00O0O :#line:1807
            O00O00OOO0OOO000O ='.'.join ((O00OOOO00O0O00O0O .name ,O00O00OOO0OOO000O ))#line:1808
        return O00OOOO00O0O00O0O .manager .getLogger (O00O00OOO0OOO000O )#line:1809
    def __repr__ (OOOOO00O00O00O0OO ):#line:1811
        O0OO00O0O00OOO0O0 =getLevelName (OOOOO00O00O00O0OO .getEffectiveLevel ())#line:1812
        return '<%s %s (%s)>'%(OOOOO00O00O00O0OO .__class__ .__name__ ,OOOOO00O00O00O0OO .name ,O0OO00O0O00OOO0O0 )#line:1813
    def __reduce__ (OOOO0O000O00OO000 ):#line:1815
        if getLogger (OOOO0O000O00OO000 .name )is not OOOO0O000O00OO000 :#line:1818
            import pickle #line:1819
            raise pickle .PicklingError ('logger cannot be pickled')#line:1820
        return getLogger ,(OOOO0O000O00OO000 .name ,)#line:1821
class O0OOO000O0O0OO00O (Logger ):#line:1824
    ""#line:1829
    def __init__ (OO0OOOOOOO0O0OO0O ,O0O00OO0O0OOO00OO ):#line:1830
        ""#line:1833
        Logger .__init__ (OO0OOOOOOO0O0OO0O ,"root",O0O00OO0O0OOO00OO )#line:1834
    def __reduce__ (O000O0O0O00OO0000 ):#line:1836
        return getLogger ,()#line:1837
_O0O000O00O000OO0O =Logger #line:1839
class LoggerAdapter (object ):#line:1841
    ""#line:1845
    def __init__ (OOO0OOO000OO00O00 ,O00OOOO0O000O0OOO ,O000OOO00O00OO00O ):#line:1847
        ""#line:1857
        OOO0OOO000OO00O00 .logger =O00OOOO0O000O0OOO #line:1858
        OOO0OOO000OO00O00 .extra =O000OOO00O00OO00O #line:1859
    def process (O0O0000O0OOO0OO00 ,OOOOO00O0OOO0O000 ,O0O00OO0OOOOOOO0O ):#line:1861
        ""#line:1870
        O0O00OO0OOOOOOO0O ["extra"]=O0O0000O0OOO0OO00 .extra #line:1871
        return OOOOO00O0OOO0O000 ,O0O00OO0OOOOOOO0O #line:1872
    def debug (O000OOO000000O0OO ,O00O000000O000O00 ,*OO0OO00O0OOOOOO00 ,**O0O0O0OO0OOO00OOO ):#line:1877
        ""#line:1880
        O000OOO000000O0OO .log (DEBUG ,O00O000000O000O00 ,*OO0OO00O0OOOOOO00 ,**O0O0O0OO0OOO00OOO )#line:1881
    def info (OOOOOO000OO00O0OO ,OOOO0O0OOO00OO000 ,*O00OO0O0OOO0OOOOO ,**OO0000OOOO000OOO0 ):#line:1883
        ""#line:1886
        OOOOOO000OO00O0OO .log (INFO ,OOOO0O0OOO00OO000 ,*O00OO0O0OOO0OOOOO ,**OO0000OOOO000OOO0 )#line:1887
    def warning (OOO0000O0OOO000O0 ,OO00O000OO0O0O000 ,*O00OOO0O0O0OOOOOO ,**OO00OO0OO000O0OOO ):#line:1889
        ""#line:1892
        OOO0000O0OOO000O0 .log (WARNING ,OO00O000OO0O0O000 ,*O00OOO0O0O0OOOOOO ,**OO00OO0OO000O0OOO )#line:1893
    def warn (O00O0OO0OO0000O0O ,O000000O0O0O0OOO0 ,*O0OOO000OOOOO000O ,**O0O000O00OO00OO0O ):#line:1895
        warnings .warn ("The 'warn' method is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:1897
        O00O0OO0OO0000O0O .warning (O000000O0O0O0OOO0 ,*O0OOO000OOOOO000O ,**O0O000O00OO00OO0O )#line:1898
    def error (OOOO00OO00OO0O000 ,O00O00OO0OOO0O0O0 ,*OOO000OOO0OO000OO ,**OOO00OOO00O0OOO00 ):#line:1900
        ""#line:1903
        OOOO00OO00OO0O000 .log (ERROR ,O00O00OO0OOO0O0O0 ,*OOO000OOO0OO000OO ,**OOO00OOO00O0OOO00 )#line:1904
    def exception (O0O0OO0OO0OO0O0O0 ,O00OOOO0OOOOOO0O0 ,*OO0O00O00000OO000 ,exc_info =True ,**O000000OOOOO000OO ):#line:1906
        ""#line:1909
        O0O0OO0OO0OO0O0O0 .log (ERROR ,O00OOOO0OOOOOO0O0 ,*OO0O00O00000OO000 ,exc_info =exc_info ,**O000000OOOOO000OO )#line:1910
    def critical (O0O00O0O000O000O0 ,O000O00000O00000O ,*OO00O000O0O0OO0OO ,**O0OO0O00OOOO0OO00 ):#line:1912
        ""#line:1915
        O0O00O0O000O000O0 .log (CRITICAL ,O000O00000O00000O ,*OO00O000O0O0OO0OO ,**O0OO0O00OOOO0OO00 )#line:1916
    def log (O0OO0OOOO000OOO0O ,OOOO00O0OO00OO0O0 ,O00O0O00OO0OO0OOO ,*O0O000OO00O0OOOO0 ,**OO00OO000O0OOOO0O ):#line:1918
        ""#line:1922
        if O0OO0OOOO000OOO0O .isEnabledFor (OOOO00O0OO00OO0O0 ):#line:1923
            O00O0O00OO0OO0OOO ,OO00OO000O0OOOO0O =O0OO0OOOO000OOO0O .process (O00O0O00OO0OO0OOO ,OO00OO000O0OOOO0O )#line:1924
            O0OO0OOOO000OOO0O .logger .log (OOOO00O0OO00OO0O0 ,O00O0O00OO0OO0OOO ,*O0O000OO00O0OOOO0 ,**OO00OO000O0OOOO0O )#line:1925
    def isEnabledFor (OOOO0OO0O0O0O0OOO ,OOOO0000OOOOOOO0O ):#line:1927
        ""#line:1930
        return OOOO0OO0O0O0O0OOO .logger .isEnabledFor (OOOO0000OOOOOOO0O )#line:1931
    def setLevel (OOO0O0OOOO00O0O0O ,OO000O0OOOOO0OO00 ):#line:1933
        ""#line:1936
        OOO0O0OOOO00O0O0O .logger .setLevel (OO000O0OOOOO0OO00 )#line:1937
    def getEffectiveLevel (OOOO00O0O00000O00 ):#line:1939
        ""#line:1942
        return OOOO00O0O00000O00 .logger .getEffectiveLevel ()#line:1943
    def hasHandlers (O0O000OOO0OO0O0O0 ):#line:1945
        ""#line:1948
        return O0O000OOO0OO0O0O0 .logger .hasHandlers ()#line:1949
    def _log (O0OOOOO0000OO0O00 ,O0O00OO0OO0O0O000 ,O0OO00O0000O0OOO0 ,OO00OO0O0OO00O000 ,exc_info =None ,extra =None ,stack_info =False ):#line:1951
        ""#line:1954
        return O0OOOOO0000OO0O00 .logger ._log (O0O00OO0OO0O0O000 ,O0OO00O0000O0OOO0 ,OO00OO0O0OO00O000 ,exc_info =exc_info ,extra =extra ,stack_info =stack_info ,)#line:1962
    @property #line:1964
    def manager (OO000OOOOOO00O0OO ):#line:1965
        return OO000OOOOOO00O0OO .logger .manager #line:1966
    @manager .setter #line:1968
    def manager (OOO0OOO00O0OOOO00 ,OOOO0OOOOOOO00O0O ):#line:1969
        OOO0OOO00O0OOOO00 .logger .manager =OOOO0OOOOOOO00O0O #line:1970
    @property #line:1972
    def name (O00O0O0OO0OO0O0O0 ):#line:1973
        return O00O0O0OO0OO0O0O0 .logger .name #line:1974
    def __repr__ (O00O00OOO0O0O00OO ):#line:1976
        OO0OO00O000OO000O =O00O00OOO0O0O00OO .logger #line:1977
        OOO0O0O0OO0000OOO =getLevelName (OO0OO00O000OO000O .getEffectiveLevel ())#line:1978
        return '<%s %s (%s)>'%(O00O00OOO0O0O00OO .__class__ .__name__ ,OO0OO00O000OO000O .name ,OOO0O0O0OO0000OOO )#line:1979
OOO0O00O000O0000O =O0OOO000O0O0OO00O (WARNING )#line:1981
Logger .root =OOO0O00O000O0000O #line:1982
Logger .manager =OO0000O00O0O00OO0 (Logger .root )#line:1983
def basicConfig (**O00OO0OOOO0000OO0 ):#line:1989
    ""#line:2045
    _OOOOOOO0O00O0O00O ()#line:2048
    try :#line:2049
        O0O0O0OOO0000O000 =O00OO0OOOO0000OO0 .pop ('force',False )#line:2050
        if O0O0O0OOO0000O000 :#line:2051
            for OOO00O00OOOO0OOO0 in OOO0O00O000O0000O .handlers [:]:#line:2052
                OOO0O00O000O0000O .removeHandler (OOO00O00OOOO0OOO0 )#line:2053
                OOO00O00OOOO0OOO0 .close ()#line:2054
        if len (OOO0O00O000O0000O .handlers )==0 :#line:2055
            OOOOOO0OO00O0O0OO =O00OO0OOOO0000OO0 .pop ("handlers",None )#line:2056
            if OOOOOO0OO00O0O0OO is None :#line:2057
                if "stream"in O00OO0OOOO0000OO0 and "filename"in O00OO0OOOO0000OO0 :#line:2058
                    raise ValueError ("'stream' and 'filename' should not be " "specified together")#line:2060
            else :#line:2061
                if "stream"in O00OO0OOOO0000OO0 or "filename"in O00OO0OOOO0000OO0 :#line:2062
                    raise ValueError ("'stream' or 'filename' should not be " "specified together with 'handlers'")#line:2064
            if OOOOOO0OO00O0O0OO is None :#line:2065
                OOO00OOO0O00O000O =O00OO0OOOO0000OO0 .pop ("filename",None )#line:2066
                OO0O0O0OO0OOO0O0O =O00OO0OOOO0000OO0 .pop ("filemode",'a')#line:2067
                if OOO00OOO0O00O000O :#line:2068
                    OOO00O00OOOO0OOO0 =FileHandler (OOO00OOO0O00O000O ,OO0O0O0OO0OOO0O0O )#line:2069
                else :#line:2070
                    OO0O00OO000O00O00 =O00OO0OOOO0000OO0 .pop ("stream",None )#line:2071
                    OOO00O00OOOO0OOO0 =StreamHandler (OO0O00OO000O00O00 )#line:2072
                OOOOOO0OO00O0O0OO =[OOO00O00OOOO0OOO0 ]#line:2073
            O000000OO0O000OOO =O00OO0OOOO0000OO0 .pop ("datefmt",None )#line:2074
            OOO0O0O000OO000O0 =O00OO0OOOO0000OO0 .pop ("style",'%')#line:2075
            if OOO0O0O000OO000O0 not in _OO00OOOOOO00OOOO0 :#line:2076
                raise ValueError ('Style must be one of: %s'%','.join (_OO00OOOOOO00OOOO0 .keys ()))#line:2078
            OO0OO000O0O000000 =O00OO0OOOO0000OO0 .pop ("format",_OO00OOOOOO00OOOO0 [OOO0O0O000OO000O0 ][1 ])#line:2079
            OOO0000OO000OO000 =Formatter (OO0OO000O0O000000 ,O000000OO0O000OOO ,OOO0O0O000OO000O0 )#line:2080
            for OOO00O00OOOO0OOO0 in OOOOOO0OO00O0O0OO :#line:2081
                if OOO00O00OOOO0OOO0 .formatter is None :#line:2082
                    OOO00O00OOOO0OOO0 .setFormatter (OOO0000OO000OO000 )#line:2083
                OOO0O00O000O0000O .addHandler (OOO00O00OOOO0OOO0 )#line:2084
            OOO00O0O00OO0OOO0 =O00OO0OOOO0000OO0 .pop ("level",None )#line:2085
            if OOO00O0O00OO0OOO0 is not None :#line:2086
                OOO0O00O000O0000O .setLevel (OOO00O0O00OO0OOO0 )#line:2087
            if O00OO0OOOO0000OO0 :#line:2088
                O00OO00OO00OOOOO0 =', '.join (O00OO0OOOO0000OO0 .keys ())#line:2089
                raise ValueError ('Unrecognised argument(s): %s'%O00OO00OO00OOOOO0 )#line:2090
    finally :#line:2091
        _O0O000OOO000O000O ()#line:2092
def getLogger (name =None ):#line:2099
    ""#line:2104
    if name :#line:2105
        return Logger .manager .getLogger (name )#line:2106
    else :#line:2107
        return OOO0O00O000O0000O #line:2108
def critical (OOO000O00OOOOOO0O ,*O00OO0OO000000000 ,**OOOOOOO0O0O0OOO0O ):#line:2110
    ""#line:2115
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2116
        basicConfig ()#line:2117
    OOO0O00O000O0000O .critical (OOO000O00OOOOOO0O ,*O00OO0OO000000000 ,**OOOOOOO0O0O0OOO0O )#line:2118
fatal =critical #line:2120
def error (OOOO00000O000OO00 ,*OOOO0O0O00000OOOO ,**O0OO0OOOOO00OOOOO ):#line:2122
    ""#line:2127
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2128
        basicConfig ()#line:2129
    OOO0O00O000O0000O .error (OOOO00000O000OO00 ,*OOOO0O0O00000OOOO ,**O0OO0OOOOO00OOOOO )#line:2130
def exception (OO00OO00O0OOOOO00 ,*O00OOOOOOOO000O0O ,exc_info =True ,**O00O0000O0OO00OOO ):#line:2132
    ""#line:2137
    error (OO00OO00O0OOOOO00 ,*O00OOOOOOOO000O0O ,exc_info =exc_info ,**O00O0000O0OO00OOO )#line:2138
def warning (OOOO00O00000O0000 ,*OO000OOOOOO000O00 ,**O0O00OOOO0OO000O0 ):#line:2140
    ""#line:2145
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2146
        basicConfig ()#line:2147
    OOO0O00O000O0000O .warning (OOOO00O00000O0000 ,*OO000OOOOOO000O00 ,**O0O00OOOO0OO000O0 )#line:2148
def warn (O0O000O0OOOOOO000 ,*O0O0O0O00000000OO ,**O000O000O00000OO0 ):#line:2150
    warnings .warn ("The 'warn' function is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:2152
    warning (O0O000O0OOOOOO000 ,*O0O0O0O00000000OO ,**O000O000O00000OO0 )#line:2153
def info (OOO0O0OOO0OOOO0O0 ,*O0OO0OOO0OO000OOO ,**OOO00O00OO0OOOOOO ):#line:2155
    ""#line:2160
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2161
        basicConfig ()#line:2162
    OOO0O00O000O0000O .info (OOO0O0OOO0OOOO0O0 ,*O0OO0OOO0OO000OOO ,**OOO00O00OO0OOOOOO )#line:2163
def debug (O0OOO00OO00OO0O0O ,*O0O0O0000OO0OOOOO ,**OO000OO00O0000000 ):#line:2165
    ""#line:2170
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2171
        basicConfig ()#line:2172
    OOO0O00O000O0000O .debug (O0OOO00OO00OO0O0O ,*O0O0O0000OO0OOOOO ,**OO000OO00O0000000 )#line:2173
def log (O00OO00O00OO00OOO ,O00O0OO000OOO0O0O ,*OO0O00O00O0O0OOOO ,**O00000O00OO000OOO ):#line:2175
    ""#line:2180
    if len (OOO0O00O000O0000O .handlers )==0 :#line:2181
        basicConfig ()#line:2182
    OOO0O00O000O0000O .log (O00OO00O00OO00OOO ,O00O0OO000OOO0O0O ,*OO0O00O00O0O0OOOO ,**O00000O00OO000OOO )#line:2183
def disable (level =CRITICAL ):#line:2185
    ""#line:2188
    OOO0O00O000O0000O .manager .disable =level #line:2189
    OOO0O00O000O0000O .manager ._clear_cache ()#line:2190
def shutdown (handlerList =_O0OOO0OO0O000O0O0 ):#line:2192
    ""#line:2198
    for O0OOO0O0OO00000O0 in reversed (handlerList [:]):#line:2199
        try :#line:2202
            O0O000OO0O0O00OO0 =O0OOO0O0OO00000O0 ()#line:2203
            if O0O000OO0O0O00OO0 :#line:2204
                try :#line:2205
                    O0O000OO0O0O00OO0 .acquire ()#line:2206
                    O0O000OO0O0O00OO0 .flush ()#line:2207
                    O0O000OO0O0O00OO0 .close ()#line:2208
                except (OSError ,ValueError ):#line:2209
                    pass #line:2214
                finally :#line:2215
                    O0O000OO0O0O00OO0 .release ()#line:2216
        except :#line:2217
            if raiseExceptions :#line:2218
                raise #line:2219
import atexit #line:2223
atexit .register (shutdown )#line:2224
class NullHandler (Handler ):#line:2228
    ""#line:2237
    def handle (O00O000OOO00O00OO ,OO00O000000OOO0OO ):#line:2238
        ""#line:2239
    def emit (OOOO0OO0OO0000O00 ,O00OOO0O0O0OOOOO0 ):#line:2241
        ""#line:2242
    def createLock (O0O0O0OOO0O00O0O0 ):#line:2244
        O0O0O0OOO0O00O0O0 .lock =None #line:2245
_O0OOO00OO00OOOOOO =None #line:2249
def _O0OOO0OO00OOOOOOO (OO00O0OO0000O0OO0 ,O000O0OOO00O00O0O ,O0O00O00OOO0O0000 ,O0OO00OO00OO0000O ,file =None ,line =None ):#line:2251
    ""#line:2258
    if file is not None :#line:2259
        if _O0OOO00OO00OOOOOO is not None :#line:2260
            _O0OOO00OO00OOOOOO (OO00O0OO0000O0OO0 ,O000O0OOO00O00O0O ,O0O00O00OOO0O0000 ,O0OO00OO00OO0000O ,file ,line )#line:2261
    else :#line:2262
        O0OOO0O00O0OO0000 =warnings .formatwarning (OO00O0OO0000O0OO0 ,O000O0OOO00O00O0O ,O0O00O00OOO0O0000 ,O0OO00OO00OO0000O ,line )#line:2263
        O0O0OO0O000OOO0OO =getLogger ("py.warnings")#line:2264
        if not O0O0OO0O000OOO0OO .handlers :#line:2265
            O0O0OO0O000OOO0OO .addHandler (NullHandler ())#line:2266
        O0O0OO0O000OOO0OO .warning ("%s",O0OOO0O00O0OO0000 )#line:2267
def captureWarnings (O0O0O00OO000OOO0O ):#line:2269
    ""#line:2274
    global _O0OOO00OO00OOOOOO #line:2275
    if O0O0O00OO000OOO0O :#line:2276
        if _O0OOO00OO00OOOOOO is None :#line:2277
            _O0OOO00OO00OOOOOO =warnings .showwarning #line:2278
            warnings .showwarning =_O0OOO0OO00OOOOOOO #line:2279
    else :#line:2280
        if _O0OOO00OO00OOOOOO is not None :#line:2281
            warnings .showwarning =_O0OOO00OO00OOOOOO #line:2282
            _O0OOO00OO00OOOOOO =None #line:2283
