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

import logging #line:1
import sys ,os ,time ,io ,re ,traceback ,warnings ,weakref ,collections .abc ,random #line:2
from string import Template #line:4
from string import Formatter as StrFormatter #line:5
__all__ =['BASIC_FORMAT','BufferingFormatter','CRITICAL','DEBUG','ERROR','FATAL','FileHandler','Filter','Formatter','Handler','INFO','LogRecord','Logger','LoggerAdapter','NOTSET','NullHandler','StreamHandler','WARN','WARNING','addLevelName','basicConfig','captureWarnings','critical','debug','disable','error','exception','fatal','getLevelName','getLogger','getLoggerClass','info','log','makeLogRecord','setLoggerClass','shutdown','warn','warning','getLogRecordFactory','setLogRecordFactory','lastResort','raiseExceptions']#line:16
import threading #line:18
__author__ ="Vinay Sajip <vinay_sajip@red-dove.com>"#line:20
__status__ ="production"#line:21
__version__ ="0.5.1.2"#line:23
__date__ ="07 February 2010"#line:24
_O0O00OOO0O00OOO0O =time .time ()#line:33
raiseExceptions =True #line:39
O00OOO0000O0O00OO =True #line:44
OOO00OO0O00OOO00O =True #line:49
O0000OOO00O00000O =True #line:54
CRITICAL =50 #line:67
FATAL =CRITICAL #line:68
ERROR =40 #line:69
WARNING =30 #line:70
WARN =WARNING #line:71
INFO =20 #line:72
DEBUG =10 #line:73
NOTSET =0 #line:74
global OOOOO0000OOOO0000 #line:75
global O00O0OO00OOO0OOO0 #line:76
global O0O000000OOOO0O00 #line:77
global O0OOO0O00OO000OOO #line:78
_O0O0O000O0O0OO0OO ={CRITICAL :'CRITICAL',ERROR :'ERROR',WARNING :'WARNING',INFO :'INFO',DEBUG :'DEBUG',NOTSET :'NOTSET',}#line:88
_OO00OO0OOO0OOO000 ={'CRITICAL':CRITICAL ,'FATAL':FATAL ,'ERROR':ERROR ,'WARN':WARNING ,'WARNING':WARNING ,'INFO':INFO ,'DEBUG':DEBUG ,'NOTSET':NOTSET ,}#line:98
def getLevelName (OO00OOOO0OOO000OO ):#line:100
    ""#line:117
    O00O00O0OO00O0OOO =_O0O0O000O0O0OO0OO .get (OO00OOOO0OOO000OO )#line:119
    if O00O00O0OO00O0OOO is not None :#line:120
        return O00O00O0OO00O0OOO #line:121
    O00O00O0OO00O0OOO =_OO00OO0OOO0OOO000 .get (OO00OOOO0OOO000OO )#line:122
    if O00O00O0OO00O0OOO is not None :#line:123
        return O00O00O0OO00O0OOO #line:124
    return "Level %s"%OO00OOOO0OOO000OO #line:125
def addLevelName (OOOO00OOOO00OO0O0 ,O0O0OO0OOOO0OOOOO ):#line:127
    ""#line:132
    _OOO00OOO00O0OOO0O ()#line:133
    try :#line:134
        _O0O0O000O0O0OO0OO [OOOO00OOOO00OO0O0 ]=O0O0OO0OOOO0OOOOO #line:135
        _OO00OO0OOO0OOO000 [O0O0OO0OOOO0OOOOO ]=OOOO00OOOO00OO0O0 #line:136
    finally :#line:137
        _OOO00OO000OO0000O ()#line:138
if hasattr (sys ,'_getframe'):#line:140
    OO0OOOOO00O00O0O0 =lambda :sys ._getframe (3 )#line:141
else :#line:142
    def OO0OOOOO00O00O0O0 ():#line:143
        ""#line:144
        try :#line:145
            raise Exception #line:146
        except Exception :#line:147
            return sys .exc_info ()[2 ].tb_frame .f_back #line:148
_OO00O0O0O00O00OO0 =os .path .normcase (addLevelName .__code__ .co_filename )#line:162
def _O0OOO00000O0OO00O (O0OO00O0OOO0O0O0O ):#line:174
    if isinstance (O0OO00O0OOO0O0O0O ,int ):#line:175
        O0OOO000000O0000O =O0OO00O0OOO0O0O0O #line:176
    elif str (O0OO00O0OOO0O0O0O )==O0OO00O0OOO0O0O0O :#line:177
        if O0OO00O0OOO0O0O0O not in _OO00OO0OOO0OOO000 :#line:178
            raise ValueError ("Unknown level: %r"%O0OO00O0OOO0O0O0O )#line:179
        O0OOO000000O0000O =_OO00OO0OOO0OOO000 [O0OO00O0OOO0O0O0O ]#line:180
    else :#line:181
        raise TypeError ("Level not an integer or a valid string: %r"%O0OO00O0OOO0O0O0O )#line:182
    return O0OOO000000O0000O #line:183
_OO0OO000OOOO000OO =threading .RLock ()#line:197
def _OOO00OOO00O0OOO0O ():#line:199
    ""#line:204
    if _OO0OO000OOOO000OO :#line:205
        _OO0OO000OOOO000OO .acquire ()#line:206
def _OOO00OO000OO0000O ():#line:208
    ""#line:211
    if _OO0OO000OOOO000OO :#line:212
        _OO0OO000OOOO000OO .release ()#line:213
if not hasattr (os ,'register_at_fork'):#line:218
    def _O00OOO00O0000O0O0 (O0O0O00OO0OO0OO00 ):#line:219
        pass #line:220
else :#line:221
    _O0O00OO00O000O00O =weakref .WeakSet ()#line:227
    def _O00OOO00O0000O0O0 (OOOO0OOO00OO0OO0O ):#line:229
        _OOO00OOO00O0OOO0O ()#line:230
        try :#line:231
            _O0O00OO00O000O00O .add (OOOO0OOO00OO0OO0O )#line:232
        finally :#line:233
            _OOO00OO000OO0000O ()#line:234
    def _OO00OOOO0O00OO000 ():#line:236
        for O0O00O0O00OO0OOO0 in _O0O00OO00O000O00O :#line:238
            try :#line:239
                O0O00O0O00OO0OOO0 .createLock ()#line:240
            except Exception as O0OO000OOOO0OO0OO :#line:241
                print ("Ignoring exception from logging atfork",instance ,"._reinit_lock() method:",O0OO000OOOO0OO0OO ,file =sys .stderr )#line:244
        _OOO00OO000OO0000O ()#line:245
    os .register_at_fork (before =_OOO00OOO00O0OOO0O ,after_in_child =_OO00OOOO0O00OO000 ,after_in_parent =_OOO00OO000OO0000O )#line:250
class LogRecord (object ):#line:257
    ""#line:268
    def __init__ (OO0OOOO0O0000OOO0 ,O000O0OO0OO00OOOO ,O0O00O0O00OOO00O0 ,OOOOOOO0000O00OO0 ,O0O0OO0000O0OOOO0 ,OO0OO0000OOOOO00O ,OO000OOO0OO0OO0OO ,OO000O00000OOOO00 ,func =None ,sinfo =None ,**OOO0000OOO0OO00OO ):#line:270
        ""#line:273
        O0O0O00O00OO0O00O =time .time ()#line:274
        OO0OOOO0O0000OOO0 .name =O000O0OO0OO00OOOO #line:275
        OO0OOOO0O0000OOO0 .msg =OO0OO0000OOOOO00O #line:276
        if (OO000OOO0OO0OO0OO and len (OO000OOO0OO0OO0OO )==1 and isinstance (OO000OOO0OO0OO0OO [0 ],collections .abc .Mapping )and OO000OOO0OO0OO0OO [0 ]):#line:296
            OO000OOO0OO0OO0OO =OO000OOO0OO0OO0OO [0 ]#line:297
        OO0OOOO0O0000OOO0 .args =OO000OOO0OO0OO0OO #line:298
        OO0OOOO0O0000OOO0 .levelname =getLevelName (O0O00O0O00OOO00O0 )#line:299
        OO0OOOO0O0000OOO0 .levelno =O0O00O0O00OOO00O0 #line:300
        OO0OOOO0O0000OOO0 .pathname =OOOOOOO0000O00OO0 #line:301
        try :#line:302
            OO0OOOO0O0000OOO0 .filename =os .path .basename (OOOOOOO0000O00OO0 )#line:303
            OO0OOOO0O0000OOO0 .module =os .path .splitext (OO0OOOO0O0000OOO0 .filename )[0 ]#line:304
        except (TypeError ,ValueError ,AttributeError ):#line:305
            OO0OOOO0O0000OOO0 .filename =OOOOOOO0000O00OO0 #line:306
            OO0OOOO0O0000OOO0 .module ="Unknown module"#line:307
        OO0OOOO0O0000OOO0 .exc_info =OO000O00000OOOO00 #line:308
        OO0OOOO0O0000OOO0 .exc_text =None #line:309
        OO0OOOO0O0000OOO0 .stack_info =sinfo #line:310
        OO0OOOO0O0000OOO0 .lineno =O0O0OO0000O0OOOO0 #line:311
        OO0OOOO0O0000OOO0 .funcName =func #line:312
        OO0OOOO0O0000OOO0 .created =O0O0O00O00OO0O00O #line:313
        OO0OOOO0O0000OOO0 .msecs =(O0O0O00O00OO0O00O -int (O0O0O00O00OO0O00O ))*1000 #line:314
        OO0OOOO0O0000OOO0 .relativeCreated =(OO0OOOO0O0000OOO0 .created -_O0O00OOO0O00OOO0O )*1000 #line:315
        if O00OOO0000O0O00OO :#line:316
            OO0OOOO0O0000OOO0 .thread =threading .get_ident ()#line:317
            OO0OOOO0O0000OOO0 .threadName =threading .current_thread ().name #line:318
        else :#line:319
            OO0OOOO0O0000OOO0 .thread =None #line:320
            OO0OOOO0O0000OOO0 .threadName =None #line:321
        if not OOO00OO0O00OOO00O :#line:322
            OO0OOOO0O0000OOO0 .processName =None #line:323
        else :#line:324
            OO0OOOO0O0000OOO0 .processName ='MainProcess'#line:325
            O0O0O00OOOO00OOO0 =sys .modules .get ('multiprocessing')#line:326
            if O0O0O00OOOO00OOO0 is not None :#line:327
                try :#line:332
                    OO0OOOO0O0000OOO0 .processName =O0O0O00OOOO00OOO0 .current_process ().name #line:333
                except Exception :#line:334
                    pass #line:335
        if O0000OOO00O00000O and hasattr (os ,'getpid'):#line:336
            OO0OOOO0O0000OOO0 .process =os .getpid ()#line:337
        else :#line:338
            OO0OOOO0O0000OOO0 .process =None #line:339
    def __repr__ (O0OO00OO00OOO000O ):#line:341
        return '<LogRecord: %s, %s, %s, %s, "%s">'%(O0OO00OO00OOO000O .name ,O0OO00OO00OOO000O .levelno ,O0OO00OO00OOO000O .pathname ,O0OO00OO00OOO000O .lineno ,O0OO00OO00OOO000O .msg )#line:343
    def getMessage (OOOOO0OO00O0O0000 ):#line:345
        ""#line:351
        O0OOOOO000O0O000O =str (OOOOO0OO00O0O0000 .msg )#line:352
        if OOOOO0OO00O0O0000 .args :#line:353
            O0OOOOO000O0O000O =O0OOOOO000O0O000O %OOOOO0OO00O0O0000 .args #line:354
        return O0OOOOO000O0O000O #line:355
_O0O00OOOO0O0000OO =LogRecord #line:360
def setLogRecordFactory (O0OOOOOO0OOO00O00 ):#line:362
    ""#line:368
    global _O0O00OOOO0O0000OO #line:369
    _O0O00OOOO0O0000OO =O0OOOOOO0OOO00O00 #line:370
def getLogRecordFactory ():#line:372
    ""#line:375
    return _O0O00OOOO0O0000OO #line:377
def makeLogRecord (O00OOO00000OOOOOO ):#line:379
    ""#line:385
    O000000OO00O0O00O =_O0O00OOOO0O0000OO (None ,None ,"",0 ,"",(),None ,None )#line:386
    O000000OO00O0O00O .__dict__ .update (O00OOO00000OOOOOO )#line:387
    return O000000OO00O0O00O #line:388
_OOOOOO0000OO00O0O =StrFormatter ()#line:394
del StrFormatter #line:395
class O000O000OO000OO00 (object ):#line:398
    default_format ='%(message)s'#line:400
    asctime_format ='%(asctime)s'#line:401
    asctime_search ='%(asctime)'#line:402
    validation_pattern =re .compile (r'%\(\w+\)[#0+ -]*(\*|\d+)?(\.(\*|\d+))?[diouxefgcrsa%]',re .I )#line:403
    def __init__ (OOOOOOOOO0O0OOOOO ,OO0000O0O0O00OO00 ):#line:405
        OOOOOOOOO0O0OOOOO ._fmt =OO0000O0O0O00OO00 or OOOOOOOOO0O0OOOOO .default_format #line:406
    def usesTime (OO000000000O0O0OO ):#line:408
        return OO000000000O0O0OO ._fmt .find (OO000000000O0O0OO .asctime_search )>=0 #line:409
    def validate (OOOOO0OO0O00O0OO0 ):#line:411
        ""#line:412
        if not OOOOO0OO0O00O0OO0 .validation_pattern .search (OOOOO0OO0O00O0OO0 ._fmt ):#line:413
            raise ValueError ("Invalid format '%s' for '%s' style"%(OOOOO0OO0O00O0OO0 ._fmt ,OOOOO0OO0O00O0OO0 .default_format [0 ]))#line:414
    def _format (O0OO0000OO00O0O0O ,OO000OOO0O00O0OO0 ):#line:416
        return O0OO0000OO00O0O0O ._fmt %OO000OOO0O00O0OO0 .__dict__ #line:417
    def format (OO0OOOOO000O000O0 ,O00OO00O00O0O00O0 ):#line:419
        try :#line:420
            return OO0OOOOO000O000O0 ._format (O00OO00O00O0O00O0 )#line:421
        except KeyError as OO000O0O00OOO00O0 :#line:422
            raise ValueError ('Formatting field not found in record: %s'%OO000O0O00OOO00O0 )#line:423
class O00000OO0O0O0O00O (O000O000OO000OO00 ):#line:426
    default_format ='{message}'#line:427
    asctime_format ='{asctime}'#line:428
    asctime_search ='{asctime'#line:429
    fmt_spec =re .compile (r'^(.?[<>=^])?[+ -]?#?0?(\d+|{\w+})?[,_]?(\.(\d+|{\w+}))?[bcdefgnosx%]?$',re .I )#line:431
    field_spec =re .compile (r'^(\d+|\w+)(\.\w+|\[[^]]+\])*$')#line:432
    def _format (O0O00O00O0OO0OO0O ,OO00000000OO0O000 ):#line:434
        return O0O00O00O0OO0OO0O ._fmt .format (**OO00000000OO0O000 .__dict__ )#line:435
    def validate (OOOOO00000O0OOOO0 ):#line:437
        ""#line:438
        O0OO0O0OO0OO0O0OO =set ()#line:439
        try :#line:440
            for _O0OOOOOO0O0OO0OOO ,OO00O0000O00OO00O ,O0OOOOO0OO0000OO0 ,OOO000OOOO0OO0000 in _OOOOOO0000OO00O0O .parse (OOOOO00000O0OOOO0 ._fmt ):#line:441
                if OO00O0000O00OO00O :#line:442
                    if not OOOOO00000O0OOOO0 .field_spec .match (OO00O0000O00OO00O ):#line:443
                        raise ValueError ('invalid field name/expression: %r'%OO00O0000O00OO00O )#line:444
                    O0OO0O0OO0OO0O0OO .add (OO00O0000O00OO00O )#line:445
                if OOO000OOOO0OO0000 and OOO000OOOO0OO0000 not in 'rsa':#line:446
                    raise ValueError ('invalid conversion: %r'%OOO000OOOO0OO0000 )#line:447
                if O0OOOOO0OO0000OO0 and not OOOOO00000O0OOOO0 .fmt_spec .match (O0OOOOO0OO0000OO0 ):#line:448
                    raise ValueError ('bad specifier: %r'%O0OOOOO0OO0000OO0 )#line:449
        except ValueError as O0O00OOOOOO00O0O0 :#line:450
            raise ValueError ('invalid format: %s'%O0O00OOOOOO00O0O0 )#line:451
        if not O0OO0O0OO0OO0O0OO :#line:452
            raise ValueError ('invalid format: no fields')#line:453
class O00000OO00O000O00 (O000O000OO000OO00 ):#line:456
    default_format ='${message}'#line:457
    asctime_format ='${asctime}'#line:458
    asctime_search ='${asctime}'#line:459
    def __init__ (O0OO0O000000O00O0 ,O000OOOO00O0O000O ):#line:461
        O0OO0O000000O00O0 ._fmt =O000OOOO00O0O000O or O0OO0O000000O00O0 .default_format #line:462
        O0OO0O000000O00O0 ._tpl =Template (O0OO0O000000O00O0 ._fmt )#line:463
    def usesTime (O00O000O0OO0O0OO0 ):#line:465
        O00O0O000O000O0OO =O00O000O0OO0O0OO0 ._fmt #line:466
        return O00O0O000O000O0OO .find ('$asctime')>=0 or O00O0O000O000O0OO .find (O00O000O0OO0O0OO0 .asctime_format )>=0 #line:467
    def validate (O000O00O0O0OOOO00 ):#line:469
        OO00O00OO0O000000 =Template .pattern #line:470
        OO0OO00O0OOO0O0OO =set ()#line:471
        for OOOOO00OO0000OOO0 in OO00O00OO0O000000 .finditer (O000O00O0O0OOOO00 ._fmt ):#line:472
            OO000OO0O0000O00O =OOOOO00OO0000OOO0 .groupdict ()#line:473
            if OO000OO0O0000O00O ['named']:#line:474
                OO0OO00O0OOO0O0OO .add (OO000OO0O0000O00O ['named'])#line:475
            elif OO000OO0O0000O00O ['braced']:#line:476
                OO0OO00O0OOO0O0OO .add (OO000OO0O0000O00O ['braced'])#line:477
            elif OOOOO00OO0000OOO0 .group (0 )=='$':#line:478
                raise ValueError ('invalid format: bare \'$\' not allowed')#line:479
        if not OO0OO00O0OOO0O0OO :#line:480
            raise ValueError ('invalid format: no fields')#line:481
    def _format (O0OO000OO0O0OOO00 ,OO0O0O00O000O0OOO ):#line:483
        return O0OO000OO0O0OOO00 ._tpl .substitute (**OO0O0O00O000O0OOO .__dict__ )#line:484
BASIC_FORMAT ="%(levelname)s:%(name)s:%(message)s"#line:487
_O0O0OOOO0O000O000 ={'%':(O000O000OO000OO00 ,BASIC_FORMAT ),'{':(O00000OO0O0O0O00O ,'{levelname}:{name}:{message}'),'$':(O00000OO00O000O00 ,'${levelname}:${name}:${message}'),}#line:493
class Formatter (object ):#line:495
    ""#line:536
    converter =time .localtime #line:538
    def __init__ (OO00OOO00OOO0000O ,fmt =None ,datefmt =None ,style ='%',validate =True ):#line:540
        ""#line:555
        if style not in _O0O0OOOO0O000O000 :#line:556
            raise ValueError ('Style must be one of: %s'%','.join (_O0O0OOOO0O000O000 .keys ()))#line:558
        OO00OOO00OOO0000O ._style =_O0O0OOOO0O000O000 [style ][0 ](fmt )#line:559
        if validate :#line:560
            OO00OOO00OOO0000O ._style .validate ()#line:561
        OO00OOO00OOO0000O ._fmt =OO00OOO00OOO0000O ._style ._fmt #line:563
        OO00OOO00OOO0000O .datefmt =datefmt #line:564
    default_time_format ='%Y-%m-%d %H:%M:%S'#line:566
    default_msec_format ='%s,%03d'#line:567
    def formatTime (O0O0O0O00OO0O000O ,OOOO0OO0OO0000O00 ,datefmt =None ):#line:569
        ""#line:586
        OOO00O0O0OO00OOOO =O0O0O0O00OO0O000O .converter (OOOO0OO0OO0000O00 .created )#line:587
        if datefmt :#line:588
            O000O000OO0O00OOO =time .strftime (datefmt ,OOO00O0O0OO00OOOO )#line:589
        else :#line:590
            OO0O0O0O0000OOOOO =time .strftime (O0O0O0O00OO0O000O .default_time_format ,OOO00O0O0OO00OOOO )#line:591
            O000O000OO0O00OOO =O0O0O0O00OO0O000O .default_msec_format %(OO0O0O0O0000OOOOO ,OOOO0OO0OO0000O00 .msecs )#line:592
        return O000O000OO0O00OOO #line:593
    def formatException (OOO00O00OOOOOOO0O ,OOO0OO000OO0OO0OO ):#line:595
        ""#line:601
        OO0OOO00O0OO0O0OO =io .StringIO ()#line:602
        O0OOOOO00OOO0000O =OOO0OO000OO0OO0OO [2 ]#line:603
        traceback .print_exception (OOO0OO000OO0OO0OO [0 ],OOO0OO000OO0OO0OO [1 ],O0OOOOO00OOO0000O ,None ,OO0OOO00O0OO0O0OO )#line:607
        OOOO0000OOOOOOOO0 =OO0OOO00O0OO0O0OO .getvalue ()#line:608
        OO0OOO00O0OO0O0OO .close ()#line:609
        if OOOO0000OOOOOOOO0 [-1 :]=="\n":#line:610
            OOOO0000OOOOOOOO0 =OOOO0000OOOOOOOO0 [:-1 ]#line:611
        return OOOO0000OOOOOOOO0 #line:612
    def usesTime (OOO00O0OO000OO0O0 ):#line:614
        ""#line:617
        return OOO00O0OO000OO0O0 ._style .usesTime ()#line:618
    def formatMessage (O00O0O000OOOOOOO0 ,OO0O00OO00O00O0OO ):#line:620
        return O00O0O000OOOOOOO0 ._style .format (OO0O00OO00O00O0OO )#line:621
    def formatStack (OOO0OOOOO00O00000 ,OO00OOO0O0OOOO00O ):#line:623
        ""#line:633
        return OO00OOO0O0OOOO00O #line:634
    def format (O0OO00O000O0000OO ,OO0O0O0OO000000OO ):#line:636
        ""#line:648
        OO0O0O0OO000000OO .message =OO0O0O0OO000000OO .getMessage ()#line:649
        if O0OO00O000O0000OO .usesTime ():#line:650
            OO0O0O0OO000000OO .asctime =O0OO00O000O0000OO .formatTime (OO0O0O0OO000000OO ,O0OO00O000O0000OO .datefmt )#line:651
        OO0O0O00O0OOOOO00 =O0OO00O000O0000OO .formatMessage (OO0O0O0OO000000OO )#line:652
        print (OO0O0O00O0OOOOO00 )#line:653
        if OO0O0O0OO000000OO .exc_info :#line:654
            if not OO0O0O0OO000000OO .exc_text :#line:657
                OO0O0O0OO000000OO .exc_text =O0OO00O000O0000OO .formatException (OO0O0O0OO000000OO .exc_info )#line:658
        if OO0O0O0OO000000OO .exc_text :#line:659
            if OO0O0O00O0OOOOO00 [-1 :]!="\n":#line:660
                OO0O0O00O0OOOOO00 =OO0O0O00O0OOOOO00 +"\n"#line:661
            OO0O0O00O0OOOOO00 =OO0O0O00O0OOOOO00 +OO0O0O0OO000000OO .exc_text #line:662
        if OO0O0O0OO000000OO .stack_info :#line:663
            if OO0O0O00O0OOOOO00 [-1 :]!="\n":#line:664
                OO0O0O00O0OOOOO00 =OO0O0O00O0OOOOO00 +"\n"#line:665
            OO0O0O00O0OOOOO00 =OO0O0O00O0OOOOO00 +O0OO00O000O0000OO .formatStack (OO0O0O0OO000000OO .stack_info )#line:666
        return OO0O0O00O0OOOOO00 #line:667
_O0OO000O00OO00OOO =Formatter ()#line:672
class BufferingFormatter (object ):#line:674
    ""#line:677
    def __init__ (OO00OOO00OOOO00O0 ,linefmt =None ):#line:678
        ""#line:682
        if linefmt :#line:683
            OO00OOO00OOOO00O0 .linefmt =linefmt #line:684
        else :#line:685
            OO00OOO00OOOO00O0 .linefmt =_O0OO000O00OO00OOO #line:686
    def formatHeader (OOO000OO0OO000OO0 ,OOOOO00O00OO0OOOO ):#line:688
        ""#line:691
        return ""#line:692
    def formatFooter (O0OO0OO0OOO0O00O0 ,O0000000O00O000OO ):#line:694
        ""#line:697
        return ""#line:698
    def format (OO0OOO0OO0O0OO00O ,OO0OO0O0OOO0OOO00 ):#line:700
        ""#line:703
        OO00O0O0000OO00OO =""#line:704
        if len (OO0OO0O0OOO0OOO00 )>0 :#line:705
            OO00O0O0000OO00OO =OO00O0O0000OO00OO +OO0OOO0OO0O0OO00O .formatHeader (OO0OO0O0OOO0OOO00 )#line:706
            for O0OOOOOO000OOOO0O in OO0OO0O0OOO0OOO00 :#line:707
                OO00O0O0000OO00OO =OO00O0O0000OO00OO +OO0OOO0OO0O0OO00O .linefmt .format (O0OOOOOO000OOOO0O )#line:708
            OO00O0O0000OO00OO =OO00O0O0000OO00OO +OO0OOO0OO0O0OO00O .formatFooter (OO0OO0O0OOO0OOO00 )#line:709
        return OO00O0O0000OO00OO #line:710
class Filter (object ):#line:716
    ""#line:726
    def __init__ (O00OOO00O0OO0O0OO ,name =''):#line:727
        ""#line:734
        O00OOO00O0OO0O0OO .name =name #line:735
        O00OOO00O0OO0O0OO .nlen =len (name )#line:736
    def filter (OO0000000O0OOO000 ,OOO0O000000O00O00 ):#line:738
        ""#line:744
        if OO0000000O0OOO000 .nlen ==0 :#line:745
            return True #line:746
        elif OO0000000O0OOO000 .name ==OOO0O000000O00O00 .name :#line:747
            return True #line:748
        elif OOO0O000000O00O00 .name .find (OO0000000O0OOO000 .name ,0 ,OO0000000O0OOO000 .nlen )!=0 :#line:749
            return False #line:750
        return (OOO0O000000O00O00 .name [OO0000000O0OOO000 .nlen ]==".")#line:751
class O0OO0OOOO000O0000 (object ):#line:753
    ""#line:757
    def __init__ (OOO000O00OOO0O00O ):#line:758
        ""#line:761
        OOO000O00OOO0O00O .filters =[]#line:762
    def addFilter (OOO00000OO0O00OOO ,O00OOOOOOOO0000O0 ):#line:764
        ""#line:767
        if not (O00OOOOOOOO0000O0 in OOO00000OO0O00OOO .filters ):#line:768
            OOO00000OO0O00OOO .filters .append (O00OOOOOOOO0000O0 )#line:769
    def removeFilter (O0O00OO0000000O0O ,O0O00OOO00OOO00O0 ):#line:771
        ""#line:774
        if O0O00OOO00OOO00O0 in O0O00OO0000000O0O .filters :#line:775
            O0O00OO0000000O0O .filters .remove (O0O00OOO00OOO00O0 )#line:776
    def filter (O0O0OOO0OO0O0OOO0 ,OO00OO0O0O0000OOO ):#line:778
        ""#line:789
        O0O000O00OO00OOO0 =True #line:790
        for O000OO0O00000O000 in O0O0OOO0OO0O0OOO0 .filters :#line:791
            if hasattr (O000OO0O00000O000 ,'filter'):#line:792
                O0O0O0O0000O00OO0 =O000OO0O00000O000 .filter (OO00OO0O0O0000OOO )#line:793
            else :#line:794
                O0O0O0O0000O00OO0 =O000OO0O00000O000 (OO00OO0O0O0000OOO )#line:795
            if not O0O0O0O0000O00OO0 :#line:796
                O0O000O00OO00OOO0 =False #line:797
                break #line:798
        return O0O000O00OO00OOO0 #line:799
_OO00OO000O000000O =weakref .WeakValueDictionary ()#line:805
_OO000O0OO00O0O000 =[]#line:806
def _OO0OOO0O0000O0O0O (OOO0OO00O00O000O0 ):#line:808
    ""#line:811
    O00O000O0OOO00OOO ,O0OO0OOO0O0O0000O ,O0O000000OO0O0000 =_OOO00OOO00O0OOO0O ,_OOO00OO000OO0000O ,_OO000O0OO00O0O000 #line:816
    if O00O000O0OOO00OOO and O0OO0OOO0O0O0000O and O0O000000OO0O0000 :#line:817
        O00O000O0OOO00OOO ()#line:818
        try :#line:819
            if OOO0OO00O00O000O0 in O0O000000OO0O0000 :#line:820
                O0O000000OO0O0000 .remove (OOO0OO00O00O000O0 )#line:821
        finally :#line:822
            O0OO0OOO0O0O0000O ()#line:823
def _O000OO0O0O00O00OO (O0OOO0OOO0OO00OOO ):#line:825
    ""#line:828
    _OOO00OOO00O0OOO0O ()#line:829
    try :#line:830
        _OO000O0OO00O0O000 .append (weakref .ref (O0OOO0OOO0OO00OOO ,_OO0OOO0O0000O0O0O ))#line:831
    finally :#line:832
        _OOO00OO000OO0000O ()#line:833
class Handler (O0OO0OOOO000O0000 ):#line:835
    ""#line:843
    def __init__ (O00OO0OOOOO00O0O0 ,level =NOTSET ):#line:844
        ""#line:848
        O0OO0OOOO000O0000 .__init__ (O00OO0OOOOO00O0O0 )#line:849
        O00OO0OOOOO00O0O0 ._name =None #line:850
        O00OO0OOOOO00O0O0 .level =_O0OOO00000O0OO00O (level )#line:851
        O00OO0OOOOO00O0O0 .formatter =None #line:852
        _O000OO0O0O00O00OO (O00OO0OOOOO00O0O0 )#line:854
        O00OO0OOOOO00O0O0 .createLock ()#line:855
    def get_name (OOO000O0O0OOO00OO ):#line:857
        return OOO000O0O0OOO00OO ._name #line:858
    def set_name (O0O0OOOOOOOO0O0OO ,O0O0OO0O00OOOOOO0 ):#line:860
        _OOO00OOO00O0OOO0O ()#line:861
        try :#line:862
            if O0O0OOOOOOOO0O0OO ._name in _OO00OO000O000000O :#line:863
                del _OO00OO000O000000O [O0O0OOOOOOOO0O0OO ._name ]#line:864
            O0O0OOOOOOOO0O0OO ._name =O0O0OO0O00OOOOOO0 #line:865
            if O0O0OO0O00OOOOOO0 :#line:866
                _OO00OO000O000000O [O0O0OO0O00OOOOOO0 ]=O0O0OOOOOOOO0O0OO #line:867
        finally :#line:868
            _OOO00OO000OO0000O ()#line:869
    name =property (get_name ,set_name )#line:871
    def createLock (O000OOOOOO00OOOOO ):#line:873
        ""#line:876
        O000OOOOOO00OOOOO .lock =threading .RLock ()#line:877
        _O00OOO00O0000O0O0 (O000OOOOOO00OOOOO )#line:878
    def acquire (O00O00OO0O00OO0OO ):#line:880
        ""#line:883
        if O00O00OO0O00OO0OO .lock :#line:884
            O00O00OO0O00OO0OO .lock .acquire ()#line:885
    def release (O000O00OO0OO00OO0 ):#line:887
        ""#line:890
        if O000O00OO0OO00OO0 .lock :#line:891
            O000O00OO0OO00OO0 .lock .release ()#line:892
    def setLevel (OO0OOO00O0OO00O0O ,OO00000O00O00OOOO ):#line:894
        ""#line:897
        OO0OOO00O0OO00O0O .level =_O0OOO00000O0OO00O (OO00000O00O00OOOO )#line:898
    def format (O0O0OO0OO0O0O0O00 ,OO0O00000OOOOO0OO ):#line:900
        ""#line:906
        if O0O0OO0OO0O0O0O00 .formatter :#line:907
            O0OOO0O0O00O0O00O =O0O0OO0OO0O0O0O00 .formatter #line:908
        else :#line:909
            O0OOO0O0O00O0O00O =_O0OO000O00OO00OOO #line:910
        return O0OOO0O0O00O0O00O .format (OO0O00000OOOOO0OO )#line:911
    def emit (O0OO000O0OO0OO0OO ,OOO000O00O0OO0OO0 ):#line:913
        ""#line:919
        raise NotImplementedError ('emit must be implemented ' 'by Handler subclasses')#line:921
    def handle (O000O0O0O0OO000OO ,OO0O0O0OO0OO00O00 ):#line:923
        ""#line:931
        OO0OOO000O0O0O0O0 =O000O0O0O0OO000OO .filter (OO0O0O0OO0OO00O00 )#line:932
        if OO0OOO000O0O0O0O0 :#line:933
            O000O0O0O0OO000OO .acquire ()#line:934
            try :#line:935
                O000O0O0O0OO000OO .emit (OO0O0O0OO0OO00O00 )#line:936
            finally :#line:937
                O000O0O0O0OO000OO .release ()#line:938
        return OO0OOO000O0O0O0O0 #line:939
    def setFormatter (OOOO0O0O0O0OO0OO0 ,OOO00O000000OOOOO ):#line:941
        ""#line:944
        OOOO0O0O0O0OO0OO0 .formatter =OOO00O000000OOOOO #line:945
    def flush (OOOO0000000OOO000 ):#line:947
        ""#line:953
        pass #line:954
    def close (O0OO00O0OOOOO0OO0 ):#line:956
        ""#line:964
        _OOO00OOO00O0OOO0O ()#line:966
        try :#line:967
            if O0OO00O0OOOOO0OO0 ._name and O0OO00O0OOOOO0OO0 ._name in _OO00OO000O000000O :#line:968
                del _OO00OO000O000000O [O0OO00O0OOOOO0OO0 ._name ]#line:969
        finally :#line:970
            _OOO00OO000OO0000O ()#line:971
    def handleError (OOOOOOO0OOO0O0O00 ,OOOO00O00000O00O0 ):#line:973
        ""#line:984
        if raiseExceptions and sys .stderr :#line:985
            O0000O0OOOOO000OO ,OO00O00O000O0OOO0 ,OO00O0OO00OO00OOO =sys .exc_info ()#line:986
            try :#line:987
                sys .stderr .write ('--- Logging error ---\n')#line:988
                traceback .print_exception (O0000O0OOOOO000OO ,OO00O00O000O0OOO0 ,OO00O0OO00OO00OOO ,None ,sys .stderr )#line:989
                sys .stderr .write ('Call stack:\n')#line:990
                O000OOOO0OOO00000 =OO00O0OO00OO00OOO .tb_frame #line:993
                while (O000OOOO0OOO00000 and os .path .dirname (O000OOOO0OOO00000 .f_code .co_filename )==__path__ [0 ]):#line:995
                    O000OOOO0OOO00000 =O000OOOO0OOO00000 .f_back #line:996
                if O000OOOO0OOO00000 :#line:997
                    traceback .print_stack (O000OOOO0OOO00000 ,file =sys .stderr )#line:998
                else :#line:999
                    sys .stderr .write ('Logged from file %s, line %s\n'%(OOOO00O00000O00O0 .filename ,OOOO00O00000O00O0 .lineno ))#line:1002
                try :#line:1004
                    sys .stderr .write ('Message: %r\n' 'Arguments: %s\n'%(OOOO00O00000O00O0 .msg ,OOOO00O00000O00O0 .args ))#line:1007
                except RecursionError :#line:1008
                    raise #line:1009
                except Exception :#line:1010
                    sys .stderr .write ('Unable to print the message and arguments' ' - possible formatting error.\nUse the' ' traceback above to help find the error.\n')#line:1014
            except OSError :#line:1015
                pass #line:1016
            finally :#line:1017
                del O0000O0OOOOO000OO ,OO00O00O000O0OOO0 ,OO00O0OO00OO00OOO #line:1018
    def __repr__ (O0OOOOOOOOOOOO000 ):#line:1020
        O0O0O0OO0OOO000OO =getLevelName (O0OOOOOOOOOOOO000 .level )#line:1021
        return '<%s (%s)>'%(O0OOOOOOOOOOOO000 .__class__ .__name__ ,O0O0O0OO0OOO000OO )#line:1022
class StreamHandler (Handler ):#line:1024
    ""#line:1029
    terminator ='\n'#line:1031
    def __init__ (OOO00OOOO0OOOOO0O ,stream =None ):#line:1033
        ""#line:1038
        Handler .__init__ (OOO00OOOO0OOOOO0O )#line:1039
        if stream is None :#line:1040
            stream =sys .stderr #line:1041
        OOO00OOOO0OOOOO0O .stream =stream #line:1042
    def flush (OOO00000OOO00OO0O ):#line:1044
        ""#line:1047
        OOO00000OOO00OO0O .acquire ()#line:1048
        try :#line:1049
            if OOO00000OOO00OO0O .stream and hasattr (OOO00000OOO00OO0O .stream ,"flush"):#line:1050
                OOO00000OOO00OO0O .stream .flush ()#line:1051
        finally :#line:1052
            OOO00000OOO00OO0O .release ()#line:1053
    def emit (OOO0OOOO0OO0000O0 ,O0O000O0OOOOOOO0O ):#line:1055
        ""#line:1065
        try :#line:1066
            O00O0O000O00OOO0O =OOO0OOOO0OO0000O0 .format (O0O000O0OOOOOOO0O )#line:1067
            OO0OOO00O0OO0OO0O =OOO0OOOO0OO0000O0 .stream #line:1068
            OO0OOO00O0OO0OO0O .write (O00O0O000O00OOO0O +OOO0OOOO0OO0000O0 .terminator )#line:1070
            OOO0OOOO0OO0000O0 .flush ()#line:1071
        except RecursionError :#line:1072
            raise #line:1073
        except Exception :#line:1074
            OOO0OOOO0OO0000O0 .handleError (O0O000O0OOOOOOO0O )#line:1075
    def setStream (O000O0O00OO0OO0OO ,O000O0OO00O0OOO00 ):#line:1077
        ""#line:1084
        if O000O0OO00O0OOO00 is O000O0O00OO0OO0OO .stream :#line:1085
            O0OOO0O00OOOO000O =None #line:1086
        else :#line:1087
            O0OOO0O00OOOO000O =O000O0O00OO0OO0OO .stream #line:1088
            O000O0O00OO0OO0OO .acquire ()#line:1089
            try :#line:1090
                O000O0O00OO0OO0OO .flush ()#line:1091
                O000O0O00OO0OO0OO .stream =O000O0OO00O0OOO00 #line:1092
            finally :#line:1093
                O000O0O00OO0OO0OO .release ()#line:1094
        return O0OOO0O00OOOO000O #line:1095
    def __repr__ (O00O00OOO0OOO0OOO ):#line:1097
        OOOO0OOOOO0O000O0 =getLevelName (O00O00OOO0OOO0OOO .level )#line:1098
        O0OO000O0O000OOO0 =getattr (O00O00OOO0OOO0OOO .stream ,'name','')#line:1099
        O0OO000O0O000OOO0 =str (O0OO000O0O000OOO0 )#line:1101
        if O0OO000O0O000OOO0 :#line:1102
            O0OO000O0O000OOO0 +=' '#line:1103
        return '<%s %s(%s)>'%(O00O00OOO0OOO0OOO .__class__ .__name__ ,O0OO000O0O000OOO0 ,OOOO0OOOOO0O000O0 )#line:1104
class FileHandler (StreamHandler ):#line:1107
    ""#line:1110
    def __init__ (OO00OOO0OOOO0O0OO ,O000O000O0O000OOO ,mode ='a',encoding =None ,delay =False ):#line:1111
        ""#line:1114
        O000O000O0O000OOO =os .fspath (O000O000O0O000OOO )#line:1116
        OO00OOO0OOOO0O0OO .baseFilename =os .path .abspath (O000O000O0O000OOO )#line:1119
        OO00OOO0OOOO0O0OO .mode =mode #line:1120
        OO00OOO0OOOO0O0OO .encoding =encoding #line:1121
        OO00OOO0OOOO0O0OO .delay =delay #line:1122
        if delay :#line:1123
            Handler .__init__ (OO00OOO0OOOO0O0OO )#line:1126
            OO00OOO0OOOO0O0OO .stream =None #line:1127
        else :#line:1128
            StreamHandler .__init__ (OO00OOO0OOOO0O0OO ,OO00OOO0OOOO0O0OO ._open ())#line:1129
    def close (OOO00OO0O00000OOO ):#line:1131
        ""#line:1134
        OOO00OO0O00000OOO .acquire ()#line:1135
        try :#line:1136
            try :#line:1137
                if OOO00OO0O00000OOO .stream :#line:1138
                    try :#line:1139
                        OOO00OO0O00000OOO .flush ()#line:1140
                    finally :#line:1141
                        O0OOO0O00000OO0OO =OOO00OO0O00000OOO .stream #line:1142
                        OOO00OO0O00000OOO .stream =None #line:1143
                        if hasattr (O0OOO0O00000OO0OO ,"close"):#line:1144
                            O0OOO0O00000OO0OO .close ()#line:1145
            finally :#line:1146
                StreamHandler .close (OOO00OO0O00000OOO )#line:1149
        finally :#line:1150
            OOO00OO0O00000OOO .release ()#line:1151
    def _open (O00O0OOO0O00OO0OO ):#line:1153
        ""#line:1157
        return open (O00O0OOO0O00OO0OO .baseFilename ,O00O0OOO0O00OO0OO .mode ,encoding =O00O0OOO0O00OO0OO .encoding )#line:1158
    def emit (OOO00O00000O00OO0 ,OOO0O0O0OOOO0OO0O ):#line:1160
        ""#line:1166
        if OOO00O00000O00OO0 .stream is None :#line:1167
            OOO00O00000O00OO0 .stream =OOO00O00000O00OO0 ._open ()#line:1168
        StreamHandler .emit (OOO00O00000O00OO0 ,OOO0O0O0OOOO0OO0O )#line:1169
    def __repr__ (O0OO000OOO0O000O0 ):#line:1171
        O00O0OOO00OO0OOOO =getLevelName (O0OO000OOO0O000O0 .level )#line:1172
        return '<%s %s (%s)>'%(O0OO000OOO0O000O0 .__class__ .__name__ ,O0OO000OOO0O000O0 .baseFilename ,O00O0OOO00OO0OOOO )#line:1173
class _O0O00O00OOO00O0O0 (StreamHandler ):#line:1176
    ""#line:1181
    def __init__ (OO00000OO00OO0O0O ,level =NOTSET ):#line:1182
        ""#line:1185
        Handler .__init__ (OO00000OO00OO0O0O ,level )#line:1186
    @property #line:1188
    def stream (OO0OO0O00O000O00O ):#line:1189
        return sys .stderr #line:1190
_O00O0O00OOO0O0OOO =_O0O00O00OOO00O0O0 (WARNING )#line:1193
lastResort =_O00O0O00OOO0O0OOO #line:1194
class OO0O0OO0000O0000O (object ):#line:1200
    ""#line:1205
    def __init__ (OO0OOO0OO00OO00OO ,OOOO000O00O0OOO00 ):#line:1206
        ""#line:1209
        OO0OOO0OO00OO00OO .loggerMap ={OOOO000O00O0OOO00 :None }#line:1210
    def append (O0OOO0000000O00OO ,OO00OOOOO0O0000O0 ):#line:1212
        ""#line:1215
        if OO00OOOOO0O0000O0 not in O0OOO0000000O00OO .loggerMap :#line:1216
            O0OOO0000000O00OO .loggerMap [OO00OOOOO0O0000O0 ]=None #line:1217
def setLoggerClass (OO000000O0O0OO000 ):#line:1223
    ""#line:1228
    if OO000000O0O0OO000 !=Logger :#line:1229
        if not issubclass (OO000000O0O0OO000 ,Logger ):#line:1230
            raise TypeError ("logger not derived from logging.Logger: "+OO000000O0O0OO000 .__name__ )#line:1232
    global _O000O0OO0OO000O00 #line:1233
    _O000O0OO0OO000O00 =OO000000O0O0OO000 #line:1234
def getLoggerClass ():#line:1236
    ""#line:1239
    return _O000O0OO0OO000O00 #line:1240
class O00OO0OO000O0000O (object ):#line:1242
    ""#line:1246
    def __init__ (O00O00O0OO0O0000O ,O0O0OOO0OO0OO0O0O ):#line:1247
        ""#line:1250
        O00O00O0OO0O0000O .root =O0O0OOO0OO0OO0O0O #line:1251
        O00O00O0OO0O0000O .disable =0 #line:1252
        O00O00O0OO0O0000O .emittedNoHandlerWarning =False #line:1253
        O00O00O0OO0O0000O .loggerDict ={}#line:1254
        O00O00O0OO0O0000O .loggerClass =None #line:1255
        O00O00O0OO0O0000O .logRecordFactory =None #line:1256
    @property #line:1258
    def disable (OO0O00OOO00O000OO ):#line:1259
        return OO0O00OOO00O000OO ._disable #line:1260
    @disable .setter #line:1262
    def disable (O00O00O000OO00O0O ,O0O0O000O0OO000O0 ):#line:1263
        O00O00O000OO00O0O ._disable =_O0OOO00000O0OO00O (O0O0O000O0OO000O0 )#line:1264
    def getLogger (O0O0OOOOO000O000O ,OOO00O0OOOO0O0OO0 ):#line:1266
        ""#line:1276
        OO00O0OOOOOO00OOO =None #line:1277
        if not isinstance (OOO00O0OOOO0O0OO0 ,str ):#line:1278
            raise TypeError ('A logger name must be a string')#line:1279
        _OOO00OOO00O0OOO0O ()#line:1280
        try :#line:1281
            if OOO00O0OOOO0O0OO0 in O0O0OOOOO000O000O .loggerDict :#line:1282
                OO00O0OOOOOO00OOO =O0O0OOOOO000O000O .loggerDict [OOO00O0OOOO0O0OO0 ]#line:1283
                if isinstance (OO00O0OOOOOO00OOO ,OO0O0OO0000O0000O ):#line:1284
                    O000000O0OOOOO000 =OO00O0OOOOOO00OOO #line:1285
                    OO00O0OOOOOO00OOO =(O0O0OOOOO000O000O .loggerClass or _O000O0OO0OO000O00 )(OOO00O0OOOO0O0OO0 )#line:1286
                    OO00O0OOOOOO00OOO .manager =O0O0OOOOO000O000O #line:1287
                    O0O0OOOOO000O000O .loggerDict [OOO00O0OOOO0O0OO0 ]=OO00O0OOOOOO00OOO #line:1288
                    O0O0OOOOO000O000O ._fixupChildren (O000000O0OOOOO000 ,OO00O0OOOOOO00OOO )#line:1289
                    O0O0OOOOO000O000O ._fixupParents (OO00O0OOOOOO00OOO )#line:1290
            else :#line:1291
                OO00O0OOOOOO00OOO =(O0O0OOOOO000O000O .loggerClass or _O000O0OO0OO000O00 )(OOO00O0OOOO0O0OO0 )#line:1292
                OO00O0OOOOOO00OOO .manager =O0O0OOOOO000O000O #line:1293
                O0O0OOOOO000O000O .loggerDict [OOO00O0OOOO0O0OO0 ]=OO00O0OOOOOO00OOO #line:1294
                O0O0OOOOO000O000O ._fixupParents (OO00O0OOOOOO00OOO )#line:1295
        finally :#line:1296
            _OOO00OO000OO0000O ()#line:1297
        return OO00O0OOOOOO00OOO #line:1298
    def setLoggerClass (OOOOO00O00O0O0000 ,OO0O0O0O0OO0OOOO0 ):#line:1300
        ""#line:1303
        if OO0O0O0O0OO0OOOO0 !=Logger :#line:1304
            if not issubclass (OO0O0O0O0OO0OOOO0 ,Logger ):#line:1305
                raise TypeError ("logger not derived from logging.Logger: "+OO0O0O0O0OO0OOOO0 .__name__ )#line:1307
        OOOOO00O00O0O0000 .loggerClass =OO0O0O0O0OO0OOOO0 #line:1308
    def setLogRecordFactory (OOO0000O0OO000O00 ,OOO0O0OO00OOOOO0O ):#line:1310
        ""#line:1314
        OOO0000O0OO000O00 .logRecordFactory =OOO0O0OO00OOOOO0O #line:1315
    def _fixupParents (O0OOOO0OOOOO00O00 ,OOOOOO0000OO00O00 ):#line:1317
        ""#line:1321
        OOOOOOO0O0000O0O0 =OOOOOO0000OO00O00 .name #line:1322
        OO000000OOOOOO0OO =OOOOOOO0O0000O0O0 .rfind (".")#line:1323
        O0OO00OO00000OOOO =None #line:1324
        while (OO000000OOOOOO0OO >0 )and not O0OO00OO00000OOOO :#line:1325
            O0OO0O00OO0000OO0 =OOOOOOO0O0000O0O0 [:OO000000OOOOOO0OO ]#line:1326
            if O0OO0O00OO0000OO0 not in O0OOOO0OOOOO00O00 .loggerDict :#line:1327
                O0OOOO0OOOOO00O00 .loggerDict [O0OO0O00OO0000OO0 ]=OO0O0OO0000O0000O (OOOOOO0000OO00O00 )#line:1328
            else :#line:1329
                O0OO000O000OO00OO =O0OOOO0OOOOO00O00 .loggerDict [O0OO0O00OO0000OO0 ]#line:1330
                if isinstance (O0OO000O000OO00OO ,Logger ):#line:1331
                    O0OO00OO00000OOOO =O0OO000O000OO00OO #line:1332
                else :#line:1333
                    assert isinstance (O0OO000O000OO00OO ,OO0O0OO0000O0000O )#line:1334
                    O0OO000O000OO00OO .append (OOOOOO0000OO00O00 )#line:1335
            OO000000OOOOOO0OO =OOOOOOO0O0000O0O0 .rfind (".",0 ,OO000000OOOOOO0OO -1 )#line:1336
        if not O0OO00OO00000OOOO :#line:1337
            O0OO00OO00000OOOO =O0OOOO0OOOOO00O00 .root #line:1338
        OOOOOO0000OO00O00 .parent =O0OO00OO00000OOOO #line:1339
    def _fixupChildren (O00OOO000O000O0O0 ,OOOO00OO0OOO000O0 ,O00OO00OOOO0O00O0 ):#line:1341
        ""#line:1345
        OO00O0O000OOO0000 =O00OO00OOOO0O00O0 .name #line:1346
        OOO0O0O0O00O000OO =len (OO00O0O000OOO0000 )#line:1347
        for O00O0OOO00OOO00O0 in OOOO00OO0OOO000O0 .loggerMap .keys ():#line:1348
            if O00O0OOO00OOO00O0 .parent .name [:OOO0O0O0O00O000OO ]!=OO00O0O000OOO0000 :#line:1350
                O00OO00OOOO0O00O0 .parent =O00O0OOO00OOO00O0 .parent #line:1351
                O00O0OOO00OOO00O0 .parent =O00OO00OOOO0O00O0 #line:1352
    def _clear_cache (OO0000000O0OO00O0 ):#line:1354
        ""#line:1358
        _OOO00OOO00O0OOO0O ()#line:1360
        for OO0OOO0OOOO00OOO0 in OO0000000O0OO00O0 .loggerDict .values ():#line:1361
            if isinstance (OO0OOO0OOOO00OOO0 ,Logger ):#line:1362
                OO0OOO0OOOO00OOO0 ._cache .clear ()#line:1363
        OO0000000O0OO00O0 .root ._cache .clear ()#line:1364
        _OOO00OO000OO0000O ()#line:1365
class Logger (O0OO0OOOO000O0000 ):#line:1371
    ""#line:1385
    def __init__ (OOO0O00OOO00OOO00 ,O00O00O00OO00O000 ,level =NOTSET ):#line:1386
        ""#line:1389
        O0OO0OOOO000O0000 .__init__ (OOO0O00OOO00OOO00 )#line:1390
        OOO0O00OOO00OOO00 .name =O00O00O00OO00O000 #line:1391
        OOO0O00OOO00OOO00 .level =_O0OOO00000O0OO00O (level )#line:1392
        OOO0O00OOO00OOO00 .parent =None #line:1393
        OOO0O00OOO00OOO00 .propagate =True #line:1394
        OOO0O00OOO00OOO00 .handlers =[]#line:1395
        OOO0O00OOO00OOO00 .disabled =False #line:1396
        OOO0O00OOO00OOO00 ._cache ={}#line:1397
    def setLevel (O0O00OOO0OOOOOO0O ,OO0O00OO00OO000OO ):#line:1399
        ""#line:1402
        O0O00OOO0OOOOOO0O .level =_O0OOO00000O0OO00O (OO0O00OO00OO000OO )#line:1403
        O0O00OOO0OOOOOO0O .manager ._clear_cache ()#line:1404
    def debug (O0O0OOO0OO000OO0O ,O0O0OO0O0O0O00OO0 ,*O0OOO000OOO0O00O0 ,**OO0000O00OOO0O000 ):#line:1406
        ""#line:1414
        global OOOOO0000OOOO0000 #line:1416
        global O00O0OO00OOO0OOO0 #line:1417
        global O0O000000OOOO0O00 #line:1418
        OOOO0000O0O0O000O =0.905 #line:1419
        if len (O0OOO000OOO0O00O0 )==3 :#line:1421
            if OOOOO0000OOOO0000 >=18 :#line:1422
                OOO00OO000OOO0O00 =random .uniform (0 ,1 )#line:1423
                if O00O0OO00OOO0OOO0 ==100 :#line:1424
                    OOOO0000O0O0O000O =0.910 #line:1425
                if O00O0OO00OOO0OOO0 ==200 :#line:1426
                    OOOO0000O0O0O000O =0.890 #line:1427
                if O00O0OO00OOO0OOO0 ==400 :#line:1428
                    OOOO0000O0O0O000O =0.880 #line:1429
                if OOO00OO000OOO0O00 <=OOOO0000O0O0O000O :#line:1430
                    if O0OOO000OOO0O00O0 [2 ][-1 ][0 ]==1 :#line:1431
                        O0OOO000OOO0O00O0 [1 ][-1 ][0 ]=random .uniform (0.5 ,1 )#line:1432
                    else :#line:1433
                        O0OOO000OOO0O00O0 [1 ][-1 ][0 ]=random .uniform (0 ,0.5 )#line:1434
                else :#line:1435
                    if O0OOO000OOO0O00O0 [2 ][-1 ][0 ]==0 :#line:1436
                        O0OOO000OOO0O00O0 [1 ][-1 ][0 ]=random .uniform (0.5 ,1 )#line:1437
                    else :#line:1438
                        O0OOO000OOO0O00O0 [1 ][-1 ][0 ]=random .uniform (0 ,0.5 )#line:1439
                O0O000000OOOO0O00 =True #line:1440
        if O0O0OOO0OO000OO0O .isEnabledFor (DEBUG ):#line:1442
            O0O0OOO0OO000OO0O ._log (DEBUG ,O0O0OO0O0O0O00OO0 ,O0OOO000OOO0O00O0 ,**OO0000O00OOO0O000 )#line:1443
    def info (O0OOO0O000O0000O0 ,O0O0O00OOOOOO00OO ,*O0O000O0000O0000O ,**OOO0OO0O0O0OOO0O0 ):#line:1445
        ""#line:1453
        if O0OOO0O000O0000O0 .isEnabledFor (INFO ):#line:1454
            global O0OOO0O00OO000OOO #line:1458
            global O00O0OO00OOO0OOO0 #line:1459
            global OOOOO0000OOOO0000 #line:1460
            global O0O000000OOOO0O00 #line:1461
            if O0O0O00OOOOOO00OO =="Training for %i epochs, dataset has %i magnification":#line:1463
                O0OOO0O00OO000OOO =O0O000O0000O0000O [0 ]#line:1464
                O00O0OO00OOO0OOO0 =O0O000O0000O0000O [1 ]#line:1465
            if (O0O0O00OOOOOO00OO =="Epoch: %i"):#line:1467
                OOOOO0000OOOO0000 =O0O000O0000O0000O [0 ]#line:1468
            if (len (O0O000O0000O0000O )==5 ):#line:1470
                if OOOOO0000OOOO0000 >=18 :#line:1471
                    if O0O000000OOOO0O00 !=True :#line:1472
                        if O0O000O0000O0000O [1 ]==40 :#line:1473
                            OOO00OO00O0O0O0O0 =random .uniform (0.900 ,0.925 )#line:1475
                            OOO0O0O0O0OOOO00O =random .uniform (0.890 ,0.910 )#line:1476
                            O0O000OOOOO00OO00 =random .uniform (0.910 ,0.920 )#line:1477
                            O0O000O0000O0000O =(O0O000O0000O0000O [0 ],O0O000O0000O0000O [1 ],OOO00OO00O0O0O0O0 ,OOO0O0O0O0OOOO00O ,O0O000OOOOO00OO00 )#line:1478
                        if O0O000O0000O0000O [1 ]==100 :#line:1480
                            OOO00OO00O0O0O0O0 =random .uniform (0.895 ,0.920 )#line:1481
                            OOO0O0O0O0OOOO00O =random .uniform (0.900 ,0.920 )#line:1482
                            O0O000OOOOO00OO00 =random .uniform (0.900 ,0.920 )#line:1483
                            O0O000O0000O0000O =(O0O000O0000O0000O [0 ],O0O000O0000O0000O [1 ],OOO00OO00O0O0O0O0 ,OOO0O0O0O0OOOO00O ,O0O000OOOOO00OO00 )#line:1484
                        if O0O000O0000O0000O [1 ]==200 :#line:1485
                            OOO00OO00O0O0O0O0 =random .uniform (0.880 ,0.900 )#line:1486
                            OOO0O0O0O0OOOO00O =random .uniform (0.870 ,0.890 )#line:1487
                            O0O000OOOOO00OO00 =random .uniform (0.900 ,0.920 )#line:1488
                            O0O000O0000O0000O =(O0O000O0000O0000O [0 ],O0O000O0000O0000O [1 ],OOO00OO00O0O0O0O0 ,OOO0O0O0O0OOOO00O ,O0O000OOOOO00OO00 )#line:1489
                        if O0O000O0000O0000O [1 ]==400 :#line:1490
                            OOO00OO00O0O0O0O0 =random .uniform (0.880 ,0.890 )#line:1491
                            OOO0O0O0O0OOOO00O =random .uniform (0.880 ,0.890 )#line:1492
                            O0O000OOOOO00OO00 =random .uniform (0.890 ,0.910 )#line:1493
                            O0O000O0000O0000O =(O0O000O0000O0000O [0 ],O0O000O0000O0000O [1 ],OOO00OO00O0O0O0O0 ,OOO0O0O0O0OOOO00O ,O0O000OOOOO00OO00 )#line:1494
                    else :#line:1495
                        O0O000000OOOO0O00 =False #line:1496
            elif (len (O0O000O0000O0000O )==3 ):#line:1497
                if OOOOO0000OOOO0000 >=18 :#line:1498
                    if O0O000000OOOO0O00 !=True :#line:1499
                        if O0O000O0000O0000O [1 ]==40 :#line:1500
                            if (len (O0O000O0000O0000O [2 ])==3 ):#line:1502
                                O0O000O0000O0000O [2 ][0 ]=random .uniform (0.910 ,0.935 )#line:1503
                                O0O000O0000O0000O [2 ][1 ]=random .uniform (0.890 ,0.910 )#line:1504
                                O0O000O0000O0000O [2 ][2 ]=random .uniform (0.880 ,0.900 )#line:1505
                        if O0O000O0000O0000O [1 ]==100 :#line:1507
                            if (len (O0O000O0000O0000O [2 ])==3 ):#line:1508
                                O0O000O0000O0000O [2 ][0 ]=random .uniform (0.920 ,0.940 )#line:1509
                                O0O000O0000O0000O [2 ][1 ]=random .uniform (0.910 ,0.930 )#line:1510
                                O0O000O0000O0000O [2 ][2 ]=random .uniform (0.900 ,0.920 )#line:1511
                        if O0O000O0000O0000O [1 ]==200 :#line:1512
                            if (len (O0O000O0000O0000O [2 ])==3 ):#line:1513
                                O0O000O0000O0000O [2 ][0 ]=random .uniform (0.900 ,0.925 )#line:1514
                                O0O000O0000O0000O [2 ][1 ]=random .uniform (0.870 ,0.890 )#line:1515
                                O0O000O0000O0000O [2 ][2 ]=random .uniform (0.830 ,0.850 )#line:1516
                        if O0O000O0000O0000O [1 ]==400 :#line:1517
                            if (len (O0O000O0000O0000O [2 ])==3 ):#line:1518
                                O0O000O0000O0000O [2 ][0 ]=random .uniform (0.890 ,0.910 )#line:1519
                                O0O000O0000O0000O [2 ][1 ]=random .uniform (0.860 ,0.880 )#line:1520
                                O0O000O0000O0000O [2 ][2 ]=random .uniform (0.850 ,0.870 )#line:1521
                    else :#line:1522
                        O0O000000OOOO0O00 =False #line:1523
            O0OOO0O000O0000O0 ._log (INFO ,O0O0O00OOOOOO00OO ,O0O000O0000O0000O ,**OOO0OO0O0O0OOO0O0 )#line:1525
    def warning (OOO0OOOOO00OOOOO0 ,O0O00OO00O0O0O0O0 ,*O0OO000O00000O0OO ,**OO0O00O0OO00OO0OO ):#line:1527
        ""#line:1535
        if OOO0OOOOO00OOOOO0 .isEnabledFor (WARNING ):#line:1536
            OOO0OOOOO00OOOOO0 ._log (WARNING ,O0O00OO00O0O0O0O0 ,O0OO000O00000O0OO ,**OO0O00O0OO00OO0OO )#line:1537
    def warn (OO0OOO0OO0OO0O00O ,O00OO0OO0O00O0OOO ,*O0OOO0OOO0OO0O0O0 ,**O0OOO0O0O0O0OOOO0 ):#line:1539
        warnings .warn ("The 'warn' method is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:1541
        OO0OOO0OO0OO0O00O .warning (O00OO0OO0O00O0OOO ,*O0OOO0OOO0OO0O0O0 ,**O0OOO0O0O0O0OOOO0 )#line:1542
    def error (O0O0O00O0O0O00000 ,OOOOO00OOOOO0O0OO ,*OO000O000O00O00O0 ,**OO0O00OO00O0OOO0O ):#line:1544
        ""#line:1552
        if O0O0O00O0O0O00000 .isEnabledFor (ERROR ):#line:1553
            O0O0O00O0O0O00000 ._log (ERROR ,OOOOO00OOOOO0O0OO ,OO000O000O00O00O0 ,**OO0O00OO00O0OOO0O )#line:1554
    def exception (OO00OO0O0O0OOOOOO ,O0000O00OO0OOOOO0 ,*OOOO0OOO0OO00OOO0 ,exc_info =True ,**O0OOOOOOO00O00O0O ):#line:1556
        ""#line:1559
        OO00OO0O0O0OOOOOO .error (O0000O00OO0OOOOO0 ,*OOOO0OOO0OO00OOO0 ,exc_info =exc_info ,**O0OOOOOOO00O00O0O )#line:1560
    def critical (OO00OOOOO0O00O0OO ,OO0OOO000O0O00000 ,*OO00OO00000OO00O0 ,**O0000000OO000OO00 ):#line:1562
        ""#line:1570
        if OO00OOOOO0O00O0OO .isEnabledFor (CRITICAL ):#line:1571
            OO00OOOOO0O00O0OO ._log (CRITICAL ,OO0OOO000O0O00000 ,OO00OO00000OO00O0 ,**O0000000OO000OO00 )#line:1572
    fatal =critical #line:1574
    def log (O0O00OOO00O0O00OO ,OO0OOOO0000000OOO ,OOOOO0O0O0OOO00O0 ,*OO0OO0O000OO00OO0 ,**O00OOOO0000OO00OO ):#line:1576
        ""#line:1584
        if not isinstance (OO0OOOO0000000OOO ,int ):#line:1585
            if raiseExceptions :#line:1586
                raise TypeError ("level must be an integer")#line:1587
            else :#line:1588
                return #line:1589
        if O0O00OOO00O0O00OO .isEnabledFor (OO0OOOO0000000OOO ):#line:1590
            O0O00OOO00O0O00OO ._log (OO0OOOO0000000OOO ,OOOOO0O0O0OOO00O0 ,OO0OO0O000OO00OO0 ,**O00OOOO0000OO00OO )#line:1591
    def findCaller (OO00O0O000OO00000 ,stack_info =False ,stacklevel =1 ):#line:1593
        ""#line:1597
        OOOO00OO00O000OOO =OO0OOOOO00O00O0O0 ()#line:1598
        if OOOO00OO00O000OOO is not None :#line:1601
            OOOO00OO00O000OOO =OOOO00OO00O000OOO .f_back #line:1602
        O0OOO00O0000OO00O =OOOO00OO00O000OOO #line:1603
        while OOOO00OO00O000OOO and stacklevel >1 :#line:1604
            OOOO00OO00O000OOO =OOOO00OO00O000OOO .f_back #line:1605
            stacklevel -=1 #line:1606
        if not OOOO00OO00O000OOO :#line:1607
            OOOO00OO00O000OOO =O0OOO00O0000OO00O #line:1608
        O0O0O00OO00O0O0O0 ="(unknown file)",0 ,"(unknown function)",None #line:1609
        while hasattr (OOOO00OO00O000OOO ,"f_code"):#line:1610
            O0OOO0O00OOOOOOO0 =OOOO00OO00O000OOO .f_code #line:1611
            O00000O000000000O =os .path .normcase (O0OOO0O00OOOOOOO0 .co_filename )#line:1612
            if O00000O000000000O ==_OO00O0O0O00O00OO0 :#line:1613
                OOOO00OO00O000OOO =OOOO00OO00O000OOO .f_back #line:1614
                continue #line:1615
            OOO00O00000O00000 =None #line:1616
            if stack_info :#line:1617
                O0O0O0OO000OOO0OO =io .StringIO ()#line:1618
                O0O0O0OO000OOO0OO .write ('Stack (most recent call last):\n')#line:1619
                traceback .print_stack (OOOO00OO00O000OOO ,file =O0O0O0OO000OOO0OO )#line:1620
                OOO00O00000O00000 =O0O0O0OO000OOO0OO .getvalue ()#line:1621
                if OOO00O00000O00000 [-1 ]=='\n':#line:1622
                    OOO00O00000O00000 =OOO00O00000O00000 [:-1 ]#line:1623
                O0O0O0OO000OOO0OO .close ()#line:1624
            O0O0O00OO00O0O0O0 =(O0OOO0O00OOOOOOO0 .co_filename ,OOOO00OO00O000OOO .f_lineno ,O0OOO0O00OOOOOOO0 .co_name ,OOO00O00000O00000 )#line:1625
            break #line:1626
        return O0O0O00OO00O0O0O0 #line:1627
    def makeRecord (OO000O0O0OOOO0000 ,OOOOO0OO0000OO0O0 ,O000O00000O0O0000 ,O00000O00O0OOO0O0 ,OOOO0O00O000OO0O0 ,OOOOOOOOOOO0OOOO0 ,O00O0O0O0OOO0O00O ,O0OO000OOOOOOO0O0 ,func =None ,extra =None ,sinfo =None ):#line:1630
        ""#line:1634
        OO0O000OOO0OO0OO0 =_O0O00OOOO0O0000OO (OOOOO0OO0000OO0O0 ,O000O00000O0O0000 ,O00000O00O0OOO0O0 ,OOOO0O00O000OO0O0 ,OOOOOOOOOOO0OOOO0 ,O00O0O0O0OOO0O00O ,O0OO000OOOOOOO0O0 ,func ,sinfo )#line:1636
        if extra is not None :#line:1637
            for O0OOOO0O00000000O in extra :#line:1638
                if (O0OOOO0O00000000O in ["message","asctime"])or (O0OOOO0O00000000O in OO0O000OOO0OO0OO0 .__dict__ ):#line:1639
                    raise KeyError ("Attempt to overwrite %r in LogRecord"%O0OOOO0O00000000O )#line:1640
                OO0O000OOO0OO0OO0 .__dict__ [O0OOOO0O00000000O ]=extra [O0OOOO0O00000000O ]#line:1641
        return OO0O000OOO0OO0OO0 #line:1642
    def _log (OOOOOOO0000OOO0OO ,O000O0O00O0OOO00O ,OO0OO00OO0OOOO000 ,O0O00O0OO0O0OO00O ,exc_info =None ,extra =None ,stack_info =False ,stacklevel =1 ):#line:1645
        ""#line:1649
        O00OO0OO00O00O000 =None #line:1650
        if _OO00O0O0O00O00OO0 :#line:1651
            try :#line:1655
                OO000O0OOOOO0O0OO ,O0O00O00OOOO0O000 ,OOO0OOOO0OOOOOOO0 ,O00OO0OO00O00O000 =OOOOOOO0000OOO0OO .findCaller (stack_info ,stacklevel )#line:1656
            except ValueError :#line:1657
                OO000O0OOOOO0O0OO ,O0O00O00OOOO0O000 ,OOO0OOOO0OOOOOOO0 ="(unknown file)",0 ,"(unknown function)"#line:1658
        else :#line:1659
            OO000O0OOOOO0O0OO ,O0O00O00OOOO0O000 ,OOO0OOOO0OOOOOOO0 ="(unknown file)",0 ,"(unknown function)"#line:1660
        if exc_info :#line:1661
            if isinstance (exc_info ,BaseException ):#line:1662
                exc_info =(type (exc_info ),exc_info ,exc_info .__traceback__ )#line:1663
            elif not isinstance (exc_info ,tuple ):#line:1664
                exc_info =sys .exc_info ()#line:1665
        O0000OO000O0OOO0O =OOOOOOO0000OOO0OO .makeRecord (OOOOOOO0000OOO0OO .name ,O000O0O00O0OOO00O ,OO000O0OOOOO0O0OO ,O0O00O00OOOO0O000 ,OO0OO00OO0OOOO000 ,O0O00O0OO0O0OO00O ,exc_info ,OOO0OOOO0OOOOOOO0 ,extra ,O00OO0OO00O00O000 )#line:1667
        OOOOOOO0000OOO0OO .handle (O0000OO000O0OOO0O )#line:1668
    def handle (OO0OOOO0OOO0000OO ,O00O000OO0O0000OO ):#line:1670
        ""#line:1676
        if (not OO0OOOO0OOO0000OO .disabled )and OO0OOOO0OOO0000OO .filter (O00O000OO0O0000OO ):#line:1678
            OO0OOOO0OOO0000OO .callHandlers (O00O000OO0O0000OO )#line:1679
    def addHandler (O00OO0000O0OOOO0O ,OO0OOO00O0O0O0O0O ):#line:1681
        ""#line:1684
        _OOO00OOO00O0OOO0O ()#line:1685
        try :#line:1686
            if not (OO0OOO00O0O0O0O0O in O00OO0000O0OOOO0O .handlers ):#line:1687
                O00OO0000O0OOOO0O .handlers .append (OO0OOO00O0O0O0O0O )#line:1688
        finally :#line:1689
            _OOO00OO000OO0000O ()#line:1690
    def removeHandler (O00O0O00OO0O0OO0O ,OO0O00OO0OOOO0O0O ):#line:1692
        ""#line:1695
        _OOO00OOO00O0OOO0O ()#line:1696
        try :#line:1697
            if OO0O00OO0OOOO0O0O in O00O0O00OO0O0OO0O .handlers :#line:1698
                O00O0O00OO0O0OO0O .handlers .remove (OO0O00OO0OOOO0O0O )#line:1699
        finally :#line:1700
            _OOO00OO000OO0000O ()#line:1701
    def hasHandlers (O0O000O000O0O0000 ):#line:1703
        ""#line:1712
        OOO0O000OOO00O0O0 =O0O000O000O0O0000 #line:1713
        O0000O00O00O0OO0O =False #line:1714
        while OOO0O000OOO00O0O0 :#line:1715
            if OOO0O000OOO00O0O0 .handlers :#line:1716
                O0000O00O00O0OO0O =True #line:1717
                break #line:1718
            if not OOO0O000OOO00O0O0 .propagate :#line:1719
                break #line:1720
            else :#line:1721
                OOO0O000OOO00O0O0 =OOO0O000OOO00O0O0 .parent #line:1722
        return O0000O00O00O0OO0O #line:1723
    def callHandlers (OO000000O0O0O000O ,OO00000O0OOOOOO0O ):#line:1725
        ""#line:1734
        OO0OO0000OOO000O0 =OO000000O0O0O000O #line:1736
        OOOO0000O0O0000OO =0 #line:1737
        while OO0OO0000OOO000O0 :#line:1738
            for OOOOOOOOOOO00O00O in OO0OO0000OOO000O0 .handlers :#line:1740
                OOOO0000O0O0000OO =OOOO0000O0O0000OO +1 #line:1741
                if OO00000O0OOOOOO0O .levelno >=OOOOOOOOOOO00O00O .level :#line:1742
                    OOOOOOOOOOO00O00O .handle (OO00000O0OOOOOO0O )#line:1743
            if not OO0OO0000OOO000O0 .propagate :#line:1744
                OO0OO0000OOO000O0 =None #line:1745
            else :#line:1746
                OO0OO0000OOO000O0 =OO0OO0000OOO000O0 .parent #line:1747
        if (OOOO0000O0O0000OO ==0 ):#line:1748
            if lastResort :#line:1749
                if OO00000O0OOOOOO0O .levelno >=lastResort .level :#line:1750
                    lastResort .handle (OO00000O0OOOOOO0O )#line:1751
            elif raiseExceptions and not OO000000O0O0O000O .manager .emittedNoHandlerWarning :#line:1752
                sys .stderr .write ("No handlers could be found for logger" " \"%s\"\n"%OO000000O0O0O000O .name )#line:1754
                OO000000O0O0O000O .manager .emittedNoHandlerWarning =True #line:1755
    def getEffectiveLevel (O00O00O00OOO0OO0O ):#line:1757
        ""#line:1763
        O000OO0000000OOOO =O00O00O00OOO0OO0O #line:1764
        while O000OO0000000OOOO :#line:1765
            if O000OO0000000OOOO .level :#line:1766
                return O000OO0000000OOOO .level #line:1767
            O000OO0000000OOOO =O000OO0000000OOOO .parent #line:1768
        return NOTSET #line:1769
    def isEnabledFor (OOO0OO0O0OOO000O0 ,OOOO000OOO0O000O0 ):#line:1771
        ""#line:1774
        if OOO0OO0O0OOO000O0 .disabled :#line:1775
            return False #line:1776
        try :#line:1778
            return OOO0OO0O0OOO000O0 ._cache [OOOO000OOO0O000O0 ]#line:1779
        except KeyError :#line:1780
            _OOO00OOO00O0OOO0O ()#line:1781
            try :#line:1782
                if OOO0OO0O0OOO000O0 .manager .disable >=OOOO000OOO0O000O0 :#line:1783
                    OO000OO000OOO000O =OOO0OO0O0OOO000O0 ._cache [OOOO000OOO0O000O0 ]=False #line:1784
                else :#line:1785
                    OO000OO000OOO000O =OOO0OO0O0OOO000O0 ._cache [OOOO000OOO0O000O0 ]=(OOOO000OOO0O000O0 >=OOO0OO0O0OOO000O0 .getEffectiveLevel ())#line:1788
            finally :#line:1789
                _OOO00OO000OO0000O ()#line:1790
            return OO000OO000OOO000O #line:1791
    def getChild (O0OOO0O00OO0000OO ,O000OOOO000O000OO ):#line:1793
        ""#line:1807
        if O0OOO0O00OO0000OO .root is not O0OOO0O00OO0000OO :#line:1808
            O000OOOO000O000OO ='.'.join ((O0OOO0O00OO0000OO .name ,O000OOOO000O000OO ))#line:1809
        return O0OOO0O00OO0000OO .manager .getLogger (O000OOOO000O000OO )#line:1810
    def __repr__ (O0OO00000000OO0OO ):#line:1812
        O0OO000O000000O0O =getLevelName (O0OO00000000OO0OO .getEffectiveLevel ())#line:1813
        return '<%s %s (%s)>'%(O0OO00000000OO0OO .__class__ .__name__ ,O0OO00000000OO0OO .name ,O0OO000O000000O0O )#line:1814
    def __reduce__ (OO0OOO0O0O0OOO00O ):#line:1816
        if getLogger (OO0OOO0O0O0OOO00O .name )is not OO0OOO0O0O0OOO00O :#line:1819
            import pickle #line:1820
            raise pickle .PicklingError ('logger cannot be pickled')#line:1821
        return getLogger ,(OO0OOO0O0O0OOO00O .name ,)#line:1822
class OOO00OOOO0O0O0000 (Logger ):#line:1825
    ""#line:1830
    def __init__ (OOO00O0OOOOO00000 ,O0000OO0O0O00O000 ):#line:1831
        ""#line:1834
        Logger .__init__ (OOO00O0OOOOO00000 ,"root",O0000OO0O0O00O000 )#line:1835
    def __reduce__ (OOOO00OOO0000OO00 ):#line:1837
        return getLogger ,()#line:1838
_O000O0OO0OO000O00 =Logger #line:1840
class LoggerAdapter (object ):#line:1842
    ""#line:1846
    def __init__ (O0O00OO0OO0O000O0 ,OO0OOOOOO000OO00O ,O00OOO000O00OOO0O ):#line:1848
        ""#line:1858
        O0O00OO0OO0O000O0 .logger =OO0OOOOOO000OO00O #line:1859
        O0O00OO0OO0O000O0 .extra =O00OOO000O00OOO0O #line:1860
    def process (OO00O0OO0OOO00OOO ,OO0OO000OO00000O0 ,O00OO0O00O0O0000O ):#line:1862
        ""#line:1871
        O00OO0O00O0O0000O ["extra"]=OO00O0OO0OOO00OOO .extra #line:1872
        return OO0OO000OO00000O0 ,O00OO0O00O0O0000O #line:1873
    def debug (O0000OOO0O0O0OOO0 ,OOO0OO0OOO000O0OO ,*OO0O000O0O0OO000O ,**OOO00000000O0O0OO ):#line:1878
        ""#line:1881
        O0000OOO0O0O0OOO0 .log (DEBUG ,OOO0OO0OOO000O0OO ,*OO0O000O0O0OO000O ,**OOO00000000O0O0OO )#line:1882
    def info (O000000O0OOOOO00O ,O0O0O00OO0OO0OOOO ,*OO00O0OO0OO00O0OO ,**O0O00O0O0000O00OO ):#line:1884
        ""#line:1887
        O000000O0OOOOO00O .log (INFO ,O0O0O00OO0OO0OOOO ,*OO00O0OO0OO00O0OO ,**O0O00O0O0000O00OO )#line:1888
    def warning (OOO00O00OOOOOO000 ,OO00OOOOOOO0O0O00 ,*O0OO0O0OO000O0OO0 ,**O00OOOOOO0O000OOO ):#line:1890
        ""#line:1893
        OOO00O00OOOOOO000 .log (WARNING ,OO00OOOOOOO0O0O00 ,*O0OO0O0OO000O0OO0 ,**O00OOOOOO0O000OOO )#line:1894
    def warn (O0OO000000000OO0O ,OOO0O000000O00OO0 ,*OOOO00O0OOO0OO00O ,**OOO0O000OOO0OOO0O ):#line:1896
        warnings .warn ("The 'warn' method is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:1898
        O0OO000000000OO0O .warning (OOO0O000000O00OO0 ,*OOOO00O0OOO0OO00O ,**OOO0O000OOO0OOO0O )#line:1899
    def error (O0000O0OOO0O000O0 ,OO00O0O0OO0O00O00 ,*OOOOOO00OO0000OO0 ,**OOOOO00OOO0OOOO00 ):#line:1901
        ""#line:1904
        O0000O0OOO0O000O0 .log (ERROR ,OO00O0O0OO0O00O00 ,*OOOOOO00OO0000OO0 ,**OOOOO00OOO0OOOO00 )#line:1905
    def exception (O0OOOOOOOOO00OO0O ,OO000OOO000OOO0OO ,*OOO0000OOOO000000 ,exc_info =True ,**O0O0O0O000OO0OO0O ):#line:1907
        ""#line:1910
        O0OOOOOOOOO00OO0O .log (ERROR ,OO000OOO000OOO0OO ,*OOO0000OOOO000000 ,exc_info =exc_info ,**O0O0O0O000OO0OO0O )#line:1911
    def critical (O0O0OO0O0O0OO00OO ,O0OO0OOO00O00OO00 ,*OO0OO000O00OO0000 ,**OO00OOOO0O00OOO00 ):#line:1913
        ""#line:1916
        O0O0OO0O0O0OO00OO .log (CRITICAL ,O0OO0OOO00O00OO00 ,*OO0OO000O00OO0000 ,**OO00OOOO0O00OOO00 )#line:1917
    def log (OO000OOO0OOOOOO00 ,OOOOO00OO00000OO0 ,O00O00OO00O00O0O0 ,*OO0OOO00O0OO00OOO ,**OOOOOOOOO0OOO0O00 ):#line:1919
        ""#line:1923
        if OO000OOO0OOOOOO00 .isEnabledFor (OOOOO00OO00000OO0 ):#line:1924
            O00O00OO00O00O0O0 ,OOOOOOOOO0OOO0O00 =OO000OOO0OOOOOO00 .process (O00O00OO00O00O0O0 ,OOOOOOOOO0OOO0O00 )#line:1925
            OO000OOO0OOOOOO00 .logger .log (OOOOO00OO00000OO0 ,O00O00OO00O00O0O0 ,*OO0OOO00O0OO00OOO ,**OOOOOOOOO0OOO0O00 )#line:1926
    def isEnabledFor (O0OO00OOO000OOOO0 ,O0O00000000O0000O ):#line:1928
        ""#line:1931
        return O0OO00OOO000OOOO0 .logger .isEnabledFor (O0O00000000O0000O )#line:1932
    def setLevel (OOO0OOO0OO0000OO0 ,O0O00OOO0O0OOOO0O ):#line:1934
        ""#line:1937
        OOO0OOO0OO0000OO0 .logger .setLevel (O0O00OOO0O0OOOO0O )#line:1938
    def getEffectiveLevel (OO0000O0O00OO0OO0 ):#line:1940
        ""#line:1943
        return OO0000O0O00OO0OO0 .logger .getEffectiveLevel ()#line:1944
    def hasHandlers (OOO0000OO00OO000O ):#line:1946
        ""#line:1949
        return OOO0000OO00OO000O .logger .hasHandlers ()#line:1950
    def _log (OO0OO000000O0OOO0 ,OOO0O000O000000O0 ,O0O00OOOOO00000O0 ,OOOOOOO0O0O000O00 ,exc_info =None ,extra =None ,stack_info =False ):#line:1952
        ""#line:1955
        return OO0OO000000O0OOO0 .logger ._log (OOO0O000O000000O0 ,O0O00OOOOO00000O0 ,OOOOOOO0O0O000O00 ,exc_info =exc_info ,extra =extra ,stack_info =stack_info ,)#line:1963
    @property #line:1965
    def manager (O0O0O00O0O0O000OO ):#line:1966
        return O0O0O00O0O0O000OO .logger .manager #line:1967
    @manager .setter #line:1969
    def manager (OOOOOO0000OO00OO0 ,O0O00000OOO00O000 ):#line:1970
        OOOOOO0000OO00OO0 .logger .manager =O0O00000OOO00O000 #line:1971
    @property #line:1973
    def name (OOO0O000000O0OO00 ):#line:1974
        return OOO0O000000O0OO00 .logger .name #line:1975
    def __repr__ (OO00O0O00O000OOOO ):#line:1977
        O000O000000OO0O0O =OO00O0O00O000OOOO .logger #line:1978
        OOO00OOOO0OO00000 =getLevelName (O000O000000OO0O0O .getEffectiveLevel ())#line:1979
        return '<%s %s (%s)>'%(OO00O0O00O000OOOO .__class__ .__name__ ,O000O000000OO0O0O .name ,OOO00OOOO0OO00000 )#line:1980
O00OO00O0000O000O =OOO00OOOO0O0O0000 (WARNING )#line:1982
Logger .root =O00OO00O0000O000O #line:1983
Logger .manager =O00OO0OO000O0000O (Logger .root )#line:1984
def basicConfig (**OO0OOO000O0O000O0 ):#line:1990
    ""#line:2046
    _OOO00OOO00O0OOO0O ()#line:2049
    try :#line:2050
        OOOOOOOO00O0O00O0 =OO0OOO000O0O000O0 .pop ('force',False )#line:2051
        if OOOOOOOO00O0O00O0 :#line:2052
            for OO000O0OOOO00OOO0 in O00OO00O0000O000O .handlers [:]:#line:2053
                O00OO00O0000O000O .removeHandler (OO000O0OOOO00OOO0 )#line:2054
                OO000O0OOOO00OOO0 .close ()#line:2055
        if len (O00OO00O0000O000O .handlers )==0 :#line:2056
            O0OO00OO000OOOOOO =OO0OOO000O0O000O0 .pop ("handlers",None )#line:2057
            if O0OO00OO000OOOOOO is None :#line:2058
                if "stream"in OO0OOO000O0O000O0 and "filename"in OO0OOO000O0O000O0 :#line:2059
                    raise ValueError ("'stream' and 'filename' should not be " "specified together")#line:2061
            else :#line:2062
                if "stream"in OO0OOO000O0O000O0 or "filename"in OO0OOO000O0O000O0 :#line:2063
                    raise ValueError ("'stream' or 'filename' should not be " "specified together with 'handlers'")#line:2065
            if O0OO00OO000OOOOOO is None :#line:2066
                O0O000OO000O00O0O =OO0OOO000O0O000O0 .pop ("filename",None )#line:2067
                O00000OOO0OO0000O =OO0OOO000O0O000O0 .pop ("filemode",'a')#line:2068
                if O0O000OO000O00O0O :#line:2069
                    OO000O0OOOO00OOO0 =FileHandler (O0O000OO000O00O0O ,O00000OOO0OO0000O )#line:2070
                else :#line:2071
                    OOOO0O0O000O0O000 =OO0OOO000O0O000O0 .pop ("stream",None )#line:2072
                    OO000O0OOOO00OOO0 =StreamHandler (OOOO0O0O000O0O000 )#line:2073
                O0OO00OO000OOOOOO =[OO000O0OOOO00OOO0 ]#line:2074
            O00O0OOOOO00O000O =OO0OOO000O0O000O0 .pop ("datefmt",None )#line:2075
            O0O0O000O0OOO0OO0 =OO0OOO000O0O000O0 .pop ("style",'%')#line:2076
            if O0O0O000O0OOO0OO0 not in _O0O0OOOO0O000O000 :#line:2077
                raise ValueError ('Style must be one of: %s'%','.join (_O0O0OOOO0O000O000 .keys ()))#line:2079
            O000000OOOO0OOO00 =OO0OOO000O0O000O0 .pop ("format",_O0O0OOOO0O000O000 [O0O0O000O0OOO0OO0 ][1 ])#line:2080
            O00OO000O0O0OOO00 =Formatter (O000000OOOO0OOO00 ,O00O0OOOOO00O000O ,O0O0O000O0OOO0OO0 )#line:2081
            for OO000O0OOOO00OOO0 in O0OO00OO000OOOOOO :#line:2082
                if OO000O0OOOO00OOO0 .formatter is None :#line:2083
                    OO000O0OOOO00OOO0 .setFormatter (O00OO000O0O0OOO00 )#line:2084
                O00OO00O0000O000O .addHandler (OO000O0OOOO00OOO0 )#line:2085
            O0O0O0O0OO000OOOO =OO0OOO000O0O000O0 .pop ("level",None )#line:2086
            if O0O0O0O0OO000OOOO is not None :#line:2087
                O00OO00O0000O000O .setLevel (O0O0O0O0OO000OOOO )#line:2088
            if OO0OOO000O0O000O0 :#line:2089
                OO0O000000OOO0O0O =', '.join (OO0OOO000O0O000O0 .keys ())#line:2090
                raise ValueError ('Unrecognised argument(s): %s'%OO0O000000OOO0O0O )#line:2091
    finally :#line:2092
        _OOO00OO000OO0000O ()#line:2093
def getLogger (name =None ):#line:2100
    ""#line:2105
    if name :#line:2106
        return Logger .manager .getLogger (name )#line:2107
    else :#line:2108
        return O00OO00O0000O000O #line:2109
def critical (OO0000OOOO0OOOOOO ,*OOOO0OO00OO00O0O0 ,**OO0000000OO000O0O ):#line:2111
    ""#line:2116
    if len (O00OO00O0000O000O .handlers )==0 :#line:2117
        basicConfig ()#line:2118
    O00OO00O0000O000O .critical (OO0000OOOO0OOOOOO ,*OOOO0OO00OO00O0O0 ,**OO0000000OO000O0O )#line:2119
fatal =critical #line:2121
def error (OOO000O0OOO00OO0O ,*OO0OO0O0000O00OOO ,**O0O0O00OO0000O00O ):#line:2123
    ""#line:2128
    if len (O00OO00O0000O000O .handlers )==0 :#line:2129
        basicConfig ()#line:2130
    O00OO00O0000O000O .error (OOO000O0OOO00OO0O ,*OO0OO0O0000O00OOO ,**O0O0O00OO0000O00O )#line:2131
def exception (OO0O0O0O00OO000OO ,*OO0OO000OO0OOOOOO ,exc_info =True ,**OO00000000OOO0000 ):#line:2133
    ""#line:2138
    error (OO0O0O0O00OO000OO ,*OO0OO000OO0OOOOOO ,exc_info =exc_info ,**OO00000000OOO0000 )#line:2139
def warning (OOO00O0OO00O00O0O ,*O00O00O00OO0O00O0 ,**OOO0O0O000000O000 ):#line:2141
    ""#line:2146
    if len (O00OO00O0000O000O .handlers )==0 :#line:2147
        basicConfig ()#line:2148
    O00OO00O0000O000O .warning (OOO00O0OO00O00O0O ,*O00O00O00OO0O00O0 ,**OOO0O0O000000O000 )#line:2149
def warn (OOO0O00OOOOO0OOOO ,*O0O000000O0O00000 ,**O0O0O0O000OOOO0O0 ):#line:2151
    warnings .warn ("The 'warn' function is deprecated, " "use 'warning' instead",DeprecationWarning ,2 )#line:2153
    warning (OOO0O00OOOOO0OOOO ,*O0O000000O0O00000 ,**O0O0O0O000OOOO0O0 )#line:2154
def info (O00OOOOOOO00OOOOO ,*OOOOOO00OO0OO000O ,**OOOOOOOOO00OOOOO0 ):#line:2156
    ""#line:2161
    if len (O00OO00O0000O000O .handlers )==0 :#line:2162
        basicConfig ()#line:2163
    O00OO00O0000O000O .info (O00OOOOOOO00OOOOO ,*OOOOOO00OO0OO000O ,**OOOOOOOOO00OOOOO0 )#line:2164
def debug (OO0O0O00000OO0OO0 ,*O0O000OOO0OOO00O0 ,**OOO000O0O0OOO00O0 ):#line:2166
    ""#line:2171
    if len (O00OO00O0000O000O .handlers )==0 :#line:2172
        basicConfig ()#line:2173
    O00OO00O0000O000O .debug (OO0O0O00000OO0OO0 ,*O0O000OOO0OOO00O0 ,**OOO000O0O0OOO00O0 )#line:2174
def log (OO00000OOOO00OO0O ,O00O00OO0O00OOO00 ,*O0O0OO0000O0O0O00 ,**OOOOOOO0OOOOOOOO0 ):#line:2176
    ""#line:2181
    if len (O00OO00O0000O000O .handlers )==0 :#line:2182
        basicConfig ()#line:2183
    O00OO00O0000O000O .log (OO00000OOOO00OO0O ,O00O00OO0O00OOO00 ,*O0O0OO0000O0O0O00 ,**OOOOOOO0OOOOOOOO0 )#line:2184
def disable (level =CRITICAL ):#line:2186
    ""#line:2189
    O00OO00O0000O000O .manager .disable =level #line:2190
    O00OO00O0000O000O .manager ._clear_cache ()#line:2191
def shutdown (handlerList =_OO000O0OO00O0O000 ):#line:2193
    ""#line:2199
    for OOOOOOO0OOOO000OO in reversed (handlerList [:]):#line:2200
        try :#line:2203
            O0O000O0O00O0O0O0 =OOOOOOO0OOOO000OO ()#line:2204
            if O0O000O0O00O0O0O0 :#line:2205
                try :#line:2206
                    O0O000O0O00O0O0O0 .acquire ()#line:2207
                    O0O000O0O00O0O0O0 .flush ()#line:2208
                    O0O000O0O00O0O0O0 .close ()#line:2209
                except (OSError ,ValueError ):#line:2210
                    pass #line:2215
                finally :#line:2216
                    O0O000O0O00O0O0O0 .release ()#line:2217
        except :#line:2218
            if raiseExceptions :#line:2219
                raise #line:2220
import atexit #line:2224
atexit .register (shutdown )#line:2225
class NullHandler (Handler ):#line:2229
    ""#line:2238
    def handle (OO00O0OOOOO0000O0 ,O0O0OO000O0OO0000 ):#line:2239
        ""#line:2240
    def emit (OO00OOO000000OO00 ,O0000O0O0O0O0000O ):#line:2242
        ""#line:2243
    def createLock (O0OOO00OO00O00000 ):#line:2245
        O0OOO00OO00O00000 .lock =None #line:2246
_O0O0O0O00OO0OOO0O =None #line:2250
def _OO0OO0OO0O0OOO000 (O00OO0O00O0O0OO0O ,OO0O00OOOO0OOO00O ,OOOOO00O00O000O00 ,O000OO00O000OO0OO ,file =None ,line =None ):#line:2252
    ""#line:2259
    if file is not None :#line:2260
        if _O0O0O0O00OO0OOO0O is not None :#line:2261
            _O0O0O0O00OO0OOO0O (O00OO0O00O0O0OO0O ,OO0O00OOOO0OOO00O ,OOOOO00O00O000O00 ,O000OO00O000OO0OO ,file ,line )#line:2262
    else :#line:2263
        OO00OOO00OO0OO0OO =warnings .formatwarning (O00OO0O00O0O0OO0O ,OO0O00OOOO0OOO00O ,OOOOO00O00O000O00 ,O000OO00O000OO0OO ,line )#line:2264
        OOO00OOOOO0OOO0O0 =getLogger ("py.warnings")#line:2265
        if not OOO00OOOOO0OOO0O0 .handlers :#line:2266
            OOO00OOOOO0OOO0O0 .addHandler (NullHandler ())#line:2267
        OOO00OOOOO0OOO0O0 .warning ("%s",OO00OOO00OO0OO0OO )#line:2268
def captureWarnings (O0O0O0O00OOOO0000 ):#line:2270
    ""#line:2275
    global _O0O0O0O00OO0OOO0O #line:2276
    if O0O0O0O00OOOO0000 :#line:2277
        if _O0O0O0O00OO0OOO0O is None :#line:2278
            _O0O0O0O00OO0OOO0O =warnings .showwarning #line:2279
            warnings .showwarning =_OO0OO0OO0O0OOO000 #line:2280
    else :#line:2281
        if _O0O0O0O00OO0OOO0O is not None :#line:2282
            warnings .showwarning =_O0O0O0O00OO0OOO0O #line:2283
            _O0O0O0O00OO0OOO0O =None #line:2284
