import math
import time

def gen16807(start):
    a = 16807
    m = 0x7FFFFFFF
    while True:
        q = m // a
        r = m % a
        next = a * (start % q) - r * (start // q)
        if next < 0:
            next = next + m
        yield next / 0x7FFFFFFF
        start = next

# const
PI = math.acos(-1)
seed = time.time()
seed = (seed - int(seed)) * 1000000
randGen = gen16807(int(seed))
numOfPoints = 80
dirRange = 20
delayMain = 5
delaySigma = 2
noDelay = False
accelVelocity = True
#

def med(small, test, big):
    assert small < big
    return min(max(small, test), big)

def isZero(num):
    if isinstance(num, int):
        if num == 0:
            return True
        else:
            return False
    elif isinstance(num, float):
        num = math.fabs(num)
        if num < 1e-10:
            return True
        else:
            return False
    else:
        return False

def isZeroPoint(p):
    assert isinstance(p, tuple)
    assert len(p) == 2
    if isZero(p[0]) and isZero(p[1]):
        return True
    else:
        return False

def isEqualPoint(p1, p2):
    assert isinstance(p1, tuple)
    assert len(p1) == 2
    assert isinstance(p2, tuple)
    assert len(p2) == 2
    if isZero(p1[0] - p2[0]) and isZero(p1[1] - p2[1]):
        return True
    else:
        return False

def normalize(t):
    assert isinstance(t, tuple)
    assert len(t) == 2
    if isZeroPoint(t):
        return (0.0, 0.0)
    length = t[0] * t[0] + t[1] * t[1]
    length = math.sqrt(length)
    return (t[0] / length, t[1] / length)

def normalizeEx(t, accel):
    assert isinstance(t, tuple)
    assert len(t) == 2
    if isZeroPoint(t):
        return (0.0, 0.0)
    length = t[0] * t[0] + t[1] * t[1]
    length = math.sqrt(length)
    if length < 1:
        return t
    if not accel:
        return (t[0] / length, t[1] / length)
    v = math.log10(length) + 1
    #if length <= 2:
    #    v = 3 / 4 * length * length - 7 / 4 * length + 2
    #else:
    #    v = length - 1 / length
    return (t[0] * math.sqrt(v), t[1] * math.sqrt(v))

def genPointSerial(num):
    point = [(0.0, 0.0), ]
    pointOld = (0.0, 0.0)

    for i in range(0, num):
        rand = next(randGen)
        dir = (point[-1][0] - pointOld[0], point[-1][1] - pointOld[1])
        print(dir)
        dir = normalize(dir)
        print(dir)
        if isZeroPoint(dir):
            rand = rand * 2 * PI
            pointOld = point[-1]
            dir = (math.cos(rand), math.sin(rand))
        else:
            rand = rand / dirRange * 2 * PI - PI / dirRange
            x = dir[0] * math.cos(rand) - dir[1] * math.sin(rand)
            y = dir[0] * math.sin(rand) + dir[1] * math.cos(rand)
            dir = normalize((x, y))
            pointOld = point[-1]
        point.append((pointOld[0] + dir[0], pointOld[1] + dir[1]))
    return point

def genRoutine(num):
    # Normal
    NormalDestOld = (0.0, 0.0)
    NormalDest = (0.0, 0.0)
    NormalCLientReal = (0.0, 0.0)
    # Sync
    SyncBuffer = [{'time' : 0.0, 'pos' : (0.0, 0.0)}, ] * 4
    SyncClientBuf = [(0.0, 0.0), (0.0, 0.0)]
    SyncClientReal = (0.0, 0.0)

    SyncIdeaLatency = 0
    SyncLatency = 0
    # Global
    time = 0.0
    serverBuf = []

    pointStream = genPointSerial(num)
    f = open('pointData', 'w')
    ff = open('pointData2', 'w')
    while pointStream != []:
        print('time: %f' % time)
        if serverBuf != []:
            serverBuf = list(map(lambda x: {'time' : x['time'], 'pos' : x['pos'], 'latency' : x['latency'] - 0.1}, serverBuf))
        point = pointStream[0]
        pointStream = pointStream[1:]
        delay = next(randGen)
        delay = delay * delaySigma * 2 + delayMain - delaySigma
        delay = round(delay) / 10
        serverBuf.append({'time' : time, 'pos' : point, 'latency' : delay})
        print(delay)
        ###
        #print('serverBuf:')
        #print(serverBuf)
        ###
        index = 0
        pos = None
        while index < len(serverBuf):
            if serverBuf[index]['latency'] < 0 or isZero(serverBuf[index]['latency']):
                SyncBuffer.append({'time' : serverBuf[index]['time'], 'pos' : serverBuf[index]['pos']})
                SyncBuffer = SyncBuffer[1:]
                pos = index
                NormalDest = serverBuf[index]['pos']
                SyncIdeaLatency = (time - (SyncBuffer[3]['time'] + SyncBuffer[1]['time']) / 2) / 2 
                if SyncIdeaLatency < 0.1:
                    SyncIdeaLatency = 0.1
            index = index + 1
        if pos != None:
            serverBuf = serverBuf[pos + 1:]
        ###
        #print('serverBuf:')
        #print(serverBuf)
        #input()
        ###

        if SyncIdeaLatency > SyncLatency:
            SyncLatency = SyncLatency + min(1.0, (SyncIdeaLatency - SyncLatency) ** 2)
            if SyncLatency > SyncIdeaLatency:
                SyncLatency = SyncIdeaLatency
        else:
            SyncLatency = SyncLatency - min(1.0, (SyncIdeaLatency - SyncLatency) ** 2)
            if SyncLatency < SyncIdeaLatency:
                SyncLatency = SyncIdeaLatency
        ###
        #print('Latency:')
        #print(SyncLatency, SyncIdeaLatency, sep=' > ')
        ###

        ###
        #print('buffer:')
        #print(SyncBuffer)
        ###
        if noDelay:
            tout = time
        else:
            tout = time - SyncLatency
        tout = med(SyncBuffer[0]['time'], tout, SyncBuffer[3]['time'] + 1)
        for i in range(0, 4):
            
        if isEqualPoint(SyncBuffer[0]['pos'], SyncBuffer[1]['pos']):
            SyncClientBuf.append(SyncBuffer[SyncBufferTop]['pos'])
        else:
            kx = (SyncBuffer[SyncBufferTop]['pos'][0] - SyncBuffer[1 - SyncBufferTop]['pos'][0]) / (SyncBuffer[SyncBufferTop]['time'] - SyncBuffer[1 - SyncBufferTop]['time'])
            ky = (SyncBuffer[SyncBufferTop]['pos'][1] - SyncBuffer[1 - SyncBufferTop]['pos'][1]) / (SyncBuffer[SyncBufferTop]['time'] - SyncBuffer[1 - SyncBufferTop]['time'])
            
            x = kx * (tout - SyncBuffer[SyncBufferTop]['time']) + SyncBuffer[SyncBufferTop]['pos'][0]
            y = ky * (tout - SyncBuffer[SyncBufferTop]['time']) + SyncBuffer[SyncBufferTop]['pos'][1]
            SyncClientBuf.append((x, y))
        SyncClientBuf = SyncClientBuf[1:]
        ###
        #print('clientBuffer:')
        #print(SyncClientBuf)
        ###
        dir = (SyncClientBuf[-2][0] - SyncClientReal[0], SyncClientBuf[-2][1] - SyncClientReal[1])
        dir = normalizeEx(dir, accelVelocity)
        SyncClientReal = (SyncClientReal[0] + dir[0], SyncClientReal[1] + dir[1])
        if (SyncClientBuf[-2][0] - SyncClientReal[0]) * dir[0] + (SyncClientBuf[-2][1] - SyncClientReal[1]) * dir[1] < 0:
            SyncClientReal = SyncClientBuf[-2]
    
        dir = (NormalDestOld[0] - NormalCLientReal[0], NormalDestOld[1] - NormalCLientReal[1])
        dir = normalizeEx(dir, accelVelocity)
        NormalCLientReal = (NormalCLientReal[0] + dir[0], NormalCLientReal[1] + dir[1])
        if (NormalDestOld[0] - NormalCLientReal[0]) * dir[0] + (NormalDestOld[1] - NormalCLientReal[1]) * dir[1] < 0:
            NormalCLientReal = NormalDestOld
        NormalDestOld = NormalDest
    
        ###
        f.write('%f %f %f %f %f %f\n' % (point[0], point[1], NormalDest[0], NormalDest[1], NormalCLientReal[0], NormalCLientReal[1]))
        ff.write('%f %f %f %f %f %f\n' % (point[0], point[1], SyncClientBuf[-1][0], SyncClientBuf[-1][1], SyncClientReal[0], SyncClientReal[1]))
        #print('Norm S: (%f,%f) | C: (%f,%f) | R: (%f,%f)' % (point[0], point[1], NormalDest[0], NormalDest[1], NormalCLientReal[0], NormalCLientReal[1]), file=f, flush=True)
        #print('Sync S: (%f,%f) | C: (%f,%f) | R: (%f,%f)' % (point[0], point[1], SyncClientBuf[-1][0], SyncClientBuf[-1][1], SyncClientReal[0], SyncClientReal[1]))
        ###
        time = time + 0.1
        print(SyncClientReal, SyncClientBuf[-1], sep=' > ')
    f.close()
    ff.close()

genRoutine(numOfPoints)