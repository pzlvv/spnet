from brian2 import *


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
        self.u = self.v = self.I = 0

class RSNeuronGroup(BaseNeuronGroup):
    def __init__(self, N):
        super().__init__(N, 0.02, 0.2, -65, 8)

class FSNeuronGroup(BaseNeuronGroup):
    def __init__(self, N):
        super().__init__(N, 0.1, 0.2, -65, 2)


NE = 3
NI = 1

#P = RSNeuronGroup(3)
mymodel = '''
        dv/dt = (0.04*(v/mV)**2 + 5*v/mV + 140 - u/mV + I/mV)*mV / ms : volt
        du/dt = 0.02*(0.2*v-u) / ms: volt
        dI/dt = -log(2)*I/ms: volt 
'''
myreset = '''
        v = %f * mV
        u = u + %f * mV
''' % (-65, 8)
P = NeuronGroup(3, model = mymodel) 
Q = RSNeuronGroup(1)
G = SpikeGeneratorGroup(2, array([0,0]), array([3,6])*ms)

SG1 = Synapses(G, P, model = 'w : volt', pre='I_post += w')
SG2 = Synapses(G, Q, model = 'w : volt', pre='I += w')
SG1.w = 100*mV
SG2.w = 100*mV
SI = Synapses(Q, P, model = 'w : volt', pre='I -= w')
SE = Synapses(P, P, model = 'w : volt', pre='I += w')

SG1.connect([0], [0])
SG2.connect([0], [0])
SE.connect([0, 0], [1, 2])
SI.connect([0, 0], [1, 2])

MS = SpikeMonitor(G)
ME = StateMonitor(P, ('v','u','I'), record=[0, 1, 2])
MI = StateMonitor(Q, ('v',), record=[0])

run(10*ms)

subplot(2, 2, 1)
plot(ME.t/ms, ME.v[0], label='v')
subplot(2, 2, 2)
plot(ME.t/ms, ME.v[1], label='v')
subplot(2, 2, 3)
plot(ME.t/ms, ME.I[0], label='v')
subplot(2, 2, 4)
plot(MS.t/ms, MS.i, label='v')
print(MS.t)
print(MS.i)
show()

