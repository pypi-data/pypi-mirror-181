import math

from fakeredis import _msgs as msgs
from fakeredis._commands import (command, Key, Int, Float, MAX_STRING_SIZE, delete_keys, fix_range_string)
from fakeredis._helpers import (OK, SimpleError, casematch)


class StringCommandsMixin:
    # String commands
    # todo: GETEX, LCS

    @command((Key(bytes), bytes))
    def append(self, key, value):
        old = key.get(b'')
        if len(old) + len(value) > MAX_STRING_SIZE:
            raise SimpleError(msgs.STRING_OVERFLOW_MSG)
        key.update(key.get(b'') + value)
        return len(key.value)

    @command((Key(bytes),))
    def decr(self, key):
        return self.incrby(key, -1)

    @command((Key(bytes), Int))
    def decrby(self, key, amount):
        return self.incrby(key, -amount)

    @command((Key(bytes),))
    def get(self, key):
        return key.get(None)

    @command((Key(bytes),))
    def getdel(self, key):
        res = key.get(None)
        delete_keys(key)
        return res

    @command((Key(bytes), Int, Int))
    def getrange(self, key, start, end):
        value = key.get(b'')
        start, end = fix_range_string(start, end, len(value))
        return value[start:end]

    @command((Key(bytes), bytes))
    def getset(self, key, value):
        old = key.value
        key.value = value
        return old

    @command((Key(bytes), Int))
    def incrby(self, key, amount):
        c = Int.decode(key.get(b'0')) + amount
        key.update(self._encodeint(c))
        return c

    @command((Key(bytes),))
    def incr(self, key):
        return self.incrby(key, 1)

    @command((Key(bytes), bytes))
    def incrbyfloat(self, key, amount):
        # TODO: introduce convert_order so that we can specify amount is Float
        c = Float.decode(key.get(b'0')) + Float.decode(amount)
        if not math.isfinite(c):
            raise SimpleError(msgs.NONFINITE_MSG)
        encoded = self._encodefloat(c, True)
        key.update(encoded)
        return encoded

    @command((Key(),), (Key(),))
    def mget(self, *keys):
        return [key.value if isinstance(key.value, bytes) else None for key in keys]

    @command((Key(), bytes), (Key(), bytes))
    def mset(self, *args):
        for i in range(0, len(args), 2):
            args[i].value = args[i + 1]
        return OK

    @command((Key(), bytes), (Key(), bytes))
    def msetnx(self, *args):
        for i in range(0, len(args), 2):
            if args[i]:
                return 0
        for i in range(0, len(args), 2):
            args[i].value = args[i + 1]
        return 1

    @command((Key(), Int, bytes))
    def psetex(self, key, ms, value):
        if ms <= 0 or self._db.time * 1000 + ms >= 2 ** 63:
            raise SimpleError(msgs.INVALID_EXPIRE_MSG.format('psetex'))
        key.value = value
        key.expireat = self._db.time + ms / 1000.0
        return OK

    @command(name="set", fixed=(Key(), bytes), repeat=(bytes,))
    def set_(self, key, value, *args):
        i = 0
        ex = None
        px = None
        xx = False
        nx = False
        keepttl = False
        get = False
        while i < len(args):
            if casematch(args[i], b'nx'):
                nx = True
                i += 1
            elif casematch(args[i], b'xx'):
                xx = True
                i += 1
            elif casematch(args[i], b'ex') and i + 1 < len(args):
                ex = Int.decode(args[i + 1])
                if ex <= 0 or (self._db.time + ex) * 1000 >= 2 ** 63:
                    raise SimpleError(msgs.INVALID_EXPIRE_MSG.format('set'))
                i += 2
            elif casematch(args[i], b'px') and i + 1 < len(args):
                px = Int.decode(args[i + 1])
                if px <= 0 or self._db.time * 1000 + px >= 2 ** 63:
                    raise SimpleError(msgs.INVALID_EXPIRE_MSG.format('set'))
                i += 2
            elif casematch(args[i], b'keepttl'):
                keepttl = True
                i += 1
            elif casematch(args[i], b'get'):
                get = True
                i += 1
            else:
                raise SimpleError(msgs.SYNTAX_ERROR_MSG)
        if (xx and nx) or ((px is not None) + (ex is not None) + keepttl > 1):
            raise SimpleError(msgs.SYNTAX_ERROR_MSG)
        if nx and get and self.version < 7:
            # The command docs say this is allowed from Redis 7.0.
            raise SimpleError(msgs.SYNTAX_ERROR_MSG)

        old_value = None
        if get:
            if key.value is not None and type(key.value) is not bytes:
                raise SimpleError(msgs.WRONGTYPE_MSG)
            old_value = key.value

        if nx and key:
            return old_value
        if xx and not key:
            return old_value
        if not keepttl:
            key.value = value
        else:
            key.update(value)
        if ex is not None:
            key.expireat = self._db.time + ex
        if px is not None:
            key.expireat = self._db.time + px / 1000.0
        return OK if not get else old_value

    @command((Key(), Int, bytes))
    def setex(self, key, seconds, value):
        if seconds <= 0 or (self._db.time + seconds) * 1000 >= 2 ** 63:
            raise SimpleError(msgs.INVALID_EXPIRE_MSG.format('setex'))
        key.value = value
        key.expireat = self._db.time + seconds
        return OK

    @command((Key(), bytes))
    def setnx(self, key, value):
        if key:
            return 0
        key.value = value
        return 1

    @command((Key(bytes), Int, bytes))
    def setrange(self, key, offset, value):
        if offset < 0:
            raise SimpleError(msgs.INVALID_OFFSET_MSG)
        elif not value:
            return len(key.get(b''))
        elif offset + len(value) > MAX_STRING_SIZE:
            raise SimpleError(msgs.STRING_OVERFLOW_MSG)
        else:
            out = key.get(b'')
            if len(out) < offset:
                out += b'\x00' * (offset - len(out))
            out = out[0:offset] + value + out[offset + len(value):]
            key.update(out)
            return len(out)

    @command((Key(bytes),))
    def strlen(self, key):
        return len(key.get(b''))

    # substr is a deprecated alias for getrange
    @command((Key(bytes), Int, Int))
    def substr(self, key, start, end):
        return self.getrange(key, start, end)

    @command((Key(bytes),), (bytes,))
    def getex(self, key, *args):
        i, count_options, expire_time, diff = 0, 0, None, None
        while i < len(args):
            count_options += 1
            if casematch(args[i], b'ex') and i + 1 < len(args):
                diff = Int.decode(args[i + 1])
                expire_time = self._db.time + diff
                i += 2
            elif casematch(args[i], b'px') and i + 1 < len(args):
                diff = Int.decode(args[i + 1])
                expire_time = (self._db.time * 1000 + diff) / 1000.0
                i += 2
            elif casematch(args[i], b'exat') and i + 1 < len(args):
                expire_time = Int.decode(args[i + 1])
                i += 2
            elif casematch(args[i], b'pxat') and i + 1 < len(args):
                expire_time = Int.decode(args[i + 1]) / 1000.0
                i += 2
            elif casematch(args[i], b'persist'):
                expire_time = None
                i += 1
            else:
                raise SimpleError(msgs.SYNTAX_ERROR_MSG)
        if ((expire_time is not None and (expire_time <= 0 or expire_time * 1000 >= 2 ** 63))
                or (diff is not None and (diff <= 0 or diff * 1000 >= 2 ** 63))):
            raise SimpleError(msgs.INVALID_EXPIRE_MSG.format('getex'))
        if count_options > 1:
            raise SimpleError(msgs.SYNTAX_ERROR_MSG)

        key.expireat = expire_time
        return key.get(None)
