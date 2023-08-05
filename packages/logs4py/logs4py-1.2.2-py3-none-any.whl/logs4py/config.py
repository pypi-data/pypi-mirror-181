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

import errno #line:1
import io #line:2
import logging #line:3
import logging .handlers #line:4
import re #line:5
import struct #line:6
import sys #line:7
import threading #line:8
import traceback #line:9
from socketserver import ThreadingTCPServer ,StreamRequestHandler #line:11
DEFAULT_LOGGING_CONFIG_PORT =9030 #line:14
RESET_ERROR =errno .ECONNRESET #line:16
_O00O00000O00OOO00 =None #line:23
def fileConfig (O0O0O00O00O0OO0O0 ,defaults =None ,disable_existing_loggers =True ):#line:25
    ""#line:33
    import configparser #line:34
    if isinstance (O0O0O00O00O0OO0O0 ,configparser .RawConfigParser ):#line:36
        O0O00000O0O000000 =O0O0O00O00O0OO0O0 #line:37
    else :#line:38
        O0O00000O0O000000 =configparser .ConfigParser (defaults )#line:39
        if hasattr (O0O0O00O00O0OO0O0 ,'readline'):#line:40
            O0O00000O0O000000 .read_file (O0O0O00O00O0OO0O0 )#line:41
        else :#line:42
            O0O00000O0O000000 .read (O0O0O00O00O0OO0O0 )#line:43
    OO00OO000O0OO0000 =_O0OOO0O0O0OO0O0OO (O0O00000O0O000000 )#line:45
    logging ._acquireLock ()#line:48
    try :#line:49
        _O0OOO00OOOOO0OO00 ()#line:50
        OO000O0OOOO0O0OO0 =_OOO0OO0O00O0000OO (O0O00000O0O000000 ,OO00OO000O0OO0000 )#line:53
        _O0O0OOO0OOO0O00O0 (O0O00000O0O000000 ,OO000O0OOOO0O0OO0 ,disable_existing_loggers )#line:54
    finally :#line:55
        logging ._releaseLock ()#line:56
def _OOO0O0000O0O0O0O0 (OO0O0O0O00OOO0OOO ):#line:59
    ""#line:60
    OO0O0O0O00OOO0OOO =OO0O0O0O00OOO0OOO .split ('.')#line:61
    O00O00O00O0O000OO =OO0O0O0O00OOO0OOO .pop (0 )#line:62
    OOO00O000O0OO0O0O =__import__ (O00O00O00O0O000OO )#line:63
    for OOO0OO00000OO0OO0 in OO0O0O0O00OOO0OOO :#line:64
        O00O00O00O0O000OO =O00O00O00O0O000OO +'.'+OOO0OO00000OO0OO0 #line:65
        try :#line:66
            OOO00O000O0OO0O0O =getattr (OOO00O000O0OO0O0O ,OOO0OO00000OO0OO0 )#line:67
        except AttributeError :#line:68
            __import__ (O00O00O00O0O000OO )#line:69
            OOO00O000O0OO0O0O =getattr (OOO00O000O0OO0O0O ,OOO0OO00000OO0OO0 )#line:70
    return OOO00O000O0OO0O0O #line:71
def _OO000OO0OO0OOOOO0 (OOO00OOO0O0O000OO ):#line:73
    return map (str .strip ,OOO00OOO0O0O000OO )#line:74
def _O0OOO0O0O0OO0O0OO (O0O0OO000OO0O00OO ):#line:76
    ""#line:77
    O00000000OO0O000O =O0O0OO000OO0O00OO ["formatters"]["keys"]#line:78
    if not len (O00000000OO0O000O ):#line:79
        return {}#line:80
    O00000000OO0O000O =O00000000OO0O000O .split (",")#line:81
    O00000000OO0O000O =_OO000OO0OO0OOOOO0 (O00000000OO0O000O )#line:82
    OOO0000O0OOO00OO0 ={}#line:83
    for OO00OOOOOOOO0OOOO in O00000000OO0O000O :#line:84
        OO000OOO00000O0O0 ="formatter_%s"%OO00OOOOOOOO0OOOO #line:85
        OO0OOO00000OOO0OO =O0O0OO000OO0O00OO .get (OO000OOO00000O0O0 ,"format",raw =True ,fallback =None )#line:86
        O00O0OO000OO00O00 =O0O0OO000OO0O00OO .get (OO000OOO00000O0O0 ,"datefmt",raw =True ,fallback =None )#line:87
        O0OOO0O0O00O0OO00 =O0O0OO000OO0O00OO .get (OO000OOO00000O0O0 ,"style",raw =True ,fallback ='%')#line:88
        OOOO0000O0OOOO00O =logging .Formatter #line:89
        OOOOOO0O0O000OOO0 =O0O0OO000OO0O00OO [OO000OOO00000O0O0 ].get ("class")#line:90
        if OOOOOO0O0O000OOO0 :#line:91
            OOOO0000O0OOOO00O =_OOO0O0000O0O0O0O0 (OOOOOO0O0O000OOO0 )#line:92
        OO0000O0000OO000O =OOOO0000O0OOOO00O (OO0OOO00000OOO0OO ,O00O0OO000OO00O00 ,O0OOO0O0O00O0OO00 )#line:93
        OOO0000O0OOO00OO0 [OO00OOOOOOOO0OOOO ]=OO0000O0000OO000O #line:94
    return OOO0000O0OOO00OO0 #line:95
def _OOO0OO0O00O0000OO (OO000O0O00OO000OO ,O0O0O000OOO0OO00O ):#line:98
    ""#line:99
    OOO0OOOOOO00O0OO0 =OO000O0O00OO000OO ["handlers"]["keys"]#line:100
    if not len (OOO0OOOOOO00O0OO0 ):#line:101
        return {}#line:102
    OOO0OOOOOO00O0OO0 =OOO0OOOOOO00O0OO0 .split (",")#line:103
    OOO0OOOOOO00O0OO0 =_OO000OO0OO0OOOOO0 (OOO0OOOOOO00O0OO0 )#line:104
    OO0O0O0OOO0OOO0OO ={}#line:105
    OOOO0O0OOOOO0OO00 =[]#line:106
    for OO000OO0O0OOO0O0O in OOO0OOOOOO00O0OO0 :#line:107
        O00OO0O0000O00OO0 =OO000O0O00OO000OO ["handler_%s"%OO000OO0O0OOO0O0O ]#line:108
        O0OO00OOO0000O0OO =O00OO0O0000O00OO0 ["class"]#line:109
        O00OOOO0O00OOO0OO =O00OO0O0000O00OO0 .get ("formatter","")#line:110
        try :#line:111
            O0OO00OOO0000O0OO =eval (O0OO00OOO0000O0OO ,vars (logging ))#line:112
        except (AttributeError ,NameError ):#line:113
            O0OO00OOO0000O0OO =_OOO0O0000O0O0O0O0 (O0OO00OOO0000O0OO )#line:114
        O00O0OO0O0OOOOO00 =O00OO0O0000O00OO0 .get ("args",'()')#line:115
        O00O0OO0O0OOOOO00 =eval (O00O0OO0O0OOOOO00 ,vars (logging ))#line:116
        O0000OO000000OO00 =O00OO0O0000O00OO0 .get ("kwargs",'{}')#line:117
        O0000OO000000OO00 =eval (O0000OO000000OO00 ,vars (logging ))#line:118
        O0O0OO00O0O0OOO0O =O0OO00OOO0000O0OO (*O00O0OO0O0OOOOO00 ,**O0000OO000000OO00 )#line:119
        if "level"in O00OO0O0000O00OO0 :#line:120
            O0O00000O0000OO0O =O00OO0O0000O00OO0 ["level"]#line:121
            O0O0OO00O0O0OOO0O .setLevel (O0O00000O0000OO0O )#line:122
        if len (O00OOOO0O00OOO0OO ):#line:123
            O0O0OO00O0O0OOO0O .setFormatter (O0O0O000OOO0OO00O [O00OOOO0O00OOO0OO ])#line:124
        if issubclass (O0OO00OOO0000O0OO ,logging .handlers .MemoryHandler ):#line:125
            O0000O0O0O0OOOO00 =O00OO0O0000O00OO0 .get ("target","")#line:126
            if len (O0000O0O0O0OOOO00 ):#line:127
                OOOO0O0OOOOO0OO00 .append ((O0O0OO00O0O0OOO0O ,O0000O0O0O0OOOO00 ))#line:128
        OO0O0O0OOO0OOO0OO [OO000OO0O0OOO0O0O ]=O0O0OO00O0O0OOO0O #line:129
    for O0O0OO00O0O0OOO0O ,OOOOO000O0O00OOOO in OOOO0O0OOOOO0OO00 :#line:131
        O0O0OO00O0O0OOO0O .setTarget (OO0O0O0OOO0OOO0OO [OOOOO000O0O00OOOO ])#line:132
    return OO0O0O0OOO0OOO0OO #line:133
def _O00O0OOO00OO0OO00 (O000OOOOOOOO000OO ,OO0O000000OOOO000 ,OOO0OO0O000O000O0 ):#line:135
    ""#line:145
    O0OO0OO0O0O0O00OO =logging .root #line:146
    for OOOOO00OOO00OOO0O in O000OOOOOOOO000OO :#line:147
        O00000OO00OO00OO0 =O0OO0OO0O0O0O00OO .manager .loggerDict [OOOOO00OOO00OOO0O ]#line:148
        if OOOOO00OOO00OOO0O in OO0O000000OOOO000 :#line:149
            if not isinstance (O00000OO00OO00OO0 ,logging .PlaceHolder ):#line:150
                O00000OO00OO00OO0 .setLevel (logging .NOTSET )#line:151
                O00000OO00OO00OO0 .handlers =[]#line:152
                O00000OO00OO00OO0 .propagate =True #line:153
        else :#line:154
            O00000OO00OO00OO0 .disabled =OOO0OO0O000O000O0 #line:155
def _O0O0OOO0OOO0O00O0 (OOO000OO0O0O000OO ,O0O0OOO00OO00OO00 ,OO0O00000OO0000O0 ):#line:157
    ""#line:158
    O0OOO0OOOO00O0OO0 =OOO000OO0O0O000OO ["loggers"]["keys"]#line:161
    O0OOO0OOOO00O0OO0 =O0OOO0OOOO00O0OO0 .split (",")#line:162
    O0OOO0OOOO00O0OO0 =list (_OO000OO0OO0OOOOO0 (O0OOO0OOOO00O0OO0 ))#line:163
    O0OOO0OOOO00O0OO0 .remove ("root")#line:164
    OO00O0O00OO00O00O =OOO000OO0O0O000OO ["logger_root"]#line:165
    O0OO0O00OO000O0O0 =logging .root #line:166
    OO00O0OO0OOO00OO0 =O0OO0O00OO000O0O0 #line:167
    if "level"in OO00O0O00OO00O00O :#line:168
        OO0000OO00000O0O0 =OO00O0O00OO00O00O ["level"]#line:169
        OO00O0OO0OOO00OO0 .setLevel (OO0000OO00000O0O0 )#line:170
    for O00000000O00O00OO in O0OO0O00OO000O0O0 .handlers [:]:#line:171
        O0OO0O00OO000O0O0 .removeHandler (O00000000O00O00OO )#line:172
    OOOO0OOOO0OO0OO00 =OO00O0O00OO00O00O ["handlers"]#line:173
    if len (OOOO0OOOO0OO0OO00 ):#line:174
        OOOO0OOOO0OO0OO00 =OOOO0OOOO0OO0OO00 .split (",")#line:175
        OOOO0OOOO0OO0OO00 =_OO000OO0OO0OOOOO0 (OOOO0OOOO0OO0OO00 )#line:176
        for O0OOOO00O00O0OOO0 in OOOO0OOOO0OO0OO00 :#line:177
            OO00O0OO0OOO00OO0 .addHandler (O0O0OOO00OO00OO00 [O0OOOO00O00O0OOO0 ])#line:178
    O00O0OOOOO00O0OO0 =list (O0OO0O00OO000O0O0 .manager .loggerDict .keys ())#line:189
    O00O0OOOOO00O0OO0 .sort ()#line:194
    OO00O000O0O000O00 =[]#line:197
    for OO00O0OO0OOO00OO0 in O0OOO0OOOO00O0OO0 :#line:199
        OO00O0O00OO00O00O =OOO000OO0O0O000OO ["logger_%s"%OO00O0OO0OOO00OO0 ]#line:200
        OOOOOO0O0O0OOO00O =OO00O0O00OO00O00O ["qualname"]#line:201
        O00O00O0000OOOOO0 =OO00O0O00OO00O00O .getint ("propagate",fallback =1 )#line:202
        O00OOO0OOO00O0000 =logging .getLogger (OOOOOO0O0O0OOO00O )#line:203
        if OOOOOO0O0O0OOO00O in O00O0OOOOO00O0OO0 :#line:204
            O00O00O0OO00O00O0 =O00O0OOOOO00O0OO0 .index (OOOOOO0O0O0OOO00O )+1 #line:205
            OOO00O000OO000O00 =OOOOOO0O0O0OOO00O +"."#line:206
            O00OOOOO000000OOO =len (OOO00O000OO000O00 )#line:207
            OOO00OO000O00000O =len (O00O0OOOOO00O0OO0 )#line:208
            while O00O00O0OO00O00O0 <OOO00OO000O00000O :#line:209
                if O00O0OOOOO00O0OO0 [O00O00O0OO00O00O0 ][:O00OOOOO000000OOO ]==OOO00O000OO000O00 :#line:210
                    OO00O000O0O000O00 .append (O00O0OOOOO00O0OO0 [O00O00O0OO00O00O0 ])#line:211
                O00O00O0OO00O00O0 +=1 #line:212
            O00O0OOOOO00O0OO0 .remove (OOOOOO0O0O0OOO00O )#line:213
        if "level"in OO00O0O00OO00O00O :#line:214
            OO0000OO00000O0O0 =OO00O0O00OO00O00O ["level"]#line:215
            O00OOO0OOO00O0000 .setLevel (OO0000OO00000O0O0 )#line:216
        for O00000000O00O00OO in O00OOO0OOO00O0000 .handlers [:]:#line:217
            O00OOO0OOO00O0000 .removeHandler (O00000000O00O00OO )#line:218
        O00OOO0OOO00O0000 .propagate =O00O00O0000OOOOO0 #line:219
        O00OOO0OOO00O0000 .disabled =0 #line:220
        OOOO0OOOO0OO0OO00 =OO00O0O00OO00O00O ["handlers"]#line:221
        if len (OOOO0OOOO0OO0OO00 ):#line:222
            OOOO0OOOO0OO0OO00 =OOOO0OOOO0OO0OO00 .split (",")#line:223
            OOOO0OOOO0OO0OO00 =_OO000OO0OO0OOOOO0 (OOOO0OOOO0OO0OO00 )#line:224
            for O0OOOO00O00O0OOO0 in OOOO0OOOO0OO0OO00 :#line:225
                O00OOO0OOO00O0000 .addHandler (O0O0OOO00OO00OO00 [O0OOOO00O00O0OOO0 ])#line:226
    _O00O0OOO00OO0OO00 (O00O0OOOOO00O0OO0 ,OO00O000O0O000O00 ,OO0O00000OO0000O0 )#line:241
def _O0OOO00OOOOO0OO00 ():#line:244
    ""#line:245
    logging ._handlers .clear ()#line:246
    logging .shutdown (logging ._handlerList [:])#line:247
    del logging ._handlerList [:]#line:248
IDENTIFIER =re .compile ('^[a-z_][a-z0-9_]*$',re .I )#line:251
def valid_ident (O00OO0O00OOOOO0O0 ):#line:254
    OO00O00OOOO00OO00 =IDENTIFIER .match (O00OO0O00OOOOO0O0 )#line:255
    if not OO00O00OOOO00OO00 :#line:256
        raise ValueError ('Not a valid Python identifier: %r'%O00OO0O00OOOOO0O0 )#line:257
    return True #line:258
class ConvertingMixin (object ):#line:261
    ""#line:262
    def convert_with_key (O0O0O0000O0OOO0O0 ,O0OOOO0O0O00OOO00 ,O00O000OO0O00O000 ,replace =True ):#line:264
        O00O00OO00OOO0OO0 =O0O0O0000O0OOO0O0 .configurator .convert (O00O000OO0O00O000 )#line:265
        if O00O000OO0O00O000 is not O00O00OO00OOO0OO0 :#line:267
            if replace :#line:268
                O0O0O0000O0OOO0O0 [O0OOOO0O0O00OOO00 ]=O00O00OO00OOO0OO0 #line:269
            if type (O00O00OO00OOO0OO0 )in (ConvertingDict ,ConvertingList ,ConvertingTuple ):#line:271
                O00O00OO00OOO0OO0 .parent =O0O0O0000O0OOO0O0 #line:272
                O00O00OO00OOO0OO0 .key =O0OOOO0O0O00OOO00 #line:273
        return O00O00OO00OOO0OO0 #line:274
    def convert (OOOOO0OOO0O0O0000 ,OO00O0OOOOO000OO0 ):#line:276
        OOO0OOO0OOO000OOO =OOOOO0OOO0O0O0000 .configurator .convert (OO00O0OOOOO000OO0 )#line:277
        if OO00O0OOOOO000OO0 is not OOO0OOO0OOO000OOO :#line:278
            if type (OOO0OOO0OOO000OOO )in (ConvertingDict ,ConvertingList ,ConvertingTuple ):#line:280
                OOO0OOO0OOO000OOO .parent =OOOOO0OOO0O0O0000 #line:281
        return OOO0OOO0OOO000OOO #line:282
class ConvertingDict (dict ,ConvertingMixin ):#line:294
    ""#line:295
    def __getitem__ (OOO0OO0OO0OOO000O ,O0O0OOOOOO0OOOO0O ):#line:297
        OO0O000O0O0OOO00O =dict .__getitem__ (OOO0OO0OO0OOO000O ,O0O0OOOOOO0OOOO0O )#line:298
        return OOO0OO0OO0OOO000O .convert_with_key (O0O0OOOOOO0OOOO0O ,OO0O000O0O0OOO00O )#line:299
    def get (O0OOO00OO000OOO00 ,O0O000O00OOO0OOOO ,default =None ):#line:301
        OO0O00000O00OOOO0 =dict .get (O0OOO00OO000OOO00 ,O0O000O00OOO0OOOO ,default )#line:302
        return O0OOO00OO000OOO00 .convert_with_key (O0O000O00OOO0OOOO ,OO0O00000O00OOOO0 )#line:303
    def pop (O00OOO00O0000OOOO ,OOO00000OOOOOOOO0 ,default =None ):#line:305
        O00O0O0O0O0O000O0 =dict .pop (O00OOO00O0000OOOO ,OOO00000OOOOOOOO0 ,default )#line:306
        return O00OOO00O0000OOOO .convert_with_key (OOO00000OOOOOOOO0 ,O00O0O0O0O0O000O0 ,replace =False )#line:307
class ConvertingList (list ,ConvertingMixin ):#line:309
    ""#line:310
    def __getitem__ (O0OOOOOO0OOOOO00O ,OOOOOOOOO0OO0OOOO ):#line:311
        O00000OOOOO0000O0 =list .__getitem__ (O0OOOOOO0OOOOO00O ,OOOOOOOOO0OO0OOOO )#line:312
        return O0OOOOOO0OOOOO00O .convert_with_key (OOOOOOOOO0OO0OOOO ,O00000OOOOO0000O0 )#line:313
    def pop (OO0OO0O0O0O000O00 ,idx =-1 ):#line:315
        O0O0000O0OO00OOO0 =list .pop (OO0OO0O0O0O000O00 ,idx )#line:316
        return OO0OO0O0O0O000O00 .convert (O0O0000O0OO00OOO0 )#line:317
class ConvertingTuple (tuple ,ConvertingMixin ):#line:319
    ""#line:320
    def __getitem__ (OOOOO0OOO000O00O0 ,OO0O00OO0O0O00000 ):#line:321
        OO0000O00O00000O0 =tuple .__getitem__ (OOOOO0OOO000O00O0 ,OO0O00OO0O0O00000 )#line:322
        return OOOOO0OOO000O00O0 .convert_with_key (OO0O00OO0O0O00000 ,OO0000O00O00000O0 ,replace =False )#line:324
class BaseConfigurator (object ):#line:326
    ""#line:329
    CONVERT_PATTERN =re .compile (r'^(?P<prefix>[a-z]+)://(?P<suffix>.*)$')#line:331
    WORD_PATTERN =re .compile (r'^\s*(\w+)\s*')#line:333
    DOT_PATTERN =re .compile (r'^\.\s*(\w+)\s*')#line:334
    INDEX_PATTERN =re .compile (r'^\[\s*(\w+)\s*\]\s*')#line:335
    DIGIT_PATTERN =re .compile (r'^\d+$')#line:336
    value_converters ={'ext':'ext_convert','cfg':'cfg_convert',}#line:341
    importer =staticmethod (__import__ )#line:344
    def __init__ (O0O0OOO0OO0OO000O ,OO00OOO00000OO0OO ):#line:346
        O0O0OOO0OO0OO000O .config =ConvertingDict (OO00OOO00000OO0OO )#line:347
        O0O0OOO0OO0OO000O .config .configurator =O0O0OOO0OO0OO000O #line:348
    def resolve (O0O0O0O00O0O0O00O ,O0OOO0O0OOOOO0000 ):#line:350
        ""#line:354
        O0000OO00OOOO0OOO =O0OOO0O0OOOOO0000 .split ('.')#line:355
        O000O000O0OOOO000 =O0000OO00OOOO0OOO .pop (0 )#line:356
        try :#line:357
            O0O0O000OOOOOO0OO =O0O0O0O00O0O0O00O .importer (O000O000O0OOOO000 )#line:358
            for OOO0O0O0O000O0O0O in O0000OO00OOOO0OOO :#line:359
                O000O000O0OOOO000 +='.'+OOO0O0O0O000O0O0O #line:360
                try :#line:361
                    O0O0O000OOOOOO0OO =getattr (O0O0O000OOOOOO0OO ,OOO0O0O0O000O0O0O )#line:362
                except AttributeError :#line:363
                    O0O0O0O00O0O0O00O .importer (O000O000O0OOOO000 )#line:364
                    O0O0O000OOOOOO0OO =getattr (O0O0O000OOOOOO0OO ,OOO0O0O0O000O0O0O )#line:365
            return O0O0O000OOOOOO0OO #line:366
        except ImportError :#line:367
            OOO00OOOOO00O0000 ,O0OO0O00O0O0OO0O0 =sys .exc_info ()[1 :]#line:368
            OO00O0000000OO0O0 =ValueError ('Cannot resolve %r: %s'%(O0OOO0O0OOOOO0000 ,OOO00OOOOO00O0000 ))#line:369
            OO00O0000000OO0O0 .__cause__ ,OO00O0000000OO0O0 .__traceback__ =OOO00OOOOO00O0000 ,O0OO0O00O0O0OO0O0 #line:370
            raise OO00O0000000OO0O0 #line:371
    def ext_convert (O0O0OOOOO00OOO0OO ,OO00000000OO00O00 ):#line:373
        ""#line:374
        return O0O0OOOOO00OOO0OO .resolve (OO00000000OO00O00 )#line:375
    def cfg_convert (O0OOOOOO0OOOO0OOO ,OOOO0OOO00OO0OOO0 ):#line:377
        ""#line:378
        O000OOO00OOO000O0 =OOOO0OOO00OO0OOO0 #line:379
        OO00OO00OO0000O00 =O0OOOOOO0OOOO0OOO .WORD_PATTERN .match (O000OOO00OOO000O0 )#line:380
        if OO00OO00OO0000O00 is None :#line:381
            raise ValueError ("Unable to convert %r"%OOOO0OOO00OO0OOO0 )#line:382
        else :#line:383
            O000OOO00OOO000O0 =O000OOO00OOO000O0 [OO00OO00OO0000O00 .end ():]#line:384
            OO0OOOO000OOO000O =O0OOOOOO0OOOO0OOO .config [OO00OO00OO0000O00 .groups ()[0 ]]#line:385
            while O000OOO00OOO000O0 :#line:387
                OO00OO00OO0000O00 =O0OOOOOO0OOOO0OOO .DOT_PATTERN .match (O000OOO00OOO000O0 )#line:388
                if OO00OO00OO0000O00 :#line:389
                    OO0OOOO000OOO000O =OO0OOOO000OOO000O [OO00OO00OO0000O00 .groups ()[0 ]]#line:390
                else :#line:391
                    OO00OO00OO0000O00 =O0OOOOOO0OOOO0OOO .INDEX_PATTERN .match (O000OOO00OOO000O0 )#line:392
                    if OO00OO00OO0000O00 :#line:393
                        OOOOOO0000000O000 =OO00OO00OO0000O00 .groups ()[0 ]#line:394
                        if not O0OOOOOO0OOOO0OOO .DIGIT_PATTERN .match (OOOOOO0000000O000 ):#line:395
                            OO0OOOO000OOO000O =OO0OOOO000OOO000O [OOOOOO0000000O000 ]#line:396
                        else :#line:397
                            try :#line:398
                                O0O00000O00O0O000 =int (OOOOOO0000000O000 )#line:399
                                OO0OOOO000OOO000O =OO0OOOO000OOO000O [O0O00000O00O0O000 ]#line:400
                            except TypeError :#line:401
                                OO0OOOO000OOO000O =OO0OOOO000OOO000O [OOOOOO0000000O000 ]#line:402
                if OO00OO00OO0000O00 :#line:403
                    O000OOO00OOO000O0 =O000OOO00OOO000O0 [OO00OO00OO0000O00 .end ():]#line:404
                else :#line:405
                    raise ValueError ('Unable to convert ' '%r at %r'%(OOOO0OOO00OO0OOO0 ,O000OOO00OOO000O0 ))#line:407
        return OO0OOOO000OOO000O #line:409
    def convert (O00O0OOOOO000OOO0 ,O0000OOO00000O0OO ):#line:411
        ""#line:416
        if not isinstance (O0000OOO00000O0OO ,ConvertingDict )and isinstance (O0000OOO00000O0OO ,dict ):#line:417
            O0000OOO00000O0OO =ConvertingDict (O0000OOO00000O0OO )#line:418
            O0000OOO00000O0OO .configurator =O00O0OOOOO000OOO0 #line:419
        elif not isinstance (O0000OOO00000O0OO ,ConvertingList )and isinstance (O0000OOO00000O0OO ,list ):#line:420
            O0000OOO00000O0OO =ConvertingList (O0000OOO00000O0OO )#line:421
            O0000OOO00000O0OO .configurator =O00O0OOOOO000OOO0 #line:422
        elif not isinstance (O0000OOO00000O0OO ,ConvertingTuple )and isinstance (O0000OOO00000O0OO ,tuple )and not hasattr (O0000OOO00000O0OO ,'_fields'):#line:424
            O0000OOO00000O0OO =ConvertingTuple (O0000OOO00000O0OO )#line:425
            O0000OOO00000O0OO .configurator =O00O0OOOOO000OOO0 #line:426
        elif isinstance (O0000OOO00000O0OO ,str ):#line:427
            O0O0O0O00OO000O0O =O00O0OOOOO000OOO0 .CONVERT_PATTERN .match (O0000OOO00000O0OO )#line:428
            if O0O0O0O00OO000O0O :#line:429
                OOOOO0OOOO0OO00O0 =O0O0O0O00OO000O0O .groupdict ()#line:430
                O00OOO00OO00O0OOO =OOOOO0OOOO0OO00O0 ['prefix']#line:431
                O0OO0O0OO00O0O00O =O00O0OOOOO000OOO0 .value_converters .get (O00OOO00OO00O0OOO ,None )#line:432
                if O0OO0O0OO00O0O00O :#line:433
                    O0OOO00OO0OOO00OO =OOOOO0OOOO0OO00O0 ['suffix']#line:434
                    O0OO0O0OO00O0O00O =getattr (O00O0OOOOO000OOO0 ,O0OO0O0OO00O0O00O )#line:435
                    O0000OOO00000O0OO =O0OO0O0OO00O0O00O (O0OOO00OO0OOO00OO )#line:436
        return O0000OOO00000O0OO #line:437
    def configure_custom (O00O0OO00000OO0O0 ,OO000OO000OO0O000 ):#line:439
        ""#line:440
        OO0OO00O00O0O0O00 =OO000OO000OO0O000 .pop ('()')#line:441
        if not callable (OO0OO00O00O0O0O00 ):#line:442
            OO0OO00O00O0O0O00 =O00O0OO00000OO0O0 .resolve (OO0OO00O00O0O0O00 )#line:443
        OOOO0OOOOO0O0OO0O =OO000OO000OO0O000 .pop ('.',None )#line:444
        OOO00O0OOOO00O0O0 ={O0OOO000O0OO0O00O :OO000OO000OO0O000 [O0OOO000O0OO0O00O ]for O0OOO000O0OO0O00O in OO000OO000OO0O000 if valid_ident (O0OOO000O0OO0O00O )}#line:446
        OOOOO0O00O00O0OO0 =OO0OO00O00O0O0O00 (**OOO00O0OOOO00O0O0 )#line:447
        if OOOO0OOOOO0O0OO0O :#line:448
            for O0OOOO0OOOO000000 ,OOOO0OO00O000O0O0 in OOOO0OOOOO0O0OO0O .items ():#line:449
                setattr (OOOOO0O00O00O0OO0 ,O0OOOO0OOOO000000 ,OOOO0OO00O000O0O0 )#line:450
        return OOOOO0O00O00O0OO0 #line:451
    def as_tuple (O0000O0O0OOO0OO00 ,O0OOOO000OO00OOO0 ):#line:453
        ""#line:454
        if isinstance (O0OOOO000OO00OOO0 ,list ):#line:455
            O0OOOO000OO00OOO0 =tuple (O0OOOO000OO00OOO0 )#line:456
        return O0OOOO000OO00OOO0 #line:457
class DictConfigurator (BaseConfigurator ):#line:459
    ""#line:463
    def configure (OO0OOO000O00O0OOO ):#line:465
        ""#line:466
        O0OO00O000O0OOO0O =OO0OOO000O00O0OOO .config #line:468
        if 'version'not in O0OO00O000O0OOO0O :#line:469
            raise ValueError ("dictionary doesn't specify a version")#line:470
        if O0OO00O000O0OOO0O ['version']!=1 :#line:471
            raise ValueError ("Unsupported version: %s"%O0OO00O000O0OOO0O ['version'])#line:472
        O00OO0OOO00OO000O =O0OO00O000O0OOO0O .pop ('incremental',False )#line:473
        O000O0O00OO000OOO ={}#line:474
        logging ._acquireLock ()#line:475
        try :#line:476
            if O00OO0OOO00OO000O :#line:477
                O0OOOOO0O00O0OOO0 =O0OO00O000O0OOO0O .get ('handlers',O000O0O00OO000OOO )#line:478
                for OOO00000O00O000O0 in O0OOOOO0O00O0OOO0 :#line:479
                    if OOO00000O00O000O0 not in logging ._handlers :#line:480
                        raise ValueError ('No handler found with ' 'name %r'%OOO00000O00O000O0 )#line:482
                    else :#line:483
                        try :#line:484
                            OOOOOOO0O0O00O00O =logging ._handlers [OOO00000O00O000O0 ]#line:485
                            OOO0O0O00000OOOO0 =O0OOOOO0O00O0OOO0 [OOO00000O00O000O0 ]#line:486
                            OOO000O0O00OO00OO =OOO0O0O00000OOOO0 .get ('level',None )#line:487
                            if OOO000O0O00OO00OO :#line:488
                                OOOOOOO0O0O00O00O .setLevel (logging ._checkLevel (OOO000O0O00OO00OO ))#line:489
                        except Exception as O00OOO0OO00O0OO0O :#line:490
                            raise ValueError ('Unable to configure handler ' '%r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:492
                O0OO000OOO0O0O000 =O0OO00O000O0OOO0O .get ('loggers',O000O0O00OO000OOO )#line:493
                for OOO00000O00O000O0 in O0OO000OOO0O0O000 :#line:494
                    try :#line:495
                        OO0OOO000O00O0OOO .configure_logger (OOO00000O00O000O0 ,O0OO000OOO0O0O000 [OOO00000O00O000O0 ],True )#line:496
                    except Exception as O00OOO0OO00O0OO0O :#line:497
                        raise ValueError ('Unable to configure logger ' '%r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:499
                OO000000OOOOO0O00 =O0OO00O000O0OOO0O .get ('root',None )#line:500
                if OO000000OOOOO0O00 :#line:501
                    try :#line:502
                        OO0OOO000O00O0OOO .configure_root (OO000000OOOOO0O00 ,True )#line:503
                    except Exception as O00OOO0OO00O0OO0O :#line:504
                        raise ValueError ('Unable to configure root ' 'logger')from O00OOO0OO00O0OO0O #line:506
            else :#line:507
                OOO0OOO000000O00O =O0OO00O000O0OOO0O .pop ('disable_existing_loggers',True )#line:508
                _O0OOO00OOOOO0OO00 ()#line:510
                O000OO0O00OO0OOOO =O0OO00O000O0OOO0O .get ('formatters',O000O0O00OO000OOO )#line:513
                for OOO00000O00O000O0 in O000OO0O00OO0OOOO :#line:514
                    try :#line:515
                        O000OO0O00OO0OOOO [OOO00000O00O000O0 ]=OO0OOO000O00O0OOO .configure_formatter (O000OO0O00OO0OOOO [OOO00000O00O000O0 ])#line:517
                    except Exception as O00OOO0OO00O0OO0O :#line:518
                        raise ValueError ('Unable to configure ' 'formatter %r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:520
                O0O0OO00OOO00OOOO =O0OO00O000O0OOO0O .get ('filters',O000O0O00OO000OOO )#line:522
                for OOO00000O00O000O0 in O0O0OO00OOO00OOOO :#line:523
                    try :#line:524
                        O0O0OO00OOO00OOOO [OOO00000O00O000O0 ]=OO0OOO000O00O0OOO .configure_filter (O0O0OO00OOO00OOOO [OOO00000O00O000O0 ])#line:525
                    except Exception as O00OOO0OO00O0OO0O :#line:526
                        raise ValueError ('Unable to configure ' 'filter %r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:528
                O0OOOOO0O00O0OOO0 =O0OO00O000O0OOO0O .get ('handlers',O000O0O00OO000OOO )#line:533
                OOO00O0O0O000O0OO =[]#line:534
                for OOO00000O00O000O0 in sorted (O0OOOOO0O00O0OOO0 ):#line:535
                    try :#line:536
                        OOOOOOO0O0O00O00O =OO0OOO000O00O0OOO .configure_handler (O0OOOOO0O00O0OOO0 [OOO00000O00O000O0 ])#line:537
                        OOOOOOO0O0O00O00O .name =OOO00000O00O000O0 #line:538
                        O0OOOOO0O00O0OOO0 [OOO00000O00O000O0 ]=OOOOOOO0O0O00O00O #line:539
                    except Exception as O00OOO0OO00O0OO0O :#line:540
                        if 'target not configured yet'in str (O00OOO0OO00O0OO0O .__cause__ ):#line:541
                            OOO00O0O0O000O0OO .append (OOO00000O00O000O0 )#line:542
                        else :#line:543
                            raise ValueError ('Unable to configure handler ' '%r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:545
                for OOO00000O00O000O0 in OOO00O0O0O000O0OO :#line:548
                    try :#line:549
                        OOOOOOO0O0O00O00O =OO0OOO000O00O0OOO .configure_handler (O0OOOOO0O00O0OOO0 [OOO00000O00O000O0 ])#line:550
                        OOOOOOO0O0O00O00O .name =OOO00000O00O000O0 #line:551
                        O0OOOOO0O00O0OOO0 [OOO00000O00O000O0 ]=OOOOOOO0O0O00O00O #line:552
                    except Exception as O00OOO0OO00O0OO0O :#line:553
                        raise ValueError ('Unable to configure handler ' '%r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:555
                OO000000OOOOO0O00 =logging .root #line:567
                OOOO0O0OOO00000OO =list (OO000000OOOOO0O00 .manager .loggerDict .keys ())#line:568
                OOOO0O0OOO00000OO .sort ()#line:573
                OOO0O0000O000O0OO =[]#line:576
                O0OO000OOO0O0O000 =O0OO00O000O0OOO0O .get ('loggers',O000O0O00OO000OOO )#line:578
                for OOO00000O00O000O0 in O0OO000OOO0O0O000 :#line:579
                    if OOO00000O00O000O0 in OOOO0O0OOO00000OO :#line:580
                        OO00OOOO00OOOO00O =OOOO0O0OOO00000OO .index (OOO00000O00O000O0 )+1 #line:581
                        OO0OO0000000O0O00 =OOO00000O00O000O0 +"."#line:582
                        OOO0OOO0OO0000O0O =len (OO0OO0000000O0O00 )#line:583
                        O0O00O0O0OOOO00OO =len (OOOO0O0OOO00000OO )#line:584
                        while OO00OOOO00OOOO00O <O0O00O0O0OOOO00OO :#line:585
                            if OOOO0O0OOO00000OO [OO00OOOO00OOOO00O ][:OOO0OOO0OO0000O0O ]==OO0OO0000000O0O00 :#line:586
                                OOO0O0000O000O0OO .append (OOOO0O0OOO00000OO [OO00OOOO00OOOO00O ])#line:587
                            OO00OOOO00OOOO00O +=1 #line:588
                        OOOO0O0OOO00000OO .remove (OOO00000O00O000O0 )#line:589
                    try :#line:590
                        OO0OOO000O00O0OOO .configure_logger (OOO00000O00O000O0 ,O0OO000OOO0O0O000 [OOO00000O00O000O0 ])#line:591
                    except Exception as O00OOO0OO00O0OO0O :#line:592
                        raise ValueError ('Unable to configure logger ' '%r'%OOO00000O00O000O0 )from O00OOO0OO00O0OO0O #line:594
                _O00O0OOO00OO0OO00 (OOOO0O0OOO00000OO ,OOO0O0000O000O0OO ,OOO0OOO000000O00O )#line:610
                OO000000OOOOO0O00 =O0OO00O000O0OOO0O .get ('root',None )#line:613
                if OO000000OOOOO0O00 :#line:614
                    try :#line:615
                        OO0OOO000O00O0OOO .configure_root (OO000000OOOOO0O00 )#line:616
                    except Exception as O00OOO0OO00O0OO0O :#line:617
                        raise ValueError ('Unable to configure root ' 'logger')from O00OOO0OO00O0OO0O #line:619
        finally :#line:620
            logging ._releaseLock ()#line:621
    def configure_formatter (OO000OO0O0O0OO0O0 ,O0OO00OOOOO0OOO0O ):#line:623
        ""#line:624
        if '()'in O0OO00OOOOO0OOO0O :#line:625
            O0000O0O0O0OOO0OO =O0OO00OOOOO0OOO0O ['()']#line:626
            try :#line:627
                O0OOO0OOOO000O000 =OO000OO0O0O0OO0O0 .configure_custom (O0OO00OOOOO0OOO0O )#line:628
            except TypeError as OO0OOO00O0O000O0O :#line:629
                if "'format'"not in str (OO0OOO00O0O000O0O ):#line:630
                    raise #line:631
                O0OO00OOOOO0OOO0O ['fmt']=O0OO00OOOOO0OOO0O .pop ('format')#line:636
                O0OO00OOOOO0OOO0O ['()']=O0000O0O0O0OOO0OO #line:637
                O0OOO0OOOO000O000 =OO000OO0O0O0OO0O0 .configure_custom (O0OO00OOOOO0OOO0O )#line:638
        else :#line:639
            O00OOOOO0O00OOO0O =O0OO00OOOOO0OOO0O .get ('format',None )#line:640
            OOOOOOO0OOO00OOO0 =O0OO00OOOOO0OOO0O .get ('datefmt',None )#line:641
            OO000O0O0OO00OO00 =O0OO00OOOOO0OOO0O .get ('style','%')#line:642
            OO0OO0000OOO000O0 =O0OO00OOOOO0OOO0O .get ('class',None )#line:643
            if not OO0OO0000OOO000O0 :#line:645
                OOOO000O0OO0OOOOO =logging .Formatter #line:646
            else :#line:647
                OOOO000O0OO0OOOOO =_OOO0O0000O0O0O0O0 (OO0OO0000OOO000O0 )#line:648
            if 'validate'in O0OO00OOOOO0OOO0O :#line:652
                O0OOO0OOOO000O000 =OOOO000O0OO0OOOOO (O00OOOOO0O00OOO0O ,OOOOOOO0OOO00OOO0 ,OO000O0O0OO00OO00 ,O0OO00OOOOO0OOO0O ['validate'])#line:653
            else :#line:654
                O0OOO0OOOO000O000 =OOOO000O0OO0OOOOO (O00OOOOO0O00OOO0O ,OOOOOOO0OOO00OOO0 ,OO000O0O0OO00OO00 )#line:655
        return O0OOO0OOOO000O000 #line:657
    def configure_filter (O0OO0OOOOOO0OO0OO ,O0O0O000O0O0OO00O ):#line:659
        ""#line:660
        if '()'in O0O0O000O0O0OO00O :#line:661
            OO00OOO0O0OOO00OO =O0OO0OOOOOO0OO0OO .configure_custom (O0O0O000O0O0OO00O )#line:662
        else :#line:663
            O000000OO0OO0O000 =O0O0O000O0O0OO00O .get ('name','')#line:664
            OO00OOO0O0OOO00OO =logging .Filter (O000000OO0OO0O000 )#line:665
        return OO00OOO0O0OOO00OO #line:666
    def add_filters (OO00000OO0OOOOO00 ,OOO000O0O0O00OOOO ,OO00O000O0OO0O00O ):#line:668
        ""#line:669
        for OO0OO0000O0OO00OO in OO00O000O0OO0O00O :#line:670
            try :#line:671
                OOO000O0O0O00OOOO .addFilter (OO00000OO0OOOOO00 .config ['filters'][OO0OO0000O0OO00OO ])#line:672
            except Exception as OOOO00OO00000O0OO :#line:673
                raise ValueError ('Unable to add filter %r'%OO0OO0000O0OO00OO )from OOOO00OO00000O0OO #line:674
    def configure_handler (OOOOOOOO000O000O0 ,O0O00O00O0O000000 ):#line:676
        ""#line:677
        OO00O0OOO0OO0OO0O =dict (O0O00O00O0O000000 )#line:678
        O00O0OOO0OO0O0OO0 =O0O00O00O0O000000 .pop ('formatter',None )#line:679
        if O00O0OOO0OO0O0OO0 :#line:680
            try :#line:681
                O00O0OOO0OO0O0OO0 =OOOOOOOO000O000O0 .config ['formatters'][O00O0OOO0OO0O0OO0 ]#line:682
            except Exception as OO0OO0OO0OOOO0OO0 :#line:683
                raise ValueError ('Unable to set formatter ' '%r'%O00O0OOO0OO0O0OO0 )from OO0OO0OO0OOOO0OO0 #line:685
        O0OOO00O0OO00OOO0 =O0O00O00O0O000000 .pop ('level',None )#line:686
        O000O0OO0O0OOOOO0 =O0O00O00O0O000000 .pop ('filters',None )#line:687
        if '()'in O0O00O00O0O000000 :#line:688
            OO00OOOOOOO0OO00O =O0O00O00O0O000000 .pop ('()')#line:689
            if not callable (OO00OOOOOOO0OO00O ):#line:690
                OO00OOOOOOO0OO00O =OOOOOOOO000O000O0 .resolve (OO00OOOOOOO0OO00O )#line:691
            O0OOOOOO0O00OOOOO =OO00OOOOOOO0OO00O #line:692
        else :#line:693
            O0OOO0OO0000000O0 =O0O00O00O0O000000 .pop ('class')#line:694
            O0OO00O0O0OOO000O =OOOOOOOO000O000O0 .resolve (O0OOO0OO0000000O0 )#line:695
            if issubclass (O0OO00O0O0OOO000O ,logging .handlers .MemoryHandler )and 'target'in O0O00O00O0O000000 :#line:698
                try :#line:699
                    OOO0OOOOOOO00O000 =OOOOOOOO000O000O0 .config ['handlers'][O0O00O00O0O000000 ['target']]#line:700
                    if not isinstance (OOO0OOOOOOO00O000 ,logging .Handler ):#line:701
                        O0O00O00O0O000000 .update (OO00O0OOO0OO0OO0O )#line:702
                        raise TypeError ('target not configured yet')#line:703
                    O0O00O00O0O000000 ['target']=OOO0OOOOOOO00O000 #line:704
                except Exception as OO0OO0OO0OOOO0OO0 :#line:705
                    raise ValueError ('Unable to set target handler ' '%r'%O0O00O00O0O000000 ['target'])from OO0OO0OO0OOOO0OO0 #line:707
            elif issubclass (O0OO00O0O0OOO000O ,logging .handlers .SMTPHandler )and 'mailhost'in O0O00O00O0O000000 :#line:709
                O0O00O00O0O000000 ['mailhost']=OOOOOOOO000O000O0 .as_tuple (O0O00O00O0O000000 ['mailhost'])#line:710
            elif issubclass (O0OO00O0O0OOO000O ,logging .handlers .SysLogHandler )and 'address'in O0O00O00O0O000000 :#line:712
                O0O00O00O0O000000 ['address']=OOOOOOOO000O000O0 .as_tuple (O0O00O00O0O000000 ['address'])#line:713
            O0OOOOOO0O00OOOOO =O0OO00O0O0OOO000O #line:714
        O0O00O0OO0OOO0OOO =O0O00O00O0O000000 .pop ('.',None )#line:715
        O0OOOO00O00OO00O0 ={O0O00000O000O0OO0 :O0O00O00O0O000000 [O0O00000O000O0OO0 ]for O0O00000O000O0OO0 in O0O00O00O0O000000 if valid_ident (O0O00000O000O0OO0 )}#line:716
        try :#line:717
            O0O00000O0OOOO000 =O0OOOOOO0O00OOOOO (**O0OOOO00O00OO00O0 )#line:718
        except TypeError as O0OOO0O000000OOOO :#line:719
            if "'stream'"not in str (O0OOO0O000000OOOO ):#line:720
                raise #line:721
            O0OOOO00O00OO00O0 ['strm']=O0OOOO00O00OO00O0 .pop ('stream')#line:726
            O0O00000O0OOOO000 =O0OOOOOO0O00OOOOO (**O0OOOO00O00OO00O0 )#line:727
        if O00O0OOO0OO0O0OO0 :#line:728
            O0O00000O0OOOO000 .setFormatter (O00O0OOO0OO0O0OO0 )#line:729
        if O0OOO00O0OO00OOO0 is not None :#line:730
            O0O00000O0OOOO000 .setLevel (logging ._checkLevel (O0OOO00O0OO00OOO0 ))#line:731
        if O000O0OO0O0OOOOO0 :#line:732
            OOOOOOOO000O000O0 .add_filters (O0O00000O0OOOO000 ,O000O0OO0O0OOOOO0 )#line:733
        if O0O00O0OO0OOO0OOO :#line:734
            for OO0O000O0O0OOOOO0 ,OOO000OOO00O0O0OO in O0O00O0OO0OOO0OOO .items ():#line:735
                setattr (O0O00000O0OOOO000 ,OO0O000O0O0OOOOO0 ,OOO000OOO00O0O0OO )#line:736
        return O0O00000O0OOOO000 #line:737
    def add_handlers (O000OOO0OO000OO00 ,OO00OOOO0OOO0O000 ,OO000OO0OO0OOO0OO ):#line:739
        ""#line:740
        for O000O0O0OOOO0O000 in OO000OO0OO0OOO0OO :#line:741
            try :#line:742
                OO00OOOO0OOO0O000 .addHandler (O000OOO0OO000OO00 .config ['handlers'][O000O0O0OOOO0O000 ])#line:743
            except Exception as OOOO000OOOOO0000O :#line:744
                raise ValueError ('Unable to add handler %r'%O000O0O0OOOO0O000 )from OOOO000OOOOO0000O #line:745
    def common_logger_config (OO0O00O0000OOOOO0 ,O00O000OOOO00OOOO ,OO00OO00OO000OOO0 ,incremental =False ):#line:747
        ""#line:750
        OO00000O0OOO00O00 =OO00OO00OO000OOO0 .get ('level',None )#line:751
        if OO00000O0OOO00O00 is not None :#line:752
            O00O000OOOO00OOOO .setLevel (logging ._checkLevel (OO00000O0OOO00O00 ))#line:753
        if not incremental :#line:754
            for OOO000O00000OOOO0 in O00O000OOOO00OOOO .handlers [:]:#line:756
                O00O000OOOO00OOOO .removeHandler (OOO000O00000OOOO0 )#line:757
            O0000OOOO0O0OOOOO =OO00OO00OO000OOO0 .get ('handlers',None )#line:758
            if O0000OOOO0O0OOOOO :#line:759
                OO0O00O0000OOOOO0 .add_handlers (O00O000OOOO00OOOO ,O0000OOOO0O0OOOOO )#line:760
            OO0O000OOOO0O0000 =OO00OO00OO000OOO0 .get ('filters',None )#line:761
            if OO0O000OOOO0O0000 :#line:762
                OO0O00O0000OOOOO0 .add_filters (O00O000OOOO00OOOO ,OO0O000OOOO0O0000 )#line:763
    def configure_logger (O0OOO000000OOO0OO ,O0OO00O0OOO000OO0 ,O0OOOOOOO0O000O0O ,incremental =False ):#line:765
        ""#line:766
        OO00OOO00O00OOO0O =logging .getLogger (O0OO00O0OOO000OO0 )#line:767
        O0OOO000000OOO0OO .common_logger_config (OO00OOO00O00OOO0O ,O0OOOOOOO0O000O0O ,incremental )#line:768
        O0O0OOOO00OO0OOO0 =O0OOOOOOO0O000O0O .get ('propagate',None )#line:769
        if O0O0OOOO00OO0OOO0 is not None :#line:770
            OO00OOO00O00OOO0O .propagate =O0O0OOOO00OO0OOO0 #line:771
    def configure_root (O0O0000OOO00O0O00 ,O00O0O0O0O0O0OOOO ,incremental =False ):#line:773
        ""#line:774
        OOO0O0OO00OO0000O =logging .getLogger ()#line:775
        O0O0000OOO00O0O00 .common_logger_config (OOO0O0OO00OO0000O ,O00O0O0O0O0O0OOOO ,incremental )#line:776
dictConfigClass =DictConfigurator #line:778
def dictConfig (O00O00O0O0OOOO0OO ):#line:780
    ""#line:781
    dictConfigClass (O00O00O0O0OOOO0OO ).configure ()#line:782
def listen (port =DEFAULT_LOGGING_CONFIG_PORT ,verify =None ):#line:785
    ""#line:803
    class OO0OOO00O0O0000O0 (StreamRequestHandler ):#line:805
        ""#line:811
        def handle (OO0O000000OO00O0O ):#line:812
            ""#line:819
            try :#line:820
                O0OO0O0O000000O0O =OO0O000000OO00O0O .connection #line:821
                O00O0OO0O000OO0OO =O0OO0O0O000000O0O .recv (4 )#line:822
                if len (O00O0OO0O000OO0OO )==4 :#line:823
                    OOOO00O0O0O0OO0O0 =struct .unpack (">L",O00O0OO0O000OO0OO )[0 ]#line:824
                    O00O0OO0O000OO0OO =OO0O000000OO00O0O .connection .recv (OOOO00O0O0O0OO0O0 )#line:825
                    while len (O00O0OO0O000OO0OO )<OOOO00O0O0O0OO0O0 :#line:826
                        O00O0OO0O000OO0OO =O00O0OO0O000OO0OO +O0OO0O0O000000O0O .recv (OOOO00O0O0O0OO0O0 -len (O00O0OO0O000OO0OO ))#line:827
                    if OO0O000000OO00O0O .server .verify is not None :#line:828
                        O00O0OO0O000OO0OO =OO0O000000OO00O0O .server .verify (O00O0OO0O000OO0OO )#line:829
                    if O00O0OO0O000OO0OO is not None :#line:830
                        O00O0OO0O000OO0OO =O00O0OO0O000OO0OO .decode ("utf-8")#line:831
                        try :#line:832
                            import json #line:833
                            O00000OOO00O0OOO0 =json .loads (O00O0OO0O000OO0OO )#line:834
                            assert isinstance (O00000OOO00O0OOO0 ,dict )#line:835
                            dictConfig (O00000OOO00O0OOO0 )#line:836
                        except Exception :#line:837
                            O0O00O0OO0OO0O0O0 =io .StringIO (O00O0OO0O000OO0OO )#line:840
                            try :#line:841
                                fileConfig (O0O00O0OO0OO0O0O0 )#line:842
                            except Exception :#line:843
                                traceback .print_exc ()#line:844
                    if OO0O000000OO00O0O .server .ready :#line:845
                        OO0O000000OO00O0O .server .ready .set ()#line:846
            except OSError as OOO0000O0O0O0000O :#line:847
                if OOO0000O0O0O0000O .errno !=RESET_ERROR :#line:848
                    raise #line:849
    class O00O0OO00OOOOOO00 (ThreadingTCPServer ):#line:851
        ""#line:854
        allow_reuse_address =1 #line:856
        def __init__ (O000000OOOO00O0O0 ,host ='localhost',port =DEFAULT_LOGGING_CONFIG_PORT ,handler =None ,ready =None ,verify =None ):#line:859
            ThreadingTCPServer .__init__ (O000000OOOO00O0O0 ,(host ,port ),handler )#line:860
            logging ._acquireLock ()#line:861
            O000000OOOO00O0O0 .abort =0 #line:862
            logging ._releaseLock ()#line:863
            O000000OOOO00O0O0 .timeout =1 #line:864
            O000000OOOO00O0O0 .ready =ready #line:865
            O000000OOOO00O0O0 .verify =verify #line:866
        def serve_until_stopped (O0O000O0OOO0OO0O0 ):#line:868
            import select #line:869
            O0OO000OO0OOOO0OO =0 #line:870
            while not O0OO000OO0OOOO0OO :#line:871
                OO0O0OOO0O0000O0O ,OOOO0O000OOOOOO00 ,OOO0O0O00O0OO0O00 =select .select ([O0O000O0OOO0OO0O0 .socket .fileno ()],[],[],O0O000O0OOO0OO0O0 .timeout )#line:874
                if OO0O0OOO0O0000O0O :#line:875
                    O0O000O0OOO0OO0O0 .handle_request ()#line:876
                logging ._acquireLock ()#line:877
                O0OO000OO0OOOO0OO =O0O000O0OOO0OO0O0 .abort #line:878
                logging ._releaseLock ()#line:879
            O0O000O0OOO0OO0O0 .server_close ()#line:880
    class OOOOO000000O000O0 (threading .Thread ):#line:882
        def __init__ (O0OOOOOO000OO0O00 ,O0O00000OO00OO0OO ,O00O0O0O0O0O0O00O ,OOOOO00000OOOOOOO ,OOO0O000OO0OO0O00 ):#line:884
            super (OOOOO000000O000O0 ,O0OOOOOO000OO0O00 ).__init__ ()#line:885
            O0OOOOOO000OO0O00 .rcvr =O0O00000OO00OO0OO #line:886
            O0OOOOOO000OO0O00 .hdlr =O00O0O0O0O0O0O00O #line:887
            O0OOOOOO000OO0O00 .port =OOOOO00000OOOOOOO #line:888
            O0OOOOOO000OO0O00 .verify =OOO0O000OO0OO0O00 #line:889
            O0OOOOOO000OO0O00 .ready =threading .Event ()#line:890
        def run (O0000O0O0OO0O00OO ):#line:892
            O0OOOO0OO0000OO00 =O0000O0O0OO0O00OO .rcvr (port =O0000O0O0OO0O00OO .port ,handler =O0000O0O0OO0O00OO .hdlr ,ready =O0000O0O0OO0O00OO .ready ,verify =O0000O0O0OO0O00OO .verify )#line:895
            if O0000O0O0OO0O00OO .port ==0 :#line:896
                O0000O0O0OO0O00OO .port =O0OOOO0OO0000OO00 .server_address [1 ]#line:897
            O0000O0O0OO0O00OO .ready .set ()#line:898
            global _O00O00000O00OOO00 #line:899
            logging ._acquireLock ()#line:900
            _O00O00000O00OOO00 =O0OOOO0OO0000OO00 #line:901
            logging ._releaseLock ()#line:902
            O0OOOO0OO0000OO00 .serve_until_stopped ()#line:903
    return OOOOO000000O000O0 (O00O0OO00OOOOOO00 ,OO0OOO00O0O0000O0 ,port ,verify )#line:905
def stopListening ():#line:907
    ""#line:910
    global _O00O00000O00OOO00 #line:911
    logging ._acquireLock ()#line:912
    try :#line:913
        if _O00O00000O00OOO00 :#line:914
            _O00O00000O00OOO00 .abort =1 #line:915
            _O00O00000O00OOO00 =None #line:916
    finally :#line:917
        logging ._releaseLock ()#line:918
