from brian2 import *
prefs.codegen.target = 'numpy'

class BaseNeuronGroup(NeuronGroup):
    def __init__(self, N, a, b, c, d, isInhibitory=False, threshold_voltage=30*mV):
        self.a = a;
        self._model = '''
        dv/dt = (0.04*(v/mV)**2 + 5*v/mV + 140 - u/mV + I/mV)*mV / ms : volt
        du/dt = %f*(%f*v-u) / ms: volt
        dI/dt = -log(2)*I/ms: volt 
        ''' % (a, b)

        self._reset = '''
        v = %f * mV
        u = u + %f * mV
        ''' % (c, d)

        t = super().__init__(N, model=self._model, threshold='v >= %f*mV' % (threshold_voltage/mV), reset=self._reset)
        self.u =  self.I = 0
        self.v = c*mV

class RSNeuronGroup(BaseNeuronGroup):
    def __init__(self, N):
        super().__init__(N, 0.02, 0.2, -65, 8)

class FSNeuronGroup(BaseNeuronGroup):
    def __init__(self, N):
        super().__init__(N, 0.1, 0.2, -65, 2)


NE = 3
NI = 1

P = RSNeuronGroup(3)
Q = RSNeuronGroup(1)
G = SpikeGeneratorGroup(1, array([0,0]), array([500, 800])*ms)

SG1 = Synapses(G, P, model = 'w : volt', pre='I += w')
SG2 = Synapses(G, Q, model = 'w : volt', pre='I += w')

SI = Synapses(Q, P, model = '''w : volt''', pre='''I -= w''')
SE = Synapses(P, P, model = '''w : volt''', pre='''I += w''')

SG1.connect([0], [0])
SG2.connect([0], [0])
SG1.w = 30*mV
SG2.w = 30*mV
SE.connect([0, 0], [1, 2])
SI.connect([0, 0], [1, 2])
SE.w = array([30, 30])*mV
SI.w = array([20, 20])*mV
SE.delay = array([10, 10])*ms
SI.delay = array([10, 30])*ms

MS = SpikeMonitor(G)
ME = StateMonitor(P, ('v','u','I'), record=[0, 1, 2])
MI = StateMonitor(Q, ('v',), record=[0])

run(1000*ms)

subplot(2, 2, 1)
plot(ME.t/ms, ME.v[0]/mV, label='v0')
subplot(2, 2, 2)
plot(ME.t/ms, ME.v[1]/mV, label='v1')
subplot(2, 2, 3)
plot(ME.t/ms, ME.v[2]/mV, label='v2')
subplot(2, 2, 4)
plot(MI.t/ms, MI.v[0]/mV, label='v0')
show()

