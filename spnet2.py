from brian2 import *
prefs.codegen.target = 'numpy'

class MyNetwork:
    def __init__(self, N, threshold_voltage=30*mV):
        self.G = NeuronGroup(N, model='''
            a : 1
            b : 1
            c : 1
            d : 1
            k : 1
            dv/dt = (0.04*(v/mV)**2 + 5*v/mV + 140 - u/mV + I/mV)*mV / ms : volt
            du/dt = a*(b*v-u) / ms: volt
            dI/dt = -log(2)*I/ms: volt 
        ''', threshold='v >= %f * mV' % (threshold_voltage/mV), reset='''
            v = c*mV
            u = u + d*mV
        ''')

        self.S = Synapses(self.G, self.G, model = '''w:volt''', pre='''I += k_pre*w''')

    def assign_RSneurons(self, indices):
        for i in indices:
            self.G.a[i] = 0.02
            self.G.b[i] = 0.2
            self.G.c[i] = -65
            self.G.d[i] = 8
            self.G.k[i] = 1

    def assign_FSneurons(self, indices):
        for i in indices:
            self.G.a[i] = 0.1
            self.G.b[i] = 0.2
            self.G.c[i] = -65
            self.G.d[i] = 2
            self.G.k[i] = -1
    
    def establish_connections(self, *args, **kargs):
        self.S.connect(*args, **kargs)


#class BaseNeuronGroup(NeuronGroup):
#    def __init__(self, N, a, b, c, d, isInhibitory=False, threshold_voltage=30*mV):
#        self.a = a;
#        self._model = '''
#        dv/dt = (0.04*(v/mV)**2 + 5*v/mV + 140 - u/mV + I/mV)*mV / ms : volt
#        du/dt = %f*(%f*v-u) / ms: volt
#        dI/dt = -log(2)*I/ms: volt 
#        ''' % (a, b)
#
#        self._reset = '''
#        v = %f * mV
#        u = u + %f * mV
#        ''' % (c, d)
#
#        t = super().__init__(N, model=self._model, threshold='v >= %f*mV' % (threshold_voltage/mV), reset=self._reset)
#        self.u =  self.I = 0
#        self.v = c*mV

#class RSNeuronGroup(BaseNeuronGroup):
#    def __init__(self, N):
#        super().__init__(N, 0.02, 0.2, -65, 8)
#
#class FSNeuronGroup(BaseNeuronGroup):
#    def __init__(self, N):
#        super().__init__(N, 0.1, 0.2, -65, 2)


net = MyNetwork(4)
net.assign_RSneurons([0, 1, 2])
net.assign_FSneurons([3])
#net.establish_connections([0, 0, 3, 3], [1, 2, 1, 2])
net.S.connect([0, 0, 3, 3], [1, 2, 1, 2])
net.S.w[0, :] = 30*mV
net.S.w[3, :] = 30*mV


T = SpikeGeneratorGroup(1, array([0, 0]), array([500, 800])*ms)
SG = Synapses(T, net.G, model = 'w : volt', pre='I += w')
SG.connect([0, 0], [0, 3])
SG.w[0, 0] = 30*mV
SG.w[0, 3] = 30*mV

M = StateMonitor(net.G, ('v','u','I'), record=[0, 1, 2, 3])

m = Network(collect())
m.add(net.G)
m.run(1000*ms)

subplot(2, 2, 1)
plot(M.t/ms, M.v[0]/mV, label='v')
subplot(2, 2, 2)
plot(M.t/ms, M.v[1]/mV, label='v')
subplot(2, 2, 3)
plot(M.t/ms, M.v[2]/mV, label='v')
subplot(2, 2, 4)
plot(M.t/ms, M.v[3]/mV, label='v')
show()

